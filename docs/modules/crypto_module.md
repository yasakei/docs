# Crypto Module

The `crypto` module provides cryptographic functions for Neutron applications, including hashing, encoding, random generation, and basic encryption utilities.

## Import

```js
use crypto;
```

## Functions

### Base64 Encoding

#### `crypto.base64_encode(data)`

Encodes a string to Base64 format.

**Parameters:**
- `data` (string): The string to encode

**Returns:** Base64 encoded string

**Example:**
```js
use crypto;

var original = "Hello, World!";
var encoded = crypto.base64_encode(original);
say(encoded); // SGVsbG8sIFdvcmxkIQ==
```

#### `crypto.base64_decode(encoded)`

Decodes a Base64 encoded string.

**Parameters:**
- `encoded` (string): The Base64 encoded string to decode

**Returns:** Decoded string

**Throws:** Error if the input is not valid Base64

**Example:**
```js
use crypto;

var encoded = "SGVsbG8sIFdvcmxkIQ==";
var decoded = crypto.base64_decode(encoded);
say(decoded); // Hello, World!
```

### Hash Functions

#### `crypto.sha256(data)`

Computes the SHA-256 hash of a string.

**Parameters:**
- `data` (string): The string to hash

**Returns:** Hexadecimal string representation of the SHA-256 hash

**Example:**
```js
use crypto;

var hash = crypto.sha256("Hello, World!");
say(hash); // a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
```

**Note:** SHA-256 is cryptographically secure and suitable for security applications.

#### `crypto.sha1(data)`

Computes the SHA-1 hash of a string.

**Parameters:**
- `data` (string): The string to hash

**Returns:** Hexadecimal string (40 chars)

> ⚠️ SHA-1 is cryptographically broken. Use only for legacy compatibility (e.g. Git object IDs). Prefer `sha256` or `sha512` for new code.

**Example:**
```js
use crypto;
say(crypto.sha1("hello")); // aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
```

#### `crypto.sha512(data)`

Computes the SHA-512 hash of a string.

**Parameters:**
- `data` (string): The string to hash

**Returns:** Hexadecimal string (128 chars)

**Example:**
```js
use crypto;
say(crypto.sha512("hello"));
```

#### `crypto.md5(data)` ⚠️ **DEPRECATED**

**This function throws an error and is not implemented due to security vulnerabilities in MD5.**

Use `crypto.sha256()` instead for secure hashing.

### Random Generation

#### `crypto.random_bytes(length)`

Generates cryptographically secure random bytes.

**Parameters:**
- `length` (number): Number of bytes to generate (1-1048576)

**Returns:** Hexadecimal string representation of the random bytes

**Example:**
```js
use crypto;

var randomHex = crypto.random_bytes(16);
say(randomHex); // e.g., "a1b2c3d4e5f6789012345678901234ab"
```

**Security:** Uses platform-specific secure random number generators:
- Windows: `CryptGenRandom`
- Unix/Linux/macOS: `/dev/urandom`

#### `crypto.random_string(length, charset?)`

Generates a random string using the specified character set.

**Parameters:**
- `length` (number): Length of the string to generate (1-1024)
- `charset` (string, optional): Characters to use. Default: `"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"`

**Returns:** Random string

**Example:**
```js
use crypto;

// Default charset (alphanumeric)
var password = crypto.random_string(12);
say(password); // e.g., "aB3xY9mN2kL8"

// Custom charset (numbers only)
var pin = crypto.random_string(4, "0123456789");
say(pin); // e.g., "7392"

// Custom charset (hex)
var hexId = crypto.random_string(8, "0123456789ABCDEF");
say(hexId); // e.g., "A1B2C3D4"
```

### Hex Encoding

#### `crypto.hex_encode(data)`

Encodes a string to hexadecimal format.

### HMAC

#### `crypto.hmac_sha256(key, message)`

Computes HMAC-SHA256 — a message authentication code using SHA-256.

**Parameters:**
- `key` (string): The secret key
- `message` (string): The message to authenticate

**Returns:** Hexadecimal string (64 chars)

**Example:**
```js
use crypto;

var mac = crypto.hmac_sha256("my-secret-key", "important data");
say(mac);

// Verify a webhook signature
fun verify_webhook(payload, signature, secret) {
    var expected = crypto.hmac_sha256(secret, payload);
    return crypto.constant_time_compare(expected, signature);
}
```

### Key Derivation

#### `crypto.pbkdf2(password, salt, iterations?, keylen?)`

Derives a cryptographic key from a password using PBKDF2-HMAC-SHA256.

**Parameters:**
- `password` (string): The password to derive from
- `salt` (string): A unique salt (use `crypto.random_bytes(16)` to generate)
- `iterations` (number, optional): Number of iterations. Default: `100000`
- `keylen` (number, optional): Output key length in bytes (1–64). Default: `32`

**Returns:** Hexadecimal string

**Example:**
```js
use crypto;

var salt = crypto.random_bytes(16);
var hash = crypto.pbkdf2("user_password", salt, 100000, 32);
say("Stored hash: " + hash);
say("Salt: " + salt);
```

### Utilities

#### `crypto.constant_time_compare(a, b)`

Compares two strings in constant time to prevent timing attacks.

**Parameters:**
- `a` (string): First string
- `b` (string): Second string

**Returns:** `true` if equal, `false` otherwise

**Example:**
```js
use crypto;

// Safe token comparison — won't leak timing info
var stored = crypto.hmac_sha256("secret", "token");
var provided = "...";
if (crypto.constant_time_compare(stored, provided)) {
    say("Valid token");
}
```

#### `crypto.uuid_v4()`

Generates a random UUID v4 (RFC 4122).

**Returns:** UUID string in the format `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`

**Example:**
```js
use crypto;

var id = crypto.uuid_v4();
say(id); // e.g. "f6a31913-cc6a-43f9-a3a9-a30f8c4714f5"
```

### Simple Ciphers
- `data` (string): The string to encode

**Returns:** Hexadecimal string (lowercase)

**Example:**
```js
use crypto;

var hex = crypto.hex_encode("Hello");
say(hex); // 48656c6c6f
```

#### `crypto.hex_decode(hex)`

Decodes a hexadecimal string.

**Parameters:**
- `hex` (string): The hexadecimal string to decode (case-insensitive)

**Returns:** Decoded string

**Throws:** Error if the input is not valid hexadecimal

**Example:**
```js
use crypto;

var decoded = crypto.hex_decode("48656c6c6f");
say(decoded); // Hello
```

### Simple Ciphers

#### `crypto.xor_cipher(data, key)`

Applies XOR cipher encryption/decryption.

**Parameters:**
- `data` (string): The data to encrypt or decrypt
- `key` (string): The encryption key

**Returns:** Encrypted/decrypted string

**Example:**
```js
use crypto;

var plaintext = "Secret message";
var key = "mykey";

// Encrypt
var encrypted = crypto.xor_cipher(plaintext, key);
say("Encrypted: " + crypto.hex_encode(encrypted));

// Decrypt (XOR is symmetric)
var decrypted = crypto.xor_cipher(encrypted, key);
say("Decrypted: " + decrypted); // Secret message
```

**Security Note:** XOR cipher is provided for educational purposes and simple obfuscation. It is **not cryptographically secure** and should not be used for protecting sensitive data.

## Security Considerations

### Secure Functions
- `crypto.sha256()` - Cryptographically secure hash function
- `crypto.random_bytes()` - Cryptographically secure random generation
- `crypto.random_string()` - Uses secure random generation

### Educational/Utility Functions
- `crypto.xor_cipher()` - Simple cipher for learning/obfuscation only
- `crypto.base64_encode/decode()` - Encoding, not encryption
- `crypto.hex_encode/decode()` - Encoding, not encryption

### Best Practices

1. **Use SHA-256 for hashing** - Avoid MD5 and SHA-1
2. **Use secure random generation** - Always use `crypto.random_bytes()` or `crypto.random_string()` for security-critical randomness
3. **Don't use XOR for security** - XOR cipher is for educational purposes only
4. **Validate inputs** - Always validate and sanitize cryptographic inputs
5. **Key management** - Store encryption keys securely, never hardcode them

## Cross-Platform Compatibility

The crypto module is designed to work across all supported platforms:

- **Windows**: Uses Windows Crypto API (`CryptGenRandom`)
- **Linux/Unix**: Uses `/dev/urandom` for secure random generation
- **macOS**: Uses `/dev/urandom` for secure random generation

All hash functions and encoding utilities work identically across platforms.

## Error Handling

The crypto module throws descriptive errors for invalid inputs:

```js
use crypto;

try {
    crypto.base64_decode("invalid base64!");
} catch (e) {
    say("Error: " + e); // Error: Invalid base64 string
}

try {
    crypto.random_bytes(-1);
} catch (e) {
    say("Error: " + e); // Error: Length must be between 1 and 1048576 bytes.
}
```

## Examples

### Password Generation
```js
use crypto;

// Generate a secure password
var password = crypto.random_string(16, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*");
say("Generated password: " + password);
```

### Data Integrity Check
```js
use crypto;

var data = "Important data that must not be tampered with";
var hash = crypto.sha256(data);
say("Data hash: " + hash);

// Later, verify integrity
var newHash = crypto.sha256(data);
if (hash == newHash) {
    say("Data integrity verified");
} else {
    say("Data has been tampered with!");
}
```

### API Token Generation
```js
use crypto;

// Generate a secure API token
var tokenBytes = crypto.random_bytes(32);
var token = crypto.base64_encode(crypto.hex_decode(tokenBytes));
say("API Token: " + token);
```

### Simple Data Obfuscation
```js
use crypto;

var sensitiveData = "user:password:email@example.com";
var obfuscationKey = crypto.random_string(16);

// Obfuscate
var obfuscated = crypto.xor_cipher(sensitiveData, obfuscationKey);
var obfuscatedHex = crypto.hex_encode(obfuscated);

say("Obfuscated: " + obfuscatedHex);
say("Key: " + obfuscationKey);

// De-obfuscate
var deobfuscated = crypto.xor_cipher(crypto.hex_decode(obfuscatedHex), obfuscationKey);
say("Original: " + deobfuscated);
```