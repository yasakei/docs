# Math Module Documentation

The `math` module provides mathematical operations, functions, and constants for Neutron programs.

## Usage

```neutron
use math;

var result = math.pow(2, 8);
var angle = math.sin(math.PI / 2);
say(math.PI); // 3.14159...
```

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `math.PI` | 3.14159265358979... | Pi |
| `math.E` | 2.71828182845904... | Euler's number |
| `math.INF` | Infinity | Positive infinity |
| `math.NAN` | NaN | Not a Number |

## Arithmetic

### `math.add(a, b)` / `math.subtract(a, b)` / `math.multiply(a, b)` / `math.divide(a, b)`
Basic arithmetic. `divide` throws on zero divisor.

### `math.pow(base, exp)`
Returns `base ^ exp`.

### `math.sqrt(n)`
Square root. Returns NaN for negative input.

### `math.abs(n)`
Absolute value.

### `math.ceil(n)` / `math.floor(n)` / `math.round(n)` / `math.trunc(n)`
Rounding functions. `trunc` removes the fractional part toward zero.

## Trigonometry

### `math.sin(x)` / `math.cos(x)` / `math.tan(x)`
Standard trig functions (radians).

### `math.asin(x)` / `math.acos(x)` / `math.atan(x)`
Inverse trig functions. Return radians.

### `math.atan2(y, x)`
Two-argument arctangent. Returns angle in radians in `(-π, π]`.

### `math.hypot(x, y)`
Returns `sqrt(x² + y²)` without overflow risk.

## Logarithms & Exponential

### `math.log(value, base?)`
Natural log by default. Pass a second argument for a custom base.

```neutron
math.log(math.E);     // 1
math.log(100, 10);    // 2
math.log(8, 2);       // 3
```

Throws if `value <= 0` or `base <= 0` or `base == 1`.

### `math.log2(n)` / `math.log10(n)`
Base-2 and base-10 logarithms. Throw if `n <= 0`.

### `math.exp(n)`
Returns `e ^ n`.

## Utility

### `math.min(a, b, ...)` / `math.max(a, b, ...)`
Return the minimum/maximum of two or more numbers.

### `math.clamp(value, min, max)`
Clamps `value` to `[min, max]`.

```neutron
math.clamp(15, 0, 10); // 10
math.clamp(-5, 0, 10); // 0
math.clamp(5, 0, 10);  // 5
```

### `math.sign(n)`
Returns `1`, `-1`, or `0`.

### `math.isnan(n)` / `math.isinf(n)`
Returns `true`/`false`. Useful after operations that may produce `NaN` or `Inf`.

```neutron
math.isnan(math.NAN);  // true
math.isinf(math.INF);  // true
math.isnan(1 / 0);     // false (1/0 = Inf, not NaN)
```

### `math.random()`
Returns a random float in `[0, 1)` using a seeded Mersenne Twister (mt19937). Better distribution than `rand()`.

## Examples

```neutron
use math;

// Circle area
fun circleArea(r) {
    return math.PI * math.pow(r, 2);
}

// Clamp a sensor reading
var reading = math.clamp(sensorValue, 0, 100);

// Safe log
if (x > 0) {
    var l = math.log(x);
}

// Pythagorean distance
var dist = math.hypot(dx, dy);
```

## Error Handling

All functions throw a runtime error on invalid input (wrong type, wrong arg count, domain errors like `log(0)`).
