# Fmt Module Documentation

The `fmt` module provides type conversion, type detection, string formatting, and number representation utilities.

## Usage

```neutron
use fmt;

fmt.to_int("42");        // 42
fmt.to_str(3.14);        // "3.14"
fmt.type(true);          // "bool"
fmt.is_string("hello");  // true
fmt.to_hex(255);         // "ff"
fmt.pad_left("5", 3, "0"); // "005"
```

## Type Conversion

### `fmt.to_int(value)`
Converts to integer (truncates decimals).

| Input | Output |
|-------|--------|
| `42.7` | `42` |
| `"123"` | `123` |
| `true` | `1` |
| `nil` | `0` |
| array/object/function | throws |

### `fmt.to_float(value)`
Converts to floating-point number.

| Input | Output |
|-------|--------|
| `42` | `42` |
| `"3.14"` | `3.14` |
| `true` | `1.0` |
| `nil` | `0.0` |

### `fmt.to_str(value)`
Converts to string.

| Input | Output |
|-------|--------|
| `42` | `"42"` |
| `true` | `"true"` |
| `nil` | `"nil"` |
| `"hi"` | `"hi"` |

### `fmt.to_bin(value)`
Converts integer to binary string (no leading zeros).

```neutron
fmt.to_bin(10);    // "1010"
fmt.to_bin(255);   // "11111111"
fmt.to_bin(true);  // "1"
fmt.to_bin(0);     // "0"
```

## Type Detection

### `fmt.type(value)`
Returns the type name as a string: `"nil"`, `"bool"`, `"number"`, `"string"`, `"function"`, `"object"`, `"array"`, `"module"`.

### Type Predicates

All take one argument and return a boolean.

| Function | Returns `true` when |
|----------|---------------------|
| `fmt.is_int(v)` | value is a number with no fractional part |
| `fmt.is_float(v)` | value is any number |
| `fmt.is_string(v)` | value is a string |
| `fmt.is_bool(v)` | value is a boolean |
| `fmt.is_nil(v)` | value is nil |
| `fmt.is_array(v)` | value is an array |

Note: `fmt.is_int` and `fmt.is_float` both require a `number` type — `is_int` additionally checks that the value has no fractional part.

```neutron
fmt.is_int(42);     // true
fmt.is_int(42.5);   // false
fmt.is_float(42.5); // true
fmt.is_float("x");  // false
```

## Number Formatting

### `fmt.to_hex(n)`
Returns lowercase hex string of integer `n`.

```neutron
fmt.to_hex(255);   // "ff"
fmt.to_hex(16);    // "10"
fmt.to_hex(0);     // "0"
```

### `fmt.to_oct(n)`
Returns octal string of integer `n`.

```neutron
fmt.to_oct(8);    // "10"
fmt.to_oct(255);  // "377"
```

## String Padding

### `fmt.pad_left(str, width, char?)`
Pads `str` on the left to reach `width`. Default pad char is space.

```neutron
fmt.pad_left("42", 5);       // "   42"
fmt.pad_left("42", 5, "0");  // "00042"
```

### `fmt.pad_right(str, width, char?)`
Pads `str` on the right to reach `width`.

```neutron
fmt.pad_right("hi", 5);      // "hi   "
fmt.pad_right("hi", 5, "-"); // "hi---"
```

If `str` is already at or beyond `width`, it's returned unchanged.

## Examples

```neutron
use fmt;

// Zero-pad a number for display
var id = fmt.pad_left(fmt.to_str(7), 4, "0"); // "0007"

// Hex dump style
var hex = fmt.to_hex(255); // "ff"

// Safe type check before math
if (fmt.is_float(userInput)) {
    var result = userInput * 2;
}

// Dynamic dispatch by type
fun describe(v) {
    say(fmt.type(v) + ": " + fmt.to_str(v));
}
```
