# Random Module

The `random` module provides functions for generating random numbers and performing random operations, similar to Python's random module. It uses a high-quality Mersenne Twister random number generator with cross-platform secure seeding.

## Usage

```neutron
use random

// Generate random numbers
let r = random.random()        // 0.0 <= r < 1.0
let i = random.randint(1, 10)  // 1 <= i <= 10
let f = random.uniform(5.0, 15.0)  // 5.0 <= f <= 15.0
```

## Core Functions

### `random()`
Returns a random floating-point number between 0.0 (inclusive) and 1.0 (exclusive).

```neutron
let r = random.random()
print(r)  // e.g., 0.7394881546974297
```

### `uniform(a, b)`
Returns a random floating-point number between `a` and `b` (inclusive).

**Parameters:**
- `a` (number): Lower bound
- `b` (number): Upper bound

```neutron
let temp = random.uniform(20.0, 30.0)
print(temp)  // e.g., 25.847392
```

### `randint(a, b)`
Returns a random integer between `a` and `b` (both inclusive).

**Parameters:**
- `a` (number): Lower bound (integer)
- `b` (number): Upper bound (integer)

```neutron
let dice = random.randint(1, 6)
print(dice)  // e.g., 4
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
```

### `shuffle(array)`
Shuffles the array in-place using the Fisher-Yates algorithm. Returns `nil`.

**Parameters:**
- `array` (array): Array to shuffle

```neutron
let cards = [1, 2, 3, 4, 5]
random.shuffle(cards)
print(cards)  // e.g., [3, 1, 5, 2, 4]
```

### `sample(array, k)`
Returns a new array containing `k` random elements from the original array without replacement.

**Parameters:**
- `array` (array): Source array
- `k` (number): Number of elements to sample

```neutron
let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
let sample = random.sample(numbers, 3)
print(sample)  // e.g., [7, 2, 9]
```

## State Management

### `seed(value?)`
Sets the random number generator seed. If no value is provided, uses a secure random seed.

**Parameters:**
- `value` (number, optional): Seed value

```neutron
// Use specific seed for reproducible results
random.seed(12345)
let r1 = random.random()

random.seed(12345)  // Reset to same seed
let r2 = random.random()
// r1 == r2 (same sequence)

// Use secure random seed
random.seed()
```

## Distribution Functions

### `gauss(mu, sigma)`
Returns a random number from a Gaussian (normal) distribution.

**Parameters:**
- `mu` (number): Mean of the distribution
- `sigma` (number): Standard deviation (must be positive)

```neutron
// Standard normal distribution (mean=0, std=1)
let value = random.gauss(0.0, 1.0)

// Custom distribution (mean=100, std=15)
let iq = random.gauss(100.0, 15.0)
```

### `expovariate(lambd)`
Returns a random number from an exponential distribution.

**Parameters:**
- `lambd` (number): Rate parameter (must be positive)

```neutron
// Exponential distribution with rate 1.0
let wait_time = random.expovariate(1.0)
```

### `triangular(low, high, mode)`
Returns a random number from a triangular distribution.

**Parameters:**
- `low` (number): Lower bound
- `high` (number): Upper bound (must be > low)
- `mode` (number): Mode (most likely value, must be between low and high)

```neutron
// Triangular distribution from 0 to 10 with mode at 5
let value = random.triangular(0.0, 10.0, 5.0)
```

## Utility Functions

### `getrandbits(k)`
Returns a random integer with `k` random bits.

**Parameters:**
- `k` (number): Number of bits (1-32)

```neutron
let byte_value = random.getrandbits(8)    // 0-255
let bit = random.getrandbits(1)           // 0 or 1
let word = random.getrandbits(16)         // 0-65535
```

## Examples

### Dice Rolling Simulation
```neutron
use random

fn roll_dice(sides) {
    return random.randint(1, sides)
}

fn roll_multiple(count, sides) {
    let results = []
    for (let i = 0; i < count; i++) {
        results.push(roll_dice(sides))
    }
    return results
}

// Roll 5 six-sided dice
let rolls = roll_multiple(5, 6)
print("Dice rolls: " + rolls.join(", "))
```

### Random Password Generator
```neutron
use random

fn generate_password(length) {
    let chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
    let password = ""
    
    for (let i = 0; i < length; i++) {
        let char_array = chars.split("")
        password += random.choice(char_array)
    }
    
    return password
}

let password = generate_password(12)
print("Generated password: " + password)
```

### Monte Carlo Pi Estimation
```neutron
use random

fn estimate_pi(samples) {
    let inside_circle = 0
    
    for (let i = 0; i < samples; i++) {
        let x = random.uniform(-1.0, 1.0)
        let y = random.uniform(-1.0, 1.0)
        
        if (x * x + y * y <= 1.0) {
            inside_circle++
        }
    }
    
    return 4.0 * inside_circle / samples
}

let pi_estimate = estimate_pi(100000)
print("Pi estimate: " + pi_estimate)
```

### Weighted Random Selection
```neutron
use random

fn weighted_choice(items, weights) {
    let total_weight = 0
    for (let i = 0; i < weights.length; i++) {
        total_weight += weights[i]
    }
    
    let r = random.uniform(0.0, total_weight)
    let cumulative = 0.0
    
    for (let i = 0; i < items.length; i++) {
        cumulative += weights[i]
        if (r <= cumulative) {
            return items[i]
        }
    }
    
    return items[items.length - 1]
}

let items = ["common", "uncommon", "rare", "legendary"]
let weights = [50, 30, 15, 5]  // Probabilities

let result = weighted_choice(items, weights)
print("Selected: " + result)
```

## Error Handling

The random module throws runtime errors for invalid arguments:

- **Invalid argument types**: All functions validate their argument types
- **Empty arrays**: `choice()` throws an error for empty arrays
- **Invalid ranges**: Functions validate that ranges are valid (e.g., `low < high`)
- **Negative parameters**: Distribution functions validate positive parameters where required
- **Sample size**: `sample()` throws an error if `k` > array length
- **Bit count**: `getrandbits()` validates bit count is between 1 and 32

```neutron
try {
    random.choice([])  // Error: empty array
} catch (e) {
    print("Error: " + e)
}

try {
    random.gauss(0.0, -1.0)  // Error: negative sigma
} catch (e) {
    print("Error: " + e)
}
```

## Cross-Platform Compatibility

The random module is designed to work consistently across all supported platforms:

- **Windows**: Uses `CryptGenRandom` for secure seeding
- **Unix/Linux/macOS**: Uses `/dev/urandom` for secure seeding
- **Fallback**: Uses high-resolution timer if secure sources unavailable

The Mersenne Twister algorithm ensures consistent random sequences across platforms when using the same seed.

## Performance Notes

- The module uses a single global random number generator for efficiency
- `shuffle()` uses the Fisher-Yates algorithm with O(n) time complexity
- `sample()` creates a copy of indices and shuffles them, also O(n)
- Distribution functions use standard mathematical transformations
- Seeding is thread-safe but individual random calls are not (use separate instances for multi-threading)

## Thread Safety

The random module uses a global random number generator state. For multi-threaded applications, consider:

1. Using separate random instances per thread (if available in future versions)
2. Synchronizing access to random functions
3. Pre-generating random numbers in a single thread

## See Also

- [Math Module](math_module.md) - Mathematical functions and constants
- [Crypto Module](crypto_module.md) - Cryptographic functions including secure random generation