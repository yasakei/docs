# Path Module

The `path` module provides utilities for working with file and directory paths in a cross-platform manner. It handles the differences between Windows and Unix-style paths automatically.

## Import

```js
use path;
```

## Functions

### Core Path Operations

#### `path.join(...paths)`

Joins path segments using the platform-appropriate separator.

**Parameters:**
- `...paths` (strings): Path segments to join

**Returns:** Joined path string

**Example:**
```js
use path;

var fullPath = path.join("home", "user", "documents", "file.txt");
say(fullPath); // "home/user/documents/file.txt" on Unix
               // "home\user\documents\file.txt" on Windows

// Absolute paths override previous segments
var absolutePath = path.join("home", "/usr", "local");
say(absolutePath); // "/usr/local"
```

#### `path.split(path)`

Splits a path into directory and filename components.

**Parameters:**
- `path` (string): Path to split

**Returns:** Array with two elements: `[directory, filename]`

**Example:**
```js
use path;

var parts = path.split("/home/user/document.txt");
say(parts[0]); // "/home/user"
say(parts[1]); // "document.txt"

var parts2 = path.split("file.txt");
say(parts2[0]); // ""
say(parts2[1]); // "file.txt"
```

#### `path.dirname(path)`

Returns the directory portion of a path.

**Parameters:**
- `path` (string): Path to analyze

**Returns:** Directory portion of the path

**Example:**
```js
use path;

say(path.dirname("/home/user/file.txt")); // "/home/user"
say(path.dirname("file.txt"));            // "."
say(path.dirname("/file.txt"));           // "/"
```

#### `path.basename(path)`

Returns the filename portion of a path.

**Parameters:**
- `path` (string): Path to analyze

**Returns:** Filename portion of the path

**Example:**
```js
use path;

say(path.basename("/home/user/file.txt")); // "file.txt"
say(path.basename("/home/user/"));         // ""
say(path.basename("file.txt"));            // "file.txt"
```

#### `path.extname(path)`

Returns the file extension of a path.

**Parameters:**
- `path` (string): Path to analyze

**Returns:** File extension including the dot, or empty string if no extension

**Example:**
```js
use path;

say(path.extname("file.txt"));        // ".txt"
say(path.extname("file.tar.gz"));     // ".gz"
say(path.extname("file"));            // ""
say(path.extname(".hidden"));         // ""
say(path.extname("/path/file.txt"));  // ".txt"
```

### Path Analysis

#### `path.isabs(path)`

Checks if a path is absolute.

**Parameters:**
- `path` (string): Path to check

**Returns:** `true` if the path is absolute, `false` otherwise

**Example:**
```js
use path;

say(path.isabs("/home/user"));    // true (Unix)
say(path.isabs("C:\\Users"));     // true (Windows)
say(path.isabs("relative/path")); // false
say(path.isabs("./current"));     // false
```

#### `path.normalize(path)`

Normalizes a path by resolving `.` and `..` segments.

**Parameters:**
- `path` (string): Path to normalize

**Returns:** Normalized path

**Example:**
```js
use path;

say(path.normalize("/home/user/../user/./file")); // "/home/user/file"
say(path.normalize("./file"));                    // "file"
say(path.normalize("home/../file"));              // "file"
say(path.normalize(""));                          // "."
```

#### `path.resolve(path)`

Converts a path to an absolute path.

**Parameters:**
- `path` (string): Path to resolve

**Returns:** Absolute path

**Example:**
```js
use path;

// If current directory is /home/user
say(path.resolve("documents"));        // "/home/user/documents"
say(path.resolve("/absolute/path"));   // "/absolute/path"
say(path.resolve("../parent"));        // "/home/parent"
```

#### `path.relative(from, to)`

Returns the relative path from one location to another.

**Parameters:**
- `from` (string): Starting path
- `to` (string): Target path

**Returns:** Relative path from `from` to `to`

**Example:**
```js
use path;

say(path.relative("/home/user", "/home/user/documents")); // "documents"
say(path.relative("/home/user/docs", "/home/user"));      // ".."
say(path.relative("/home/user", "/home/user"));           // "."
```

### Platform Constants

#### `path.sep`

The platform-specific path segment separator.

**Value:** 
- `"/"` on Unix/Linux/macOS
- `"\\"` on Windows

**Example:**
```js
use path;

say("Path separator: " + path.sep);
var manualPath = "home" + path.sep + "user" + path.sep + "file.txt";
```

#### `path.delimiter`

The platform-specific path delimiter used in environment variables like PATH.

**Value:**
- `":"` on Unix/Linux/macOS  
- `";"` on Windows

**Example:**
```js
use path;

say("Path delimiter: " + path.delimiter);
// For parsing PATH environment variable
var paths = pathEnvVar.split(path.delimiter);
```

### Cross-Platform Utilities

#### `path.toUnix(path)`

Converts a path to Unix-style (forward slashes).

**Parameters:**
- `path` (string): Path to convert

**Returns:** Path with forward slashes

**Example:**
```js
use path;

say(path.toUnix("home\\user\\file")); // "home/user/file"
say(path.toUnix("home/user/file"));   // "home/user/file" (unchanged)
```

#### `path.toWindows(path)`

Converts a path to Windows-style (backslashes).

**Parameters:**
- `path` (string): Path to convert

**Returns:** Path with backslashes

**Example:**
```js
use path;

say(path.toWindows("home/user/file"));   // "home\\user\\file"
say(path.toWindows("home\\user\\file")); // "home\\user\\file" (unchanged)
```

## Cross-Platform Considerations

The path module automatically handles platform differences:

### Path Separators
- **Unix/Linux/macOS**: Uses `/` as the path separator
- **Windows**: Uses `\` as the path separator, but also accepts `/`

### Absolute Paths
- **Unix/Linux/macOS**: Paths starting with `/` (e.g., `/home/user`)
- **Windows**: Paths starting with drive letter (e.g., `C:\Users`) or UNC paths (e.g., `\\server\share`)

### Best Practices

1. **Always use `path.join()`** instead of manual string concatenation:
   ```js
   // Good
   var fullPath = path.join(baseDir, "subdir", "file.txt");
   
   // Bad - won't work on all platforms
   var fullPath = baseDir + "/" + "subdir" + "/" + "file.txt";
   ```

2. **Use `path.normalize()`** to clean up paths:
   ```js
   var cleanPath = path.normalize(userInputPath);
   ```

3. **Use `path.resolve()`** to convert relative paths to absolute:
   ```js
   var absolutePath = path.resolve(relativePath);
   ```

4. **Check if paths are absolute** before processing:
   ```js
   if (!path.isabs(inputPath)) {
       inputPath = path.resolve(inputPath);
   }
   ```

## Error Handling

The path module throws descriptive errors for invalid inputs:

```js
use path;

try {
    path.join("valid", 123); // Invalid argument type
} catch (e) {
    say("Error: " + e); // "All arguments to path.join() must be strings."
}

try {
    path.split(null); // Invalid argument type
} catch (e) {
    say("Error: " + e); // "Argument for path.split() must be a string."
}
```

## Examples

### File Path Manipulation
```js
use path;

var filePath = "/home/user/documents/report.pdf";

say("Directory: " + path.dirname(filePath));  // "/home/user/documents"
say("Filename: " + path.basename(filePath));  // "report.pdf"
say("Extension: " + path.extname(filePath));  // ".pdf"

// Change extension
var nameWithoutExt = path.basename(filePath, path.extname(filePath));
var newPath = path.join(path.dirname(filePath), nameWithoutExt + ".txt");
say("New path: " + newPath); // "/home/user/documents/report.txt"
```

### Building Configuration Paths
```js
use path;

var configDir = path.join(homeDir, ".myapp");
var configFile = path.join(configDir, "config.json");
var logFile = path.join(configDir, "logs", "app.log");

say("Config directory: " + configDir);
say("Config file: " + configFile);
say("Log file: " + logFile);
```

### Cross-Platform Path Handling
```js
use path;

// Works on both Windows and Unix
var projectPath = path.join("projects", "myapp", "src", "main.nt");
var absoluteProject = path.resolve(projectPath);

say("Project path: " + projectPath);
say("Absolute path: " + absoluteProject);
say("Is absolute: " + path.isabs(absoluteProject));
```

### Relative Path Calculations
```js
use path;

var sourceDir = "/home/user/project/src";
var testDir = "/home/user/project/tests";
var libFile = "/home/user/project/lib/utils.nt";

// Calculate relative paths for imports
var testToSrc = path.relative(testDir, sourceDir);
var srcToLib = path.relative(sourceDir, libFile);

say("From tests to src: " + testToSrc);    // "../src"
say("From src to lib: " + srcToLib);       // "../lib/utils.nt"
```