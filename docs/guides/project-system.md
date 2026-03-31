# Neutron Project System

The Neutron project system provides a structured way to organize, build, and manage Neutron applications. Projects use `.quark` configuration files and support building standalone executables with all dependencies bundled.

## Quick Start

```bash
# Create a new project
./neutron init my-app

# Run the project
./neutron run

# Build to executable (AOT compilation when possible)
./neutron build

# Install Box package manager
./neutron install box
```

> **AOT Compilation:** The `neutron build` command automatically uses **Ahead-of-Time (AOT) compilation** when your code is compatible, generating optimized native executables. For pure computation code, this eliminates VM overhead entirely. See [AOT Documentation](../implementation/aot.md) for details.

## Project Structure

A typical Neutron project looks like this:

```
my-app/
├── .quark           # Project configuration
├── main.nt          # Entry point
├── .gitignore       # Git ignore rules
├── bin/             # Local tools (box symlink)
├── build/           # Compiled executables (created on build)
├── .box/            # Box modules (if used)
│   └── modules/
└── deps/            # Dependencies like Box (if installed)
    └── nt-box/
```

## The `.quark` Configuration File

The `.quark` file uses a simple INI-style format:

```ini
# Neutron Project Configuration

[project]
name = "my-app"
version = "1.0.0"
entry = "main.nt"
author = "Your Name"
description = "A Neutron project"

[dependencies]
# Box modules will be listed here
# base64 = "1.0.0"
```

### Configuration Options

#### `[project]` Section

- **`name`** (required) - Project name, used for the executable filename
- **`version`** (required) - Project version (semantic versioning recommended)
- **`entry`** (required) - Entry point file (default: `main.nt`)
- **`author`** (optional) - Project author
- **`description`** (optional) - Project description

#### `[dependencies]` Section

Lists Box modules and their versions (managed by Box package manager).

## Commands

### `neutron init [project-name]`

Initialize a new Neutron project in the current directory.

**Usage:**
```bash
# Use current directory name as project name
./neutron init

# Specify project name
./neutron init my-awesome-app
```

**Creates:**
- `.quark` - Project configuration
- `main.nt` - Sample entry file
- `bin/` - Local tools directory
- `build/` - Build output directory
- `.box/modules/` - Box modules directory
- `.gitignore` - Git ignore file

**Example:**
```bash
$ ./neutron init calculator
Initializing Neutron project: calculator
Created: main.nt
Created: build/
Created: .box/modules/
Created: .gitignore

✓ Project initialized successfully!

Next steps:
  1. Edit main.nt to add your code
  2. Run: ./neutron run
  3. Build: ./neutron build

To install Box package manager:
  ./neutron install box
```

### `neutron run`

Run the project's entry point without building an executable.

**Usage:**
```bash
./neutron run
```

**Requirements:**
- Must be in a Neutron project directory (has `.quark` file)
- Entry file specified in `.quark` must exist

**Example:**
```bash
$ ./neutron run
Running: my-app v1.0.0
Entry: main.nt

Hello from my-app!
```

### `neutron build`

Compile the project to a standalone native executable in the `build/` directory.

**Usage:**
```bash
./neutron build
```

**Requirements:**
- Must be in a Neutron project directory
- C++ compiler must be available (MSVC, GCC, or Clang)
- Entry file must exist

**Output:**
- Linux/macOS: `build/<project-name>`
- Windows: `build/<project-name>.exe`

**What gets bundled:**
- All Neutron runtime code
- Built-in modules (sys, json, http, etc.)
- Project Box modules from `.box/modules/`
- Your application code

**Example:
```bash
$ ./neutron build
Building: my-app v1.0.0
Entry: main.nt
Output: build/my-app

Compiling to executable: build/my-app
Executable created: build/my-app

$ ./build/my-app
Hello from my-app!
```

**Features:**
- ✅ Bundles all dependencies (runtime + modules)
- ✅ Standalone executable (no Neutron runtime needed)
- ✅ Cross-platform (Linux, macOS, Windows)
- ✅ Automatically includes Box modules from `.box/modules/`
- ✅ Includes all built-in modules
- ✅ Fast native execution
- ✅ Single binary distribution

### `neutron install box`

Install the Box package manager into the project's `deps/` directory.

**Usage:**
```bash
./neutron install box
```

**Requirements:**
- Must be in a Neutron project directory
- Git must be installed
- CMake and C++ compiler must be available

**What it does:**
1. Clones the [nt-box repository](https://github.com/yasakei/nt-box) to `deps/nt-box`
2. Builds Box for your platform
3. Makes Box available for installing native modules

**Example:**
```bash
$ ./neutron install box
Installing Box package manager...
Created: deps/
Cloning Box repository from https://github.com/yasakei/nt-box...
Cloning into 'deps/nt-box'...

Building Box for your platform...
[100%] Built target box

✓ Box installed successfully!

Box location: deps/nt-box/box
Local alias: bin/box

You can now use Box to install modules:
  box install <module-name>

Note: Add 'bin/' to your PATH or use './bin/box' directly
  export PATH="$PWD/bin:$PATH"  # Add to shell config for persistence
```

**Using Box after installation:**
```bash
# Add bin/ to PATH (recommended)
export PATH="$PWD/bin:$PATH"

# Install a module (automatically installs to .box/modules/)
box install base64

# Box detects .quark and installs locally + updates dependencies
# Or use direct path
./bin/box install base64

# Use in your code
use base64;
var encoded = base64.encode("Hello!");
say(encoded);
```

## Multi-File Projects

Projects can have multiple `.nt` files. Use the `using` statement to import other files:

```
my-app/
├── .quark
├── main.nt
├── utils.nt
└── lib/
    └── helper.nt
```

**main.nt:**
```js
using 'utils.nt';
using 'lib/helper.nt';

say("Starting app...");
greet("World");
```

**utils.nt:**
```js
fun greet(name) {
    say("Hello, ${name}!");
}
```

**lib/helper.nt:**
```js
fun calculate(x, y) {
    return x + y;
}
```

## Backward Compatibility

The project system is fully compatible with existing workflows:

```bash
# Direct script execution still works
./neutron script.nt

# Legacy binary compilation still works
./neutron -b script.nt output

# REPL still works
./neutron
```

## Best Practices

### 1. **Use Projects for Applications**
For any non-trivial application, use the project system:
- Better organization
- Reproducible builds
- Dependency management
- Version control

### 2. **Version Your Projects**
Update the `version` field in `.quark` when releasing:
```ini
[project]
version = "1.2.0"
```

### 3. **Use .gitignore**
The generated `.gitignore` excludes build artifacts:
```
build/
deps/
.box/
bin/
*.out
```

### 4. **Document Dependencies**
If using Box modules, they're automatically tracked in `.quark`:
```ini
[dependencies]
base64 = "1.0.0"
http-client = "2.1.3"
```

### 5. **Structure Large Projects**
```
my-app/
├── .quark
├── main.nt
├── src/
│   ├── core.nt
│   ├── api.nt
│   └── utils.nt
├── lib/
│   └── helpers.nt
└── tests/
    └── test_core.nt
```

## Examples

### Web Server Project

```bash
./neutron init my-server
cd my-server
./neutron install box
./deps/nt-box/box install http
```

**main.nt:**
```js
use http;

say("Starting server on port 8080...");

// Your server code here
```

```bash
./neutron build
./build/my-server
```

### CLI Tool Project

```bash
./neutron init my-tool
```

**main.nt:**
```js
use sys;

// Get command line arguments
var args = sys.argv();

if (args.length < 2) {
    say("Usage: my-tool <input>");
    return;
}

say("Processing: ${args[1]}");
```

```bash
./neutron build
./build/my-tool file.txt
```

### Multi-File Application

```bash
./neutron init calculator
```

**main.nt:**
```js
using 'operations.nt';
using 'display.nt';

var result = add(10, 5);
showResult("Addition", result);
```

**operations.nt:**
```js
fun add(a, b) {
    return a + b;
}

fun multiply(a, b) {
    return a * b;
}
```

**display.nt:**
```js
fun showResult(operation, value) {
    say("${operation}: ${value}");
}
```

```bash
./neutron run
# Output: Addition: 15

./neutron build
./build/calculator
# Output: Addition: 15
```

## Troubleshooting

### "Not in a Neutron project"

**Error:**
```
Error: Not in a Neutron project. Run './neutron init' to create one.
```

**Solution:**
Run `./neutron init` first or navigate to a directory with a `.quark` file.

### "Entry file not found"

**Error:**
```
Error: Entry file not found: main.nt
```

**Solution:**
- Check that the entry file specified in `.quark` exists
- Or update `.quark` to point to the correct entry file

### Box Installation Failed

**Error:**
```
Error: Failed to clone Box repository
```

**Solution:**
- Check internet connection
- Verify git is installed: `git --version`
- Try manually: `git clone https://github.com/yasakei/nt-box.git deps/nt-box`

### Build Failed

**Error:**
```
Failed to create executable
```

**Solution:**
- Ensure C++ compiler is installed (MSVC, GCC, or Clang)
- Check compiler availability: `gcc --version` or `clang --version`
- See [Build Guide](../guides/build.md) for platform-specific setup

## Migration from Scripts

Converting an existing script to a project:

```bash
# 1. Navigate to your script directory
cd my-scripts

# 2. Initialize project
./path/to/neutron init my-project

# 3. Update .quark if needed
# Change entry point if your main file isn't main.nt
nano .quark

# 4. Test
./path/to/neutron run

# 5. Build
./path/to/neutron build
```

## Summary

The Neutron project system provides:

✅ **Simple initialization** - One command to set up a project  
✅ **Easy execution** - `neutron run` for quick testing  
✅ **Native builds** - `neutron build` for standalone executables  
✅ **Dependency management** - Box integration with `neutron install box`  
✅ **Multi-file support** - Organize code across multiple files  
✅ **Backward compatible** - All existing features still work  
✅ **Cross-platform** - Works on Linux, macOS, and Windows  

Ready to start? Run `./neutron init` and build something amazing! 🚀
