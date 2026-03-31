# Strings Module Documentation

The `strings` module provides string manipulation utilities that complement Neutron's built-in string operators.

## Usage

```neutron
use strings;

var parts = strings.split("a,b,c", ",");  // ["a", "b", "c"]
var upper = strings.upper("hello");        // "HELLO"
var trimmed = strings.trim("  hi  ");      // "hi"
```

## Functions

### Splitting & Joining

#### `strings.split(str, delim?)`
Splits `str` by `delim` (default `" "`). If `delim` is `""`, splits into individual characters.

```neutron
strings.split("a,b,c", ",");   // ["a", "b", "c"]
strings.split("hello", "");    // ["h","e","l","l","o"]
strings.split("a b c");        // ["a", "b", "c"]
```

#### `strings.join(array, delim?)`
Joins array elements into a string. Default delimiter is `""`.

```neutron
strings.join(["a", "b", "c"], ", ");  // "a, b, c"
strings.join(["x", "y"]);             // "xy"
```

---

### Case

#### `strings.upper(str)` / `strings.lower(str)`
```neutron
strings.upper("hello");  // "HELLO"
strings.lower("WORLD");  // "world"
```

---

### Trimming

#### `strings.trim(str)`
Removes leading and trailing whitespace (`space`, `\t`, `\r`, `\n`).

#### `strings.trim_left(str)` / `strings.trim_right(str)`
One-sided trim.

```neutron
strings.trim("  hi  ");        // "hi"
strings.trim_left("  hi  ");   // "hi  "
strings.trim_right("  hi  ");  // "  hi"
```

---

### Searching

#### `strings.contains(str, substr)` → bool
#### `strings.starts_with(str, prefix)` → bool
#### `strings.ends_with(str, suffix)` → bool

```neutron
strings.contains("hello world", "world");   // true
strings.starts_with("hello", "hel");        // true
strings.ends_with("hello", "llo");          // true
```

#### `strings.index_of(str, substr, start?)` → number
Returns the index of the first occurrence, or `-1` if not found. Optional `start` offset.

#### `strings.last_index_of(str, substr)` → number
Returns the index of the last occurrence, or `-1`.

```neutron
strings.index_of("abcabc", "bc");     // 1
strings.last_index_of("abcabc", "bc"); // 4
strings.index_of("hello", "x");       // -1
```

---

### Replacing

#### `strings.replace(str, from, to)` → string
Replaces all occurrences of `from` with `to`.

#### `strings.replace_first(str, from, to)` → string
Replaces only the first occurrence.

```neutron
strings.replace("aabbaa", "a", "x");        // "xxbbxx"
strings.replace_first("aabbaa", "a", "x");  // "xabbaa"
```

---

### Slicing

#### `strings.substring(str, start, end?)` → string
Returns characters from `start` (inclusive) to `end` (exclusive). Defaults to end of string.

```neutron
strings.substring("hello", 1, 3);  // "el"
strings.substring("hello", 2);     // "llo"
```

---

### Utility

#### `strings.length(str)` → number
Returns byte length of the string.

#### `strings.count(str, substr)` → number
Counts non-overlapping occurrences of `substr`.

```neutron
strings.count("banana", "an");  // 2
```

#### `strings.repeat(str, n)` → string
```neutron
strings.repeat("ab", 3);  // "ababab"
```

#### `strings.reverse(str)` → string
```neutron
strings.reverse("hello");  // "olleh"
```

---

### Character Operations

#### `strings.char_at(str, index)` → string
Returns the character at `index` as a single-character string.

#### `strings.char_code(str, index?)` → number
Returns the ASCII code of the character at `index` (default 0).

#### `strings.from_char_code(code)` → string
Returns a single-character string for the given ASCII code (0–127).

```neutron
strings.char_at("hello", 1);      // "e"
strings.char_code("A");           // 65
strings.from_char_code(65);       // "A"
```

---

### Type Checks

#### `strings.is_empty(str)` → bool
#### `strings.is_alpha(str)` → bool — all alphabetic characters
#### `strings.is_digit(str)` → bool — all digit characters
#### `strings.is_alnum(str)` → bool — all alphanumeric characters

```neutron
strings.is_empty("");       // true
strings.is_digit("123");    // true
strings.is_alpha("abc");    // true
strings.is_alnum("abc123"); // true
```

---

## Examples

```neutron
use strings;

// CSV row parser
fun parse_csv(line) {
    return strings.split(line, ",");
}

// Title case
fun title_case(s) {
    var words = strings.split(s, " ");
    var i = 0;
    while (i < words.length) {
        var w = words[i];
        if (w.length > 0) {
            words[i] = strings.upper(strings.substring(w, 0, 1))
                     + strings.lower(strings.substring(w, 1));
        }
        i = i + 1;
    }
    return strings.join(words, " ");
}

// Slug generator
fun slugify(s) {
    return strings.replace(strings.lower(strings.trim(s)), " ", "-");
}
```
