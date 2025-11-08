"""
Map Server Implementation

A Flask-based REST API that provides mapping and routing services.
"""

from flask import Flask, jsonify, request
from typing import Dict, List, Tuple
import math
import os

app = Flask(__name__)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'
app.config['HOST'] = os.getenv('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.getenv('FLASK_PORT', 5000))

# Simple in-memory data store for locations
locations = {
    'sf': {'name': 'San Francisco', 'lat': 37.7749, 'lon': -122.4194},
    'oak': {'name': 'Oakland', 'lat': 37.8044, 'lon': -122.2712},
    'sj': {'name': 'San Jose', 'lat': 37.3382, 'lon': -121.8863},
    'berkeley': {'name': 'Berkeley', 'lat': 37.8715, 'lon': -122.2730}
}


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


@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'map-server',
        'version': '1.0.0',
        'endpoints': {
            'health': '/',
            'route': '/route',
            'location': '/location/<id>',
            'locations': '/locations',
            'add_location': '/location (POST)',
            'nearby': '/nearby'
        }
    })


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
        
        # Validate coordinates
        if not (-90 <= start_lat <= 90 and -90 <= end_lat <= 90):
            return jsonify({
                'success': False,
                'error': 'Invalid latitude (must be between -90 and 90)'
            }), 400
        
        if not (-180 <= start_lon <= 180 and -180 <= end_lon <= 180):
            return jsonify({
                'success': False,
                'error': 'Invalid longitude (must be between -180 and 180)'
            }), 400
        
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
            'steps': len(route),
            'start': {'lat': start_lat, 'lon': start_lon},
            'end': {'lat': end_lat, 'lon': end_lon}
        })
        
    except (TypeError, ValueError) as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameters',
            'message': 'Please provide valid start_lat, start_lon, end_lat, and end_lon'
        }), 400
    except Exception as e:
        app.logger.error(f"Error calculating route: {e}")
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500


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
            'error': 'Location not found',
            'message': f'No location found with id: {location_id}'
        }), 404


@app.route('/location', methods=['POST'])
def add_location():
    """Add a new location."""
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        location_id = data.get('id')
        
        if not location_id:
            return jsonify({
                'success': False,
                'error': 'Missing location ID'
            }), 400
        
        locations[location_id] = {
            'name': data.get('name', 'Unnamed'),
            'lat': float(data.get('lat')),
            'lon': float(data.get('lon'))
        }
        
        return jsonify({
            'success': True,
            'message': 'Location added successfully',
            'location_id': location_id
        }), 201
        
    except (TypeError, ValueError) as e:
        return jsonify({
            'success': False,
            'error': 'Invalid data format',
            'message': str(e)
        }), 400
    except Exception as e:
        app.logger.error(f"Error adding location: {e}")
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500


@app.route('/locations', methods=['GET'])
def list_locations():
    """List all locations."""
    return jsonify({
        'success': True,
        'count': len(locations),
        'locations': locations
    })


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
            'search_center': {'lat': lat, 'lon': lon},
            'search_radius': radius,
            'locations': nearby
        })
        
    except (TypeError, ValueError) as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameters',
            'message': 'Please provide valid lat, lon, and optionally radius'
        }), 400
    except Exception as e:
        app.logger.error(f"Error finding nearby locations: {e}")
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'Something went wrong on the server'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🗺️  Map Server Starting")
    print("=" * 60)
    print(f"Host: {app.config['HOST']}")
    print(f"Port: {app.config['PORT']}")
    print(f"Debug: {app.config['DEBUG']}")
    print("\nAvailable Endpoints:")
    print("  GET  /              - Health check")
    print("  GET  /route         - Calculate route")
    print("  GET  /location/:id  - Get location details")
    print("  POST /location      - Add new location")
    print("  GET  /locations     - List all locations")
    print("  GET  /nearby        - Find nearby locations")
    print("=" * 60)
    print(f"\n✓ Server running at http://{app.config['HOST']}:{app.config['PORT']}")
    print("  Press CTRL+C to quit\n")
    
    app.run(
        debug=app.config['DEBUG'], 
        host=app.config['HOST'], 
        port=app.config['PORT']
    )
