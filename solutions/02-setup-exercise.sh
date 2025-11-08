#!/bin/bash
# Solution for Lesson 2: Python Setup Exercise

echo "Setting up hello-python project..."
echo

# Step 1: Create project directory
echo "1. Creating project directory..."
mkdir -p hello-python
cd hello-python

# Step 2: Create standard project structure
echo "2. Creating project structure..."
mkdir -p src tests docs
touch README.md .gitignore

# Step 3: Create .gitignore
echo "3. Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
EOF

# Step 4: Create virtual environment
echo "4. Creating virtual environment..."
python3 -m venv venv

# Step 5: Activate virtual environment
echo "5. Activating virtual environment..."
source venv/bin/activate

# Step 6: Create main.py
echo "6. Creating main.py..."
cat > src/main.py << 'EOF'
"""
Hello Python - A simple Python script
"""

def main():
    """Main function."""
    print("Hello from Python!")
    print("This is a Python project for Java engineers.")
    
    # Demonstrate some Python features
    name = "Python"
    version = 3.11
    features = ["Simple", "Powerful", "Fun"]
    
    print(f"\nLanguage: {name}")
    print(f"Version: {version}")
    print(f"Features: {', '.join(features)}")

if __name__ == "__main__":
    main()
EOF

# Step 7: Run the script
echo "7. Running the script..."
echo
python src/main.py
echo

# Step 8: Create requirements.txt
echo "8. Creating requirements.txt..."
touch requirements.txt

echo
echo "✓ Setup complete!"
echo
echo "Project structure:"
tree -L 2 . 2>/dev/null || find . -maxdepth 2 -not -path '*/venv/*' -not -path '*/.git/*'
echo
echo "To run the script:"
echo "  cd hello-python"
echo "  source venv/bin/activate"
echo "  python src/main.py"
