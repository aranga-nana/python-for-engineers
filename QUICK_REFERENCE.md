# Python Quick Reference for Java Engineers

This is a quick reference card comparing Python and Java syntax.

## Basic Syntax

| Feature | Java | Python |
|---------|------|--------|
| Variable | `String name = "Alice";` | `name = "Alice"` |
| Constant | `final int MAX = 100;` | `MAX = 100` (convention: ALL_CAPS) |
| Comment | `// comment` or `/* comment */` | `# comment` or `"""comment"""` |
| Print | `System.out.println("Hi");` | `print("Hi")` |
| Null | `null` | `None` |
| Boolean | `true`, `false` | `True`, `False` |

## Data Structures

| Structure | Java | Python |
|-----------|------|--------|
| Array/List | `List<String> list = new ArrayList<>();` | `list = []` or `list = ["a", "b"]` |
| Map/Dict | `Map<K,V> map = new HashMap<>();` | `dict = {}` or `dict = {"k": "v"}` |
| Set | `Set<String> set = new HashSet<>();` | `set = set()` or `set = {1, 2, 3}` |

## Control Flow

### If Statement
**Java:**
```java
if (x > 10) {
    // code
} else if (x > 5) {
    // code
} else {
    // code
}
```

**Python:**
```python
if x > 10:
    # code
elif x > 5:
    # code
else:
    # code
```

### For Loop
**Java:**
```java
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

for (String item : list) {
    System.out.println(item);
}
```

**Python:**
```python
for i in range(10):
    print(i)

for item in list:
    print(item)
```

### While Loop
**Java:**
```java
while (condition) {
    // code
}
```

**Python:**
```python
while condition:
    # code
```

## Functions/Methods

**Java:**
```java
public int add(int a, int b) {
    return a + b;
}
```

**Python:**
```python
def add(a, b):
    return a + b
```

## Classes

**Java:**
```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void greet() {
        System.out.println("Hello, " + name);
    }
}

Person p = new Person("Alice", 30);
```

**Python:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        print(f"Hello, {self.name}")

p = Person("Alice", 30)
```

## Exception Handling

**Java:**
```java
try {
    // code
} catch (IOException e) {
    e.printStackTrace();
} finally {
    // cleanup
}
```

**Python:**
```python
try:
    # code
except IOError as e:
    print(e)
finally:
    # cleanup
```

## Common Operations

### String Operations

| Operation | Java | Python |
|-----------|------|--------|
| Length | `str.length()` | `len(str)` |
| Substring | `str.substring(0, 5)` | `str[0:5]` |
| Split | `str.split(",")` | `str.split(",")` |
| Join | `String.join(",", list)` | `",".join(list)` |
| Format | `String.format("Hi %s", name)` | `f"Hi {name}"` |
| Contains | `str.contains("x")` | `"x" in str` |

### List Operations

| Operation | Java | Python |
|-----------|------|--------|
| Add | `list.add(item)` | `list.append(item)` |
| Get | `list.get(0)` | `list[0]` |
| Size | `list.size()` | `len(list)` |
| Remove | `list.remove(item)` | `list.remove(item)` |
| Sort | `Collections.sort(list)` | `list.sort()` or `sorted(list)` |

## File I/O

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
```

## Virtual Environment & Dependencies

**Java (Maven):**
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.9</version>
    </dependency>
</dependencies>
```

**Python:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# requirements.txt
flask==3.0.0
requests==2.31.0

# Install
pip install -r requirements.txt
```

## REST API

**Java (Spring Boot):**
```java
@RestController
public class MyController {
    @GetMapping("/api/data")
    public Data getData() {
        return new Data();
    }
}
```

**Python (Flask):**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({'key': 'value'})

app.run()
```

## Docker

**Java (Spring Boot):**
```dockerfile
FROM openjdk:11-jre-slim
COPY target/myapp.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Python:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Common Patterns

### List Comprehension (Python)
```python
# Instead of:
squares = []
for i in range(10):
    squares.append(i * i)

# Use:
squares = [i * i for i in range(10)]
```

### Lambda Functions
**Java:**
```java
list.stream()
    .filter(x -> x > 5)
    .map(x -> x * 2)
    .collect(Collectors.toList());
```

**Python:**
```python
result = [x * 2 for x in list if x > 5]
# or
result = list(map(lambda x: x * 2, filter(lambda x: x > 5, list)))
```

## Important Differences

1. **Indentation matters** in Python (no braces)
2. **No semicolons** in Python
3. **Dynamic typing** in Python (no type declarations)
4. **`self` must be explicit** in Python methods
5. **No access modifiers** (public/private) in Python (convention: `_private`)
6. **Multiple return values** easy in Python: `return x, y`
7. **List slicing** is powerful: `list[start:end:step]`
8. **Duck typing** in Python (no interfaces needed)

## Python Idioms

### Check if list is empty
```python
if not my_list:  # Pythonic
    print("Empty")
```

### Swap variables
```python
a, b = b, a  # No temp variable needed!
```

### Iterate with index
```python
for i, item in enumerate(my_list):
    print(f"{i}: {item}")
```

### Dictionary get with default
```python
value = my_dict.get('key', 'default')
```

### Check membership
```python
if item in my_list:  # Very readable
    print("Found")
```

## Common Pitfalls

1. **Mutable default arguments**
   ```python
   # BAD
   def add_item(item, list=[]):
       list.append(item)
       return list
   
   # GOOD
   def add_item(item, list=None):
       if list is None:
           list = []
       list.append(item)
       return list
   ```

2. **Integer division**
   ```python
   # Python 3
   5 / 2   # 2.5 (float division)
   5 // 2  # 2 (integer division)
   ```

3. **Comparing to None**
   ```python
   # GOOD
   if x is None:
   
   # BAD
   if x == None:
   ```

## Resources

- [Python Official Docs](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python for Java Programmers](https://docs.python.org/3/tutorial/)

---

**Tip:** When in doubt, use `type()`, `dir()`, and `help()` in the Python REPL!

```python
>>> type([1, 2, 3])
<class 'list'>
>>> dir(list)
['append', 'clear', 'copy', ...]
>>> help(list.append)
```
