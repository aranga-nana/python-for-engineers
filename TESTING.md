# Testing Guide

This document describes how to test the tutorial code and verify everything works correctly.

## Quick Test

```bash
# 1. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Test map server
python src/map_server/app.py
# In another terminal:
curl http://localhost:5000/

# 3. Test agent (with server running)
python src/agent/main.py
```

## Detailed Testing

### 1. Map Server Tests

**Start the server:**
```bash
python src/map_server/app.py
```

**Test health endpoint:**
```bash
curl http://localhost:5000/
# Expected: {"status": "ok", ...}
```

**Test route calculation:**
```bash
curl "http://localhost:5000/route?start_lat=37.7749&start_lon=-122.4194&end_lat=37.8044&end_lon=-122.2712"
# Expected: {"success": true, "route": [...], "distance": 13.43, ...}
```

**Test invalid parameters:**
```bash
curl "http://localhost:5000/route?start_lat=invalid"
# Expected: 400 error with message
```

**Test location endpoints:**
```bash
# Get location
curl http://localhost:5000/location/sf
# Expected: {"success": true, "data": {...}}

# List all locations
curl http://localhost:5000/locations
# Expected: {"success": true, "locations": {...}}

# Add location
curl -X POST http://localhost:5000/location \
  -H "Content-Type: application/json" \
  -d '{"id":"test","name":"Test City","lat":37.5,"lon":-122.0}'
# Expected: 201 status, {"success": true}

# Find nearby
curl "http://localhost:5000/nearby?lat=37.7749&lon=-122.4194&radius=50"
# Expected: List of locations within radius
```

### 2. Agent Tests

**Basic test (with server running):**
```bash
python src/agent/main.py
# Expected: Agent navigates between two locations
```

**Test with different server URL:**
```bash
MAP_SERVER_URL=http://localhost:5000 python src/agent/main.py
```

**Test error handling (server not running):**
```bash
# Stop map server
MAP_SERVER_URL=http://localhost:9999 python src/agent/main.py
# Expected: Connection error, retry messages
```

### 3. Interactive Python Testing

```bash
# Start Python REPL
python

# Test agent
from src.agent.agent import NavigationAgent
agent = NavigationAgent("http://localhost:5000")
agent.position = (37.7749, -122.4194)
success = agent.plan_route((37.8044, -122.2712))
print(f"Route planned: {success}")
status = agent.get_status()
print(status)
```

### 4. Solution Tests

**Test calculator solution:**
```bash
python solutions/01-calculator.py
# Expected: Calculator demo output
```

**Test setup exercise:**
```bash
cd /tmp
bash solutions/02-setup-exercise.sh
# Expected: Creates hello-python project
```

### 5. Docker Tests

**Build images:**
```bash
docker-compose build
```

**Start services:**
```bash
docker-compose up
```

**Test map server in container:**
```bash
curl http://localhost:5000/
```

**View logs:**
```bash
docker-compose logs mapserver
docker-compose logs agent
```

**Stop services:**
```bash
docker-compose down
```

### 6. Load Testing

**Simple load test with curl:**
```bash
for i in {1..100}; do
  curl -s "http://localhost:5000/route?start_lat=37.7749&start_lon=-122.4194&end_lat=37.8044&end_lon=-122.2712" > /dev/null
  echo "Request $i complete"
done
```

**Using Apache Bench (if installed):**
```bash
ab -n 100 -c 10 http://localhost:5000/
```

## Expected Results

### Map Server

✅ Health check returns status "ok"  
✅ Route calculation returns valid route with 6 steps  
✅ Distance calculation is approximately 13.43 km  
✅ Invalid parameters return 400 error  
✅ Location endpoints work correctly  

### Agent

✅ Agent connects to map server  
✅ Route is planned successfully  
✅ Agent moves through all waypoints  
✅ Total distance is calculated  
✅ Error handling works (retries on failure)  

### Docker

✅ Images build without errors  
✅ Services start in correct order  
✅ Agent waits for map server health check  
✅ Agent completes navigation  
✅ Services can be stopped cleanly  

## Troubleshooting

### Server won't start

**Problem:** Port 5000 already in use

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
FLASK_PORT=5001 python src/map_server/app.py
```

### Module not found

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Agent can't connect

**Problem:** Agent shows connection errors

**Solution:**
1. Make sure map server is running
2. Check the URL is correct
3. Verify port is accessible
4. Check firewall settings

### Docker issues

**Problem:** Docker build fails

**Solution:**
```bash
# Clean up Docker
docker-compose down
docker system prune

# Rebuild
docker-compose build --no-cache
```

## Continuous Testing

### Watch for file changes

**Using entr (if installed):**
```bash
# Auto-restart server on changes
ls src/map_server/*.py | entr -r python src/map_server/app.py
```

### Pre-commit checks

Before committing code:

1. ✅ Run map server - no errors
2. ✅ Run agent - completes successfully
3. ✅ Test all API endpoints
4. ✅ Check for Python syntax errors
5. ✅ Verify imports work
6. ✅ Test Docker build (if applicable)

## Automated Testing

**Create test script:**
```bash
#!/bin/bash
# test.sh

echo "Running tests..."

# Start server in background
python src/map_server/app.py &
SERVER_PID=$!
sleep 2

# Test health endpoint
curl -f http://localhost:5000/ || { echo "Health check failed"; exit 1; }

# Test route endpoint
curl -f "http://localhost:5000/route?start_lat=37.7&start_lon=-122.4&end_lat=37.8&end_lon=-122.3" || { echo "Route test failed"; exit 1; }

# Stop server
kill $SERVER_PID

echo "All tests passed!"
```

## Performance Benchmarks

Expected performance (on typical hardware):

- **Route calculation**: < 50ms
- **Health check**: < 10ms
- **Agent navigation** (5 steps): < 3s
- **Docker startup**: < 30s

## Success Criteria

All tests should pass with:
- ✅ No Python exceptions
- ✅ Correct output format
- ✅ Expected values
- ✅ Proper error handling
- ✅ Clean shutdown

---

**Run these tests before submitting changes or deploying!**
