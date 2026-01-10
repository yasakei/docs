# Neutron Language Server Protocol (LSP)

The Neutron LSP provides intelligent language features for `.nt`, `.ntsc`, and `.quark` files in your editor.

## Features

### 🎨 Syntax Highlighting
- Full syntax highlighting for Neutron code (`.nt`, `.ntsc`)
- Separate syntax highlighting for Quark config files (`.quark`)
- Keywords, strings, numbers, comments, and operators are colorized

### 🧠 Autocomplete
- **Keywords**: `fn`, `let`, `const`, `if`, `else`, `while`, `for`, `return`, `class`, `use`, `safe`, etc.
- **Built-in Functions**: `print`, `println`, `input`, `len`, `type`, `str`, `int`, `float`, `range`, `typeof`, etc.
- **Modules**: Context-aware module completions (only available after `use` import)
  - `use "math"` → enables `math.` completions
  - `use "sys"` → enables `sys.` completions
  - `use "http"` → enables `http.` completions
  - And more: `json`, `fmt`, `time`, `regex`, `process`, `async`, `websocket`

### 📖 Hover Documentation
- Hover over keywords to see descriptions
- Hover over built-in functions to see signatures and documentation
- Safe mode indicators for `.ntsc` files

### ▶️ CodeLens
- **Run** button at the top of `.nt` and `.ntsc` files to execute scripts
- **Format** button to format the current file

### 📝 Document Formatting
- Format your code with proper indentation
- Accessible via CodeLens "Format" button or editor format command

### ✅ Safe Mode Validation
- `.ntsc` files enforce type-safe Neutron
- `safe { }` blocks in `.nt` files are validated
- Missing type annotations are flagged as errors

---

## Installation

### VS Code Extension

1. **Build the extension** (from the repository root):
   ```bash
   cd vscode-extension
   npm install
   npm run compile
   ```

2. **Package the extension**:
   ```bash
   npx vsce package
   ```

3. **Install the `.vsix` file**:
   - Open VS Code
   - Press `Ctrl+Shift+P` → "Extensions: Install from VSIX..."
   - Select the generated `neutron-X.X.X.vsix` file

### LSP Server

The LSP server (`neutron-lsp`) must be built and available in your PATH or specified in the extension settings.

1. **Build from source**:
   ```bash
   mkdir build && cd build
   cmake ..
   make neutron-lsp
   ```

2. **Verify installation**:
   ```bash
   ./neutron-lsp --version
   ```

---

## Usage

### Autocomplete

Start typing and suggestions will appear automatically:

```neutron
fn main() {
    let x = 10
    pri  // <- autocomplete shows: print, println
}
```

For module functions, first import the module:

```neutron
use "math"

fn main() {
    let result = math.  // <- shows: abs, sqrt, pow, sin, cos, etc.
}
```

### Hover Information

Hover over any keyword or built-in function to see documentation:

- `fn` → "Function declaration keyword"
- `print` → "print(value) - Prints a value to stdout"
- `len` → "len(value) - Returns the length of a string, array, or map"

### Running Scripts

Click the **▶ Run** CodeLens button at the top of any `.nt` or `.ntsc` file to execute it.

Alternatively, use the command palette:
- `Ctrl+Shift+P` → "Neutron: Run Current File"

### Formatting

Click the **📝 Format** CodeLens button or:
- `Ctrl+Shift+P` → "Neutron: Format Current File"
- Or use the standard VS Code format command: `Shift+Alt+F`

### Safe Mode

For type-safe Neutron code, use `.ntsc` files or `safe { }` blocks:

```neutron
// In a .ntsc file, all variables must have type annotations
fn add(a: int, b: int) -> int {
    return a + b
}

let x: int = 10  // OK
let y = 20       // ERROR: Missing type annotation
```

```neutron
// In a .nt file, use safe blocks for type-checked sections
safe {
    let x: int = 10  // OK - inside safe block
    let y = 20       // ERROR: Missing type annotation
}

let z = 30  // OK - outside safe block, no type required
```

---

## Supported File Types

| Extension | Language | Description |
|-----------|----------|-------------|
| `.nt` | Neutron | Standard Neutron source files |
| `.ntsc` | Neutron | Type-safe Neutron (Safe Contract) |
| `.quark` | Quark | Configuration files (TOML-like syntax) |

---

## Quark Configuration Files

Quark files use a TOML/INI-like syntax for project configuration:

```quark
# Project configuration
[project]
name = "my-app"
version = "1.0.0"
entry = "src/main.nt"

[dependencies]
math = "1.0"
http = "2.1"

[build]
output = "dist/"
optimize = true
```

---

## Troubleshooting

### LSP not starting

1. Check that `neutron-lsp` is in your PATH or correctly configured
2. Look at VS Code's Output panel → "Neutron Language Server"
3. Ensure the binary has execute permissions: `chmod +x neutron-lsp`

### No autocomplete suggestions

1. Ensure the file has a `.nt`, `.ntsc`, or `.quark` extension
2. For module completions, make sure you've imported the module with `use "module_name"`
3. Restart the language server: `Ctrl+Shift+P` → "Developer: Reload Window"

### Formatting not working

1. Check that the formatter is enabled in your settings
2. Try the CodeLens "Format" button directly
3. Check the Output panel for any error messages

### Safe mode errors not showing

1. Ensure the file has `.ntsc` extension for full type-safe mode
2. For `.nt` files, code must be inside a `safe { }` block
3. Reload the file or restart the language server

---

## Commands

| Command | Description |
|---------|-------------|
| `Neutron: Run Current File` | Execute the current Neutron script |
| `Neutron: Format Current File` | Format the current file |

---

## Development

### Building the LSP Server

```bash
# From repository root
mkdir build && cd build
cmake ..
make neutron-lsp

# The binary will be at build/neutron-lsp
```

### Building the VS Code Extension

```bash
cd vscode-extension
npm install
npm run compile

# For packaging
npx vsce package
```

### Testing

1. Open the `vscode-extension` folder in VS Code
2. Press `F5` to launch the Extension Development Host
3. Open a `.nt` file in the new window to test features

---

## Architecture

```
┌─────────────────┐     JSON-RPC      ┌─────────────────┐
│   VS Code       │ ◄───────────────► │  neutron-lsp    │
│   Extension     │     (stdio)       │  (C++ Server)   │
└─────────────────┘                   └─────────────────┘
        │                                     │
        ▼                                     ▼
┌─────────────────┐                   ┌─────────────────┐
│ TextMate Grammar│                   │ Parser/Analyzer │
│ (Highlighting)  │                   │ (Completions)   │
└─────────────────┘                   └─────────────────┘
```

The extension uses:
- **vscode-languageclient** to communicate with the LSP server
- **TextMate grammars** for syntax highlighting
- **JSON-RPC 2.0** protocol over stdio for server communication

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on contributing to the LSP and extension.
