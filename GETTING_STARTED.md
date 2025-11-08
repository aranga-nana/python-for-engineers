# Getting Started Guide

Welcome! This guide will help you get started with the Python for Engineers tutorial.

## Prerequisites

Before starting, ensure you have:

- **macOS** (these instructions are Mac-specific)
- **Python 3.8+** installed
- **Docker Desktop** (for Lesson 7)
- **Terminal** access
- **Text editor** or IDE (VS Code recommended)

## Quick Start Options

### Option 1: Run Locally (Recommended for Learning)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/python-for-engineers.git
   cd python-for-engineers
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the map server** (Terminal 1)
   ```bash
   python src/map_server/app.py
   ```

5. **Run the agent** (Terminal 2)
   ```bash
   # Keep the map server running in Terminal 1
   # In a new terminal:
   source venv/bin/activate
   python src/agent/main.py
   ```

### Option 2: Run with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/python-for-engineers.git
   cd python-for-engineers
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the map server**
   ```
   Open http://localhost:5000 in your browser
   ```

4. **Stop the services**
   ```bash
   docker-compose down
   ```

## Learning Path

Follow the lessons in order:

1. **[Lesson 1: Python Basics](lessons/01-python-basics/README.md)**
   - Start here if you're new to Python
   - Compares Python to Java
   - Duration: 25 minutes

2. **[Lesson 2: Python Setup](lessons/02-python-setup/README.md)**
   - Setting up your Mac for Python development
   - Duration: 15 minutes

3. **[Lesson 3: Dependency Management](lessons/03-dependency-management/README.md)**
   - Virtual environments and pip
   - Duration: 20 minutes

4. **[Lesson 4: AI Agents Intro](lessons/04-ai-agents-intro/README.md)**
   - Understanding AI agents
   - Duration: 20 minutes

5. **[Lesson 5: Building an Agent](lessons/05-building-agent/README.md)**
   - Hands-on: Create the navigation agent
   - Duration: 30 minutes

6. **[Lesson 6: Map Server](lessons/06-map-server/README.md)**
   - Build a Flask REST API
   - Duration: 30 minutes

7. **[Lesson 7: Docker Deployment](lessons/07-docker-deployment/README.md)**
   - Containerize and deploy
   - Duration: 40 minutes

**Total time: ~3 hours**

## Testing Your Setup

### Test Map Server

```bash
# Start the server
python src/map_server/app.py

# In another terminal, test with curl:
curl http://localhost:5000/

# Should return: {"status": "ok", ...}
```

### Test Agent

```bash
# Make sure map server is running first
python src/agent/main.py

# Should see agent navigating between locations
```

### Test with Docker

```bash
docker-compose up

# Watch the logs to see the agent navigating
```

## Project Structure

```
python-for-engineers/
├── lessons/              # Tutorial lessons (start here!)
│   ├── 01-python-basics/
│   ├── 02-python-setup/
│   ├── 03-dependency-management/
│   ├── 04-ai-agents-intro/
│   ├── 05-building-agent/
│   ├── 06-map-server/
│   └── 07-docker-deployment/
├── src/                  # Source code
│   ├── agent/           # Navigation agent
│   └── map_server/      # Map server API
├── solutions/           # Exercise solutions
├── requirements.txt     # Python dependencies
├── Dockerfile.mapserver # Map server Docker image
├── Dockerfile.agent    # Agent Docker image
├── docker-compose.yml  # Multi-container setup
└── README.md           # Project overview
```

## Common Issues

### Python not found
```bash
# Check Python installation
python3 --version

# If not installed, use Homebrew:
brew install python3
```

### Permission errors
```bash
# Don't use sudo! Use virtual environment instead:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Module not found
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port already in use
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process or use a different port
```

### Docker issues
```bash
# Make sure Docker Desktop is running
# Restart Docker if needed

# Clean up Docker resources
docker-compose down
docker system prune
```

## Getting Help

- **Check the lessons**: Each lesson has detailed explanations
- **Review solutions**: Look in the `solutions/` directory
- **Read error messages**: Python error messages are helpful!
- **Search online**: Python has excellent documentation

## Next Steps

1. **Start with Lesson 1**: [Python Basics](lessons/01-python-basics/README.md)
2. **Complete each lesson in order**
3. **Try the exercises**
4. **Experiment with the code**
5. **Build something new!**

## Tips for Success

✅ **Follow the lessons sequentially** - Each builds on previous concepts  
✅ **Type the code yourself** - Don't just copy-paste  
✅ **Experiment** - Modify the code and see what happens  
✅ **Use the REPL** - Test small snippets with `python3`  
✅ **Read error messages** - They tell you what's wrong  
✅ **Take breaks** - The tutorial is 3 hours, pace yourself  

## Questions?

This tutorial covers:
- Python fundamentals for Java developers
- Setting up Python projects on Mac
- Virtual environments and dependency management
- Building AI agents
- Creating REST APIs with Flask
- Docker containerization

Ready to start? Head to [Lesson 1: Python Basics](lessons/01-python-basics/README.md)!

---

**Happy Learning! 🚀**
