# Lesson 5: Building a Simple AI Agent

**Duration:** 30 minutes

## Overview

Build a functional navigation agent in Python that communicates with a map server, maintains state, and makes autonomous decisions.

## 1. Agent Design

### Requirements

Our NavigationAgent will:
- Maintain current position
- Store destination
- Query map server for routes
- Update position along route
- Handle navigation commands

### Class Structure

```python
class NavigationAgent:
    def __init__(self, map_server_url):
        self.position = None
        self.destination = None
        self.current_route = None
        self.map_server_url = map_server_url
        self.is_active = False
```

## 2. Building the Agent - Step by Step

### Step 1: Initialize the Agent

```python
import requests
import time
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
```

### Step 2: Perception - Querying the Map Server

```python
    def query_route(self, start: Tuple[float, float], 
                   end: Tuple[float, float]) -> Optional[Dict]:
        """
        Query the map server for a route.
        
        Args:
            start: Starting coordinates (lat, lon)
            end: Ending coordinates (lat, lon)
            
        Returns:
            Route data or None if request fails
        """
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
                print(f"[{self.agent_id}] Error: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"[{self.agent_id}] Connection error: {e}")
            return None
```

### Step 3: Reasoning - Planning Navigation

```python
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
            print(f"[{self.agent_id}] Route planned: {len(self.current_route)} steps")
            print(f"[{self.agent_id}] Distance: {route_data.get('distance', 0):.2f} km")
            return True
        else:
            print(f"[{self.agent_id}] Failed to plan route")
            return False
```

### Step 4: Action - Moving Along Route

```python
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
            print(f"[{self.agent_id}] Destination reached!")
            self.is_active = False
            return False
        
        # Move to next point
        next_point = self.current_route.pop(0)
        old_position = self.position
        self.position = tuple(next_point)
        
        # Calculate distance moved
        distance = self._calculate_distance(old_position, self.position)
        self.distance_traveled += distance
        
        print(f"[{self.agent_id}] Moved to {self.position}")
        print(f"[{self.agent_id}] Steps remaining: {len(self.current_route)}")
        
        return True
    
    def _calculate_distance(self, point1: Tuple[float, float], 
                          point2: Tuple[float, float]) -> float:
        """Calculate simple Euclidean distance between two points."""
        import math
        return math.sqrt(
            (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2
        )
```

### Step 5: Main Agent Loop

```python
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
        
        print(f"\n[{self.agent_id}] Starting navigation")
        print(f"[{self.agent_id}] From: {start}")
        print(f"[{self.agent_id}] To: {destination}\n")
        
        # Plan the route
        if not self.plan_route(destination):
            print(f"[{self.agent_id}] Navigation aborted")
            return
        
        # Execute navigation
        while self.is_active and self.current_route:
            self.move_to_next_point()
            time.sleep(step_delay)
        
        # Report completion
        print(f"\n[{self.agent_id}] Navigation complete")
        print(f"[{self.agent_id}] Total distance: {self.distance_traveled:.2f} km")
```

### Step 6: Additional Utility Methods

```python
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
        print(f"[{self.agent_id}] Stopping navigation")
        self.is_active = False
```

## 3. Complete Agent Code

**File: `src/agent/agent.py`**

See the complete implementation in the `src/agent/` directory.

## 4. Testing the Agent (Without Server)

### Mock Server for Testing

```python
# test_agent_mock.py
from unittest.mock import Mock, patch
from agent import NavigationAgent

def test_agent_with_mock():
    # Create agent
    agent = NavigationAgent("http://localhost:5000")
    
    # Mock the requests.get call
    with patch('requests.get') as mock_get:
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'route': [[37.7749, -122.4194], [37.7750, -122.4190]],
            'distance': 0.5
        }
        mock_get.return_value = mock_response
        
        # Test planning
        agent.position = (37.7749, -122.4194)
        success = agent.plan_route((37.7750, -122.4190))
        
        assert success
        assert len(agent.current_route) == 2

if __name__ == "__main__":
    test_agent_with_mock()
    print("✅ Tests passed!")
```

## 5. Using the Agent

### Basic Usage

```python
# main.py
from agent import NavigationAgent

def main():
    # Initialize agent
    agent = NavigationAgent(
        map_server_url="http://localhost:5000",
        agent_id="navigator-1"
    )
    
    # Define start and destination
    start = (37.7749, -122.4194)      # San Francisco
    destination = (37.7849, -122.4094) # 1km away
    
    # Start navigation
    agent.start_navigation(start, destination, step_delay=1.0)
    
    # Get final status
    status = agent.get_status()
    print(f"\nFinal Status: {status}")

if __name__ == "__main__":
    main()
```

## 6. Error Handling

### Robust Agent with Error Handling

```python
    def query_route(self, start, end, max_retries=3):
        """Query route with retry logic."""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    return response.json()
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
```

## 7. Advanced Features

### Dynamic Route Updates

```python
    def update_route(self, new_destination: Tuple[float, float]):
        """Update route while navigating."""
        if self.is_active:
            print(f"[{self.agent_id}] Updating route to {new_destination}")
            self.plan_route(new_destination)
```

### Obstacle Detection

```python
    def check_obstacles(self, next_point: Tuple[float, float]) -> bool:
        """Check if path to next point is clear."""
        try:
            url = f"{self.map_server_url}/check_path"
            params = {
                'from_lat': self.position[0],
                'from_lon': self.position[1],
                'to_lat': next_point[0],
                'to_lon': next_point[1]
            }
            response = requests.get(url, params=params)
            data = response.json()
            return data.get('is_clear', True)
        except:
            return True  # Assume clear on error
```

## 8. Agent Communication

### Agent-to-Agent Communication

```python
class CommunicatingAgent(NavigationAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nearby_agents = []
    
    def broadcast_position(self):
        """Broadcast position to other agents."""
        message = {
            'agent_id': self.agent_id,
            'position': self.position,
            'timestamp': time.time()
        }
        # Send to server or message queue
        requests.post(f"{self.map_server_url}/broadcast", json=message)
    
    def receive_positions(self):
        """Receive positions from other agents."""
        response = requests.get(f"{self.map_server_url}/agents")
        self.nearby_agents = response.json().get('agents', [])
```

## 9. Comparing to Java

### Java Version (Sketch)

```java
public class NavigationAgent {
    private Position position;
    private Position destination;
    private List<Position> currentRoute;
    private String mapServerUrl;
    
    public NavigationAgent(String mapServerUrl) {
        this.mapServerUrl = mapServerUrl;
    }
    
    public RouteData queryRoute(Position start, Position end) {
        // HTTP client call
        RestTemplate restTemplate = new RestTemplate();
        String url = String.format("%s/route?start_lat=%f&start_lon=%f...",
                                   mapServerUrl, start.lat, start.lon);
        return restTemplate.getForObject(url, RouteData.class);
    }
}
```

**Python advantages:**
- Less boilerplate
- Duck typing (no Position class needed)
- Simpler HTTP requests
- More concise

## Practice Exercise

Enhance the agent with:

1. **Priority destinations**: Agent can have multiple destinations with priorities
2. **Battery management**: Agent tracks battery and returns to base when low
3. **Learning**: Agent remembers frequently traveled routes
4. **Multi-threaded**: Run multiple agents simultaneously

**Solution in:** `solutions/05-enhanced-agent.py`

## Testing Checklist

✅ Agent initializes correctly  
✅ Can query map server  
✅ Plans route successfully  
✅ Moves along route  
✅ Handles server errors gracefully  
✅ Reports status accurately  
✅ Stops when destination reached  

## Key Takeaways

✅ Agents have clear perception, reasoning, and action phases  
✅ Use requests library for HTTP communication  
✅ Maintain state in instance variables  
✅ Implement error handling and retries  
✅ Type hints improve code clarity  
✅ Agent loop drives autonomous behavior  

## Next Steps

Now that we have an agent, we need a map server for it to communicate with!

---

**Next:** [Lesson 6: Building a Map Server](../06-map-server/README.md)
