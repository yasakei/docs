# Log Module Documentation

The `log` module provides structured, leveled logging with optional timestamps, color output, and file writing.

## Usage

```neutron
use log;

log.info("Server started on port 8080");
log.warn("Config file not found, using defaults");
log.error("Database connection failed");
```

## Log Levels

| Constant | Value | Color |
|----------|-------|-------|
| `log.DEBUG` | 0 | Cyan |
| `log.INFO` | 1 | Green |
| `log.WARN` | 2 | Yellow |
| `log.ERROR` | 3 | Red |

Default level is `INFO` — debug messages are suppressed unless you call `log.set_level(log.DEBUG)`.

## Logging Functions

### `log.debug(...)` / `log.info(...)` / `log.warn(...)` / `log.error(...)`

All four accept any number of arguments. Multiple arguments are joined with a space.

```neutron
log.info("User logged in:", userId);
log.warn("Retry attempt", attempt, "of", maxRetries);
log.error("Failed:", errorMessage);
```

Output format (default):
```
[2026-03-19 14:30:00] [INFO] User logged in: 42
```

## Configuration

### `log.set_level(n)`
Sets the minimum level to emit. Messages below this level are silently dropped.

```neutron
log.set_level(log.DEBUG);  // show everything
log.set_level(log.WARN);   // only warnings and errors
log.set_level(log.ERROR);  // only errors
```

### `log.get_level()` → number
Returns the current level.

### `log.set_file(path)`
Writes all log output (at or above the current level) to a file in addition to stdout. File output has no color codes.

```neutron
log.set_file("app.log");
log.info("This goes to stdout AND app.log");
```

### `log.set_color(bool)`
Enable or disable ANSI color codes in stdout output. Default: `true`.

```neutron
log.set_color(false);  // plain text output
```

### `log.set_timestamp(bool)`
Enable or disable the timestamp prefix. Default: `true`.

```neutron
log.set_timestamp(false);
log.info("hello");  // "[INFO] hello"
```

## Examples

### Basic application logging
```neutron
use log;

log.set_level(log.DEBUG);
log.set_file("app.log");

log.debug("Starting up");
log.info("Listening on port 3000");
log.warn("Memory usage above 80%");
log.error("Unhandled exception in worker");
```

### Conditional debug logging
```neutron
use log;

var DEBUG_MODE = true;

if (DEBUG_MODE) {
    log.set_level(log.DEBUG);
}

fun process(item) {
    log.debug("Processing item:", item);
    // ...
    log.info("Done:", item);
}
```

### Production config (no color, file only)
```neutron
use log;

log.set_color(false);
log.set_level(log.WARN);
log.set_file("/var/log/myapp.log");

log.info("This is suppressed (below WARN)");
log.warn("This goes to file");
log.error("This too");
```

## Notes

- Module state (level, file, color, timestamp) is global per process — configure once at startup.
- File output appends to the file if it already exists.
- Color codes use standard ANSI escapes and work on Linux/macOS terminals. Use `log.set_color(false)` on Windows or when piping output.
