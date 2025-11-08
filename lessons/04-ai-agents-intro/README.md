# Lesson 4: Introduction to AI Agents

**Duration:** 20 minutes

## Overview

Understand what AI agents are, their architecture, and how to design them. This lesson provides the conceptual foundation for building our practical agent.

## 1. What is an AI Agent?

An **AI agent** is a software entity that:
- **Perceives** its environment through sensors
- **Reasons** about the information
- **Acts** to achieve goals
- **Learns** from experience (in advanced cases)

### Simple Analogy

Think of a thermostat:
- **Perceives**: Temperature sensor
- **Reasons**: Compare to target temperature
- **Acts**: Turn heating/cooling on or off
- **Goal**: Maintain desired temperature

### Software Agent Example

A map navigation agent:
- **Perceives**: Current location, destination, traffic data
- **Reasons**: Calculate optimal route
- **Acts**: Provide turn-by-turn directions
- **Goal**: Get user to destination efficiently

## 2. Types of Agents

### Simple Reflex Agents
React directly to current percept (like an if-statement)

```python
# Pseudocode
if temperature > 25:
    turn_on_ac()
else:
    turn_off_ac()
```

### Model-Based Reflex Agents
Maintain internal state about the world

```python
class ThermostatAgent:
    def __init__(self):
        self.temperature_history = []
        self.target_temp = 22
    
    def perceive(self, current_temp):
        self.temperature_history.append(current_temp)
        
    def act(self):
        avg_temp = sum(self.temperature_history[-5:]) / 5
        if avg_temp > self.target_temp:
            return "COOL"
        return "HEAT"
```

### Goal-Based Agents
Consider future consequences of actions

```python
# Navigation agent considers:
# - Current position
# - Destination (goal)
# - Possible routes
# - Traffic predictions
# -> Chooses best path to achieve goal
```

### Learning Agents
Improve performance over time through experience

## 3. Agent Architecture

### Basic Agent Loop

```python
class Agent:
    def __init__(self):
        self.state = {}
    
    def perceive(self, environment):
        """Gather information from environment"""
        return environment.get_data()
    
    def reason(self, percepts):
        """Decide what to do"""
        # Decision logic here
        return action
    
    def act(self, action):
        """Execute the action"""
        # Perform action
        pass
    
    def run(self):
        """Main agent loop"""
        while True:
            percepts = self.perceive(environment)
            action = self.reason(percepts)
            self.act(action)
```

### Components of an Agent

1. **Sensors** (Input)
   - API calls
   - Database queries
   - User input
   - File system

2. **Actuators** (Output)
   - API requests
   - Database updates
   - UI updates
   - Notifications

3. **Knowledge Base**
   - Internal state
   - Memory
   - Rules
   - Models

4. **Reasoning Engine**
   - Decision logic
   - Planning algorithms
   - Learning mechanisms

## 4. Our Tutorial: Map Navigation Agent

### Scenario

We'll build an agent that:
- Queries a map server for route information
- Maintains current position
- Makes navigation decisions
- Responds to real-time updates

### Agent Responsibilities

```python
class NavigationAgent:
    """
    Perceives:
      - Current GPS position
      - Destination
      - Map data from server
    
    Reasons:
      - Calculate best route
      - Handle obstacles
      - Consider traffic
    
    Acts:
      - Request map data
      - Update position
      - Provide directions
    """
    pass
```

### Map Server Responsibilities

```python
class MapServer:
    """
    Provides:
      - Map data
      - Route calculations
      - Point of interest info
      - Real-time updates
    """
    pass
```

### Architecture Diagram

```
┌─────────────────┐
│  User/Client    │
└────────┬────────┘
         │
         │ requests
         ▼
┌─────────────────┐      ┌──────────────┐
│ Navigation      │◄────►│  Map Server  │
│ Agent           │      │  (Flask API) │
└─────────────────┘      └──────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐      ┌──────────────┐
│  Agent State    │      │  Map Data    │
│  (memory)       │      │  (database)  │
└─────────────────┘      └──────────────┘
```

## 5. Agent Communication Patterns

### Request-Response (Synchronous)

```python
# Agent requests data from server
response = requests.get('http://mapserver/route', 
                       params={'from': 'A', 'to': 'B'})
route = response.json()
```

### Publish-Subscribe (Asynchronous)

```python
# Agent subscribes to updates
def on_traffic_update(data):
    agent.update_route(data)

subscribe('traffic_updates', on_traffic_update)
```

### Message Queue

```python
# Agent sends message to queue
queue.put({"type": "route_request", "data": {...}})

# Server processes from queue
message = queue.get()
process_route_request(message)
```

## 6. Agent Design Principles

### 1. Autonomy
Agents operate without direct human intervention
```python
# Good: Agent makes decisions
if self.battery_low():
    self.return_to_base()

# Bad: Requires human decision
if self.battery_low():
    print("Battery low! What should I do?")
    action = input()
```

### 2. Reactivity
Agents respond to changes in environment
```python
def perceive(self):
    if self.detect_obstacle():
        self.replan_route()  # React immediately
```

### 3. Pro-activeness
Agents take initiative toward goals
```python
def check_goal_progress(self):
    if self.distance_to_goal > self.threshold:
        self.optimize_route()  # Take initiative
```

### 4. Social Ability
Agents interact with other agents/systems
```python
def coordinate(self, other_agents):
    # Share information
    self.broadcast_position()
    # Negotiate
    self.request_priority(other_agents)
```

## 7. State Management

### Stateless Agent (Simple)
```python
def process_request(request):
    # No memory of previous requests
    route = calculate_route(request.start, request.end)
    return route
```

### Stateful Agent (Complex)
```python
class StatefulAgent:
    def __init__(self):
        self.journey_history = []
        self.preferences = {}
        self.learned_patterns = {}
    
    def process_request(self, request):
        # Consider history
        if self.frequently_travels(request.route):
            route = self.preferred_route(request)
        else:
            route = self.calculate_new_route(request)
        
        self.journey_history.append(route)
        return route
```

## 8. Real-World Agent Applications

### Autonomous Vehicles
- **Perceive**: Cameras, LIDAR, GPS
- **Reason**: Path planning, obstacle avoidance
- **Act**: Steering, acceleration, braking

### Trading Bots
- **Perceive**: Market data, news
- **Reason**: Price predictions, risk analysis
- **Act**: Buy/sell orders

### Smart Home Systems
- **Perceive**: Sensors (temp, motion, time)
- **Reason**: User preferences, schedules
- **Act**: Adjust lights, temperature, security

### Customer Service Chatbots
- **Perceive**: User messages, context
- **Reason**: Intent classification, response generation
- **Act**: Send responses, escalate to human

### Recommendation Systems
- **Perceive**: User behavior, ratings
- **Reason**: Collaborative filtering, content analysis
- **Act**: Suggest items

## 9. Agent vs Traditional Software

| Traditional Software | Agent Software |
|---------------------|----------------|
| Passive (waits for calls) | Active (initiates actions) |
| Deterministic | Adaptive |
| Fixed behavior | Learning behavior |
| Direct control | Autonomous |
| Immediate response | Long-term goals |

### Traditional:
```python
def get_route(start, end):
    # Called when user requests
    return calculate_route(start, end)
```

### Agent:
```python
class RouteAgent:
    def run(self):
        while self.active:
            # Continuously monitoring
            if self.detect_traffic():
                self.replan_route()
            if self.near_destination():
                self.prepare_arrival()
            time.sleep(1)
```

## 10. Planning Our Agent

### Requirements

Our navigation agent needs to:
1. ✅ Maintain current position
2. ✅ Query map server for routes
3. ✅ Update route based on conditions
4. ✅ Provide turn-by-turn directions
5. ✅ Handle errors gracefully

### Design Decisions

**Language**: Python (simple, readable)  
**Communication**: REST API (HTTP/JSON)  
**State**: In-memory (simple)  
**Deployment**: Docker container  

### Next Steps

In the next lessons, we'll:
1. Build the map server (Flask API)
2. Implement the navigation agent
3. Containerize with Docker

## Practice Exercise

Design an agent for a different scenario:

**Scenario**: Smart refrigerator agent that:
- Monitors food inventory
- Checks expiration dates
- Suggests recipes based on available ingredients
- Orders groceries when items run low

**Define:**
1. What the agent perceives
2. How it reasons
3. What actions it takes
4. What its goals are

**Solution in:** `solutions/04-fridge-agent-design.md`

## Key Takeaways

✅ Agents perceive, reason, and act autonomously  
✅ Different types of agents suit different problems  
✅ Agent loop: perceive → reason → act → repeat  
✅ Agents maintain state and adapt to environment  
✅ Good design separates concerns (perception, reasoning, action)  
✅ Our tutorial builds a navigation agent with map server  

## Further Reading

- Russell & Norvig: "Artificial Intelligence: A Modern Approach"
- Multi-agent systems
- Reinforcement learning
- Agent communication languages (ACL)

---

**Next:** [Lesson 5: Building a Simple AI Agent](../05-building-agent/README.md)
