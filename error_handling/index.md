# Error Handling

Documentation for Neutron's error handling system.

## Files

| Document | Description |
|----------|-------------|
| **[Error Handling Guide](error-handling.md)** | Comprehensive error handling guide |

## Error Types

| Type | Description |
|------|-------------|
| `SyntaxError` | Parse/grammar errors |
| `RuntimeError` | Execution errors |
| `TypeError` | Type mismatches |
| `ReferenceError` | Undefined variables |
| `RangeError` | Index out of bounds |
| `ArgumentError` | Wrong argument count |
| `DivisionError` | Division by zero |
| `StackError` | Stack overflow |
| `ModuleError` | Module loading issues |
| `IOError` | File operation errors |
| `LexicalError` | Tokenization errors |

## Example

```neutron
try {
    var content = sys.read("missing.txt");
} catch (error) {
    say("Error: " + error);
}
```

---

**Start here:** [Error Handling Guide →](error-handling.md)
