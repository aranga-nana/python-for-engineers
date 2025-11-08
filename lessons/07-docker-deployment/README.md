# Lesson 7: Docker Deployment

**Duration:** 40 minutes

## Overview

Learn how to containerize your Python applications using Docker, and deploy both the map server and navigation agent as containers.

## 1. Introduction to Docker

Docker packages applications and their dependencies into containers that run consistently anywhere.

### Why Docker?

**Without Docker:**
- "It works on my machine" problems
- Complex setup instructions
- Dependency conflicts
- Environment differences

**With Docker:**
- Consistent environments
- Easy deployment
- Isolated applications
- Reproducible builds

### Docker Concepts

| Concept | Description | Analogy |
|---------|-------------|---------|
| Image | Template for containers | Class in OOP |
| Container | Running instance | Object instance |
| Dockerfile | Build instructions | Build script |
| Docker Compose | Multi-container orchestration | Orchestra conductor |

## 2. Docker vs Virtual Machines

### Virtual Machine
```
┌─────────────────────────┐
│     Application A       │
│     Application B       │
├─────────────────────────┤
│      Guest OS           │
├─────────────────────────┤
│      Hypervisor         │
├─────────────────────────┤
│      Host OS            │
├─────────────────────────┤
│      Hardware           │
└─────────────────────────┘
```

### Docker Container
```
┌─────────────────────────┐
│     Application A       │
│     Application B       │
├─────────────────────────┤
│    Docker Engine        │
├─────────────────────────┤
│      Host OS            │
├─────────────────────────┤
│      Hardware           │
└─────────────────────────┘
```

**Containers are lighter and faster!**

## 3. Installing Docker on Mac

### Installation

1. **Download Docker Desktop**
   - Visit [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Download for macOS

2. **Install**
   - Open the .dmg file
   - Drag Docker to Applications
   - Launch Docker Desktop

3. **Verify Installation**
```bash
docker --version
docker-compose --version

# Test with hello-world
docker run hello-world
```

### Docker Desktop Features

- GUI for managing containers
- Kubernetes integration
- Resource management
- Container logs viewer

## 4. Creating a Dockerfile

A Dockerfile contains instructions to build a Docker image.

### Dockerfile for Map Server

**File: `Dockerfile.mapserver`**

```dockerfile
# Start from official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (if needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/map_server /app/map_server

# Expose port
EXPOSE 5000

# Set Python path
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "map_server/app.py"]
```

### Dockerfile for Agent

**File: `Dockerfile.agent`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/agent /app/agent

ENV PYTHONPATH=/app

# Wait for map server, then run agent
CMD ["python", "agent/main.py"]
```

### Understanding Dockerfile Instructions

```dockerfile
# FROM - Base image
FROM python:3.11-slim

# WORKDIR - Set working directory
WORKDIR /app

# ENV - Set environment variables
ENV MY_VAR=value

# COPY - Copy files from host to container
COPY source dest

# RUN - Execute command during build
RUN pip install flask

# EXPOSE - Document which port the app uses
EXPOSE 5000

# CMD - Default command when container starts
CMD ["python", "app.py"]

# ENTRYPOINT - Configure container as executable
ENTRYPOINT ["python"]
CMD ["app.py"]  # Can be overridden
```

## 5. Building Docker Images

### Build Map Server Image

```bash
# Build image
docker build -f Dockerfile.mapserver -t map-server:latest .

# -f: Dockerfile path
# -t: Tag (name:version)
# .: Build context (current directory)

# List images
docker images

# Remove image
docker rmi map-server:latest
```

### Build Agent Image

```bash
docker build -f Dockerfile.agent -t navigation-agent:latest .
```

### Best Practices for Building

1. **Use .dockerignore**
```
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache
.coverage
.venv
venv/
.git
.gitignore
README.md
*.md
.env
```

2. **Layer Caching**
```dockerfile
# Good: Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Bad: Copy everything first
COPY . .
RUN pip install -r requirements.txt
```

3. **Multi-stage Builds** (Advanced)
```dockerfile
# Build stage
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

## 6. Running Containers

### Run Map Server Container

```bash
# Run in foreground
docker run -p 5000:5000 map-server:latest

# Run in background (detached)
docker run -d -p 5000:5000 --name mapserver map-server:latest

# -d: Detached mode
# -p: Port mapping (host:container)
# --name: Container name

# Check running containers
docker ps

# View logs
docker logs mapserver

# Follow logs
docker logs -f mapserver

# Stop container
docker stop mapserver

# Remove container
docker rm mapserver
```

### Run Agent Container

```bash
docker run -d --name agent \
  --link mapserver:mapserver \
  -e MAP_SERVER_URL=http://mapserver:5000 \
  navigation-agent:latest
```

### Common Docker Commands

```bash
# Container management
docker ps                    # List running containers
docker ps -a                 # List all containers
docker stop <container>      # Stop container
docker start <container>     # Start stopped container
docker restart <container>   # Restart container
docker rm <container>        # Remove container
docker rm -f <container>     # Force remove running container

# Image management
docker images               # List images
docker rmi <image>          # Remove image
docker pull <image>         # Download image
docker push <image>         # Upload to registry

# Logs and inspection
docker logs <container>     # View logs
docker inspect <container>  # Detailed info
docker exec -it <container> /bin/bash  # Interactive shell

# Cleanup
docker system prune         # Remove unused data
docker container prune      # Remove stopped containers
docker image prune          # Remove unused images
```

## 7. Docker Compose

Docker Compose manages multi-container applications.

### docker-compose.yml

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  # Map Server Service
  mapserver:
    build:
      context: .
      dockerfile: Dockerfile.mapserver
    image: map-server:latest
    container_name: map-server
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Navigation Agent Service
  agent:
    build:
      context: .
      dockerfile: Dockerfile.agent
    image: navigation-agent:latest
    container_name: navigation-agent
    depends_on:
      - mapserver
    environment:
      - MAP_SERVER_URL=http://mapserver:5000
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
```

### Docker Compose Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Build and start
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f mapserver

# Scale a service (multiple instances)
docker-compose up -d --scale agent=3

# Restart a service
docker-compose restart mapserver

# Execute command in service
docker-compose exec mapserver /bin/bash
```

### Understanding docker-compose.yml

```yaml
version: '3.8'  # Compose file version

services:       # Define services (containers)
  myservice:
    build: .                    # Build from Dockerfile in current dir
    image: myimage:tag          # Image name after build
    container_name: mycontainer # Container name
    ports:                      # Port mapping
      - "8080:80"              # host:container
    environment:                # Environment variables
      - KEY=value
    volumes:                    # Mount volumes
      - ./data:/app/data
    depends_on:                 # Service dependencies
      - database
    networks:                   # Connect to networks
      - mynetwork
    restart: always             # Restart policy

networks:       # Define networks
  mynetwork:
    driver: bridge

volumes:        # Define volumes
  mydata:
    driver: local
```

## 8. Environment Variables and Secrets

### Using .env File

**File: `.env`**
```bash
# Map Server Configuration
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Agent Configuration
MAP_SERVER_URL=http://mapserver:5000
AGENT_ID=agent-001
LOG_LEVEL=INFO
```

**Update docker-compose.yml:**
```yaml
services:
  mapserver:
    env_file:
      - .env
    environment:
      - FLASK_ENV=${FLASK_ENV}
      - FLASK_DEBUG=${FLASK_DEBUG}
```

**Don't commit .env to git!** Add to `.gitignore`

### Using Secrets (Docker Swarm)

```yaml
services:
  mapserver:
    secrets:
      - api_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
```

## 9. Persistent Data with Volumes

```yaml
services:
  mapserver:
    volumes:
      # Named volume (managed by Docker)
      - map-data:/app/data
      
      # Bind mount (host directory)
      - ./logs:/app/logs
      
      # Read-only mount
      - ./config:/app/config:ro

volumes:
  map-data:
    driver: local
```

### Volume Commands

```bash
# List volumes
docker volume ls

# Create volume
docker volume create mydata

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

## 10. Networking

### Network Types

1. **Bridge** (default) - Isolated network
2. **Host** - Use host's network directly
3. **None** - No networking

### Custom Networks

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

services:
  mapserver:
    networks:
      - frontend
      - backend
  
  agent:
    networks:
      - backend
```

### Network Commands

```bash
# List networks
docker network ls

# Create network
docker network create mynetwork

# Connect container to network
docker network connect mynetwork mycontainer

# Inspect network
docker network inspect mynetwork
```

## 11. Complete Deployment

### Step-by-Step Deployment

```bash
# 1. Clone repository
git clone https://github.com/yourusername/python-for-engineers.git
cd python-for-engineers

# 2. Create .env file
cp .env.example .env
# Edit .env with your settings

# 3. Build images
docker-compose build

# 4. Start services
docker-compose up -d

# 5. Check status
docker-compose ps

# 6. View logs
docker-compose logs -f

# 7. Test the services
curl http://localhost:5000/

# 8. Stop services (when done)
docker-compose down
```

### Health Checks

```bash
# Check container health
docker ps

# HEALTHY / UNHEALTHY / STARTING shown in STATUS

# Inspect health check results
docker inspect --format='{{json .State.Health}}' map-server
```

## 12. Production Considerations

### Security

```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Don't expose unnecessary ports
# Use secrets for sensitive data
# Keep base images updated
```

### Optimization

```dockerfile
# Use slim/alpine images
FROM python:3.11-slim

# Multi-stage builds
# Minimize layers
# Remove build dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install -r requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
```

### Logging

```python
# Configure logging to stdout
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
```

### Monitoring

```yaml
services:
  mapserver:
    labels:
      - "com.example.service=mapserver"
      - "com.example.version=1.0"
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 13. Troubleshooting

### Common Issues

**Container exits immediately:**
```bash
docker logs <container>
# Check for errors in logs
```

**Port already in use:**
```bash
lsof -i :5000  # Find what's using port 5000
docker-compose down  # Stop services
```

**Cannot connect to service:**
```bash
# Check if service is running
docker-compose ps

# Check network
docker network inspect python-for-engineers_app-network

# Check from inside container
docker-compose exec mapserver ping agent
```

**Build errors:**
```bash
# Clean build
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -f Dockerfile.mapserver .
```

## Practice Exercise

1. Create Docker images for both services
2. Write a docker-compose.yml file
3. Add health checks
4. Configure environment variables
5. Add persistent volumes for logs
6. Deploy and test the application

**Solution in:** `solutions/07-docker-deployment/`

## Comparing to Java

### Java (Spring Boot)

```dockerfile
FROM openjdk:11-jre-slim
COPY target/myapp.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Python (Flask)

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Python advantages:**
- No build step needed
- Smaller base images available
- Faster iteration

## Key Takeaways

✅ Docker provides consistent environments  
✅ Dockerfile defines how to build images  
✅ Docker Compose manages multi-container apps  
✅ Use .dockerignore to exclude unnecessary files  
✅ Layer caching speeds up builds  
✅ Environment variables configure containers  
✅ Volumes persist data beyond container lifecycle  
✅ Networks enable container communication  

## Quick Reference

```bash
# Build and run
docker build -t myapp .
docker run -d -p 8080:80 myapp

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f

# Cleanup
docker system prune -a
```

## 🎉 Congratulations!

You've completed the Python for Engineers tutorial! You now know how to:
- Write Python code
- Set up Python projects
- Manage dependencies
- Build AI agents
- Create REST APIs with Flask
- Deploy applications with Docker

## Next Steps

- Explore advanced Python libraries (NumPy, Pandas, TensorFlow)
- Learn about Kubernetes for orchestration
- Study design patterns in Python
- Build more complex AI agents
- Contribute to open-source Python projects

---

**Tutorial Complete! 🚀**
