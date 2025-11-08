# Lesson 6: Building a Map Server

**Duration:** 30 minutes

## Overview

Build a REST API server using Flask that provides map data and routing services to our navigation agent.

## 1. Introduction to Flask

Flask is a lightweight web framework for Python (like Spring Boot, but simpler).

### Flask vs Spring Boot

| Spring Boot (Java) | Flask (Python) |
|-------------------|----------------|
| @RestController | @app.route() |
| @GetMapping | @app.route('/', methods=['GET']) |
| @RequestParam | request.args.get() |
| @RequestBody | request.json |
| Annotations-heavy | Decorator-based |

### Simple Flask Example

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Run it:
```bash
python app.py
# Visit http://localhost:5000
```

## 2. Map Server Design

### Requirements

Our map server needs to:
- Provide route calculations
- Store map data
- Handle multiple concurrent requests
- Return JSON responses
- Handle errors gracefully

### API Endpoints

```
GET  /                      - Health check
GET  /route                 - Calculate route between two points
GET  /location/:id          - Get location details
POST /location              - Add new location
GET  /nearby                - Find nearby points of interest
```

## 3. Building the Map Server - Step by Step

### Step 1: Basic Flask Setup

```python
from flask import Flask, jsonify, request
from typing import Dict, List, Tuple
import math

app = Flask(__name__)

# Simple in-memory data store
locations = {
    'sf': {'name': 'San Francisco', 'lat': 37.7749, 'lon': -122.4194},
    'oak': {'name': 'Oakland', 'lat': 37.8044, 'lon': -122.2712},
    'sj': {'name': 'San Jose', 'lat': 37.3382, 'lon': -121.8863}
}

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'map-server',
        'version': '1.0.0'
    })
```

### Step 2: Route Calculation

```python
def calculate_distance(lat1: float, lon1: float, 
                      lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in kilometers
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def generate_route(start_lat: float, start_lon: float,
                  end_lat: float, end_lon: float,
                  num_steps: int = 5) -> List[List[float]]:
    """
    Generate a simple route with intermediate points.
    In a real system, this would use actual road networks.
    """
    route = []
    
    for i in range(num_steps + 1):
        fraction = i / num_steps
        lat = start_lat + (end_lat - start_lat) * fraction
        lon = start_lon + (end_lon - start_lon) * fraction
        route.append([lat, lon])
    
    return route

@app.route('/route', methods=['GET'])
def get_route():
    """
    Calculate route between two points.
    
    Query params:
        start_lat: Starting latitude
        start_lon: Starting longitude
        end_lat: Ending latitude
        end_lon: Ending longitude
    
    Returns:
        JSON with route information
    """
    try:
        # Get parameters
        start_lat = float(request.args.get('start_lat'))
        start_lon = float(request.args.get('start_lon'))
        end_lat = float(request.args.get('end_lat'))
        end_lon = float(request.args.get('end_lon'))
        
        # Calculate route
        route = generate_route(start_lat, start_lon, end_lat, end_lon)
        distance = calculate_distance(start_lat, start_lon, end_lat, end_lon)
        
        # Estimate duration (assuming 60 km/h average speed)
        duration_hours = distance / 60
        duration_minutes = duration_hours * 60
        
        return jsonify({
            'success': True,
            'route': route,
            'distance': round(distance, 2),
            'duration_minutes': round(duration_minutes, 2),
            'steps': len(route)
        })
        
    except (TypeError, ValueError) as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameters',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500
```

### Step 3: Location Management

```python
@app.route('/location/<location_id>', methods=['GET'])
def get_location(location_id: str):
    """Get details for a specific location."""
    location = locations.get(location_id)
    
    if location:
        return jsonify({
            'success': True,
            'location_id': location_id,
            'data': location
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Location not found'
        }), 404

@app.route('/location', methods=['POST'])
def add_location():
    """Add a new location."""
    try:
        data = request.json
        location_id = data.get('id')
        
        if not location_id:
            return jsonify({
                'success': False,
                'error': 'Missing location ID'
            }), 400
        
        locations[location_id] = {
            'name': data.get('name'),
            'lat': float(data.get('lat')),
            'lon': float(data.get('lon'))
        }
        
        return jsonify({
            'success': True,
            'message': 'Location added',
            'location_id': location_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/locations', methods=['GET'])
def list_locations():
    """List all locations."""
    return jsonify({
        'success': True,
        'count': len(locations),
        'locations': locations
    })
```

### Step 4: Nearby Search

```python
@app.route('/nearby', methods=['GET'])
def find_nearby():
    """
    Find locations near a given point.
    
    Query params:
        lat: Latitude
        lon: Longitude
        radius: Search radius in kilometers (default: 10)
    """
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius', 10))
        
        nearby = []
        
        for loc_id, loc_data in locations.items():
            distance = calculate_distance(
                lat, lon, 
                loc_data['lat'], loc_data['lon']
            )
            
            if distance <= radius:
                nearby.append({
                    'id': loc_id,
                    'name': loc_data['name'],
                    'distance': round(distance, 2),
                    'coordinates': {
                        'lat': loc_data['lat'],
                        'lon': loc_data['lon']
                    }
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance'])
        
        return jsonify({
            'success': True,
            'count': len(nearby),
            'locations': nearby
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
```

### Step 5: Running the Server

```python
if __name__ == '__main__':
    print("Starting Map Server...")
    print("Endpoints:")
    print("  GET  /              - Health check")
    print("  GET  /route         - Calculate route")
    print("  GET  /location/:id  - Get location")
    print("  POST /location      - Add location")
    print("  GET  /locations     - List all locations")
    print("  GET  /nearby        - Find nearby locations")
    print("\nServer running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 4. Complete Map Server Code

**File: `src/map_server/app.py`**

See the complete implementation in the `src/map_server/` directory.

## 5. Testing the Map Server

### Manual Testing with curl

```bash
# Health check
curl http://localhost:5000/

# Get route
curl "http://localhost:5000/route?start_lat=37.7749&start_lon=-122.4194&end_lat=37.8044&end_lon=-122.2712"

# Get location
curl http://localhost:5000/location/sf

# Add location
curl -X POST http://localhost:5000/location \
  -H "Content-Type: application/json" \
  -d '{"id":"berkeley","name":"Berkeley","lat":37.8715,"lon":-122.2730}'

# Find nearby
curl "http://localhost:5000/nearby?lat=37.7749&lon=-122.4194&radius=50"
```

### Testing with Python

```python
import requests

# Health check
response = requests.get('http://localhost:5000/')
print(response.json())

# Get route
params = {
    'start_lat': 37.7749,
    'start_lon': -122.4194,
    'end_lat': 37.8044,
    'end_lon': -122.2712
}
response = requests.get('http://localhost:5000/route', params=params)
print(response.json())
```

## 6. Error Handling and Validation

### Input Validation

```python
from flask import abort

def validate_coordinates(lat, lon):
    """Validate latitude and longitude."""
    if not (-90 <= lat <= 90):
        abort(400, description="Latitude must be between -90 and 90")
    if not (-180 <= lon <= 180):
        abort(400, description="Longitude must be between -180 and 180")

@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': 'Bad Request',
        'message': str(e.description)
    }), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Not Found',
        'message': str(e.description)
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'Something went wrong'
    }), 500
```

## 7. Adding Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('map_server.log', 
                                      maxBytes=10240, 
                                      backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Map server startup')

@app.route('/route', methods=['GET'])
def get_route():
    app.logger.info(f"Route request from {request.remote_addr}")
    # ... rest of the code
```

## 8. Configuration Management

```python
import os

class Config:
    """Application configuration."""
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

app.config.from_object(Config)
```

## 9. Advanced: Database Integration

For production, you'd use a real database:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/mapdb'
db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon
        }
```

## 10. Testing with pytest

```python
# test_map_server.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_route_calculation(client):
    response = client.get('/route?start_lat=37.7749&start_lon=-122.4194&end_lat=37.8044&end_lon=-122.2712')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'route' in data
    assert 'distance' in data

def test_invalid_route(client):
    response = client.get('/route?start_lat=invalid')
    assert response.status_code == 400
```

Run tests:
```bash
pytest test_map_server.py -v
```

## Practice Exercise

Enhance the map server with:

1. **Traffic information**: Add traffic delay factors to routes
2. **POI categories**: Categorize locations (restaurant, gas station, etc.)
3. **Route alternatives**: Return multiple route options
4. **Authentication**: Add API key authentication
5. **Rate limiting**: Limit requests per client

**Solution in:** `solutions/06-enhanced-server.py`

## Comparing Flask to Spring Boot

**Spring Boot:**
```java
@RestController
@RequestMapping("/api")
public class MapController {
    @GetMapping("/route")
    public RouteResponse getRoute(
        @RequestParam double startLat,
        @RequestParam double startLon,
        @RequestParam double endLat,
        @RequestParam double endLon
    ) {
        // Logic here
        return new RouteResponse(...);
    }
}
```

**Flask:**
```python
@app.route('/route', methods=['GET'])
def get_route():
    start_lat = float(request.args.get('start_lat'))
    # Logic here
    return jsonify({...})
```

**Python advantages:**
- Less boilerplate
- No need for separate DTO classes
- Simpler routing
- Built-in JSON serialization

## Key Takeaways

✅ Flask makes building REST APIs simple  
✅ Use `@app.route()` decorator for endpoints  
✅ `request.args` for query parameters, `request.json` for body  
✅ `jsonify()` for JSON responses  
✅ Add proper error handling and validation  
✅ Use logging for production monitoring  
✅ pytest for testing Flask applications  

## Quick Reference

```python
# Flask basics
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/path', methods=['GET', 'POST'])
def handler():
    param = request.args.get('param')  # Query param
    data = request.json                 # Request body
    return jsonify({'key': 'value'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

**Next:** [Lesson 7: Docker Deployment](../07-docker-deployment/README.md)
