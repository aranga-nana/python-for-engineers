# Python for Engineers: A 3-Hour Tutorial for Java Developers

Welcome to this comprehensive Python tutorial designed specifically for experienced Java engineers. This course will take you from Python basics to deploying AI agents in Docker containers.

## 🎯 Course Overview

This 3-hour tutorial covers:
- Python fundamentals (for Java engineers)
- Setting up Python projects on Mac
- Dependency management
- Building AI agents
- Creating a map server
- Docker containerization and deployment

## 📋 Prerequisites

- Basic understanding of programming (Java experience)
- macOS computer
- Terminal/command-line familiarity
- Text editor or IDE (VS Code recommended)

## 🚀 Quick Start

1. Clone this repository
2. Follow the lessons in order (lessons/01-python-basics through lessons/07-docker-deployment)
3. Work through exercises in each lesson
4. Deploy your final application using Docker

## 📚 Lesson Structure

### [Lesson 1: Python Basics for Java Engineers](lessons/01-python-basics/)
- Python vs Java: Key differences
- Data types and variables
- Control structures
- Functions and classes
- Exception handling
- **Duration:** 25 minutes

### [Lesson 2: Setting Up Python on Mac](lessons/02-python-setup/)
- Installing Python 3
- Setting up your development environment
- Choosing an IDE
- Project structure best practices
- **Duration:** 15 minutes

### [Lesson 3: Dependency Management](lessons/03-dependency-management/)
- Understanding pip
- Virtual environments (venv)
- requirements.txt
- Managing dependencies
- **Duration:** 20 minutes

### [Lesson 4: Introduction to AI Agents](lessons/04-ai-agents-intro/)
- What are AI agents?
- Agent architecture
- Common use cases
- Design patterns
- **Duration:** 20 minutes

### [Lesson 5: Building a Simple AI Agent](lessons/05-building-agent/)
- Creating an agent class
- Implementing agent logic
- State management
- Agent communication
- **Duration:** 30 minutes

### [Lesson 6: Building a Map Server](lessons/06-map-server/)
- REST API basics with Flask
- Creating endpoints
- Serving map data
- Integration with the agent
- **Duration:** 30 minutes

### [Lesson 7: Docker Deployment](lessons/07-docker-deployment/)
- Introduction to Docker
- Writing Dockerfiles
- Docker Compose
- Building and running containers
- Deploying your application
- **Duration:** 40 minutes

## 🛠️ Project Structure

```
python-for-engineers/
├── lessons/              # Tutorial lessons
├── src/                  # Source code
│   ├── agent/           # AI agent implementation
│   └── map_server/      # Map server implementation
├── docker/              # Docker configuration
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Multi-container setup
└── README.md           # This file
```

## 🏃 Running the Application

### Local Development
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the map server
python src/map_server/app.py

# In another terminal, run the agent
python src/agent/agent.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the map server at http://localhost:5000
```

## 📝 Exercises

Each lesson includes hands-on exercises to reinforce learning. Solutions are provided in the `solutions/` directory.

## 🎓 Learning Path

1. **Complete each lesson sequentially** - Each builds on previous concepts
2. **Try the exercises** - Hands-on practice is essential
3. **Experiment** - Modify the code and see what happens
4. **Review Java comparisons** - Understand the paradigm differences

## 🐛 Troubleshooting

### Common Issues
- **Python not found**: Ensure Python 3.8+ is installed
- **Permission errors**: Use `sudo` carefully or fix with `chmod`
- **Module not found**: Activate your virtual environment
- **Docker issues**: Ensure Docker Desktop is running

## 📖 Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Python for Java Developers](https://docs.python.org/3/tutorial/)

## 🤝 Contributing

This is a learning resource. Feel free to submit issues or pull requests to improve the tutorial.

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created for engineers transitioning from Java to Python for AI development.

---

**Ready to start?** Head to [Lesson 1: Python Basics](lessons/01-python-basics/README.md)!