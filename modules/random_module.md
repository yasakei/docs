# Random Module

The `random` module provides functions for generating random numbers and performing random operations, similar to Python's random module. It uses a high-quality Mersenne Twister random number generator with cross-platform secure seeding.

## Usage

```neutron
use random

// Generate random numbers
let r = random.random()        // 0.0 <= r < 1.0
let u = random.uniform(1, 10)  // 1.0 <= u <= 10.0
let i = random.randint(1, 6)   // 1 <= i <= 6 (dice roll)
```

## Core Functions

### `random()`
Returns a random floating-point number between 0.0 (inclusive) and 1.0 (exclusive).

```neutron
let r = random.random()
print(r)  // e.g., 0.7394881546923746
```

### `uniform(a, b)`
Returns a random floating-point number between `a` and `b`. Arguments can be in any order.

**Parameters:**
- `a` (number): Lower or upper bound
- `b` (number): Upper or lower bound

```neutron
let temp = random.uniform(20.0, 30.0)  // Random temperature
let price = random.uniform(9.99, 19.99)  // Random price
```

### `randint(a, b)`
Returns a random integer between `a` and `b` (both inclusive). Arguments can be in any order.

**Parameters:**
- `a` (number): Lower or upper bound (converted to integer)
- `b` (number): Upper or lower bound (converted to integer)

```neutron
let dice = random.randint(1, 6)      // Dice roll
let year = random.randint(1990, 2023)  // Random year
```

## Sequence Operations

### `choice(array)`
Returns a random element from the given array.

**Parameters:**
- `array` (array): Non-empty array to choose from

```neutron
let colors = ["red", "green", "blue", "yellow"]
let color = random.choice(colors)
print(color)  // e.g., "blue"

let numbers = [1, 2, 3, 4, 5]
let num = random.choice(numbers)
```

### `shuffle(array)`
Shuffles the array in-place using the Fisher-Yates algorithm. Returns `nil`.

**Parameters:**
- `array` (array): Array to shuffle

```neutron
let deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
random.shuffle(deck)
print(deck)  // e.g., [3, 7, 1, 9, 5, 2, 8, 4, 6, 10]
```

### `sample(array, k)`
Returns an array of `k` unique random elements from the input array without replacement.

**Parameters:**
- `array` (array): Array to sample from
- `k` (number): Number of elements to sample (must be <= array length)

```neutron
let population = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
let sample = random.sample(population, 3)
print(sample)  // e.g., [7, 2, 9]

// No duplicates in result
let winners = random.sample(["Alice", "Bob", "Charlie", "Diana"], 2)
```

## State Management

### `seed(value?)`
Sets the random seed for reproducible results. If no argument is provided, uses a secure random seed.

**Parameters:**
- `value` (number, optional): Seed value

```neutron
// Set specific seed for reproducible results
random.seed(12345)
let r1 = random.random()
let r2 = random.randint(1, 100)

random.seed(12345)  // Reset to same seed
let r3 = random.random()  // Same as r1
let r4 = random.randint(1, 100)  // Same as r2

// Use secure random seed
random.seed()  // Different results each time
```

## Distribution Functions

### `gauss(mu, sigma)`
Returns a random number from a Gaussian (normal) distribution.

**Parameters:**
- `mu` (number): Mean of the distribution
- `sigma` (number): Standard deviation (must be positive)

```neutron
// Standard normal distribution (mean=0, std=1)
let z = random.gauss(0.0, 1.0)

// IQ scores (mean=100, std=15)
let iq = random.gauss(100.0, 15.0)

// Height in cm (mean=170, std=10)
let height = random.gauss(170.0, 10.0)
```

### `expovariate(lambd)`
Returns a random number from an exponential distribution.

**Parameters:**
- `lambd` (number): Rate parameter (must be positive)

```neutron
// Time between events (lambda=1.5 events per unit time)
let wait_time = random.expovariate(1.5)

// Failure rate modeling
let lifetime = random.expovariate(0.1)
```

### `triangular(low, high, mode)`
Returns a random number from a triangular distribution.

**Parameters:**
- `low` (number): Lower bound
- `high` (number): Upper bound (must be > low)
- `mode` (number): Most likely value (must be between low and high)

```neutron
// Project completion time: optimistic=5, pessimistic=15, most likely=8
let completion_time = random.triangular(5.0, 15.0, 8.0)

// Test scores with peak at 85
let score = random.triangular(0.0, 100.0, 85.0)
```

## Utility Functions

### `getrandbits(k)`
Returns a random integer with exactly `k` random bits.

**Parameters:**
- `k` (number): Number of bits (1-32)

```neutron
let bit = random.getrandbits(1)      // 0 or 1
let byte = random.getrandbits(8)     // 0-255
let word = random.getrandbits(16)    // 0-65535
```

## Examples

### Dice Rolling Simulation
```neutron
use random

// Roll two dice 1000 times
let results = {}
for (let i = 0; i < 1000; i++) {
    let roll = random.randint(1, 6) + random.randint(1, 6)
    if (results[roll] == nil) {
        results[roll] = 0
    }
    results[roll] = results[roll] + 1
}

// Print distribution
for (let sum = 2; sum <= 12; sum++) {
    print("Sum " + sum + ": " + (results[sum] || 0) + " times")
}
```

### Monte Carlo Pi Estimation
```neutron
use random

let inside_circle = 0
let total_points = 100000

for (let i = 0; i < total_points; i++) {
    let x = random.uniform(-1.0, 1.0)
    let y = random.uniform(-1.0, 1.0)
    
    if (x * x + y * y <= 1.0) {
        inside_circle++
    }
}

let pi_estimate = 4.0 * inside_circle / total_points
print("Pi estimate: " + pi_estimate)
```

### Random Password Generator
```neutron
use random

let chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

let password = ""
for (let i = 0; i < 12; i++) {
    password = password + random.choice(chars)
}
print("Generated password: " + password)
```

### Weighted Random Selection
```neutron
use random

// Simulate weighted selection using uniform distribution
fn weighted_choice(items, weights) {
    let total = 0
    for (let i = 0; i < weights.length; i++) {
        total = total + weights[i]
    }
    
    let r = random.uniform(0, total)
    let cumulative = 0
    
    for (let i = 0; i < items.length; i++) {
        cumulative = cumulative + weights[i]
        if (r <= cumulative) {
            return items[i]
        }
    }
    
    return items[items.length - 1]
}

let items = ["common", "uncommon", "rare", "legendary"]
let weights = [50, 30, 15, 5]  // Probabilities

for (let i = 0; i < 10; i++) {
    let item = weighted_choice(items, weights)
    print("Found: " + item)
}
```

## Error Handling

The random module throws errors for invalid arguments:

```neutron
// These will throw errors:
random.uniform("invalid", 5.0)        // Non-numeric arguments
random.choice([])                     // Empty array
random.gauss(0.0, -1.0)              // Negative standard deviation
random.sample([1, 2, 3], 5)          // Sample size > array size
random.getrandbits(0)                 // Invalid bit count
random.triangular(10.0, 5.0, 7.0)    // Invalid range
```

## Cross-Platform Compatibility

The random module uses secure seeding on all platforms:
- **Windows**: Uses `CryptGenRandom` for secure seed generation
- **Unix/Linux/macOS**: Uses `/dev/urandom` for secure seed generation
- **Fallback**: Uses high-resolution timer if secure sources unavailable

The underlying Mersenne Twister generator ensures consistent behavior across platforms when using the same seed.

## Thread Safety

The random module uses a global random number generator state. For multi-threaded applications, consider using separate seeds in different threads or implementing thread-local generators if needed.

## Performance Notes

- All functions are optimized for performance
- `shuffle()` uses the efficient Fisher-Yates algorithm
- Distribution functions use standard mathematical algorithms
- Seeding is only done once unless explicitly called again