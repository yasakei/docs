# AOT (Ahead-of-Time) Compilation

Neutron supports **Ahead-of-Time (AOT) compilation** to generate standalone native executables from Neutron source code. This eliminates the need for the VM at runtime and provides faster startup times.

## Overview

AOT compilation translates Neutron bytecode into optimized C++ source code, which is then compiled to a native executable using your system's C++ compiler. The result is a single binary that runs without requiring the Neutron runtime.

```
Neutron Source (.nt)
        ↓
Bytecode Compiler
        ↓
AOT Compiler (C++ codegen)
        ↓
Native C++ Source (.cpp)
        ↓
System Compiler (g++/clang++/MSVC)
        ↓
Standalone Executable
```

## Quick Start

### Building a Neutron Project to Native Code

```bash
# Initialize a project (if not already done)
neutron init my-app
cd my-app

# Build to standalone executable
neutron build
```

The `neutron build` command automatically:
1. Analyzes your code for AOT compatibility
2. Compiles to native C++ if possible
3. Falls back to interpreter mode with embedded source if AOT isn't supported
4. Links all dependencies into a single executable

### Command-Line Flags

```bash
# Force AOT compilation (default behavior)
neutron build --aot

# Force interpreter mode (embeds source)
neutron build --no-aot

# Or use short flags
neutron build -c      # AOT compile
neutron build --interpret  # Interpreter mode
```

## How AOT Works

### Phase 1: Dependency Analysis

The AOT compiler analyzes your source code to determine if AOT compilation is possible:

```cpp
// AOT-compatible code
var x = 10;
var y = 20;
say(x + y);  // ✓ Pure computation

// AOT-incompatible code
use http;  // ✗ Native module requires interpreter
var response = http.get("https://api.example.com");
```

**AOT-Incompatible Modules:**
The following built-in modules require the interpreter (native code or external dependencies):

- `http` - Network operations
- `json` - JSON parsing (native C++ module)
- `sys` - File I/O and system operations
- `time` - Time and date functions
- `crypto` - Cryptographic operations
- `process` - Process management
- `arrays` - Advanced array operations
- `async` - Multi-threading support
- `regex` - Regular expressions
- `path` - Path manipulation
- `math` - Mathematical functions
- `fmt` - Type formatting utilities
- `random` - Random number generation

### Phase 2: Bytecode Generation

If your code is AOT-compatible, the compiler:

1. Scans and parses your Neutron source
2. Generates bytecode using the standard compiler
3. Passes the bytecode to the AOT code generator

```cpp
// Example: Neutron source
fun add(a, b) {
    return a + b;
}

var result = add(5, 3);
say(result);  // 8

// Compiled to bytecode, then AOT generates C++
```

### Phase 3: C++ Code Generation

The AOT compiler (`AotCompiler`) translates bytecode into C++ source code:

```cpp
// Auto-generated native code - no VM needed

#include <cstdint>
#include <cmath>

// Minimal Value struct for AOT execution
struct Value {
    enum Type { BOOL, NUMBER, STRING } type;
    union {
        bool asBool;
        double asNumber;
        const char* asString;
    };
};

// Pre-allocated global variables
Value global_result;

int neutron_main() {
    // Local variables
    Value local_a;
    Value local_b;
    Value local_result;
    
    // Compiled bytecode as C++ statements
    local_a.type = Value::NUMBER;
    local_a.asNumber = 5.0;
    
    local_b.type = Value::NUMBER;
    local_b.asNumber = 3.0;
    
    // add(a, b) inlined
    local_result.type = Value::NUMBER;
    local_result.asNumber = local_a.asNumber + local_b.asNumber;
    
    global_result = local_result;
    
    // say(result)
    printf("%g\n", global_result.asNumber);
    
    return 0;
}

int main() { return neutron_main(); }
```

### Phase 4: Native Compilation

The generated C++ code is compiled using your system's C++ compiler:

```bash
# Linux
g++ -O2 -o my-app my-app.cpp

# macOS
clang++ -O2 -o my-app my-app.cpp

# Windows (MSVC)
cl /O2 my-app.cpp
```

## AOT Compiler Limitations

The current AOT compiler (v1) has several limitations:

### Unsupported Features

| Feature | Status | Reason |
|---------|--------|--------|
| **Method Calls** | ❌ Not supported | Dynamic dispatch requires VM |
| **Closures** | ❌ Not supported | Upvalue tracking needs GC |
| **Upvalues** | ❌ Not supported | Closure environment capture |
| **Complex Objects** | ❌ Not supported | Objects need GC |
| **Index Operations** | ⚠️ Limited | Array index get/set not fully implemented |
| **Native Modules (full)** | ⚠️ Partial | AOT-compatible modules only (math, random, fmt, path) |

### Supported Features

| Feature | Status |
|---------|--------|
| **Local Variables** | ✅ Fully supported |
| **Global Variables** | ✅ Supported (v2+) |
| **Numeric Operations** | ✅ +, -, *, /, % |
| **Bitwise Operations** | ✅ AND, OR, XOR, NOT, shifts |
| **Comparisons** | ✅ <, >, ==, != |
| **Control Flow** | ✅ if/else, for, while |
| **Functions** | ✅ Basic functions (no closures) |
| **Constants** | ✅ Numeric constants |
| **Loops** | ✅ for, while (with limitations) |
| **Optimizations** | ✅ Constant folding, dead code elimination (v2+) |
| **Debug Symbols** | ✅ Source map generation (v2+) |
| **Arrays** | ✅ Static allocation pool (v2+) |
| **Native Modules** | ✅ AOT-compatible interface (v2+) |
| **Cross-Compilation** | ✅ Target platform specification (v2+) |

### Example: AOT-Compatible Code

```js
// ✓ AOT-compatible: Pure computation

fun fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fun factorial(n) {
    var result = 1;
    for (var i = 2; i <= n; i = i + 1) {
        result = result * i;
    }
    return result;
}

var fib10 = fibonacci(10);
var fact5 = factorial(5);

say(fib10);  // 55
say(fact5);  // 120
```

### Example: AOT-Incompatible Code

```js
// ✗ AOT-incompatible: Uses native modules

use http;
use json;
use sys;

// These require the interpreter
var response = http.get("https://api.example.com");
var data = json.parse(response.body);
sys.write("output.txt", data.value);
```

## Box Module Integration

AOT compilation works with **Box native modules** if they provide static libraries:

### AOT with Box Modules

```bash
# Install a Box module with static library support
box install my-native-module

# Check for static library
ls .box/modules/my-native-module/libmy-native-module.a
```

The AOT compiler checks for static libraries:

```cpp
// Project builder checks for .a files
std::string libA = projectRoot + "/.box/modules/" + mod + "/lib" + mod + ".a";
if (fileExists(libA)) {
    // Can link statically for AOT
    canAot = true;
} else {
    // Requires interpreter
    hasStaticLibs = false;
}
```

### Module Linking Priority

When building with AOT:

1. **Static library** (`.a`) - Preferred for AOT builds
2. **Shared library** (`.so`/`.dylib`/`.dll`) - Requires interpreter mode
3. **Source-only** (`.nt`) - Embedded in interpreter mode

## Build Output

### Successful AOT Build

```
[1/4] Reading project files...
[2/4] Analyzing dependencies...
      No external dependencies found
      Compiling to native code...
      Generated 47 native instructions
[3/4] Compiling C++ source...
      g++ -O2 -o my-app my-app.cpp
[4/4] Linking executable...
      Build complete: ./my-app
```

### Fallback to Interpreter Mode

```
[1/4] Reading project files...
[2/4] Analyzing dependencies...
      Module 'http' requires interpreter
      Module 'json' requires interpreter
[2/4] Embedding source files...
      Found 2 module(s) to embed
[3/4] Compiling C++ source...
      g++ -O2 -o my-app my-app.cpp
[4/4] Linking executable...
      Build complete: ./my-app (interpreter mode)
```

## Performance Characteristics

### AOT vs JIT vs Interpreter

| Metric | AOT | JIT | Interpreter |
|--------|-----|-----|-------------|
| **Startup Time** | ⚡ Fastest (no VM init) | 🐌 Slow (warmup needed) | 🐌 Slow |
| **Peak Performance** | 🚀 Good | ⚡ Best (optimized traces) | 🐢 Baseline |
| **Memory Usage** | 💾 Lowest (no VM overhead) | 💾 High (code cache) | 💾 Medium |
| **Binary Size** | 📦 Larger (embedded runtime) | 📦 Small (bytecode only) | 📦 Medium |
| **Platform Support** | ✅ Cross-compile needed | ✅ Runtime detection | ✅ Universal |

### When to Use AOT

**Use AOT when:**
- ✅ Building command-line tools
- ✅ Deploying to resource-constrained environments
- ✅ Need fast startup (no JIT warmup)
- ✅ Distributing to users without Neutron runtime
- ✅ Code is computationally pure (no I/O)

**Use JIT/Interpreter when:**
- ✅ Using native modules (http, json, sys, etc.)
- ✅ Need dynamic features (closures, objects)
- ✅ Rapid development iteration
- ✅ Debugging and profiling

## Technical Details

### AOT Compiler Architecture

**Files:**
- `include/aot/aot_compiler.h` - AOT compiler interface
- `src/aot/aot_compiler.cpp` - C++ code generation implementation

**Key Components:**

```cpp
namespace aot {

class AotCompiler {
public:
    AotCompiler(const Chunk* chunk);
    
    // Read bytecode
    uint8_t readByte();
    uint16_t readShort();
    
    // Constant pool handling
    std::string constantToCpp(size_t index);
    
    // Code generation phases
    void generatePrologue(const std::string& functionName);
    void generateBytecodeBody();
    void generateEpilogue();
    
    // Generate complete C++ source
    std::string generateCode(const std::string& functionName);
    
private:
    const Chunk* chunk;
    size_t ip;  // Instruction pointer
};

} // namespace aot
```

### Bytecode Translation

The AOT compiler translates each bytecode instruction to C++:

| Bytecode | Generated C++ |
|----------|---------------|
| `OP_LOAD_LOCAL_0` | `local_0 = ...;` |
| `OP_CONST_ZERO` | `stack.push(Value::number(0.0));` |
| `OP_ADD` | `auto b = pop(); auto a = pop(); push(a + b);` |
| `OP_SET_LOCAL` | `local_n = pop();` |
| `OP_LESS_JUMP` | `if (!(peek() < peek1())) ip = offset;` |
| `OP_LOOP` | `goto loop_top;` |

### Memory Model

AOT-compiled code uses a **static memory model**:

```cpp
// Pre-allocated globals
Value global_variables[MAX_GLOBALS];

// Stack-allocated locals (no GC needed)
Value local_variables[MAX_LOCALS];

// Value stack (fixed size)
Value stack[MAX_STACK_DEPTH];
```

This eliminates garbage collection overhead but limits dynamic features.

## Troubleshooting

### AOT Compilation Fails

**Problem:** Build falls back to interpreter mode unexpectedly

**Solution:** Check which modules are blocking AOT:

```
[2/4] Analyzing dependencies...
      Module 'sys' requires interpreter
      Module 'time' requires interpreter
```

Remove or replace incompatible modules, or accept interpreter mode.

### Missing Static Libraries

**Problem:** Box module lacks `.a` file

**Solution:** Rebuild the Box module with static library support:

```bash
cd .box/modules/my-module
box build --static
```

### Large Binary Size

**Problem:** AOT executable is unexpectedly large

**Cause:** Embedded runtime and standard library

**Solutions:**
1. Use release build flags: `-O2 -s` (strip symbols)
2. Enable LTO: `-flto`
3. Use interpreter mode for large applications

### Platform-Specific Issues

**Linux:**
```bash
# Static linking to reduce dependencies
g++ -static-libstdc++ -O2 -o my-app my-app.cpp
```

**macOS:**
```bash
# Universal binary for Intel + Apple Silicon
clang++ -arch x86_64 -arch arm64 -O2 -o my-app my-app.cpp
```

**Windows:**
```cmd
REM Static runtime to avoid DLL dependencies
cl /MT /O2 my-app.cpp
```

## Future Directions

Planned improvements for AOT compilation:

### ✅ Completed in v2+
- [x] **Global Variable Support** - Static initialization and lifetime management
- [x] **Optimization Passes** - Constant folding, dead code elimination
- [x] **Debug Symbols** - Source maps for debugging (bytecode offset -> C++ line)
- [x] **Array Support** - Static allocation pools for fixed-size arrays
- [x] **Native Module Interface** - AOT-compatible module system (math, random, fmt, path)
- [x] **Cross-Compilation** - Target platform specification (Linux, macOS, Windows)
- [x] **Function Call Support** - Basic function calls with proper stack management
- [x] **100% Test Coverage** - All 10 AOT tests compile to native code

### 🔜 Future Enhancements
- [ ] **Full Object Support** - Static object pools with property access
- [ ] **Array Index Operations** - OP_INDEX_GET and OP_INDEX_SET implementation
- [ ] **Module Linking** - Automatic linking of AOT-compatible native modules
- [ ] **Advanced Optimizations** - Function inlining, loop unrolling
- [ ] **DWARF/PDB Debug Info** - Native debug format generation
- [ ] **LTO Support** - Link-time optimization for better performance

## Test Results

**AOT Compilation Tests:** 10/10 passing (100%)

```
=== AOT Compilation Tests ===
  [PASS] test_computation.aot (AOT)
  [PASS] test_constant_folding.aot (AOT)
  [PASS] test_comprehensive.aot (AOT)
  [PASS] test_conditionals.aot (AOT)
  [PASS] test_increment.aot (AOT)
  [PASS] test_functions.aot (AOT)
  [PASS] test_globals.aot (AOT)
  [PASS] test_loops.aot (AOT)
  [PASS] test_comparisons.aot (AOT)
  [PASS] test_bitwise.aot (AOT)

AOT Test Summary:
  Passed: 10
  Failed: 0
```

**Run AOT tests:**
```bash
python3 run_tests.py --aot
```

## See Also

- [JIT Compilation](jit.md) - Multi-tier JIT architecture
- [Building from Source](../guides/build.md) - Build instructions
- [Project System](../guides/project-system.md) - Project management
- [Box Package Manager](../../nt-box/docs/) - Native module system

---

**Last Updated:** February 22, 2026  
**AOT Compiler Version:** 1.0  
**Neutron Version:** 1.0.0+
