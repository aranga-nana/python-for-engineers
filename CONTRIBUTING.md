# Contributing to Python for Engineers

Thank you for your interest in improving this tutorial! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

If you find errors, typos, or have suggestions:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear description of the problem
   - Steps to reproduce (if applicable)
   - Suggested solution (if you have one)
   - Lesson/file affected

### Submitting Changes

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR-USERNAME/python-for-engineers.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b fix/lesson-1-typo
   # or
   git checkout -b feature/add-advanced-examples
   ```

3. **Make your changes**
   - Follow the existing style
   - Test your code
   - Update documentation

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Fix typo in Lesson 1"
   ```

5. **Push and create Pull Request**
   ```bash
   git push origin fix/lesson-1-typo
   # Create PR on GitHub
   ```

## Guidelines

### Lesson Content

- **Keep it practical**: Focus on hands-on examples
- **Explain Java differences**: Compare to Java when relevant
- **Include exercises**: Add practice problems
- **Test everything**: Ensure all code examples work
- **Stay on topic**: Keep lessons focused on their subject

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints where helpful
- Add docstrings to functions/classes
- Keep functions small and focused
- Use meaningful variable names

**Example:**
```python
def calculate_distance(point1: Tuple[float, float], 
                      point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
        
    Returns:
        Distance as a float
    """
    return math.sqrt(
        (point2[0] - point1[0])**2 + 
        (point2[1] - point1[1])**2
    )
```

### Documentation

- Use clear, concise language
- Include code examples
- Add comments for complex logic
- Keep README.md updated
- Use proper Markdown formatting

### Testing

Before submitting:

1. **Test locally**
   ```bash
   python src/map_server/app.py
   python src/agent/main.py
   ```

2. **Test with Docker** (if applicable)
   ```bash
   docker-compose up --build
   ```

3. **Check for errors**
   - No Python syntax errors
   - All imports work
   - Code runs without crashes

## Areas for Contribution

### High Priority

- [ ] Add more exercises with solutions
- [ ] Expand lesson examples
- [ ] Add troubleshooting tips
- [ ] Improve error handling
- [ ] Add unit tests

### Medium Priority

- [ ] Add advanced topics (async, decorators)
- [ ] Create video tutorials
- [ ] Add interactive notebooks
- [ ] Improve Docker configuration
- [ ] Add CI/CD examples

### Nice to Have

- [ ] Windows/Linux setup guides
- [ ] More agent examples
- [ ] Database integration examples
- [ ] Deployment to cloud platforms
- [ ] Performance optimization tips

## Code Review Process

1. Maintainers will review your PR
2. May request changes or improvements
3. Once approved, will be merged
4. Your contribution will be credited

## Questions?

- Open an issue for questions
- Check existing documentation first
- Be respectful and patient

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping improve this tutorial! 🙏**
