# Time Module Documentation

The `time` module provides time-related functionality: timestamps, formatting, sleeping, and parsing.

## Usage

```neutron
use time;

var now = time.now();
say(time.format(now)); // "2026-03-19 14:30:00"
```

## Functions

### `time.now()`
Returns the current local time as a millisecond timestamp (ms since Unix epoch).

```neutron
var ts = time.now(); // e.g. 1742394600000
```

### `time.utc()`
Same as `time.now()` but explicitly documents intent: returns UTC milliseconds since epoch. Both use `system_clock` internally.

### `time.clock()`
Returns a high-resolution monotonic timestamp in **microseconds**. Use this for benchmarking — it's not wall-clock time.

```neutron
var start = time.clock();
// ... work ...
var elapsed = time.clock() - start;
say("Took " + elapsed + " µs");
```

### `time.format(timestamp, format?)`
Formats a millisecond timestamp into a string.

- `timestamp` — ms since epoch
- `format` — strftime format string (default: `"%Y-%m-%d %H:%M:%S"`)

```neutron
var now = time.now();
time.format(now);                        // "2026-03-19 14:30:00"
time.format(now, "%Y-%m-%d");            // "2026-03-19"
time.format(now, "%H:%M:%S");            // "14:30:00"
time.format(now, "%Y%m%d_%H%M%S");      // "20260319_143000"
```

Uses local system timezone.

### `time.sleep(ms)`
Pauses execution for `ms` milliseconds.

```neutron
time.sleep(1000); // wait 1 second
```

### `time.diff(a, b)`
Returns `b - a` in milliseconds. Useful for readable duration calculations.

```neutron
var start = time.now();
time.sleep(500);
var elapsed = time.diff(start, time.now()); // ~500
```

### `time.parse(str, format?)`
Parses a date string into a millisecond timestamp.

- `str` — date string to parse
- `format` — strftime format (default: `"%Y-%m-%d %H:%M:%S"`)

Returns ms since epoch (local time via `mktime`).

```neutron
var ts = time.parse("2026-03-19 14:30:00");
var ts2 = time.parse("19/03/2026", "%d/%m/%Y");
```

Throws if the string doesn't match the format or the date is out of range.

## Common Patterns

### Benchmarking
```neutron
use time;

var start = time.clock();
// ... expensive work ...
var us = time.clock() - start;
say("Elapsed: " + us + " µs (" + (us / 1000) + " ms)");
```

### Timestamped logging
```neutron
use time;

fun log(msg) {
    say("[" + time.format(time.now()) + "] " + msg);
}

log("Server started");
```

### Retry with backoff
```neutron
use time;

fun retry(fn, maxAttempts) {
    var delay = 100;
    var i = 0;
    while (i < maxAttempts) {
        var ok = fn();
        if (ok) { return true; }
        time.sleep(delay);
        delay = delay * 2;
        i = i + 1;
    }
    return false;
}
```

## Notes

- `time.now()` and `time.utc()` both return milliseconds; `time.clock()` returns microseconds.
- `time.format()` uses local timezone; `time.parse()` also interprets via local timezone (`mktime`).
- `time.clock()` uses `high_resolution_clock` — suitable for sub-millisecond timing but not for wall-clock display.
