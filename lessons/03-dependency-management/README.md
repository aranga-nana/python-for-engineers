# Lesson 3: Dependency Management

**Duration:** 20 minutes

## Overview

Learn how to manage Python dependencies effectively, similar to Maven/Gradle in Java, using pip, virtual environments, and requirements files.

## 1. Dependency Management: Java vs Python

### Java (Maven)
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.9</version>
    </dependency>
</dependencies>
```

### Python (requirements.txt)
```text
flask==2.3.0
requests==2.31.0
numpy>=1.24.0
```

## 2. Understanding pip

pip is Python's package installer (like Maven for Java).

### Basic pip Commands

```bash
# Install a package
pip install flask

# Install specific version
pip install flask==2.3.0

# Install minimum version
pip install flask>=2.0.0

# Install from requirements.txt
pip install -r requirements.txt

# Upgrade a package
pip install --upgrade flask

# Uninstall
pip uninstall flask

# Show package info
pip show flask

# List installed packages
pip list

# List outdated packages
pip list --outdated
```

### pip vs pip3

On macOS, you might have both:
- `pip` - might point to Python 2
- `pip3` - explicitly Python 3

**Best practice:** Use virtual environments, then `pip` always refers to the current environment.

## 3. Virtual Environments Deep Dive

### Why Virtual Environments?

**Problem without venv:**
```
Project A needs flask==1.1.0
Project B needs flask==2.0.0
```

**Solution:** Each project gets its own isolated environment.

### Creating Virtual Environments

```bash
# Create a virtual environment
python3 -m venv myenv

# OR specify Python version
python3.9 -m venv myenv

# Activate
source myenv/bin/activate

# Deactivate
deactivate
```

### Virtual Environment Structure

```
venv/
├── bin/              # Executables (activate script, pip, python)
├── include/          # C headers
├── lib/              # Installed packages
└── pyvenv.cfg        # Configuration
```

### Common venv Commands

```bash
# Check which Python you're using
which python

# Should point to: /path/to/project/venv/bin/python

# Check pip location
which pip

# See installed packages (in current venv)
pip list
```

## 4. requirements.txt

### Creating requirements.txt

```bash
# Automatically generate from current environment
pip freeze > requirements.txt
```

**Example requirements.txt:**
```text
flask==2.3.0
requests==2.31.0
numpy==1.24.3
gunicorn==20.1.0
```

### Version Specifiers

```text
# Exact version
flask==2.3.0

# Minimum version
flask>=2.0.0

# Maximum version
flask<=3.0.0

# Compatible release (will install 2.x but not 3.x)
flask~=2.3.0

# Any version (not recommended)
flask

# Version range
flask>=2.0.0,<3.0.0

# Latest version
flask
```

### Installing from requirements.txt

```bash
# Install all dependencies
pip install -r requirements.txt

# Upgrade all to latest versions
pip install -r requirements.txt --upgrade
```

### Multiple Requirements Files

**Development setup:**
```
requirements/
├── base.txt          # Common dependencies
├── dev.txt           # Development dependencies
└── prod.txt          # Production dependencies
```

**base.txt:**
```text
flask==2.3.0
requests==2.31.0
```

**dev.txt:**
```text
-r base.txt           # Include base
pytest==7.3.1
black==23.3.0
pylint==2.17.4
```

**prod.txt:**
```text
-r base.txt
gunicorn==20.1.0
```

**Install for development:**
```bash
pip install -r requirements/dev.txt
```

## 5. Best Practices for Dependency Management

### ✅ DO:

1. **Always use virtual environments**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Pin versions in production**
```text
flask==2.3.0  # Not flask>=2.0.0
```

3. **Keep requirements.txt updated**
```bash
pip freeze > requirements.txt
```

4. **Separate dev and prod dependencies**

5. **Document special installation steps**
```text
# requirements.txt
# Note: Requires system library libpq-dev
psycopg2==2.9.6
```

### ❌ DON'T:

1. **Don't install packages globally (without venv)**
2. **Don't commit the venv/ directory** (add to .gitignore)
3. **Don't use `sudo pip install`**
4. **Don't mix pip and system package managers**

## 6. Common Packages for This Tutorial

### Web Framework
```bash
pip install flask
```
**Flask** - Lightweight web framework (like Spring Boot but simpler)

### HTTP Client
```bash
pip install requests
```
**Requests** - Elegant HTTP library

### Data Handling
```bash
pip install numpy pandas
```
**NumPy** - Numerical computing  
**Pandas** - Data manipulation

### Testing
```bash
pip install pytest
```
**pytest** - Testing framework

### Code Quality
```bash
pip install pylint black
```
**pylint** - Linting  
**black** - Code formatting

## 7. Package Structure and __init__.py

### Creating a Package

```
mypackage/
├── __init__.py       # Makes it a package
├── module1.py
└── module2.py
```

**__init__.py:**
```python
# Can be empty, or expose modules
from .module1 import function1
from .module2 import function2

__version__ = "1.0.0"
```

### Importing from Your Package

```python
# Import entire package
import mypackage

# Import specific module
from mypackage import module1

# Import specific function
from mypackage.module1 import function1
```

## 8. Advanced: setup.py and pip install -e

### Creating Installable Package

**setup.py:**
```python
from setuptools import setup, find_packages

setup(
    name="myproject",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask>=2.3.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.0",
            "black>=23.3.0",
        ]
    },
    python_requires=">=3.8",
)
```

### Editable Install

```bash
# Install package in development mode
pip install -e .

# Now you can import your package from anywhere
python
>>> import myproject
```

**Benefits:**
- Code changes are immediately available
- No need to reinstall after changes
- Can be imported from anywhere

## 9. Troubleshooting Dependencies

### Conflicting Dependencies

```bash
# See dependency tree
pip install pipdeptree
pipdeptree

# Example output:
flask==2.3.0
  - click [required: >=8.0]
  - itsdangerous [required: >=2.0]
```

### Dependency Hell Solutions

1. **Use a clean virtual environment**
```bash
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Pin all versions explicitly**
```bash
pip freeze > requirements.txt
```

3. **Use requirements.in and pip-compile**
```bash
pip install pip-tools
pip-compile requirements.in
```

### Common Errors

**Error: "No module named X"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install the package
pip install X
```

**Error: "Permission denied"**
```bash
# Don't use sudo! Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install X
```

## 10. Comparing to Java Tools

| Java | Python | Purpose |
|------|--------|---------|
| Maven pom.xml | requirements.txt | Dependency list |
| Gradle build.gradle | setup.py | Build configuration |
| mvn install | pip install | Install packages |
| Maven Central | PyPI | Package repository |
| .m2 cache | pip cache | Local package cache |

## Practice Exercise

Create a project with the following:

1. Create a virtual environment
2. Install Flask, Requests, and pytest
3. Create a requirements.txt file
4. Create a simple Python package with:
   - An `__init__.py` file
   - A module that uses requests to fetch data
   - A test file using pytest
5. Install your package in editable mode

**Solution in:** `solutions/03-dependency-exercise/`

## Common Workflow

```bash
# Start new project
mkdir myproject && cd myproject
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install flask requests pytest

# Save dependencies
pip freeze > requirements.txt

# Work on project...

# Deactivate when done
deactivate

# Later, on another machine:
git clone <repo>
cd myproject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Key Takeaways

✅ Virtual environments isolate project dependencies  
✅ Always activate venv before installing packages  
✅ Use `requirements.txt` to track dependencies  
✅ Pin versions for production deployments  
✅ Never commit the venv/ directory  
✅ Use `pip freeze` to capture exact versions  
✅ Consider separate dev and prod requirements  

## Quick Reference

```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate
deactivate

# Package management
pip install package
pip install -r requirements.txt
pip freeze > requirements.txt
pip list
pip show package

# Check environment
which python
which pip
```

---

**Next:** [Lesson 4: Introduction to AI Agents](../04-ai-agents-intro/README.md)
