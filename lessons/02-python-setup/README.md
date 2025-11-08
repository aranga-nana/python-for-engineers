# Lesson 2: Setting Up Python on Mac

**Duration:** 15 minutes

## Overview

Learn how to set up a professional Python development environment on macOS, including best practices for project structure.

## 1. Installing Python 3

### Check Existing Installation

macOS comes with Python 2.7 pre-installed, but we need Python 3:

```bash
python --version    # Likely shows Python 2.x
python3 --version   # Check for Python 3
```

### Installation Options

#### Option A: Homebrew (Recommended)

1. **Install Homebrew** (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install Python 3**:
```bash
brew install python3
```

3. **Verify Installation**:
```bash
python3 --version   # Should show Python 3.8 or higher
pip3 --version      # pip is included
```

#### Option B: Official Python.org Installer

1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer package
3. Follow the installation wizard

### Adding Python to PATH

Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
# For Homebrew Python
export PATH="/usr/local/opt/python/libexec/bin:$PATH"

# Create alias for convenience
alias python=python3
alias pip=pip3
```

Reload your shell:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

## 2. Choosing an IDE

### Option A: Visual Studio Code (Recommended)

**Install:**
```bash
brew install --cask visual-studio-code
```

**Essential Extensions:**
- Python (Microsoft)
- Pylance
- Python Docstring Generator
- GitLens

**Configuration:**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

### Option B: PyCharm

```bash
brew install --cask pycharm-ce  # Community Edition
```

### Option C: Simple Text Editors

- Sublime Text: `brew install --cask sublime-text`
- Atom: `brew install --cask atom`

## 3. Setting Up Your First Project

### Standard Python Project Structure

```
my-project/
├── README.md           # Project documentation
├── requirements.txt    # Dependencies
├── setup.py           # Package installation (optional)
├── .gitignore         # Git ignore rules
├── src/               # Source code
│   ├── __init__.py
│   └── main.py
├── tests/             # Test files
│   ├── __init__.py
│   └── test_main.py
├── docs/              # Documentation
└── venv/              # Virtual environment (not committed)
```

### Creating a New Project

```bash
# Create project directory
mkdir my-python-project
cd my-python-project

# Initialize git
git init

# Create basic structure
mkdir src tests docs
touch README.md requirements.txt .gitignore
touch src/__init__.py src/main.py
touch tests/__init__.py tests/test_main.py
```

### Creating .gitignore

Create a `.gitignore` file:
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store

# Testing
.pytest_cache/
.coverage
```

## 4. Virtual Environments

### Why Virtual Environments?

Virtual environments isolate project dependencies, similar to Maven/Gradle in Java.

**Benefits:**
- Different projects can use different package versions
- Avoid conflicts with system Python packages
- Easy to recreate environment on another machine

### Creating a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Your prompt changes to show (venv)
(venv) $ 
```

### Using the Virtual Environment

```bash
# Install packages (only in this environment)
pip install flask requests numpy

# Check installed packages
pip list

# Deactivate when done
deactivate
```

### Saving Dependencies

```bash
# Save current packages to requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt (on another machine)
pip install -r requirements.txt
```

## 5. Essential Python Tools

### pip (Package Manager)

```bash
# Install a package
pip install package-name

# Install specific version
pip install package-name==1.2.3

# Upgrade a package
pip install --upgrade package-name

# Uninstall
pip uninstall package-name

# Search for packages
pip search keyword
```

### Python REPL (Interactive Shell)

```bash
# Start Python interactive shell
python3

>>> print("Hello, World!")
Hello, World!
>>> 2 + 2
4
>>> exit()
```

### Running Python Scripts

```bash
# Run a Python file
python3 script.py

# Run as module
python3 -m src.main

# Run with arguments
python3 script.py arg1 arg2
```

## 6. Setting Up This Tutorial Project

Let's set up the environment for this tutorial:

```bash
# Navigate to the cloned repository
cd python-for-engineers

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies (we'll create requirements.txt next)
pip install -r requirements.txt
```

## 7. Useful Mac Terminal Commands

```bash
# Navigate directories
cd /path/to/directory
cd ..               # Go up one level
cd ~                # Go to home directory
pwd                 # Print current directory

# List files
ls                  # List files
ls -la              # List all files (including hidden)

# File operations
mkdir dirname       # Create directory
touch filename      # Create empty file
rm filename         # Delete file
rm -rf dirname      # Delete directory

# Text viewing
cat filename        # Display file contents
less filename       # Page through file
head filename       # First 10 lines
tail filename       # Last 10 lines
```

## 8. Troubleshooting

### Python Not Found

```bash
# Check where Python is installed
which python3

# Check PATH
echo $PATH

# Reinstall if needed
brew reinstall python3
```

### Permission Errors

```bash
# Don't use sudo with pip (use virtual environments instead)
# If you must (not recommended):
python3 -m pip install --user package-name
```

### Virtual Environment Not Activating

```bash
# Make sure you're in the project directory
cd /path/to/project

# Try with full path
source ./venv/bin/activate

# Or recreate the environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

## Practice Exercise

1. Install Python 3 and verify the installation
2. Create a new project called `hello-python`
3. Set up the standard project structure
4. Create a virtual environment
5. Create a simple `main.py` that prints "Hello from Python!"
6. Run the script

**Solution in:** `solutions/02-setup-exercise.sh`

## VS Code Python Setup Checklist

✅ Python extension installed  
✅ Pylance installed  
✅ Interpreter selected (use virtual environment)  
✅ Linter enabled (pylint)  
✅ Formatter configured (black)  
✅ Terminal integrated  

**To select interpreter in VS Code:**
1. Press `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your virtual environment (`./venv/bin/python`)

## Key Takeaways

✅ Use Homebrew to install Python 3 on Mac  
✅ Always use virtual environments for projects  
✅ VS Code with Python extension is excellent for development  
✅ Follow standard project structure conventions  
✅ Keep dependencies in `requirements.txt`  
✅ Use `.gitignore` to exclude virtual environments  

## Quick Command Reference

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Development
python3 script.py
pip install package-name
pip freeze > requirements.txt

# Cleanup
deactivate
```

---

**Next:** [Lesson 3: Dependency Management](../03-dependency-management/README.md)
