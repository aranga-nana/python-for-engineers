"""
Solution for Lesson 1: Python Basics - Calculator Exercise
"""


class Calculator:
    """A simple calculator class with basic operations."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.last_result = None
    
    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.last_result = result
        return result
    
    def subtract(self, a, b):
        """Subtract b from a."""
        result = a - b
        self.last_result = result
        return result
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        result = a * b
        self.last_result = result
        return result
    
    def divide(self, a, b):
        """Divide a by b with error handling."""
        try:
            result = a / b
            self.last_result = result
            return result
        except ZeroDivisionError:
            print("Error: Cannot divide by zero!")
            return None


def main():
    """Demonstrate calculator usage."""
    calc = Calculator()
    
    print("Calculator Demo")
    print("=" * 40)
    
    # Addition
    result = calc.add(10, 5)
    print(f"10 + 5 = {result}")
    
    # Subtraction
    result = calc.subtract(10, 5)
    print(f"10 - 5 = {result}")
    
    # Multiplication
    result = calc.multiply(10, 5)
    print(f"10 × 5 = {result}")
    
    # Division
    result = calc.divide(10, 5)
    print(f"10 ÷ 5 = {result}")
    
    # Division by zero (error handling)
    print("\nTesting error handling:")
    result = calc.divide(10, 0)
    print(f"Result: {result}")
    
    print(f"\nLast successful result: {calc.last_result}")


if __name__ == "__main__":
    main()
