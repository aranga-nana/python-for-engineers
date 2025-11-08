# Lesson 1: Python Basics for Java Engineers

**Duration:** 25 minutes

## Overview

This lesson introduces Python fundamentals through the lens of a Java developer. We'll compare and contrast the two languages to help you leverage your Java knowledge.

## Key Differences: Python vs Java

### Typing
- **Java**: Statically typed, explicit type declarations
- **Python**: Dynamically typed, implicit type inference

### Syntax
- **Java**: Uses braces `{}` and semicolons `;`
- **Python**: Uses indentation (whitespace matters!)

### Compilation
- **Java**: Compiled to bytecode, runs on JVM
- **Python**: Interpreted (though .pyc files exist)

## 1. Variables and Data Types

### Java
```java
String name = "Alice";
int age = 30;
double salary = 75000.50;
boolean isActive = true;
```

### Python
```python
name = "Alice"          # str
age = 30                # int
salary = 75000.50       # float
is_active = True        # bool (note the capital T)
```

**Key Points:**
- No type declarations needed (dynamic typing)
- Use `snake_case` for variable names (Java uses `camelCase`)
- Boolean values are `True` and `False` (capitalized)

## 2. Collections

### Lists (like Java ArrayList)

**Java:**
```java
List<String> fruits = new ArrayList<>();
fruits.add("apple");
fruits.add("banana");
String first = fruits.get(0);
```

**Python:**
```python
fruits = ["apple", "banana"]  # List literal
fruits.append("orange")       # Add item
first = fruits[0]             # Access by index
```

### Dictionaries (like Java HashMap)

**Java:**
```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 30);
ages.put("Bob", 25);
int aliceAge = ages.get("Alice");
```

**Python:**
```python
ages = {"Alice": 30, "Bob": 25}  # Dict literal
ages["Charlie"] = 28             # Add item
alice_age = ages["Alice"]        # Access by key
```

## 3. Control Structures

### If Statements

**Java:**
```java
if (x > 10) {
    System.out.println("Greater than 10");
} else if (x > 5) {
    System.out.println("Greater than 5");
} else {
    System.out.println("5 or less");
}
```

**Python:**
```python
if x > 10:
    print("Greater than 10")
elif x > 5:
    print("Greater than 5")
else:
    print("5 or less")
```

**Key Points:**
- No parentheses needed (but allowed)
- Colon `:` after condition
- Indentation defines the block (usually 4 spaces)
- `elif` instead of `else if`

### Loops

**Java:**
```java
// For loop
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}

// For-each
for (String fruit : fruits) {
    System.out.println(fruit);
}

// While
while (x < 10) {
    x++;
}
```

**Python:**
```python
# For loop with range
for i in range(5):
    print(i)

# For-each (just 'for')
for fruit in fruits:
    print(fruit)

# While
while x < 10:
    x += 1
```

## 4. Functions

**Java:**
```java
public int add(int a, int b) {
    return a + b;
}

public static void main(String[] args) {
    int result = add(3, 4);
}
```

**Python:**
```python
def add(a, b):
    return a + b

# No main method needed, but conventional:
if __name__ == "__main__":
    result = add(3, 4)
    print(result)
```

**Key Points:**
- Use `def` keyword
- No type declarations
- No access modifiers (public, private)
- Return type is implicit

### Default Arguments

**Python only:**
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # "Hello, Alice!"
print(greet("Bob", "Hi"))       # "Hi, Bob!"
```

## 5. Classes and Objects

**Java:**
```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void introduce() {
        System.out.println("I'm " + name);
    }
}

Person p = new Person("Alice", 30);
p.introduce();
```

**Python:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        print(f"I'm {self.name}")

p = Person("Alice", 30)
p.introduce()
```

**Key Points:**
- `__init__` is the constructor
- `self` is like `this` (but must be explicitly declared)
- No `new` keyword needed
- Python uses "magic methods" like `__init__`, `__str__`, etc.

## 6. Exception Handling

**Java:**
```java
try {
    int result = divide(10, 0);
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} finally {
    cleanup();
}
```

**Python:**
```python
try:
    result = divide(10, 0)
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    cleanup()
```

**Key Points:**
- `except` instead of `catch`
- No need to declare exceptions in function signature
- `as` keyword to get exception object

## 7. Important Python Concepts

### None (like Java's null)
```python
value = None
if value is None:
    print("No value")
```

### List Comprehensions (powerful shorthand)
```python
# Instead of:
squares = []
for i in range(10):
    squares.append(i * i)

# Use:
squares = [i * i for i in range(10)]
```

### String Formatting
```python
name = "Alice"
age = 30

# f-strings (Python 3.6+)
message = f"My name is {name} and I'm {age} years old"

# format method
message = "My name is {} and I'm {} years old".format(name, age)
```

### Multiple Return Values
```python
def get_coordinates():
    return 10, 20

x, y = get_coordinates()  # Tuple unpacking
```

## 8. Python-Specific Features

### With Statement (Resource Management)
**Java:**
```java
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    String line = br.readLine();
}
```

**Python:**
```python
with open("file.txt", "r") as f:
    line = f.readline()
# File automatically closed
```

### Duck Typing
Python doesn't check types at compile time:
```python
def process(item):
    item.process()  # Works with any object that has a process() method

# No need for interfaces or inheritance
```

## Practice Exercise

Create a Python program that:
1. Defines a `Calculator` class with methods for add, subtract, multiply, divide
2. Implements error handling for division by zero
3. Creates instances and performs calculations
4. Prints results

**Solution in:** `solutions/01-calculator.py`

## Quick Reference Card

| Feature | Java | Python |
|---------|------|--------|
| Variable | `int x = 5;` | `x = 5` |
| Function | `public int add(int a, int b)` | `def add(a, b):` |
| Class | `public class MyClass {}` | `class MyClass:` |
| Constructor | `public MyClass() {}` | `def __init__(self):` |
| Inheritance | `extends` | `class Child(Parent):` |
| Null | `null` | `None` |
| Boolean | `true`, `false` | `True`, `False` |
| Print | `System.out.println()` | `print()` |

## Key Takeaways

✅ Python syntax is cleaner but indentation matters  
✅ Dynamic typing - no type declarations needed  
✅ No semicolons or braces  
✅ Use `snake_case` for variables and functions  
✅ `self` must be explicit in methods  
✅ List comprehensions are powerful  
✅ F-strings make formatting easy  

---

**Next:** [Lesson 2: Setting Up Python on Mac](../02-python-setup/README.md)
