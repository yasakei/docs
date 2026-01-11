# Neutron Language Reference

> [!NOTE]
> This is the complete language reference for Neutron. For a quick introduction, see the [Quick Start Guide](../guides/quickstart.md).

## Table of Contents
- [Lexical Structure](#lexical-structure)
- [Data Types](#data-types)
- [Variables and Declarations](#variables-and-declarations)
- [Operators](#operators)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Classes and Objects](#classes-and-objects)
- [Modules](#modules)
- [Arrays](#arrays)
- [Buffers](#buffers)
- [Built-in Functions](#built-in-functions)

---

## Lexical Structure

### Comments

Single-line comments begin with `//` and continue to the end of the line.

```js
// This is a single-line comment
var x = 10; // Inline comment
```

> [!NOTE]
> Multi-line comments are not currently supported.

---

## Data Types

Neutron is dynamically typed. Variables can hold values of any type, and types are determined at runtime.

### Primitive Types

| Type | Description | Example |
|------|-------------|---------|
| **Number** | 64-bit floating-point | `42`, `3.14`, `-17` |
| **Boolean** | Logical values | `true`, `false` |
| **String** | Character sequences | `"Hello"`, `"World"` |
| **Nil** | Absence of value | `nil` |

### Complex Types

| Type | Description |
|------|-------------|
| **Array** | Ordered collections | `[1, 2, 3]` |
| **Object** | Key-value pairs | `{"key": "value"}` |
| **Function** | Callable functions |
| **Module** | Imported modules |
| **Buffer** | Raw byte array | `sys.alloc(10)` |

### Numbers

All numeric values are 64-bit floating-point numbers (IEEE 754 double-precision).

```js
var integer = 42;
var decimal = 3.14159;
var negative = -17;
var scientific = 1.5e10;  // Scientific notation
```

### Booleans

Boolean values represent logical truth.

```js
var active = true;
var disabled = false;
```

### Strings

Strings are sequences of UTF-8 characters enclosed in double quotes.

```js
var greeting = "Hello, World!";
var escaped = "Line 1\nLine 2\tTabbed";
```

#### String Escape Sequences

Neutron supports comprehensive escape sequences for special characters and Unicode:

##### Basic Escape Sequences

| Escape | Description | Example |
|--------|-------------|---------|
| `\"` | Double quote | `"He said \"Hello\""` |
| `\\` | Backslash | `"Path: C:\\Users"` |
| `\n` | Newline | `"Line 1\nLine 2"` |
| `\r` | Carriage return | `"Text\rOverwrite"` |
| `\t` | Tab character | `"Name:\tValue"` |
| `\b` | Backspace | `"Hello\bWorld"` |
| `\f` | Form feed | `"Page 1\fPage 2"` |
| `\v` | Vertical tab | `"Line 1\vLine 2"` |
| `\0` | Null character | `"Text\0End"` |

##### Numeric Escape Sequences

| Escape | Description | Example |
|--------|-------------|---------|
| `\xHH` | Hexadecimal byte (00-FF) | `"\x41"` → `"A"` |
| `\ooo` | Octal byte (000-377) | `"\101"` → `"A"` |

##### Unicode Escape Sequences

| Escape | Description | Example |
|--------|-------------|---------|
| `\uXXXX` | Unicode character (4 hex digits) | `"\u0041"` → `"A"` |
| `\UXXXXXXXX` | Unicode character (8 hex digits) | `"\U00000041"` → `"A"` |

```js
// Basic escapes
var message = "She said, \"Hello, World!\"";
var path = "C:\\Program Files\\Neutron";
var multiline = "Line 1\nLine 2\nLine 3";

// Hexadecimal escapes
var copyright = "\xA9 2024 Neutron";  // © 2024 Neutron
var euro = "\u20AC";                  // €
var smiley = "\U0001F600";            // 😀

// Mixed usage
var greeting = "Hello \u4E16\u754C!"; // Hello 世界!
```

#### Raw String Literals

Raw strings disable escape sequence processing, useful for regular expressions and file paths:

```js
// Raw string prefix 'r'
var regex = r"\d+\.\d+";              // Literal backslashes
var windowsPath = r"C:\Users\Name";   // No need to escape backslashes
var template = r"Hello\nWorld";       // Literal \n, not newline

// Compare with regular strings
var regular = "\\d+\\.\\d+";          // Need to escape backslashes
var rawString = r"\d+\.\d+";          // Much cleaner
```

#### String Indexing and Slicing

Neutron supports Python-style string indexing with negative indices and advanced slicing:

##### Negative Indexing

```js
var text = "hello";
say(text[0]);    // "h" (first character)
say(text[-1]);   // "o" (last character)
say(text[-2]);   // "l" (second to last)
```

##### String Slicing

```js
var text = "hello world";

// Basic slicing [start:end]
say(text.slice(0, 5));     // "hello"
say(text.slice(6));        // "world" (from index 6 to end)
say(text.slice(0, -6));    // "hello" (from start to 6 from end)

// Step slicing [start:end:step]
say(text.slice(0, -1, 2)); // "hlowrl" (every 2nd character)
say(text.slice(-1, -1, -1)); // "dlrow olleh" (reverse string)
```

#### String Multiplication

Strings can be repeated using the multiplication operator:

```js
var repeated = "ha" * 3;        // "hahaha"
var separator = "-" * 10;       // "----------"
var padding = " " * 5;          // "     "

// Also works with int * string
var banner = 3 * "!";           // "!!!"
```

#### String Interpolation

Embed expressions within strings using `${expression}` syntax:

```js
var name = "Alice";
var age = 30;
say("Name: ${name}, Age: ${age}");
// Output: Name: Alice, Age: 30

var x = 5;
var y = 10;
say("Sum: ${x + y}");
// Output: Sum: 15
```

> [!TIP]
> String interpolation works with any expression, including function calls and array access.

#### String Formatting

Neutron provides advanced string formatting capabilities through the `format()` method:

##### Positional Arguments

```js
var template = "Hello {0}, you are {1} years old!";
var result = template.format("Alice", 30);
say(result); // "Hello Alice, you are 30 years old!"

// Multiple uses of same argument
var repeated = "{0} + {0} = {1}";
say(repeated.format(5, 10)); // "5 + 5 = 10"
```

##### Format Specifications

```js
// Number formatting
var price = "Price: ${0:2f}";
say(price.format(19.99)); // "Price: 19.99"

// Padding and alignment
var aligned = "{0:>10}";     // Right-align in 10 characters
var padded = "{0:0>5}";      // Pad with zeros to 5 characters
```

##### Complex Formatting Examples

```js
// Financial formatting
var invoice = "Item: {0}, Quantity: {1}, Price: ${2:.2f}";
say(invoice.format("Widget", 5, 29.99));
// Output: "Item: Widget, Quantity: 5, Price: $29.99"

// Table formatting
var header = "{0:<10} {1:>8} {2:>10}";
say(header.format("Name", "Age", "Salary"));
// Output: "Name            Age     Salary"
```

#### String Properties and Methods

Neutron provides comprehensive string functionality through both properties (no parentheses needed) and methods (parentheses required):

##### String Properties

| Property | Description | Example |
|----------|-------------|---------|
| `length` | Returns number of characters | `"abc".length` → `3` |
| `chars` | Returns array of individual characters | `"abc".chars` → `["a", "b", "c"]` |

##### Basic String Methods

| Method | Description | Example |
|--------|-------------|---------|
| `contains(substr)` | Checks if string contains substring | `"hello".contains("ll")` → `true` |
| `split(delimiter)` | Splits string into array | `"a,b".split(",")` → `["a", "b"]` |
| `substring(start, [end])` | Returns a substring | `"hello".substring(1, 4)` → `"ell"` |
| `strip([chars])` | Removes whitespace or specified characters from both ends | `" hello ".strip()` → `"hello"` |
| `lstrip([chars])` | Removes whitespace or specified characters from left end | `" hello".lstrip()` → `"hello"` |
| `rstrip([chars])` | Removes whitespace or specified characters from right end | `"hello ".rstrip()` → `"hello"` |
| `replace(old, new, [count])` | Replaces occurrences of substring | `"hello".replace("l", "x")` → `"hexxo"` |

##### String Search Methods

| Method | Description | Example |
|--------|-------------|---------|
| `find(substr, [start], [end])` | Returns index of first occurrence, -1 if not found | `"hello".find("ll")` → `2` |
| `rfind(substr, [start], [end])` | Returns index of last occurrence, -1 if not found | `"hello".rfind("l")` → `3` |
| `index(substr, [start], [end])` | Like find() but throws error if not found | `"hello".index("ll")` → `2` |
| `rindex(substr, [start], [end])` | Like rfind() but throws error if not found | `"hello".rindex("l")` → `3` |

##### Case Conversion Methods

Neutron provides Unicode-aware case conversion that properly handles international characters:

| Method | Description | Example |
|--------|-------------|---------|
| `upper()` | Converts to uppercase (Unicode-aware) | `"hello".upper()` → `"HELLO"`, `"café".upper()` → `"CAFÉ"` |
| `lower()` | Converts to lowercase (Unicode-aware) | `"HELLO".lower()` → `"hello"`, `"CAFÉ".lower()` → `"café"` |
| `capitalize()` | Capitalizes first character | `"hello".capitalize()` → `"Hello"` |
| `title()` | Converts to title case | `"hello world".title()` → `"Hello World"` |
| `swapcase()` | Swaps case of all characters | `"Hello".swapcase()` → `"hELLO"` |
| `casefold()` | Aggressive lowercase for comparisons | `"HELLO".casefold()` → `"hello"` |

```js
// Unicode case conversion examples
say("café".upper());     // "CAFÉ"
say("RÉSUMÉ".lower());   // "résumé"
say("naïve".upper());    // "NAÏVE"
say("Zürich".lower());   // "zürich"

// Works with mixed Unicode and ASCII
var text = "Hello Café!";
say(text.upper());       // "HELLO CAFÉ!"
```

##### Character Classification Methods

| Method | Description | Example |
|--------|-------------|---------|
| `isalnum()` | True if all characters are alphanumeric | `"abc123".isalnum()` → `true` |
| `isalpha()` | True if all characters are alphabetic | `"abc".isalpha()` → `true` |
| `isdigit()` | True if all characters are digits | `"123".isdigit()` → `true` |
| `islower()` | True if all characters are lowercase | `"hello".islower()` → `true` |
| `isupper()` | True if all characters are uppercase | `"HELLO".isupper()` → `true` |
| `isspace()` | True if all characters are whitespace | `"   ".isspace()` → `true` |
| `istitle()` | True if string is in title case | `"Hello World".istitle()` → `true` |

##### Sequence Operations

| Method | Description | Example |
|--------|-------------|---------|
| `slice(start, [end], [step])` | Advanced slicing with step support | `"hello".slice(1, 4, 1)` → `"ell"` |

##### Unicode Methods

| Method | Description | Example |
|--------|-------------|---------|
| `normalize(form)` | Unicode normalization (NFC, NFD, NFKC, NFKD) | `text.normalize("NFC")` |
| `encode(encoding)` | Encode string to bytes | `"hello".encode("utf-8")` |
| `isunicode()` | True if string contains Unicode characters | `"café".isunicode()` → `true` |

##### Formatting Methods

| Method | Description | Example |
|--------|-------------|---------|
| `format(args...)` | Format string with arguments | `"Hello {0}".format("World")` → `"Hello World"` |

```js
var text = "Hello, World!";

// Properties (no parentheses)
say(text.length);            // 13
say(text.chars);             // ["H", "e", "l", "l", "o", ",", " ", "W", "o", "r", "l", "d", "!"]

// Methods (parentheses required)
say(text.contains("World")); // true
say(text.upper());           // "HELLO, WORLD!"
say(text.find("World"));     // 7
say(text.replace("World", "Neutron")); // "Hello, Neutron!"

// Advanced string operations
var data = "  hello world  ";
say(data.strip());           // "hello world"
say(data.title());           // "  Hello World  "

// Character classification
say("abc123".isalnum());     // true
say("ABC".isupper());        // true
say("   ".isspace());        // true

// String slicing with negative indices
say("hello"[-1]);            // "o"
say("hello".slice(1, -1));   // "ell"
```

### Unicode Support

Neutron provides comprehensive Unicode support for international text processing:

#### Unicode Normalization

Unicode text can be normalized to different forms for consistent processing:

```js
var text = "café";  // May contain composed or decomposed characters

// Normalize to different forms
var nfc = text.normalize("NFC");   // Canonical composition
var nfd = text.normalize("NFD");   // Canonical decomposition
var nfkc = text.normalize("NFKC"); // Compatibility composition
var nfkd = text.normalize("NFKD"); // Compatibility decomposition

// Use for text comparison
fun compareText(a, b) {
    return a.normalize("NFC") == b.normalize("NFC");
}
```

#### String Encoding

Convert strings to different character encodings:

```js
var text = "Hello, 世界!";

// Encode to different formats
var utf8 = text.encode("utf-8");
var utf16 = text.encode("utf-16");
var ascii = text.encode("ascii");  // May throw error for non-ASCII

// Check if string contains Unicode characters
if (text.isunicode()) {
    say("String contains Unicode characters");
}
```

#### Unicode Case Conversion

Neutron provides proper Unicode-aware case conversion for international characters:

```js
// Latin characters with diacritics
say("café".upper());        // "CAFÉ"
say("résumé".upper());      // "RÉSUMÉ"
say("naïve".upper());       // "NAÏVE"
say("piñata".upper());      // "PIÑATA"

// Reverse conversion
say("CAFÉ".lower());        // "café"
say("ZÜRICH".lower());      // "zürich"

// Mixed text
var greeting = "Bonjour café!";
say(greeting.upper());      // "BONJOUR CAFÉ!"

// Supports Latin-1 Supplement (U+00C0-U+00FF)
// Including: À, Á, Â, Ã, Ä, Å, Æ, Ç, È, É, Ê, Ë, etc.
```

#### Unicode Character Properties

Use character classification methods with Unicode awareness:

```js
var unicodeText = "Café123";

say(unicodeText.isalnum());  // true (includes Unicode letters)
say(unicodeText.isalpha());  // false (contains digits)

// Works with various scripts
var chinese = "你好";
say(chinese.isalpha());      // true
say(chinese.isunicode());    // true
```

#### Working with Unicode Literals

```js
// Various ways to represent Unicode
var heart = "\u2764";           // ❤
var smiley = "\U0001F600";      // 😀
var chinese = "\u4F60\u597D";   // 你好

// Mixed Unicode and ASCII
var greeting = "Hello \u4E16\u754C! \U0001F44B"; // Hello 世界! 👋

// Unicode in string operations
var repeated = "\u2764" * 3;    // ❤❤❤
var found = greeting.find("\u4E16"); // Find position of 世
```

#### String Error Handling

String methods provide comprehensive error handling for edge cases:

```js
try {
    var text = "hello";
    var pos = text.index("xyz");  // Throws error if not found
} catch (error) {
    say("Substring not found: " + error);
}

// Safe alternatives that return -1 instead of throwing
var pos = text.find("xyz");      // Returns -1 if not found
if (pos != -1) {
    say("Found at position: " + pos);
}

// Encoding errors
try {
    var unicode = "café";
    var ascii = unicode.encode("ascii");  // May throw for non-ASCII
} catch (error) {
    say("Encoding error: " + error);
}
```

### Nil

The `nil` value represents the absence of a value (equivalent to `null` in other languages).

```js
var empty = nil;
```

### Objects

Objects are collections of key-value pairs, similar to dictionaries or maps in other languages.

```js
var person = {
  "name": "John Doe",
  "age": 30,
  "email": "john@example.com"
};

// Property access
say(person["name"]);  // John Doe
say(person["age"]);   // 30

// Nested objects
var config = {
  "database": {
    "host": "localhost",
    "port": 5432
  }
};
say(config["database"]["host"]);  // localhost
```

> [!NOTE]
> Objects integrate seamlessly with the `json` module for serialization and parsing.

---

## Variables and Declarations

### Variable Declaration

Variables are declared with the `var` keyword and can be initialized immediately or assigned later.

```js
var x;           // Declared (value is nil)
var y = 42;      // Declared and initialized
x = 100;         // Assignment
```

You can also declare multiple variables in a single statement:

```js
var a = 1, b = 2, c = 3;
var name = "Alice", age = 30;
```

### Dynamic Typing

Variables can hold values of any type and change types during runtime:

```js
var value = 42;       // Number
value = "hello";      // Now a string
value = true;         // Now a boolean
value = [1, 2, 3];    // Now an array
```

### Static Type Annotations

Neutron supports **optional static type annotations** that provide runtime type safety. When you declare a variable with a type annotation, Neutron enforces that type at runtime.

```js
var int x = 42;
var string name = "Alice";
var bool flag = true;
var array list = [1, 2, 3];
var object data = {"key": "value"};
var any flexible = "anything";

// Multiple variables with the same type
var int a = 1, b = 2, c = 3;
```

#### Available Type Keywords

- `int` - Integer numbers
- `float` - Floating-point numbers  
- `string` - Text strings
- `bool` - Boolean values
- `array` - Arrays
- `object` - Objects
- `any` - Any type (no restriction)

#### Runtime Type Checking

Type annotations are **enforced at runtime**. Attempting to assign a value of the wrong type will result in a runtime error:

```js
var int count = 42;
count = "hello";  // ❌ Runtime error: Type mismatch

var string name = "Alice";
name = 123;       // ❌ Runtime error: Type mismatch

var any value = 42;
value = "hello";  // ✅ OK - 'any' accepts all types
```

#### Benefits

- **Self-Documenting**: Type annotations make code intent clear
- **Runtime Safety**: Catch type errors during execution
- **Optional**: Mix typed and untyped variables as needed
- **Future-Proof**: Enables potential static analysis and IDE support

> [!TIP]
> Use type annotations for function parameters and important variables to make your code more maintainable and catch errors early.

---

## Operators

### Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition / String concatenation | `5 + 3` → `8` |
| `-` | Subtraction | `10 - 4` → `6` |
| `*` | Multiplication | `6 * 7` → `42` |
| `/` | Division | `15 / 3` → `5` |
| `%` | Modulo (remainder) | `10 % 3` → `1` |
| `++` | Increment | `x++` |
| `--` | Decrement | `x--` |

```js
var sum = 10 + 5;           // 15
var product = 4 * 3;        // 12
var remainder = 17 % 5;     // 2

// String concatenation
var message = "Hello, " + "World!";  // "Hello, World!"
```

#### Increment/Decrement

```js
var x = 5;
x++;    // x is now 6
++x;    // x is now 7
x--;    // x is now 6
--x;    // x is now 5
```

> [!NOTE]
> Currently, both prefix and postfix forms behave identically (they modify the variable and return the new value).

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal to | `5 == 5` → `true` |
| `!=` | Not equal to | `5 != 3` → `true` |
| `<` | Less than | `3 < 5` → `true` |
| `<=` | Less than or equal | `5 <= 5` → `true` |
| `>` | Greater than | `7 > 3` → `true` |
| `>=` | Greater than or equal | `5 >= 4` → `true` |

```js
say(10 == 10);  // true
say(5 < 10);    // true
say(7 >= 7);    // true
```

> [!WARNING]
> Chained comparisons like `a < b < c` are not currently supported. Use `a < b and b < c` instead.

### Bitwise Operators

Bitwise operators treat their operands as integers (converting from floating-point if necessary).

| Operator | Description | Example |
|----------|-------------|---------|
| `&` | Bitwise AND | `5 & 1` → `1` |
| `|` | Bitwise OR | `5 | 1` → `5` |
| `^` | Bitwise XOR | `5 ^ 1` → `4` |
| `~` | Bitwise NOT | `~5` → `-6` |
| `<<` | Left Shift | `5 << 1` → `10` |
| `>>` | Right Shift | `5 >> 1` → `2` |

```js
var a = 5;  // 0101
var b = 1;  // 0001

say(a & b); // 1  (0001)
say(a | b); // 5  (0101)
say(a ^ b); // 4  (0100)
say(~a);    // -6
say(a << 1); // 10 (1010)
say(a >> 1); // 2  (0010)
```

### Logical Operators

| Operator | Alternative | Description | Example |
|----------|-------------|-------------|---------|
| `and` | `&&` | Logical AND | `true and false` → `false` |
| `or` | `\|\|` | Logical OR | `true or false` → `true` |
| `!` | | Logical NOT | `!true` → `false` |

```js
var result = (x > 5) and (x < 10);
var valid = (status == "ready") or (status == "running");
var inactive = !active;
```

### Ternary Operator

The ternary operator `? :` is a shorthand for `if-else` statements.

```js
condition ? expressionIfTrue : expressionIfFalse
```

Example:
```js
var age = 20;
var status = age >= 18 ? "Adult" : "Minor";
say(status); // "Adult"
```

---

## Control Flow

### Conditional Statements

#### If-Else

```js
if (condition) {
    // Execute if condition is true
} else if (otherCondition) {
    // Execute if other condition is true
} else {
    // Execute if no conditions are true
}
```

**Example:**
```js
var score = 85;
if (score >= 90) {
    say("Grade: A");
} else if (score >= 80) {
    say("Grade: B");
} else if (score >= 70) {
    say("Grade: C");
} else {
    say("Grade: F");
}
```

### Loops

#### While Loop

Executes a block while a condition remains true.

```js
var i = 0;
while (i < 5) {
    say(i);
    i++;
}
```

#### Do-While Loop

Executes a block at least once, and then repeats while a condition remains true.

```js
var i = 0;
do {
    say(i);
    i++;
} while (i < 5);
```

#### For Loop

Provides initialization, condition, and increment in a compact syntax.

```js
for (var i = 0; i < 10; i++) {
    say(i);
}

// Iterate over array indices
var items = ["a", "b", "c"];
for (var i = 0; i < 3; i++) {
    say(items[i]);
}
```

### Match Statement

Pattern matching for cleaner conditional logic (similar to switch statements).

```js
var status = 2;
match (status) {
    case 1 => say("Initializing");
    case 2 => say("Running");
    case 3 => say("Completed");
    default => say("Unknown");
}
```

**With block statements:**
```js
match (command) {
    case "start" => {
        say("Starting system...");
        say("System online");
    }
    case "stop" => {
        say("Stopping system...");
        say("System offline");
    }
    default => say("Invalid command");
}
```

> [!TIP]
> The `default` case is optional. If omitted and no case matches, execution continues normally.

### Retry Statement

The `retry` statement allows you to automatically retry a block of code a specified number of times if an exception occurs.

```js
retry (3) {
    // Code that might fail
    if (somethingWrong) {
        throw "Error";
    }
} catch (e) {
    // Executed if all retries fail
    say("Failed after 3 attempts: " + e);
}
```

**How it works:**
1. The code block is executed.
2. If an exception is thrown, the block is re-executed.
3. This repeats up to the specified count (e.g., `3` times).
4. If the block succeeds (completes without throwing), execution continues after the retry structure.
5. If the block fails all attempts, the optional `catch` block is executed.

**Example:**
```js
var attempts = 0;
retry (3) {
    attempts++;
    say("Connecting... Attempt " + attempts);
    if (attempts < 3) {
        throw "Connection failed";
    }
    say("Connected!");
}
```

---

## Functions

### Function Declaration

Functions are declared using the `fun` keyword.

```js
fun greet(name) {
    say("Hello, " + name + "!");
}

greet("World");  // Hello, World!
```

### Return Values

Use `return` to return a value from a function. Without an explicit return, functions return `nil`.

```js
fun add(a, b) {
    return a + b;
}

fun multiply(x, y) {
    return x * y;
}

say(add(5, 3));       // 8
say(multiply(4, 7));  // 28
```

### Typed Functions

Neutron supports **typed function parameters** and **return types** with runtime validation.

#### Function Parameter Types

```js
fun add(int a, int b) {
    return a + b;
}

fun greet(string name, int age) {
    return "Hello " + name + ", you are " + age + " years old!";
}

fun processData(array items, object config) {
    return "Processed " + items.length + " items";
}
```

#### Function Return Types

```js
fun add(int a, int b) -> int {
    return a + b;
}

fun getName() -> string {
    return "Alice";
}

fun isValid(any value) -> bool {
    return value != nil;
}
```

#### Runtime Parameter Validation

Function calls are validated at runtime:

```js
fun multiply(int x, int y) -> int {
    return x * y;
}

multiply(5, 10);        // ✅ Valid
multiply("hello", 5);   // ❌ Runtime error: parameter type mismatch
```

#### Mixed Typed and Untyped Functions

```js
// Typed function
fun add(int a, int b) -> int {
    return a + b;
}

// Untyped function (backward compatibility)
fun oldFunction(x, y) {
    return x + y;  // Works with any types
}
```

### Lambda Functions

Anonymous functions can be created inline and assigned to variables or passed as arguments.

```js
// Lambda assigned to variable
var square = fun(x) {
    return x * x;
};
say(square(5));  // 25

// Lambda as array element
var operations = [
    fun(x) { return x + 10; },
    fun(x) { return x * 2; }
];
say(operations[0](5));  // 15
say(operations[1](5));  // 10
```

#### Higher-Order Functions

Functions can accept other functions as parameters:

```js
fun applyTwice(f, value) {
    return f(f(value));
}

var double = fun(x) { return x * 2; };
say(applyTwice(double, 3));  // 12
```

#### Immediately Invoked Functions

```js
var result = fun(x) { return x + 1; }(5);
say(result);  // 6
```

---

## Safe Blocks

**Safe blocks** enforce type annotations on all variables, functions, and classes within their scope, providing stricter type safety for critical code sections.

### Basic Safe Block Syntax

```js
safe {
    // All variables must have type annotations
    var int x = 10;
    var string name = "Alice";
    
    // All functions must have parameter and return types
    fun add(int a, int b) -> int {
        return a + b;
    }
    
    // All class methods and properties must have type annotations
    class Calculator {
        var int value;
        
        fun add(int x) -> int {
            this.value = this.value + x;
            return this.value;
        }
    }
}
```

### Safe Block Enforcement

Inside a safe block, the following are **required**:

1. **Variable type annotations**:
```js
safe {
    var int x = 10;        // ✅ Valid
    var y = 20;            // ❌ Error: missing type annotation
}
```

2. **Function parameter types**:
```js
safe {
    fun add(int a, int b) -> int {  // ✅ Valid
        return a + b;
    }
    
    fun invalid(x, y) {             // ❌ Error: missing parameter types
        return x + y;
    }
}
```

3. **Function return types**:
```js
safe {
    fun add(int a, int b) -> int {  // ✅ Valid
        return a + b;
    }
    
    fun invalid(int a, int b) {     // ❌ Error: missing return type
        return a + b;
    }
}
```

4. **Class method and property types**:
```js
safe {
    class Person {
        var string name;           // ✅ Valid - typed property
        var age;                   // ❌ Error: missing type annotation
        
        fun getName() -> string {  // ✅ Valid - typed method
            return this.name;
        }
        
        fun setName(n) {           // ❌ Error: missing parameter type
            this.name = n;
        }
    }
}
```

### Error Handling with Safe Blocks

Safe block violations throw runtime exceptions that can be caught:

```js
try {
    safe {
        var x = 10;  // Missing type annotation
    }
} catch (e) {
    say("Caught error: " + e);
    // Output: "Variable 'x' must have a type annotation inside a safe block."
}
```

### Mixed Safe and Regular Code

```js
// Regular code - no type requirements
var regularVar = "no type needed";

safe {
    // Strict typing required here
    var int safeVar = 100;
    
    fun multiply(int x, int y) -> int {
        return x * y;
    }
}

// Back to regular code
var anotherRegular = 3.14;
```

---

## Neutron Safe Code Files (.ntsc)

Neutron supports **safe code files** with the `.ntsc` extension. These files enforce type annotations throughout the entire file, similar to having the whole file wrapped in a `safe {}` block.

### File Extension

- `.nt` - Standard Neutron files (dynamic typing, optional type annotations)
- `.ntsc` - Neutron Safe Code files (mandatory type annotations)

### Usage

```bash
# Run a standard Neutron file
./neutron myprogram.nt

# Run a Neutron Safe Code file (type safety enforced)
./neutron myprogram.ntsc
```

### Requirements in .ntsc Files

All variables, functions, and classes must have complete type annotations:

```js
// myprogram.ntsc

// Variables must have types
var int count = 0;
var string name = "Alice";

// Functions must have parameter and return types
fun add(int a, int b) -> int {
    return a + b;
}

// Classes must have typed properties and methods
class Person {
    var string name;
    var int age;
    
    fun init(string n, int a) -> int {
        this.name = n;
        this.age = a;
        return a;
    }
    
    fun getName() -> string {
        return this.name;
    }
}

var any person = Person();
person.init("Bob", 30);
say(person.getName());
```

### Error Messages

Errors in `.ntsc` files have specific messages:

```
// Missing variable type
Variable 'x' must have a type annotation in .ntsc files.

// Missing function parameter type
Class method parameter 'x' must have a type annotation in .ntsc files.

// Missing function return type
Class method 'getName' must have a return type annotation in .ntsc files.
```

### When to Use .ntsc Files

- **Critical code**: Financial calculations, security-sensitive operations
- **Team projects**: Enforce consistent typing across the codebase
- **Library code**: Ensure clear API contracts
- **Gradual migration**: Convert files one at a time to strict typing

---

## Buffers

Buffers are raw byte arrays used for handling binary data. See [Buffers Reference](buffers.md) for more details.

```js
use sys;
var buf = sys.alloc(10);
buf[0] = 255;
```

## Built-in Functions

### Output

**`say(value)`** - Prints a value to console with newline

```js
say("Hello, World!");
say(42);
say(true);
say([1, 2, 3]);
```

> [!NOTE]
> All other functions are provided through modules. Use `use modulename;` to import them.

---

## Modules

Neutron supports two import mechanisms:

| Statement | Purpose | Example |
|-----------|---------|---------|
| `use` | Import built-in/native modules | `use sys;` |
| `using` | Import Neutron source files | `using 'utils.nt';` |

### Importing Modules

Import built-in modules with `use`:

```js
use sys;
use json;
use math;

sys.write("data.txt", "Hello!");
var data = json.parse('{"name": "John"}');
say(math.sqrt(16));
```

**Available Built-in Modules:**
- `sys` - File I/O, environment, process control
- `json` - JSON parsing and serialization
- `math` - Mathematical operations
- `http` - HTTP client
- `fmt` - Type conversion and formatting
- `arrays` - Array manipulation
- `time` - Time and date operations
- `async` - Asynchronous operations

> [!NOTE]
> Modules use lazy loading - they're only initialized when imported, providing faster startup and better memory usage.

### Importing Files

Import Neutron source files with `using`:

```js
using 'utils.nt';
using 'lib/helpers.nt';
```

**File Search Order:**
1. Current directory
2. `lib/` directory
3. `.box/modules/` directory

**Example:**

`utils.nt`:
```js
fun add(a, b) {
    return a + b;
}
```

`main.nt`:
```js
using 'utils.nt';
say(add(5, 3));  // 8
```

### Selective Imports

Import specific symbols from modules or files using the `from` keyword:

```js
// Import specific functions from a module
use (now, sleep) = from time;
now();     // Available
sleep(100); // Available
// format() is NOT available

// Import specific functions from a file
using (add, multiply) = from "math_utils.nt";
add(2, 3);      // Available
multiply(4, 5); // Available
// subtract() is NOT available (if defined in the file)
```

**Benefits:**
- **Namespace clarity**: Only import what you need
- **Avoid conflicts**: Prevent name collisions
- **Better performance**: Smaller global scope

**Syntax:**
```js
use (symbol1, symbol2, ...) = from module_name;
using (symbol1, symbol2, ...) = from "file_path.nt";
```

**Example:**

`lib.nt`:
```js
fun helper1() { return "Helper 1"; }
fun helper2() { return "Helper 2"; }
fun internal() { return "Internal"; }
```

`main.nt`:
```js
// Only import helper1 and helper2
using (helper1, helper2) = from "lib.nt";

say(helper1());  // Works
say(helper2());  // Works
say(internal()); // Error: undefined variable
```

---

## Standard Library Modules

### Math Module

Mathematical operations and functions.

```js
use math;

say(math.sqrt(16));           // 4
say(math.pow(2, 3));          // 8
say(math.abs(-5));            // 5
```

**Functions:** `add`, `subtract`, `multiply`, `divide`, `pow`, `sqrt`, `abs`

> [!TIP]
> See [Math Module Documentation](../modules/math_module.md) for complete API reference.

### Sys Module

File I/O, environment access, and process control.

```js
use sys;

// File operations
sys.write("data.txt", "Hello!");
var content = sys.read("data.txt");

// Directory operations
sys.mkdir("mydir");
sys.exists("mydir");

// Environment
var home = sys.env("HOME");
var args = sys.args();
```

**Command Line Arguments:**
**`sys.args()`** - Returns an array of command line arguments passed to the script

```js
use sys;

var arguments = sys.args();
say("Number of arguments: " + arguments.length);
for (var i = 0; i < arguments.length; i = i + 1) {
    say("Argument " + i + ": " + arguments[i]);
}
```

**Functions:** File system, environment variables, process control, command execution, command line arguments

> [!TIP]
> See [Sys Module Documentation](../modules/sys_module.md) for complete API reference.

### JSON Module

JSON parsing and serialization.

```js
use json;

var data = {"name": "Alice", "age": 30};
var jsonStr = json.stringify(data);
var parsed = json.parse(jsonStr);
say(parsed["name"]);
```

**Functions:** `stringify`, `parse`, `get`

> [!TIP]
> See [JSON Module Documentation](../modules/json_module.md) for complete API reference.

### Fmt Module

Type conversion and formatting utilities.

```js
use fmt;

var str = fmt.to_str(42);        // "42"
var num = fmt.to_int("123");     // 123
var type = fmt.type([1, 2, 3]);  // "array"
```

**Functions:** `to_str`, `to_int`, `to_float`, `to_bin`, `type`

> [!TIP]
> See [Fmt Module Documentation](../modules/fmt_module.md) for complete API reference.

### Arrays Module

Comprehensive array manipulation.

```js
use arrays;

var arr = arrays.new();
arrays.push(arr, 10);
arrays.push(arr, 20);
say(arrays.length(arr));  // 2
arrays.sort(arr);
```

**Functions:** `new`, `push`, `pop`, `length`, `at`, `set`, `sort`, `reverse`, `slice`, `join`, `contains`, and more

> [!TIP]
> See [Arrays Module Documentation](../modules/arrays_module.md) for complete API reference.

### HTTP Module

HTTP client for making web requests.

```js
use http;

var response = http.get("https://api.example.com/data");
say(response["status"]);
say(response["body"]);

var data = {"key": "value"};
http.post("https://api.example.com/submit", json.stringify(data));
```

**Methods:** `get`, `post`, `put`, `delete`, `patch`, `head`

> [!TIP]
> See [HTTP Module Documentation](../modules/http_module.md) for complete API reference.

### Time Module

Time and date operations.

```js
use time;

var now = time.now();
var formatted = time.format(now);
time.sleep(1000);  // Sleep 1 second
```

**Functions:** `now`, `format`, `sleep`

> [!TIP]
> See [Time Module Documentation](../modules/time_module.md) for complete API reference.

---

## Classes and Objects

### Class Declaration

Define classes with properties and methods using the `class` keyword.

```js
class Person {
    var name;
    var age;
    
    // Constructor
    init(name, age) {
        this.name = name;
        this.age = age;
    }
    
    fun greet() {
        say("Hello, I'm " + this.name);
    }
}
```

> [!NOTE]
> The constructor method is named `init`. It can be declared with or without the `fun` keyword (e.g., `init(...)` or `fun init(...)`).

### Creating Instances

```js
var person = Person();
person.init("Alice", 30);
person.greet();  // Hello, I'm Alice
```

### The `this` Keyword

Use `this` to access instance properties and methods.

```js
class Counter {
    var count;
    
    fun init() {
        this.count = 0;
    }
    
    fun increment() {
        this.count++;
        return this.count;
    }
}

var counter = Counter();
counter.init();
say(counter.increment());  // 1
```

### Complete Example

```js
class Rectangle {
    var width;
    var height;
    
    fun init(w, h) {
        this.width = w;
        this.height = h;
    }
    
    fun area() {
        return this.width * this.height;
    }
    
    fun perimeter() {
        return 2 * (this.width + this.height);
    }
}

var rect = Rectangle();
rect.init(5, 3);
say(rect.area());       // 15
say(rect.perimeter());  // 16
```

---



## Exception Handling

Handle errors gracefully with `try`, `catch`, `finally`, and `throw` statements.

### Basic Try-Catch

```js
try {
    var result = riskyOperation();
    say("Success: " + result);
} catch (error) {
    say("Error: " + error);
}
```

### Try-Catch-Finally

```js
try {
    processData();
} catch (error) {
    say("Error: " + error);
} finally {
    cleanup();  // Always runs
}
```

### Throwing Exceptions

```js
fun validateAge(age) {
    if (age < 0) {
        throw "Age cannot be negative";
    }
    return true;
}

try {
    validateAge(-5);
} catch (error) {
    say("Validation error: " + error);
}
```

> [!NOTE]
> You can throw any value type: strings, numbers, booleans, arrays, or objects.

---



## Arrays

Arrays are ordered collections with literal syntax and comprehensive manipulation functions.

### Array Literals

```js
var numbers = [1, 2, 3, 4, 5];
var mixed = [1, "two", true, nil];
var nested = [[1, 2], [3, 4]];
```

### Array Access

```js
var items = ["apple", "banana", "cherry"];
say(items[0]);     // "apple"
items[1] = "orange";
say(items);        // ["apple", "orange", "cherry"]
```

### Array Properties and Methods

Arrays provide both properties (no parentheses needed) and methods (parentheses required):

#### Array Properties

| Property | Description | Example |
|----------|-------------|---------|
| `length` | Returns number of elements | `[1, 2, 3].length` → `3` |

#### Array Methods

Arrays provide built-in methods for manipulation:

| Method | Description | Example |
|--------|-------------|---------|
| `push(element)` | Adds element to end | `arr.push(4)` |
| `pop()` | Removes and returns last element | `arr.pop()` → last element |
| `slice(start, [end])` | Returns portion of array | `arr.slice(1, 3)` |
| `map(function)` | Transforms each element | `arr.map(fn)` |
| `filter(function)` | Filters elements | `arr.filter(fn)` |
| `find(function)` | Finds first matching element | `arr.find(fn)` |
| `indexOf(element)` | Returns index of element | `arr.indexOf(2)` |
| `join(separator)` | Joins elements into string | `arr.join(",")` |
| `reverse()` | Reverses array in place | `arr.reverse()` |
| `sort()` | Sorts array in place | `arr.sort()` |

```js
var list = [10, 20, 30];

// Property (no parentheses)
say(list.length);  // 3

// Methods (parentheses required)
list.push(40);
say(list.length);  // 4

var last = list.pop();
say(last);         // 40
say(list.length);  // 3
```

> [!TIP]
> For more advanced array operations (push, pop, sort, etc.), use the `arrays` module.

### Array Manipulation

```js
use arrays;

var arr = [1, 2, 3];
arrays.push(arr, 4);
say(arrays.length(arr));  // 4
arrays.reverse(arr);
say(arr);                 // [4, 3, 2, 1]
```

> [!TIP]
> See [Arrays Module Documentation](../modules/arrays_module.md) for all available functions.

---

## Language Semantics

### Truthiness

| Value | Truthy/Falsy |
|-------|-------------|
| `nil` | Falsy |
| `false` | Falsy |
| `0` | Truthy |
| `""` (empty string) | Truthy |
| Everything else | Truthy |

### Error Reporting

Neutron provides detailed error messages with source context:

```js
var result = 10 / 0;  // Runtime error: Division by zero
say(undefined);       // Runtime error: Undefined variable 'undefined'
```

---

## Complete Example Programs

Here are some complete example programs demonstrating various Neutron features:

### File Processing with System Operations

```js
use sys;
use json;

// Create a simple data processing program
say("=== File Processing Demo ===");

// Create sample data with Unicode content
var data = {
  "users": [
    {"name": "Alice", "age": 30, "active": true},
    {"name": "José", "age": 25, "active": false},  // Unicode name
    {"name": "李明", "age": 28, "active": true}     // Chinese name
  ],
  "timestamp": "2024-01-11"
};

// Write data to file
var jsonString = json.stringify(data, true);
sys.write("users.json", jsonString);
say("Data written to users.json");

// Read and process the file
if (sys.exists("users.json")) {
    var content = sys.read("users.json");
    var parsed = json.parse(content);
    
    var users = parsed["users"];
    say("Found " + users.length + " users");
    
    // Process each user with string methods
    say("Processing users:");
    for (var i = 0; i < users.length; i++) {
        var user = users[i];
        var name = user["name"];
        var status = user["active"] ? "ACTIVE" : "inactive";
        
        // Use string methods for formatting
        var displayName = name.title();
        var paddedStatus = status.lower().capitalize();
        var info = "User: {0} - Status: {1}".format(displayName, paddedStatus);
        
        say(info);
        
        // Check for Unicode characters
        if (name.isunicode()) {
            say("  → Contains Unicode characters");
        }
    }
}

// Cleanup
sys.rm("users.json");
say("Cleanup completed");
```

### String Processing Example

```js
// Comprehensive string processing demonstration
say("=== String Processing Demo ===");

// Text processing with various string methods
var rawText = "  Hello, WORLD! Welcome to Neutron Programming.  ";
say("Original: '" + rawText + "'");

// Basic cleaning and formatting
var cleaned = rawText.strip();
var normalized = cleaned.lower().capitalize();
say("Cleaned: '" + normalized + "'");

// Word processing
var words = cleaned.split(" ");
say("Word count: " + words.length);

// Find and replace operations
var modified = cleaned.replace("world", "Universe");
var position = modified.find("Universe");
say("Modified: " + modified);
say("'Universe' found at position: " + position);

// Case transformations
say("Uppercase: " + cleaned.upper());
say("Title case: " + cleaned.title());
say("Swapped case: " + cleaned.swapcase());

// Character classification
var testStrings = ["Hello123", "UPPERCASE", "lowercase", "123456", "   "];
for (var i = 0; i < testStrings.length; i++) {
    var str = testStrings[i];
    var checks = [];
    
    if (str.isalnum()) checks.push("alphanumeric");
    if (str.isalpha()) checks.push("alphabetic");
    if (str.isdigit()) checks.push("numeric");
    if (str.isupper()) checks.push("uppercase");
    if (str.islower()) checks.push("lowercase");
    if (str.isspace()) checks.push("whitespace");
    
    var result = checks.length > 0 ? checks.join(", ") : "none";
    say("'" + str + "' is: " + result);
}

// Unicode processing
var unicodeText = "Café, 世界, Москва";
say("Unicode text: " + unicodeText);
say("Contains Unicode: " + unicodeText.isunicode());
say("Normalized (NFC): " + unicodeText.normalize("NFC"));

// Unicode case conversion
var frenchText = "café résumé naïve";
say("French text: " + frenchText);
say("Uppercase: " + frenchText.upper());
say("Title case: " + frenchText.title());

var germanText = "Zürich Müller";
say("German text: " + germanText);
say("Lowercase: " + germanText.lower());
say("Uppercase: " + germanText.upper());

// String slicing and indexing
var sample = "programming";
say("String: " + sample);
say("First char: " + sample[0]);
say("Last char: " + sample[-1]);
say("Slice [2:7]: " + sample.slice(2, 7));
say("Every 2nd char: " + sample.slice(0, -1, 2));
say("Reversed: " + sample.slice(-1, -1, -1));

// String multiplication and formatting
var separator = "=" * 40;
say(separator);
var template = "Language: {0}, Version: {1}, Year: {2}";
var info = template.format("Neutron", "1.2+", 2024);
say(info);
say(separator);
```

### Object-Oriented Calculator

```python
use math;

class Calculator {
    var history;
    
    fun initialize() {
        this.history = [];
    }
    
    fun add(a, b) {
        var result = math.add(a, b);
        this.recordOperation("add", a, b, result);
        return result;
    }
    
    fun multiply(a, b) {
        var result = math.multiply(a, b);
        this.recordOperation("multiply", a, b, result);
        return result;
    }
    
    fun power(base, exp) {
        var result = math.pow(base, exp);
        this.recordOperation("power", base, exp, result);
        return result;
    }
    
    fun recordOperation(op, a, b, result) {
        var record = op + "(" + a + ", " + b + ") = " + result;
        say("Calculated: " + record);
    }
}

// Usage
var calc = Calculator();
calc.initialize();

say("=== Calculator Demo ===");
var sum = calc.add(10, 5);        // 15
var product = calc.multiply(4, 7); // 28
var power = calc.power(2, 8);      // 256

say("Final results:");
say("Sum: " + sum);
say("Product: " + product);  
say("Power: " + power);
```

### Web API Client

```python
use http;
use json;
use sys;

class ApiClient {
    var baseUrl;
    
    fun initialize(url) {
        this.baseUrl = url;
    }
    
    fun get(endpoint) {
        var fullUrl = this.baseUrl + endpoint;
        say("Fetching: " + fullUrl);
        
        var response = http.get(fullUrl);
        say("Status: " + response["status"]);
        
        if (response["status"] == 200) {
            return json.parse(response["body"]);
        } else {
            say("Error: " + response["body"]);
            return nil;
        }
    }
    
    fun post(endpoint, data) {
        var fullUrl = this.baseUrl + endpoint;
        var jsonData = json.stringify(data);
        
        say("Posting to: " + fullUrl);
        var response = http.post(fullUrl, jsonData);
        
        return response;
    }
}

// Usage example (with mock responses since http module returns mock data)
var client = ApiClient();
client.initialize("https://api.example.com");

var userData = client.get("/users/1");
if (userData != nil) {
    say("User data retrieved successfully");
}

var newUser = {"name": "Charlie", "email": "charlie@example.com"};
var createResponse = client.post("/users", newUser);
say("Create response status: " + createResponse["status"]);
```

## Additional Resources

### Documentation
- [Module System Guide](module-system.md) - Detailed module loading and usage
- [Box Package Manager](../../nt-box/docs/BOX_GUIDE.md) - Managing native modules

### Module API References
- [Sys Module](../modules/sys_module.md) - File I/O and system operations
- [JSON Module](../modules/json_module.md) - JSON parsing and serialization
- [HTTP Module](../modules/http_module.md) - HTTP client functionality
- [Math Module](../modules/math_module.md) - Mathematical operations
- [Arrays Module](../modules/arrays_module.md) - Array manipulation
- [Time Module](../modules/time_module.md) - Time and date operations
- [Fmt Module](../modules/fmt_module.md) - Type conversion and formatting

### Getting Started
- [Quick Start Guide](../guides/quickstart.md) - Get up and running in 5 minutes
- [Build Guide](../guides/build.md) - Building Neutron from source
- [Test Suite](../guides/test-suite.md) - Running and writing tests

---

*Neutron Language Reference - Version 1.2+*