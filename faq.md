# Frequently Asked Questions

Common questions about Neutron.

---

## Getting Started

### What is Neutron?

Neutron is a lightweight, embeddable scripting language with JIT compilation support. It's designed to be simple yet powerful.

### How do I install Neutron?

See the [Quick Start Guide](guides/quickstart.md) for installation instructions for your platform.

### What platforms does Neutron support?

Neutron supports:
- **Linux** (Ubuntu, Debian, Fedora, RHEL, Arch)
- **macOS**
- **Windows** (Visual Studio or MSYS2)

### How do I run a Neutron program?

```bash
neutron program.nt
```

---

## Language Questions

### Is Neutron statically or dynamically typed?

Neutron is dynamically typed by default, but supports optional type annotations for runtime type safety.

### Does Neutron have classes?

Yes! Neutron supports classes with constructors (`init`) and methods. See the [Language Reference](reference/language_reference.md#classes-and-objects).

### How do I import modules?

```neutron
use sys;
use json;
use http;
```

### How do I read a file?

```neutron
use sys;

var content = sys.read("file.txt");
say(content);
```

### How do I write to a file?

```neutron
use sys;

sys.write("output.txt", "Hello, World!");
```

### How do I make HTTP requests?

```neutron
use http;

var response = http.get("https://api.example.com");
say(response.body);
```

---

## Error Questions

### What does "Undefined variable" mean?

You're trying to use a variable that hasn't been declared. Make sure you declare it with `var` first:

```neutron
var x = 10;  // Declare first
say(x);      // Then use
```

### What does "SyntaxError" mean?

There's a mistake in your code syntax. Check for:
- Missing semicolons (`;`)
- Missing quotes around strings
- Mismatched parentheses or braces

### How do I handle errors?

Use `try/catch`:

```neutron
try {
    var content = sys.read("file.txt");
} catch (error) {
    say("Error: " + error);
}
```

---

## Build Questions

### How do I build Neutron from source?

```bash
git clone https://github.com/yasakei/neutron.git
cd neutron
cmake -B build -S .
cmake --build build
```

See the [Build Guide](guides/build.md) for detailed instructions.

### What dependencies do I need?

- **CMake** 3.15+
- **C++ compiler** (GCC, Clang, or MSVC)
- **libcurl** (for HTTP module)
- **jsoncpp** (for JSON module)

See [Quick Start](guides/quickstart.md#prerequisites) for platform-specific dependencies.

### How do I run tests?

```bash
python3 run_tests.py
```

---

## Module Questions

### What modules are available?

See the [Modules Index](modules/index.md) for all built-in modules.

### Can I create my own modules?

Yes! You can create modules in Neutron or native C++ modules. See [Extending Neutron](extending-neutron.md).

### How do I share modules?

Modules can be shared via the [Neutron Universal Registry (NUR)](https://github.com/neutron-modules/nur).

---

## Editor/IDE Questions

### Is there VS Code support?

Yes! See the [LSP Documentation](lsp.md) for VS Code extension setup.

### What editors support Neutron?

Any editor that supports Language Server Protocol (LSP) can work with Neutron. See [LSP Setup](lsp.md).

---

## Performance Questions

### Is Neutron fast?

Neutron uses JIT compilation for better performance. For maximum speed, use AOT compilation to create native executables. See [AOT Guide](implementation/aot.md).

### Can I compile to a standalone executable?

Yes! See [AOT Compilation](implementation/aot.md).

---

## Getting Help

### Where can I ask questions?

- [GitHub Discussions](https://github.com/yasakei/neutron/discussions)
- [GitHub Issues](https://github.com/yasakei/neutron/issues) (for bugs)

### Where can I find examples?

Check the [examples](../programs/) directory in the repository.

---

## Quick Answers

| Question | Answer |
|----------|--------|
| File extension | `.nt` for source files |
| Print to console | `say("Hello")` |
| Get user input | `input("Prompt: ")` |
| Declare variable | `var x = 10` |
| Define function | `fun name() { }` |
| Import module | `use modulename;` |
| Comment | `// comment` |
| If statement | `if (condition) { }` |
| Loop | `for (var i = 0; i < 10; i++) { }` |

---

**Didn't find your answer?** Ask in [GitHub Discussions](https://github.com/yasakei/neutron/discussions).
