# Quick Syntax Reference

A cheat sheet for Neutron syntax.

---

## Variables

```neutron
// Declare
var x = 10;
var name = "Alice";

// Multiple declarations
var a = 1, b = 2, c = 3;

// With type annotation
var int age = 25;
var string name = "Bob";
```

## Data Types

```neutron
var number = 42;          // Number (64-bit float)
var text = "Hello";       // String
var flag = true;          // Boolean
var empty = nil;          // Nil (null)
var list = [1, 2, 3];     // Array
var obj = {"key": "val"}; // Object
```

## Operators

### Arithmetic
```neutron
a + b    // Add
a - b    // Subtract
a * b    // Multiply
a / b    // Divide
a % b    // Modulo
a ** b   // Power
a++      // Increment
a--      // Decrement
```

### Comparison
```neutron
a == b   // Equal
a != b   // Not equal
a < b    // Less than
a > b    // Greater than
a <= b   // Less or equal
a >= b   // Greater or equal
```

### Logical
```neutron
a and b    // AND
a or b     // OR
not a      // NOT
a && b     // AND (alt)
a || b     // OR (alt)
!a         // NOT (alt)
```

### String
```neutron
"Hi " + "there"    // Concatenate
"-" * 10           // Repeat
```

## Control Flow

### If/Else
```neutron
if (x > 10) {
    say("Big");
} else if (x > 5) {
    say("Medium");
} else {
    say("Small");
}
```

### Ternary
```neutron
var status = age >= 18 ? "Adult" : "Minor";
```

### Match (Switch)
```neutron
match (day) {
    case 1 => say("Monday");
    case 2 => say("Tuesday");
    default => say("Invalid");
}
```

### Match with Guards
```neutron
var score = 85;
match (score) {
    case score if score >= 90 => say("A");
    case score if score >= 80 => say("B");
    default => say("Below B");
}
```

### Loops
```neutron
// While
while (x < 10) {
    say(x);
    x++;
}

// Do-while
do {
    say(x);
    x++;
} while (x < 10);

// For
for (var i = 0; i < 10; i++) {
    say(i);
}

// For-in object (keys)
var obj = {"a": 1, "b": 2};
for (var key in obj) {
    say(key + ": " + obj[key]);
}

// For-in array (indices)
var arr = [10, 20, 30];
for (var i in arr) {
    say(arr[i]);
}
```

### Loop Control
```neutron
break;      // Exit loop
continue;   // Skip to next
```

## Functions

```neutron
// Define
fun greet(name) {
    return "Hello, " + name;
}

// Call
var msg = greet("Alice");

// Default parameters
fun greet(name, greeting = "Hello") {
    return greeting + ", " + name;
}

// Anonymous
var add = fun(a, b) { return a + b; };

// Arrow function
var add = (a, b) => a + b;
```

## Classes

```neutron
class Person {
    var name;
    var age;

    init(n, a) {
        this.name = n;
        this.age = a;
    }

    fun greet() {
        say("Hi, I'm " + this.name);
    }
}

// Usage
var p = Person();
p.init("Alice", 25);
p.greet();
```

## Modules

```neutron
// Import
use sys;
use json;
use http;

// Use
var content = sys.read("file.txt");
var data = json.parse(content);
var resp = http.get("https://api.com");
```

## Arrays

```neutron
var arr = [1, 2, 3];

arr[0]        // Access: 1
arr[-1]       // Last: 3
len(arr)      // Length: 3
arr.push(4)   // Add element
arr.pop()     // Remove last
arr.slice(1, 3)  // [2, 3]
```

## Objects

```neutron
var obj = {
    "name": "Alice",
    "age": 25
};

obj["name"]     // Access: "Alice"
obj["age"] = 26 // Update
```

## Strings

```neutron
var s = "Hello, World!";

len(s)              // Length
s.upper()           // "HELLO, WORLD!"
s.lower()           // "hello, world!"
s.contains("World") // true
s.split(", ")       // ["Hello", "World!"]
s.slice(0, 5)       // "Hello"
```

## String Interpolation

```neutron
var name = "Alice";
var age = 25;

say("Name: ${name}, Age: ${age}");
say("Next year: ${age + 1}");
```

## Input/Output

```neutron
// Output
say("Hello");
say("Value: " + x);

// Input
var name = input("Your name: ");
var num = int(input("Enter number: "));
```

## Error Handling

```neutron
try {
    var content = sys.read("file.txt");
} catch (error) {
    say("Error: " + error);
}
```

## Comments

```neutron
// Single-line comment

var x = 10;  // Inline comment
```

## Built-in Functions

```neutron
say(value)           // Print
input(prompt)        // Read input
len(value)           // Length
type(value)          // Get type
int(value)           // To integer
float(value)         // To float
str(value)           // To string
bool(value)          // To boolean
abs(number)          // Absolute value
sqrt(number)         // Square root
max(a, b)            // Maximum
min(a, b)            // Minimum
pow(base, exp)       // Power
range(n)             // Range 0 to n-1
```

## File Operations

```neutron
use sys;

sys.read("file.txt")           // Read file
sys.write("file.txt", "data")  // Write file
sys.append("file.txt", "data") // Append
sys.exists("file.txt")         // Check exists
sys.rm("file.txt")             // Delete
sys.cp("a.txt", "b.txt")       // Copy
sys.mv("a.txt", "b.txt")       // Move
sys.mkdir("dir")               // Create directory
sys.cwd()                      // Current directory
```

## HTTP Requests

```neutron
use http;

var resp = http.get("https://api.com");
var resp = http.post("https://api.com", data);
var resp = http.put("https://api.com", data);
var resp = http.delete("https://api.com");

resp.status   // Status code
resp.body     // Response body
resp.headers  // Response headers
```

## JSON

```neutron
use json;

// Stringify
var json = json.stringify({"key": "value"});

// Parse
var obj = json.parse('{"key": "value"}');
```

## Time

```neutron
use time;

var now = time.now();           // Current timestamp
var formatted = time.format(now); // Format timestamp
time.sleep(1000);               // Sleep 1 second
```

## Math

```neutron
use math;

math.add(a, b)       // Add
math.subtract(a, b)  // Subtract
math.multiply(a, b)  // Multiply
math.divide(a, b)    // Divide
math.pow(a, b)       // Power
math.sqrt(a)         // Square root
math.abs(a)          // Absolute
```

---

**Full reference:** [Language Reference](reference/language_reference.md)

## Enum

```neutron
// Auto-incrementing (starts at 0)
enum Direction { NORTH, SOUTH, EAST, WEST }
say(Direction.NORTH);  // 0
say(Direction.WEST);   // 3

// Explicit values
enum HttpStatus { OK = 200, NOT_FOUND = 404, ERROR = 500 }
say(HttpStatus.OK);    // 200

// Mixed
enum Priority { LOW = 1, MEDIUM, HIGH }  // MEDIUM=2, HIGH=3
```

## Destructuring

```neutron
// Array destructuring
var [a, b, c] = [1, 2, 3];
say(a);  // 1

// Object destructuring
var {name, age} = {"name": "Alice", "age": 30};
say(name);  // "Alice"

// Object destructuring with rename
var {name: firstName, age: years} = person;
```

## Spread Operator

```neutron
fun add(a, b, c) { return a + b + c; }

var nums = [1, 2, 3];
var result = add(...nums);  // 6

// Mix with regular args
var result2 = add(1, ...rest);
```

## Optional Chaining

```neutron
var user = {"name": "Bob"};
var name = user?.name;   // "Bob"

var missing = nil;
var safe = missing?.name;  // nil (no crash)
```

## Block Comments

```neutron
#{ This is a block comment }#

#{
    Multi-line block comment.
    var ignored = 999;
}#

var x = 1; #{ inline }# var y = 2;
```

---

**Full reference:** [Language Reference](language_reference.md)
