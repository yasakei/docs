# Process Module

The `process` module provides Erlang-style lightweight processes with message passing for concurrent and parallel programming in Neutron. It enables true multi-core parallelism using an actor-model approach.

## Importing the Module

```neutron
use process;
```

## Overview

The process module implements:
- **Lightweight processes** - Each process runs in its own thread
- **Message passing** - Processes communicate via asynchronous messages
- **Actor model** - Isolated processes with no shared state
- **Work-stealing scheduler** - Efficient distribution across CPU cores

## Functions

### `process.spawn(function)`

Creates a new process that executes the given function. The process runs in parallel with the main program.

**Parameters:**
- `function` - The function to execute in the new process

**Returns:**
- `number` - The process ID (PID) of the spawned process

**Example:**
```neutron
use process;

fun worker() {
    say("Hello from worker!");
    return 42;
}

var pid = process.spawn(worker);
say("Spawned process with PID: " + pid);
```

### `process.send(pid, message)`

Sends a message to a process. Messages are queued in the process's mailbox.

**Parameters:**
- `pid` - The process ID to send the message to
- `message` - Any value to send (number, string, array, etc.)

**Returns:**
- `boolean` - `true` if the message was delivered, `false` if the process doesn't exist

**Example:**
```neutron
use process;

fun worker() {
    var msg = process.receive();
    say("Received: " + msg);
}

var pid = process.spawn(worker);
process.send(pid, "Hello, worker!");
```

### `process.receive()`

Receives a message from the current process's mailbox. Blocks until a message arrives.

**Parameters:**
- None (or optional timeout in milliseconds)

**Returns:**
- The received message value

**Example:**
```neutron
use process;

fun echo_worker() {
    var msg = process.receive();
    say("Echo: " + msg);
    return msg;
}

var pid = process.spawn(echo_worker);
process.send(pid, "ping");
```

### `process.self()`

Returns the PID of the current process.

**Parameters:**
- None

**Returns:**
- `number` - The current process ID (0 for the main process)

**Example:**
```neutron
use process;

fun worker() {
    var my_pid = process.self();
    say("I am process " + my_pid);
}

var pid = process.spawn(worker);
say("Main process PID: " + process.self());
```

### `process.is_alive(pid)`

Checks if a process is still running.

**Parameters:**
- `pid` - The process ID to check

**Returns:**
- `boolean` - `true` if the process is alive, `false` otherwise

**Example:**
```neutron
use process;

fun short_task() {
    return "done";
}

var pid = process.spawn(short_task);
process.process_sleep(100);
say("Process alive: " + process.is_alive(pid));
```

### `process.kill(pid)`

Terminates a process.

**Parameters:**
- `pid` - The process ID to terminate

**Returns:**
- Nothing

**Example:**
```neutron
use process;

fun long_task() {
    while (true) {
        process.process_sleep(100);
    }
}

var pid = process.spawn(long_task);
process.kill(pid);
say("Process terminated");
```

### `process.process_count()`

Returns the number of active processes.

**Parameters:**
- None

**Returns:**
- `number` - Count of active (non-finished) processes

**Example:**
```neutron
use process;

fun worker() {
    process.process_sleep(1000);
}

process.spawn(worker);
process.spawn(worker);
say("Active processes: " + process.process_count());
```

### `process.process_sleep(milliseconds)`

Pauses the current process for the specified duration.

**Parameters:**
- `milliseconds` - Time to sleep in milliseconds

**Returns:**
- Nothing

**Example:**
```neutron
use process;

say("Sleeping for 1 second...");
process.process_sleep(1000);
say("Awake!");
```

## Patterns

### Worker Pool

```neutron
use process;

fun worker() {
    fun compute(n) {
        if (n < 2) return n;
        return compute(n - 1) + compute(n - 2);
    }
    
    var n = process.receive();
    return compute(n);
}

// Spawn multiple workers
var w1 = process.spawn(worker);
var w2 = process.spawn(worker);
var w3 = process.spawn(worker);
var w4 = process.spawn(worker);

// Distribute work
process.send(w1, 30);
process.send(w2, 30);
process.send(w3, 30);
process.send(w4, 30);

// Wait for completion
while (process.process_count() > 0) {
    process.process_sleep(10);
}
say("All workers completed!");
```

### Producer-Consumer

```neutron
use process;

fun consumer() {
    while (true) {
        var item = process.receive();
        if (item == "stop") {
            return;
        }
        say("Processing: " + item);
    }
}

var consumer_pid = process.spawn(consumer);

// Produce items
for (var i = 0; i < 5; i = i + 1) {
    process.send(consumer_pid, "item_" + i);
}
process.send(consumer_pid, "stop");
```

## Important Notes

1. **Isolated Processes**: Each process runs in its own VM instance. Functions defined in the parent scope are NOT accessible. Define all needed functions inside the worker.

2. **Self-Contained Workers**: Worker functions should be self-contained:
   ```neutron
   // GOOD - function defined inside worker
   fun worker() {
       fun helper(x) { return x * 2; }
       var msg = process.receive();
       return helper(msg);
   }
   
   // BAD - won't work, helper is not visible
   fun helper(x) { return x * 2; }
   fun worker() {
       var msg = process.receive();
       return helper(msg);  // Error!
   }
   ```

3. **Message Types**: Any Neutron value can be sent as a message: numbers, strings, arrays, objects.

4. **Thread Pool**: The scheduler automatically manages a pool of worker threads based on available CPU cores.

## Performance

The process module enables true parallel execution. On a 4-core machine:

| Workload | Sequential | Parallel (4 workers) | Speedup |
|----------|------------|---------------------|---------|
| 4× fib(30) | ~3400ms | ~1100ms | ~3.1x |

Near-linear scaling up to the number of CPU cores.
