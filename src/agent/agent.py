"""
Navigation Agent Implementation

An autonomous agent that queries a map server for routes and navigates
between locations.
"""

import requests
import time
import math
from typing import Tuple, List, Optional, Dict


class NavigationAgent:
    """
    An autonomous navigation agent that interacts with a map server
    to plan and execute routes.
    """
    
    def __init__(self, map_server_url: str, agent_id: str = "agent-001"):
        """
        Initialize the navigation agent.
        
        Args:
            map_server_url: Base URL of the map server
            agent_id: Unique identifier for this agent
        """
        self.agent_id = agent_id
        self.map_server_url = map_server_url.rstrip('/')
        self.position = None
        self.destination = None
        self.current_route = None
        self.is_active = False
        self.distance_traveled = 0.0
        
        print(f"[{self.agent_id}] Agent initialized")
        print(f"[{self.agent_id}] Map server: {self.map_server_url}")
    
    def query_route(self, start: Tuple[float, float], 
                   end: Tuple[float, float],
                   max_retries: int = 3) -> Optional[Dict]:
        """
        Query the map server for a route.
        
        Args:
            start: Starting coordinates (lat, lon)
            end: Ending coordinates (lat, lon)
            max_retries: Maximum number of retry attempts
            
        Returns:
            Route data or None if request fails
        """
        for attempt in range(max_retries):
            try:
                url = f"{self.map_server_url}/route"
                params = {
                    'start_lat': start[0],
                    'start_lon': start[1],
                    'end_lat': end[0],
                    'end_lon': end[1]
                }
                
                print(f"[{self.agent_id}] Querying route from {start} to {end}")
                response = requests.get(url, params=params, timeout=5)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"[{self.agent_id}] Error: HTTP {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"[{self.agent_id}] Connection error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def plan_route(self, destination: Tuple[float, float]) -> bool:
        """
        Plan a route to the destination.
        
        Args:
            destination: Target coordinates (lat, lon)
            
        Returns:
            True if route was successfully planned
        """
        if self.position is None:
            print(f"[{self.agent_id}] Error: Current position not set")
            return False
        
        print(f"[{self.agent_id}] Planning route to {destination}")
        route_data = self.query_route(self.position, destination)
        
        if route_data and route_data.get('success'):
            self.current_route = route_data.get('route', [])
            self.destination = destination
            distance = route_data.get('distance', 0)
            duration = route_data.get('duration_minutes', 0)
            
            print(f"[{self.agent_id}] ✓ Route planned successfully")
            print(f"[{self.agent_id}] Steps: {len(self.current_route)}")
            print(f"[{self.agent_id}] Distance: {distance:.2f} km")
            print(f"[{self.agent_id}] Duration: {duration:.1f} minutes")
            return True
        else:
            print(f"[{self.agent_id}] ✗ Failed to plan route")
            return False
    
    def move_to_next_point(self) -> bool:
        """
        Move to the next point in the current route.
        
        Returns:
            True if moved successfully, False if route completed or error
        """
        if not self.current_route:
            print(f"[{self.agent_id}] No route available")
            return False
        
        if len(self.current_route) == 0:
            print(f"[{self.agent_id}] 🎯 Destination reached!")
            self.is_active = False
            return False
        
        # Move to next point
        next_point = self.current_route.pop(0)
        old_position = self.position
        self.position = tuple(next_point)
        
        # Calculate distance moved
        distance = self._calculate_distance(old_position, self.position)
        self.distance_traveled += distance
        
        print(f"[{self.agent_id}] → Moved to ({self.position[0]:.4f}, {self.position[1]:.4f})")
        print(f"[{self.agent_id}] Steps remaining: {len(self.current_route)}")
        
        return True
    
    def _calculate_distance(self, point1: Tuple[float, float], 
                          point2: Tuple[float, float]) -> float:
        """Calculate simple Euclidean distance between two points."""
        return math.sqrt(
            (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2
        )
    
    def start_navigation(self, start: Tuple[float, float], 
                        destination: Tuple[float, float],
                        step_delay: float = 1.0):
        """
        Start autonomous navigation from start to destination.
        
        Args:
            start: Starting coordinates (lat, lon)
            destination: Target coordinates (lat, lon)
            step_delay: Delay between movement steps in seconds
        """
        self.position = start
        self.is_active = True
        self.distance_traveled = 0.0
        
        print(f"\n{'='*60}")
        print(f"[{self.agent_id}] 🚀 Starting navigation")
        print(f"[{self.agent_id}] From: ({start[0]:.4f}, {start[1]:.4f})")
        print(f"[{self.agent_id}] To: ({destination[0]:.4f}, {destination[1]:.4f})")
        print(f"{'='*60}\n")
        
        # Plan the route
        if not self.plan_route(destination):
            print(f"[{self.agent_id}] ⚠️  Navigation aborted")
            return
        
        print(f"\n[{self.agent_id}] Starting movement...\n")
        
        # Execute navigation
        step_count = 0
        while self.is_active and self.current_route:
            step_count += 1
            print(f"[{self.agent_id}] Step {step_count}:")
            self.move_to_next_point()
            time.sleep(step_delay)
            print()
        
        # Report completion
        print(f"{'='*60}")
        print(f"[{self.agent_id}] ✓ Navigation complete")
        print(f"[{self.agent_id}] Total steps: {step_count}")
        print(f"[{self.agent_id}] Total distance: {self.distance_traveled:.4f} units")
        print(f"{'='*60}\n")
    
    def get_status(self) -> Dict:
        """Get current agent status."""
        return {
            'agent_id': self.agent_id,
            'is_active': self.is_active,
            'position': self.position,
            'destination': self.destination,
            'steps_remaining': len(self.current_route) if self.current_route else 0,
            'distance_traveled': self.distance_traveled
        }
    
    def stop(self):
        """Stop the agent."""
        print(f"[{self.agent_id}] 🛑 Stopping navigation")
        self.is_active = False
