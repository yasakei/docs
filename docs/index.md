# Neutron Documentation

Welcome to the **Neutron Programming Language** documentation!

---

## Find What You Need

### I'm New to Neutron

Start here if you're just getting started:

1. **[Quick Start](guides/quickstart.md)** — Install Neutron and write your first program (5 minutes)
2. **[Build Guide](guides/build.md)** — Detailed build instructions for your platform
3. **[Common Pitfalls](guides/common-pitfalls.md)** — Avoid common mistakes

---

### Learn the Language

Understand how Neutron works:

| Topic | Description |
|-------|-------------|
| **[Language Reference](reference/language_reference.md)** | Complete syntax and features |
| **[Module System](reference/module-system.md)** | How to use and create modules |
| **[Type System](type-system.md)** | Understanding types in Neutron |
| **[Error Handling](error_handling/index.md)** | Handle errors gracefully |

---

### Using Modules

Pre-built functionality for your programs:

#### Core Modules
| Module | What It Does |
|--------|--------------|
| **[sys](modules/sys_module.md)** | File operations, system access |
| **[json](modules/json_module.md)** | JSON parsing and serialization |
| **[http](modules/http_module.md)** | HTTP requests (web APIs) |
| **[math](modules/math_module.md)** | Mathematical operations |

#### Utility Modules
| Module | What It Does |
|--------|--------------|
| **[fmt](modules/fmt_module.md)** | Type conversion and formatting |
| **[strings](modules/strings_module.md)** | String/text manipulation |
| **[arrays](modules/arrays_module.md)** | Array/list operations |
| **[collections](modules/collections_module.md)** | Sets, stacks, queues |
| **[time](modules/time_module.md)** | Time, dates, delays |
| **[async](modules/async_module.md)** | Async operations, timers |
| **[log](modules/log_module.md)** | Logging with levels |
| **[regex](modules/regex_module.md)** | Regular expressions |
| **[process](modules/process_module.md)** | Process management |
| **[path](modules/path_module.md)** | File path utilities |
| **[random](modules/random_module.md)** | Random numbers |
| **[crypto](modules/crypto_module.md)** | Cryptographic functions |

---

### Advanced Topics

Deep dive into Neutron internals:

| Topic | Description |
|-------|-------------|
| **[JIT Compilation](implementation/jit.md)** | How JIT works (x86-64 & ARM64) |
| **[AOT Compilation](implementation/aot.md)** | Compile to native executables |
| **[Extending Neutron](extending-neutron.md)** | Create native C++ modules |
| **[LSP Setup](lsp.md)** | Editor integration (VS Code, etc.) |
| **[Roadmap](implementation/roadmap.md)** | Future development plans |
| **[Known Issues](implementation/known-issues.md)** | Current limitations and bugs |

---

### Project Management

Manage your Neutron projects:

| Topic | Description |
|-------|-------------|
| **[Project System](guides/project-system.md)** | Organize Neutron projects |
| **[Box Integration](reference/box-project-integration.md)** | Package manager usage |
| **[Durable Execution](guides/durable-execution.md)** | Checkpoint and resume |
| **[Test Suite](guides/test-suite.md)** | Write and run tests |

---

### Troubleshooting

Having problems?

| Resource | Description |
|----------|-------------|
| **[FAQ](faq.md)** | Frequently asked questions |
| **[Quick Syntax Reference](reference/syntax-quick-ref.md)** | Cheat sheet for common operations |
| **[Error Reference](error_handling/index.md)** | Understand error messages |
| **[Common Pitfalls](guides/common-pitfalls.md)** | Avoid typical mistakes |
| **[Known Issues](implementation/known-issues.md)** | Known bugs and workarounds |

---

## Documentation Structure

```
docs/
├── guides/              # How-to guides and tutorials
│   ├── quickstart.md
│   ├── build.md
│   ├── common-pitfalls.md
│   ├── project-system.md
│   ├── test-suite.md
│   └── durable-execution.md
│
├── reference/           # Technical reference
│   ├── language_reference.md
│   ├── module-system.md
│   ├── box-project-integration.md
│   ├── cross-platform.md
│   └── buffers.md
│
├── modules/             # Module API documentation
│   ├── sys_module.md
│   ├── json_module.md
│   ├── http_module.md
│   └── ... (all modules)
│
├── implementation/      # Internals and advanced topics
│   ├── jit.md
│   ├── aot.md
│   ├── roadmap.md
│   └── known-issues.md
│
├── error_handling/      # Error handling documentation
│   ├── index.md
│   └── error-handling.md
│
├── extending-neutron.md  # Native module development
├── lsp.md                # Language server setup
└── readme.md             # You are here
```

---

## Learning Path

### Beginner
1. Read [Quick Start](guides/quickstart.md)
2. Try examples from [Language Reference](reference/language_reference.md)
3. Explore [Core Modules](#core-modules)

### Intermediate
1. Study [Module System](reference/module-system.md)
2. Learn [Error Handling](error_handling/index.md)
3. Build a project using [Project System](guides/project-system.md)

### Advanced
1. Read [JIT/AOT](implementation/jit.md) documentation
2. Create [Native Modules](extending-neutron.md)
3. Contribute to Neutron

---

## External Links

- **GitHub**: [github.com/yasakei/neutron](https://github.com/yasakei/neutron)
- **Issues**: [Report a bug](https://github.com/yasakei/neutron/issues)
- **Discussions**: [Ask questions](https://github.com/yasakei/neutron/discussions)
- **NUR**: [Native modules registry](https://github.com/neutron-modules/nur)

---

**Need help?** Check the [Error Reference](error_handling/index.md) or ask in [GitHub Discussions](https://github.com/yasakei/neutron/discussions).
