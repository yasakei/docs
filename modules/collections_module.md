# Collections Module Documentation

The `collections` module provides set, stack, and queue data structures built on top of Neutron arrays.

## Usage

```neutron
use collections;

var s = collections.set_new();
collections.set_add(s, "apple");
collections.set_add(s, "banana");
collections.set_add(s, "apple"); // ignored — already present
say(collections.set_size(s));    // 2
```

## Set

A set is an unordered collection of unique values. Equality is checked by value (numbers, strings, bools, nil).

### `collections.set_new()` → array
Creates an empty set.

### `collections.set_add(set, value)` → bool
Adds `value` to the set. Returns `true` if added, `false` if already present.

### `collections.set_has(set, value)` → bool
Returns `true` if `value` is in the set.

### `collections.set_remove(set, value)` → bool
Removes `value`. Returns `true` if it was present.

### `collections.set_size(set)` → number
Returns the number of elements.

### `collections.set_to_array(set)` → array
Returns a copy of the set as a plain array.

### `collections.set_union(a, b)` → array
Returns a new set containing all elements from both `a` and `b`.

### `collections.set_intersection(a, b)` → array
Returns a new set with only elements present in both.

### `collections.set_difference(a, b)` → array
Returns a new set with elements in `a` that are not in `b`.

```neutron
use collections;

var a = collections.set_new();
collections.set_add(a, 1);
collections.set_add(a, 2);
collections.set_add(a, 3);

var b = collections.set_new();
collections.set_add(b, 2);
collections.set_add(b, 3);
collections.set_add(b, 4);

var u = collections.set_union(a, b);        // {1,2,3,4}
var i = collections.set_intersection(a, b); // {2,3}
var d = collections.set_difference(a, b);   // {1}
```

---

## Stack

LIFO (last-in, first-out) structure.

### `collections.stack_new()` → array
Creates an empty stack.

### `collections.stack_push(stack, value)`
Pushes a value onto the top.

### `collections.stack_pop(stack)` → value
Removes and returns the top value. Throws if empty.

### `collections.stack_peek(stack)` → value
Returns the top value without removing it. Throws if empty.

### `collections.stack_size(stack)` → number
### `collections.stack_is_empty(stack)` → bool

```neutron
use collections;

var st = collections.stack_new();
collections.stack_push(st, 1);
collections.stack_push(st, 2);
collections.stack_push(st, 3);

say(collections.stack_peek(st));  // 3
say(collections.stack_pop(st));   // 3
say(collections.stack_size(st));  // 2
```

### Example: balanced parentheses checker
```neutron
use collections;

fun is_balanced(s) {
    var st = collections.stack_new();
    var i = 0;
    while (i < s.length) {
        var c = s[i];
        if (c == "(") {
            collections.stack_push(st, c);
        } else if (c == ")") {
            if (collections.stack_is_empty(st)) { return false; }
            collections.stack_pop(st);
        }
        i = i + 1;
    }
    return collections.stack_is_empty(st);
}
```

---

## Queue

FIFO (first-in, first-out) structure.

### `collections.queue_new()` → array
Creates an empty queue.

### `collections.queue_enqueue(queue, value)`
Adds a value to the back.

### `collections.queue_dequeue(queue)` → value
Removes and returns the front value. Throws if empty.

### `collections.queue_peek(queue)` → value
Returns the front value without removing it. Throws if empty.

### `collections.queue_size(queue)` → number
### `collections.queue_is_empty(queue)` → bool

```neutron
use collections;

var q = collections.queue_new();
collections.queue_enqueue(q, "first");
collections.queue_enqueue(q, "second");
collections.queue_enqueue(q, "third");

say(collections.queue_dequeue(q));  // "first"
say(collections.queue_peek(q));     // "second"
say(collections.queue_size(q));     // 2
```

---

## Notes

- All three structures are backed by plain arrays, so you can pass them to `arrays.*` functions too.
- Set equality works for `number`, `string`, `bool`, and `nil`. Objects and arrays are compared by reference (always unequal).
