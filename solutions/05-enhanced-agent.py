"""
Solution for Lesson 5: Enhanced Agent Exercise

This enhanced agent includes:
1. Priority destinations
2. Battery management
3. Learning (route memory)
4. Better error handling
"""

import requests
import time
import math
from typing import Tuple, List, Optional, Dict
from collections import defaultdict


class EnhancedNavigationAgent:
    """
    An enhanced autonomous navigation agent with additional features.
    """
    
    def __init__(self, map_server_url: str, agent_id: str = "enhanced-agent"):
        """Initialize the enhanced agent."""
        self.agent_id = agent_id
        self.map_server_url = map_server_url.rstrip('/')
        self.position = None
        self.is_active = False
        self.distance_traveled = 0.0
        
        # Enhanced features
        self.battery_level = 100.0  # Percentage
        self.battery_drain_rate = 1.0  # % per km
        self.low_battery_threshold = 20.0
        self.home_position = None
        
        # Priority queue for destinations
        self.destination_queue = []  # List of (priority, destination, name)
        
        # Learning: Remember frequently used routes
        self.route_memory = defaultdict(int)  # route_key -> count
        self.route_cache = {}  # route_key -> route_data
        
        print(f"[{self.agent_id}] Enhanced agent initialized")
        print(f"[{self.agent_id}] Battery: {self.battery_level}%")
    
    def set_home(self, position: Tuple[float, float]):
        """Set home position for battery management."""
        self.home_position = position
        print(f"[{self.agent_id}] Home set to {position}")
    
    def add_destination(self, destination: Tuple[float, float], 
                       name: str, priority: int = 5):
        """
        Add a destination to the queue with priority.
        Lower priority number = higher priority (1 is highest)
        """
        self.destination_queue.append((priority, destination, name))
        self.destination_queue.sort()  # Sort by priority
        print(f"[{self.agent_id}] Added destination: {name} (priority {priority})")
    
    def check_battery(self) -> bool:
        """Check if battery is sufficient."""
        if self.battery_level < self.low_battery_threshold:
            print(f"[{self.agent_id}] ⚠️  LOW BATTERY: {self.battery_level:.1f}%")
            return False
        return True
    
    def return_to_home(self):
        """Navigate back to home position."""
        if not self.home_position:
            print(f"[{self.agent_id}] No home position set")
            return
        
        print(f"[{self.agent_id}] 🏠 Returning to home for recharge")
        self.navigate_to(self.home_position, "Home")
        self.recharge()
    
    def recharge(self):
        """Recharge battery at home."""
        print(f"[{self.agent_id}] 🔋 Recharging battery...")
        time.sleep(2)
        self.battery_level = 100.0
        print(f"[{self.agent_id}] ✓ Battery recharged to {self.battery_level}%")
    
    def query_route(self, start: Tuple[float, float], 
                   end: Tuple[float, float]) -> Optional[Dict]:
        """Query route with caching and learning."""
        route_key = f"{start}-{end}"
        
        # Check cache first
        if route_key in self.route_cache:
            print(f"[{self.agent_id}] 📚 Using cached route")
            self.route_memory[route_key] += 1
            return self.route_cache[route_key]
        
        # Query server
        try:
            url = f"{self.map_server_url}/route"
            params = {
                'start_lat': start[0],
                'start_lon': start[1],
                'end_lat': end[0],
                'end_lon': end[1]
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                route_data = response.json()
                # Cache the route
                self.route_cache[route_key] = route_data
                self.route_memory[route_key] += 1
                return route_data
            
        except requests.RequestException as e:
            print(f"[{self.agent_id}] ❌ Connection error: {e}")
        
        return None
    
    def navigate_to(self, destination: Tuple[float, float], name: str = "Unknown"):
        """Navigate to a destination with battery management."""
        if not self.check_battery():
            if self.position != self.home_position:
                self.return_to_home()
            return False
        
        print(f"\n[{self.agent_id}] 🎯 Navigating to {name}")
        print(f"[{self.agent_id}] From: {self.position}")
        print(f"[{self.agent_id}] To: {destination}")
        print(f"[{self.agent_id}] Battery: {self.battery_level:.1f}%")
        
        # Plan route
        route_data = self.query_route(self.position, destination)
        
        if not route_data or not route_data.get('success'):
            print(f"[{self.agent_id}] ❌ Failed to plan route")
            return False
        
        route = route_data.get('route', [])
        distance = route_data.get('distance', 0)
        
        # Check if we have enough battery
        battery_needed = distance * self.battery_drain_rate
        if battery_needed > self.battery_level:
            print(f"[{self.agent_id}] ⚠️  Insufficient battery for trip")
            print(f"[{self.agent_id}] Need: {battery_needed:.1f}%, Have: {self.battery_level:.1f}%")
            self.return_to_home()
            return False
        
        print(f"[{self.agent_id}] Route: {len(route)} steps, {distance:.2f} km")
        
        # Execute navigation
        for i, point in enumerate(route, 1):
            self.position = tuple(point)
            # Drain battery based on distance
            if i > 0:
                self.battery_level -= self.battery_drain_rate
            print(f"[{self.agent_id}] Step {i}/{len(route)}: {self.position} (Battery: {self.battery_level:.1f}%)")
            time.sleep(0.3)
        
        print(f"[{self.agent_id}] ✓ Arrived at {name}")
        return True
    
    def process_destination_queue(self):
        """Process all destinations in priority order."""
        print(f"\n[{self.agent_id}] 📋 Processing {len(self.destination_queue)} destinations")
        
        while self.destination_queue:
            priority, destination, name = self.destination_queue.pop(0)
            
            print(f"\n[{self.agent_id}] Next: {name} (Priority {priority})")
            
            success = self.navigate_to(destination, name)
            
            if not success:
                print(f"[{self.agent_id}] ⚠️  Could not complete destination queue")
                break
        
        print(f"\n[{self.agent_id}] ✓ All destinations processed")
    
    def get_statistics(self) -> Dict:
        """Get agent statistics."""
        most_traveled = max(self.route_memory.items(), 
                           key=lambda x: x[1]) if self.route_memory else None
        
        return {
            'agent_id': self.agent_id,
            'position': self.position,
            'battery_level': self.battery_level,
            'distance_traveled': self.distance_traveled,
            'routes_traveled': len(self.route_memory),
            'cached_routes': len(self.route_cache),
            'most_traveled_route': most_traveled[0] if most_traveled else None,
            'most_traveled_count': most_traveled[1] if most_traveled else 0
        }


def demo():
    """Demonstrate enhanced agent features."""
    print("=" * 60)
    print("Enhanced Navigation Agent Demo")
    print("=" * 60)
    
    # Create agent
    agent = EnhancedNavigationAgent("http://localhost:5000", "enhanced-001")
    
    # Set home position
    home = (37.7749, -122.4194)  # San Francisco
    agent.position = home
    agent.set_home(home)
    
    # Add multiple destinations with priorities
    print("\n--- Adding Destinations ---")
    agent.add_destination((37.8044, -122.2712), "Oakland", priority=2)
    agent.add_destination((37.3382, -121.8863), "San Jose", priority=3)
    agent.add_destination((37.8715, -122.2730), "Berkeley", priority=1)  # Highest priority
    
    # Process all destinations
    print("\n--- Starting Navigation ---")
    agent.process_destination_queue()
    
    # Return home
    print("\n--- Returning Home ---")
    agent.return_to_home()
    
    # Display statistics
    print("\n" + "=" * 60)
    print("Agent Statistics")
    print("=" * 60)
    stats = agent.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()


if __name__ == "__main__":
    demo()
