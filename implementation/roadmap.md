# Neutron Future Enhancements Roadmap

This document outlines potential improvements and features for future development of the Neutron programming language.

## ✅ Completed Features

### 1. Break and Continue Statements ✅ IMPLEMENTED
**Status:** Complete  
**Impact:** High  
**Effort:** Medium  
**Description:** Implement `break` and `continue` statements for loop control.

**Example:**
```neutron
for (var i = 0; i < 100; i = i + 1) {
    if (i == 50) {
        break;  // Exit loop
    }
    if (i % 2 == 0) {
        continue;  // Skip to next iteration
    }
    say(i);
}
```

**Implementation:**
- ✅ Added `BREAK` and `CONTINUE` tokens
- ✅ Added bytecode operations `OP_BREAK` and `OP_CONTINUE`
- ✅ Track loop depth in compiler with breakTargets and continueTargets
- ✅ Special handling for for-loops: continue jumps to increment before condition
- ✅ Handle break/continue with jump instructions and loop stack management

**Test File:** `test_all_roadmap_features.nt`

---

### 2. Command Line Arguments ✅ IMPLEMENTED
**Status:** Complete  
**Impact:** High  
**Effort:** Low  
**Description:** Pass command line arguments to scripts via `sys.args()`.

**Example:**
```neutron
use sys;

var args = sys.args();
say("Program name: " + args[0]);
say("First argument: " + args[1]);
```

**Implementation:**
- ✅ Modified `main.cpp` to pass argc/argv to VM via `vm.setCommandLineArgs()`
- ✅ Store arguments in VM as `std::vector<std::string> commandLineArgs`
- ✅ Updated `sys_args()` in sys module to return actual arguments as array
- ✅ Arguments include script name as first element

**Test File:** `test_all_roadmap_features.nt`

---

### 3. Modulo Operator (%) ✅ IMPLEMENTED
**Status:** Complete  
**Impact:** Medium  
**Effort:** Low  
**Description:** Add `%` operator as alias for modulo operation.

**Example:**
```neutron
say(10 % 3);   // Output: 1
say(17 % 5);   // Output: 2
say(100 % 7);  // Output: 2
```

**Implementation:**
- ✅ Added `PERCENT` token to scanner
- ✅ Mapped `%` to existing `OP_MOD` bytecode operation
- ✅ Works with all numeric types

**Test File:** `test_all_roadmap_features.nt`

---

### 4. String Interpolation ✅ IMPLEMENTED
**Status:** Complete  
**Impact:** High  
**Effort:** Medium  
**Description:** Allow embedding expressions directly in strings.

**Example:**
```neutron
var name = "World";
var count = 42;
say("Hello, ${name}! Count: ${count}");
// Output: Hello, World! Count: 42
```

**Implementation:**
- ✅ Updated scanner to recognize `${...}` in strings
- ✅ Parse embedded expressions with chunk-based approach
- ✅ Generate bytecode to concatenate parts using PLUS operations
- ✅ Supports variables, literals, and complex expressions

**Test File:** `test_all_roadmap_features.nt`

---

### 5. Enhanced Array Operations ✅ IMPLEMENTED
**Status:** Complete  
**Impact:** Medium  
**Effort:** Medium  
**Description:** Add comprehensive array manipulation methods.

**Implemented Features:**
```neutron
var arr = [1, 2, 3, 4, 5];

// Property:
arr.length;             // 5

// Basic methods:
arr.slice(1, 3);        // [2, 3]
arr.indexOf(3);         // 2
arr.join(", ");         // "1, 2, 3, 4, 5"
arr.reverse();          // [5, 4, 3, 2, 1]
arr.sort();             // [1, 2, 3, 4, 5]
arr.push(6);            // Add element
arr.pop();              // Remove and return last element

// Advanced methods with callbacks:
arr.map(fun(x) { return x * 2; });      // [2, 4, 6, 8, 10]
arr.filter(fun(x) { return x > 2; });   // [3, 4, 5]
arr.find(fun(x) { return x == 3; });    // 3
```

**Implementation:**
- ✅ Added `length` property access for arrays in OP_GET_PROPERTY
- ✅ Implemented all basic array methods in `callArrayMethod()`
- ✅ Implemented advanced methods (map, filter, find) with callback support
- ✅ **Critical VM Fix:** Modified `VM::run()` to accept `minFrameDepth` parameter
  - Enables nested execution contexts for callbacks from native code
  - Allows user functions called from C++ array methods to execute properly
- ✅ Fixed stack management in array method calls

**Test Files:** `test_array_advanced.nt`, `test_all_roadmap_features.nt`

---

## 🔥 High Priority

### 6. Switch/Match Statement ✅ COMPLETED
**Impact:** Medium  
**Effort:** High  
**Description:** Add switch/match statement for cleaner conditional logic.

**Status:** Implemented and tested. See `tests/test_match.nt` for comprehensive tests.

**Example:**
```neutron
var day = 3;

match (day) {
    1 => say("Monday");
    2 => say("Tuesday");
    3 => say("Wednesday");
    default => say("Other day");
}
```

---

## 💡 Medium Priority

### 7. Try-Catch Error Handling ✅ COMPLETE
**Impact:** Medium  
**Effort:** High  
**Description:** Add structured exception handling.

**Status:** Full implementation completed with try, catch, finally, and throw statements.

**Example:**
```neutron
use sys;

try {
    var content = sys.read("nonexistent.txt");
    say(content);
} catch (error) {
    say("Error: " + error);
} finally {
    say("Cleanup operations");
}
```

**Implementation:**
- Add `try`, `catch`, `finally`, `throw` keywords
- Implement exception object type
- Add exception handling in VM
- Bytecode for try-catch blocks
- Stack unwinding mechanism
- Exception value passing to catch blocks
- Finally block execution
- Nested exception handling

---

### 8. Lambda Functions / Anonymous Functions ✅ COMPLETED
**Impact:** Medium  
**Effort:** Medium  
**Description:** Support inline function definitions.

**Status:** Fully implemented with OP_CLOSURE bytecode. See `tests/test_lambda_comprehensive.nt` for tests.

**Example:**
```neutron
var add = fun(a, b) { return a + b; };
say(add(5, 3));  // 8

// Use in array operations
var numbers = [1, 2, 3];
var doubled = numbers.map(fun(x) { return x * 2; });
```

---

### 8. Modulo Operator Alias
**Impact:** Low  
**Effort:** Low  
**Description:** Add `%` as alias for modulo operation (currently uses `mod`).

**Example:**
```neutron
var remainder = 10 % 3;  // Same as: 10 mod 3
say(remainder);  // 1
```

---

## 🚀 Advanced Features

### 9. Regular Expressions
**Impact:** Medium  
**Effort:** High  
**Description:** Add regex support for string pattern matching.

**Example:**
```neutron
use regex;

var pattern = regex.compile("\\d{3}-\\d{4}");
var text = "Call me at 555-1234";

if (pattern.test(text)) {
    var match = pattern.match(text);
    say("Found: " + match[0]);
}
```

---

### 10. File System Module Enhancements ✅ COMPLETED
**Impact:** Low  
**Effort:** Medium  
**Description:** Add more file system operations to sys module.

**Status:** Implemented and tested. See `tests/modules/test_sys_module.nt`.

**Implemented Features:**
```neutron
use sys;

// Directory listing
var files = sys.listdir(".");
for (var i = 0; i < files.length; i = i + 1) {
    say(files[i]);
}

// File info
var info = sys.stat("file.txt");
say("Size: " + info.size);
say("Modified: " + info.mtime);

// Permissions
sys.chmod("file.txt", 420); // 0644 in decimal

// Temp files
var tmpfile = sys.tmpfile();
sys.write(tmpfile, "temporary data");

// Recursive directory removal with safety
sys.rmdir("folder", true); // Cannot delete outside cwd
```

---

### 11. Async/Await or Coroutines
**Impact:** High  
**Effort:** Very High  
**Description:** Support for asynchronous programming.

**Example:**
```neutron
use http;

async fun fetchData(url) {
    var response = await http.get(url);
    return response.body;
}

var data = await fetchData("https://api.example.com/data");
say(data);
```

---

### 12. Package Manager
**Impact:** High  
**Effort:** Very High  
**Description:** Create a package manager for Neutron modules.

**Features:**
- Central package repository
- Package installation: `neutron install package-name`
- Version management
- Dependency resolution
- Package publishing

---

### 13. HTTP & JSON Module Enhancements ✅ COMPLETED
**Impact:** Medium  
**Effort:** Medium  
**Description:** Enhanced HTTP and JSON modules with additional functionality.

**Status:** Implemented and tested. See `tests/modules/test_http_module.nt` and `tests/modules/test_json_module.nt`.

**HTTP Module - Implemented Features:**
```neutron
use http;

// REST API methods (existing)
http.get(url);
http.post(url, data);
http.put(url, data);
http.delete(url);
http.patch(url, data);
http.head(url);

// New utility functions
http.request("OPTIONS", url);  // Custom method
http.urlEncode("hello world!"); // URL encoding
http.urlDecode("hello+world%21"); // URL decoding
http.parseQuery("name=John&age=30"); // Parse query strings

// Server creation (mock)
var server = http.createServer(handler);
http.listen(server, 3000);
```

**JSON Module - Implemented Features:**
```neutron
use json;

// Core functions (existing)
json.stringify(obj);
json.parse(jsonStr);
json.get(obj, key);

// New manipulation functions
json.set(obj, key, value);     // Set property
json.has(obj, key);            // Check if key exists
json.keys(obj);                // Get all keys
json.values(obj);              // Get all values
json.merge(obj1, obj2);        // Merge objects
json.delete(obj, key);         // Remove property
json.clone(obj);               // Deep copy
```

---

### 14. Regular Expressions Module ✅ COMPLETED
**Impact:** High  
**Effort:** Medium  
**Description:** Add comprehensive regex support for pattern matching and text manipulation.

**Status:** Implemented and tested. See `tests/modules/test_regex_module.nt`.

**Regex Module - Implemented Features:**
```neutron
use regex;

// Core functions
regex.test(text, pattern);        // Full string match
regex.search(text, pattern);      // Search for pattern
regex.find(text, pattern);        // Find with position and groups
regex.findAll(text, pattern);     // Find all matches
regex.replace(text, pattern, replacement);  // Replace matches
regex.split(text, pattern);       // Split by pattern

// Utilities
regex.isValid(pattern);           // Validate pattern
regex.escape(text);               // Escape special characters

// Examples
var email = "user@example.com";
if (regex.test(email, "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")) {
    say("Valid email!");
}

var phone = "1234567890";
var formatted = regex.replace(phone, "(\\d{3})(\\d{3})(\\d{4})", "($1) $2-$3");
say(formatted);  // (123) 456-7890
```

**Implementation:**
- ✅ Uses C++ std::regex (ECMAScript grammar)
- ✅ Full capture group support
- ✅ Backreferences in replacements
- ✅ Comprehensive error handling
- ✅ Position and length tracking for matches

**Documentation:** `docs/modules/regex_module.md`

---

### 15. Standard Library Expansion
**Impact:** Medium  
**Effort:** High  
**Description:** Add more built-in modules.

**Suggested Modules:**
- `os` - Operating system interfaces (separate from sys)
- `path` - Path manipulation utilities
- `crypto` - Cryptographic functions
- `random` - Random number generation
- `datetime` - Enhanced date/time handling
- `collections` - Data structures (Stack, Queue, Set, Map)
- `io` - Enhanced I/O operations
- `testing` - Unit testing framework
- `logging` - Logging utilities

---

### 16. Debugger
**Impact:** High  
**Effort:** Very High  
**Description:** Interactive debugger for Neutron scripts.

**Features:**
- Breakpoints
- Step through code
- Inspect variables
- Call stack viewing
- Watch expressions

**Usage:**
```bash
neutron --debug script.nt
```

---

### 17. Static Type Hints (Optional)
**Impact:** Medium  
**Effort:** Very High  
**Description:** Optional type annotations for better tooling support.

**Example:**
```neutron
fun add(a: number, b: number): number {
    return a + b;
}

var name: string = "John";
var age: number = 30;
```

---

### 18. Object Destructuring
**Impact:** Low  
**Effort:** Medium  
**Description:** Unpack object properties into variables.

**Example:**
```neutron
use sys;

var info = sys.info();
var { platform, arch } = info;  // Destructure

say("Platform: " + platform);
say("Architecture: " + arch);
```

---

### 17. Spread Operator
**Impact:** Low  
**Effort:** Medium  
**Description:** Expand arrays or objects in-place.

**Example:**
```neutron
var arr1 = [1, 2, 3];
var arr2 = [4, 5, 6];
var combined = [...arr1, ...arr2];  // [1, 2, 3, 4, 5, 6]

var obj1 = {"a": 1, "b": 2};
var obj2 = {"c": 3, ...obj1};  // {"a": 1, "b": 2, "c": 3}
```

---

### 18. Iterators and Generators
**Impact:** Medium  
**Effort:** High  
**Description:** Support for custom iteration protocols.

**Example:**
```neutron
fun* range(start, end) {
    var i = start;
    while (i < end) {
        yield i;
        i = i + 1;
    }
}

for (var num in range(1, 10)) {
    say(num);
}
```

---

## 🔧 Tooling & Infrastructure

### 19. Language Server Protocol (LSP)
**Impact:** High  
**Effort:** Very High  
**Description:** LSP server for IDE integration.

**Features:**
- Code completion
- Go to definition
- Find references
- Syntax highlighting
- Error diagnostics
- Code formatting

---

### 20. Formatter
**Impact:** Medium  
**Effort:** Medium  
**Description:** Automatic code formatting tool.

**Usage:**
```bash
neutron fmt script.nt
```

---

### 21. Linter
**Impact:** Medium  
**Effort:** Medium  
**Description:** Static analysis tool for code quality.

**Usage:**
```bash
neutron lint script.nt
```

---

### 22. REPL Enhancements
**Impact:** Low  
**Effort:** Low  
**Description:** Improve the interactive shell.

**Features:**
- Syntax highlighting
- Auto-completion
- Command history
- Multi-line editing
- Variable inspection

---

## 📊 Performance Improvements

### 23. JIT Compilation ✅ COMPLETED
**Impact:** Very High
**Effort:** Very High
**Description:** Just-in-time compilation for better performance.

**Status:** Multi-tier JIT fully implemented and integrated with VM. See [JIT Documentation](jit.md).

**Features:**
- Hot-spot profiler with threshold-based tier promotion
- Tier-1 threaded code compiler with inline caching
- Tier-2 tracing JIT with IR, optimization passes
- Native x86-64 and ARM64 codegen
- OSR (On-Stack Replacement)
- Deoptimization/guard failure fallback
- 10 comprehensive JIT tests

---

### 24. AOT Compilation ✅ COMPLETED
**Impact:** High
**Effort:** High
**Description:** Ahead-of-Time compilation to standalone native executables.

**Status:** AOT compiler fully functional with 100% test coverage. See [AOT Documentation](aot.md).

**Features:**
- Bytecode to C++ code generation
- Static linking for native modules
- Automatic fallback to interpreter mode
- Cross-platform executable generation
- Global variable support
- Optimization passes (constant folding, dead code elimination)
- Debug symbols (source maps)
- Array support (static allocation pools)
- Native module interface (math, random, fmt, path)
- Cross-compilation support
- Function call support
- 10/10 AOT tests passing (100%)

**Future Enhancements:**

### 24.1. AOT: Global Variable Support
**Impact:** High
**Effort:** Medium
**Description:** Add support for global variables in AOT-compiled code.

**Implementation:**
- Static initialization of globals at compile time
- Lifetime management for global scope
- Support for `var` declarations at module level
- Handle global variable initialization order

**Example:**
```neutron
// Should compile to AOT
var counter = 0;

fun increment() {
    counter = counter + 1;
    return counter;
}
```

---

### 24.2. AOT: Limited Native Module Support
**Impact:** High
**Effort:** High
**Description:** Create AOT-compatible interfaces for native modules.

**Implementation:**
- Define C ABI for module functions
- Static linking interface for Box modules
- Header generation for module functions
- Support for pure native modules (no VM dependency)

**Candidate Modules:**
- `math` - Pure mathematical functions
- `random` - Random number generation
- `fmt` - String formatting
- `path` - Path manipulation

---

### 24.3. AOT: Object/Array Support
**Impact:** Medium
**Effort:** High
**Description:** Add support for objects and arrays via static allocation pools.

**Implementation:**
- Pre-allocated object pools at compile time
- Static array size inference
- Stack allocation for small objects
- Limit: fixed-size collections known at compile time

**Example:**
```neutron
// Could work with static allocation
var point = {"x": 10, "y": 20};
var coords = [1, 2, 3, 4, 5];
```

---

### 24.4. AOT: Cross-Compilation
**Impact:** Medium
**Effort:** High
**Description:** Build AOT executables for multiple target platforms.

**Implementation:**
- Cross-compilation toolchain support
- Target platform specification
- Multi-arch binary generation
- Integration with `neutron build --target`

**Usage:**
```bash
# Build for Linux from macOS
neutron build --target linux-x64

# Build for Windows from Linux
neutron build --target windows-x64

# Universal binary (macOS)
neutron build --target macos-universal
```

---

### 24.5. AOT: Optimization Passes
**Impact:** High
**Effort:** Medium
**Description:** Add compiler optimization passes for better performance.

**Implementation:**
- Dead code elimination (remove unreachable bytecode)
- Function inlining for small functions
- Constant propagation and folding
- Loop invariant code motion
- Common subexpression elimination

**Example:**
```neutron
// Before optimization
var x = 10 + 20;  // Folded to 30
var y = x * 2;    // Propagated to 60

// After optimization
var y = 60;  // Direct constant
```

---

### 24.6. AOT: Debug Symbols
**Impact:** Medium
**Effort:** Medium
**Description:** Generate source maps and debug symbols for AOT binaries.

**Implementation:**
- DWARF debug info generation (Linux/macOS)
- PDB debug info generation (Windows)
- Source line to native instruction mapping
- Variable name preservation
- Integration with debuggers (gdb, lldb, Visual Studio)

**Usage:**
```bash
# Build with debug symbols
neutron build --debug

# Debug the native binary
gdb ./build/my-app
lldb ./build/my-app
```

---

### 24.7. AOT: Partial Evaluation
**Impact:** Medium
**Effort:** High
**Description:** Compile-time constant folding and partial evaluation.

**Implementation:**
- Constant expression evaluation at compile time
- Partial function evaluation with known arguments
- Tree shaking for unused functions
- Specialization for constant arguments

**Example:**
```neutron
// Compile-time evaluation
fun factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

var result = factorial(5);  // Evaluated to 120 at compile time
```

---

### 24. Garbage Collection Optimization
**Impact:** Medium  
**Effort:** High  
**Description:** Improve GC algorithm for better memory management.

- Generational GC
- Incremental GC
- Concurrent GC

---

### 25. Bytecode Optimization
**Impact:** Medium  
**Effort:** Medium  
**Description:** Optimize generated bytecode.

- Constant folding
- Dead code elimination
- Common subexpression elimination
- Peephole optimization

---

## 📚 Documentation & Examples

### 26. Interactive Tutorial
**Impact:** Medium  
**Effort:** Medium  
**Description:** Step-by-step interactive tutorial for beginners.

---

### 27. Cookbook
**Impact:** Low  
**Effort:** Low  
**Description:** Collection of common recipes and patterns.

---

### 28. Video Tutorials
**Impact:** Low  
**Effort:** Medium  
**Description:** Video series covering language features.

---

## 🌐 Community & Ecosystem

### 29. Online Playground
**Impact:** High  
**Effort:** High  
**Description:** Web-based Neutron interpreter.

- Run code in browser
- Share code snippets
- Embedded examples in documentation

---

### 30. Module Registry
**Impact:** Medium  
**Effort:** High  
**Description:** Central repository for community modules.

---

## Summary

### Implementation Priority Order:

1. **Quick Wins** (1-2 weeks each):
   - Command line arguments
   - Modulo operator alias
   - Empty string to int fix ✅ (Already done!)

2. **High Impact** (1-2 months each):
   - Break/Continue statements
   - String interpolation
   - Enhanced array operations
   - Lambda functions

3. **Major Features** (2-4 months each):
   - Try-catch error handling
   - Switch/match statement
   - LSP server
   - Package manager

4. **Long-term Goals** (6+ months):
   - JIT compilation
   - Async/await
   - Debugger
   - Standard library expansion

---

**Note:** This is a living document. Priorities may change based on community feedback and project needs.
