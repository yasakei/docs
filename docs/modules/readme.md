# Neutron Built-in Modules Documentation

This directory contains comprehensive documentation for all built-in modules in the Neutron programming language.

## Core Modules

### System & Environment
- **[Sys Module](sys_module.md)** - File operations, system utilities, environment access, and process control
  - **Functions:** File I/O (`read`, `write`, `append`), file operations (`cp`, `mv`, `rm`), directory operations (`mkdir`, `rmdir`, `exists`), system info (`cwd`, `env`, `info`), user input (`input`), process control (`exit`, `exec`)

### Data Processing & Conversion
- **[JSON Module](json_module.md)** - JSON parsing, serialization, and object manipulation
  - **Functions:** `stringify`, `parse`, `get`

- **[Fmt Module](fmt_module.md)** - Dynamic type conversion and type detection utilities
  - **Functions:** `to_int`, `to_str`, `to_bin`, `to_float`, `type`

- **[Strings Module](strings_module.md)** - Comprehensive string manipulation and text processing
  - **Functions:** `split`, `join`, `trim`, `upper`, `lower`, `replace`, `contains`, `starts_with`, `ends_with`, `index_of`, `last_index_of`, `repeat`, `reverse`, `pad_left`, `pad_right`, `equals`, `encode`, `decode`, `hash`

### Array & Collection Manipulation
- **[Arrays Module](arrays_module.md)** - Comprehensive array manipulation and utility functions
  - **Functions:** `new`, `length`, `push`, `pop`, `at`, `set`, `slice`, `join`, `reverse`, `sort`, `index_of`, `contains`, `remove`, `remove_at`, `clear`, `clone`, `to_string`, `flat`, `fill`, `range`, `shuffle`

- **[Collections Module](collections_module.md)** - Advanced data structures: sets, stacks, and queues
  - **Functions:** `set_new`, `set_add`, `set_has`, `set_remove`, `set_size`, `set_union`, `set_intersection`, `set_difference`, `stack_new`, `stack_push`, `stack_pop`, `stack_peek`, `queue_new`, `queue_enqueue`, `queue_dequeue`, `queue_peek`

### Mathematical Operations
- **[Math Module](math_module.md)** - Mathematical operations and functions
  - **Functions:** `add`, `subtract`, `multiply`, `divide`, `pow`, `sqrt`, `abs`

### Network & Web
- **[HTTP Module](http_module.md)** - HTTP client functionality for web requests
  - **Functions:** `get`, `post`, `put`, `delete`, `head`, `patch`

### Time & Scheduling
- **[Time Module](time_module.md)** - Time operations, formatting, and delays
  - **Functions:** `now`, `format`, `sleep`

### Asynchronous Operations
- **[Async Module](async_module.md)** - Asynchronous operations, timers, and non-blocking execution
  - **Functions:** `run`, `await`, `sleep`, `timer`, `promise`

### Logging & Debugging
- **[Log Module](log_module.md)** - Structured, leveled logging with timestamps, colors, and file output
  - **Functions:** `debug`, `info`, `warn`, `error`, `set_level`, `get_level`, `set_file`, `set_color`, `set_timestamp`

## Usage

All modules can be imported using the `use` statement:

```neutron
use sys;
use math;
use json;
use http;
use time;
use fmt;
use async;
use collections;
use log;
use strings;

// Use module functions
var currentDir = sys.cwd();
var result = math.add(10, 20);
var jsonStr = json.stringify({"key": "value"});
var response = http.get("https://api.example.com");
var timestamp = time.now();
var type = fmt.type(42);
var task = async.run(fun() {
    return "async result";
});

// Collections
var mySet = collections.set_new();
collections.set_add(mySet, "item");

// Logging
log.info("Application started");
log.debug("Debug info");

// String manipulation
var parts = strings.split("a,b,c", ",");
var upper = strings.upper("hello");
```

## Module Categories

### **File & System Operations**
- **sys**: Complete file system access, environment variables, process control

### **Data Formats & Conversion**
- **json**: JSON processing for APIs and configuration
- **fmt**: Dynamic type conversion, type detection, format utilities
- **strings**: String manipulation, text processing, encoding/decoding, hashing

### **Data Structures**
- **arrays**: Array creation, manipulation, and utility functions
- **collections**: Advanced data structures (sets, stacks, queues)

### **Mathematical Computing**
- **math**: Essential mathematical operations and functions

### **Network Communication**
- **http**: HTTP client for web API interaction

### **Time & Scheduling**
- **time**: Timestamps, formatting, delays, performance timing

### **Asynchronous Operations**
- **async**: Non-blocking execution, timers, concurrent operations

### **Logging & Debugging**
- **log**: Structured logging with levels, timestamps, colors, and file output

## Documentation Features

Each module documentation includes:

- ✅ **Complete Function Reference** with parameters and return values
- ✅ **Practical Examples** showing real-world usage patterns  
- ✅ **Error Handling** guidance and best practices
- ✅ **Common Usage Patterns** and implementation templates
- ✅ **Performance Considerations** and optimization tips
- ✅ **Compatibility Information** across interpreter and compiled modes

## Quick Reference

### Most Commonly Used Functions

```neutron
// File operations
sys.read("file.txt")
sys.write("file.txt", "content")
sys.exists("file.txt")

// Math operations
math.add(a, b)
math.pow(base, exponent)
math.sqrt(number)

// JSON processing
json.stringify(object)
json.parse(jsonString)

// HTTP requests
http.get(url)
http.post(url, data)

// Time operations
time.now()
time.format(timestamp)
time.sleep(milliseconds)

// Async operations
async.run(fun() { /* async function */ })
async.await(task)
async.timer(fun() { /* delayed function */ }, delay_ms)

// Collections
var mySet = collections.set_new();
collections.set_add(mySet, value);
collections.set_has(mySet, value);

var stack = collections.stack_new();
collections.stack_push(stack, value);
collections.stack_pop(stack);

var queue = collections.queue_new();
collections.queue_enqueue(queue, value);
collections.queue_dequeue(queue);

// Logging
log.debug("Debug message");
log.info("Info message");
log.warn("Warning message");
log.error("Error message");
log.set_level(log.DEBUG);
log.set_file("app.log");

// String manipulation
strings.split("a,b,c", ",");
strings.join(array, ", ");
strings.upper("hello");
strings.lower("WORLD");
strings.trim("  text  ");
strings.replace("hello", "e", "a");
strings.contains("hello", "ell");
```

## Getting Started

1. **Choose the module** you need from the list above
2. **Click the module link** to view comprehensive documentation
3. **Import the module** in your Neutron code using `use modulename;`
4. **Follow the examples** provided in each module's documentation

## Module System Architecture

Neutron supports two types of modules:

- **Native Modules** (C++): Built-in modules compiled into the runtime (`sys`, `math`, `json`, `http`, `time`, `fmt`)
- **Neutron Modules** (.nt files): User-created modules written in Neutron language

All built-in modules are automatically available and work in interpreter mode.
