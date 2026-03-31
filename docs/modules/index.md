# Modules

Built-in module documentation for Neutron.

## Core Modules

| Module | Description |
|--------|-------------|
| **[sys](sys_module.md)** | File I/O, system operations, environment access |
| **[json](json_module.md)** | JSON parsing and serialization |
| **[http](http_module.md)** | HTTP client for web requests |
| **[math](math_module.md)** | Mathematical operations |

## Data & Strings

| Module | Description |
|--------|-------------|
| **[fmt](fmt_module.md)** | Type conversion and formatting |
| **[strings](strings_module.md)** | String manipulation utilities |
| **[arrays](arrays_module.md)** | Array operations |
| **[collections](collections_module.md)** | Advanced data structures (sets, stacks, queues) |

## System & Time

| Module | Description |
|--------|-------------|
| **[time](time_module.md)** | Time, dates, and delays |
| **[process](process_module.md)** | Process management |
| **[path](path_module.md)** | File path utilities |
| **[async](async_module.md)** | Asynchronous operations and timers |

## Utilities

| Module | Description |
|--------|-------------|
| **[log](log_module.md)** | Structured logging |
| **[regex](regex_module.md)** | Regular expressions |
| **[random](random_module.md)** | Random number generation |
| **[crypto](crypto_module.md)** | Cryptographic functions |

---

## Quick Example

```neutron
use sys;
use json;
use http;
use math;

// File operations
var content = sys.read("file.txt");

// JSON
var data = json.parse(content);

// HTTP
var response = http.get("https://api.example.com");

// Math
var result = math.sqrt(16);
```

---

**Start here:** [sys module →](sys_module.md)
