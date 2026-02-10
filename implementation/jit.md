# JIT Compilation in Neutron

Neutron implements a **multi-tier JIT (Just-In-Time) compilation** system based on the research paper *"A Lightweight Method for Generating Multi-Tier JIT Compilation Virtual Machine"*. The JIT compiles frequently executed bytecode ("hot spots") into native machine code for significant performance gains.

**Supported architectures:** x86-64 (Intel/AMD) and ARM64/AArch64 (Apple Silicon, Linux ARM).

## Architecture Overview

The JIT uses a **three-tier execution model**:

```
┌─────────────────────────────────────────────────────────┐
│                  Execution Pipeline                      │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐│
│  │  Interpreter  │──▶│   Tier-1     │──▶│   Tier-2     ││
│  │  (Bytecode)   │   │  (Threaded)  │   │ (Tracing JIT)││
│  └──────────────┘   └──────────────┘   └──────────────┘│
│        ▲                                      │         │
│        │          Guard Failure                │         │
│        └──────────────────────────────────────┘         │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐│
│  │               Hot-Spot Profiler                     ││
│  │  Tracks execution counts per (method, bytecode_pc)  ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

| Tier | Name | Strategy | Compile Speed | Code Quality |
|------|------|----------|---------------|--------------|
| 0 | Interpreter | Bytecode dispatch | N/A | Baseline |
| 1 | Tier-1 | Subroutine-threaded code | Fast | Moderate |
| 2 | Tier-2 | Tracing JIT → native x86-64 / ARM64 | Slower | Aggressive |

## Components

### File Layout

```
include/jit/
├── jit_config.h           # Compilation thresholds, cache sizes, feature flags
├── jit_manager.h          # MultiTierJITManager orchestrator
├── jit_memory.h           # Platform-specific executable memory (mmap/VirtualAlloc)
├── jit_profiler.h         # HotSpotProfiler for detecting hot loops/methods
├── jit_tier1.h            # Tier1Compiler (threaded code generation)
├── jit_tier2.h            # Tier2Compiler (tracing JIT with IR + native codegen)
├── jit_codegen.h          # X86_64CodeGen (raw machine code emitter)
└── jit_codegen_arm64.h    # AArch64CodeGen (ARM64 machine code emitter)

src/jit/
├── jit_manager.cpp        # Tier coordination, compilation requests, statistics
├── jit_memory.cpp         # JIT memory allocation (mmap/MAP_JIT, mprotect, W^X)
├── jit_profiler.cpp       # Execution counting, warmup detection
├── jit_tier1.cpp          # Threaded code compilation and inline caching
├── jit_tier2.cpp          # Trace recording, IR optimization, x86-64 codegen (~1800 lines)
├── jit_tier2_arm64.cpp    # ARM64 native codegen (compiled only on AArch64 targets)
└── jit_codegen.cpp        # x86-64 instruction encoding (REX, ModRM, SSE2)
```

> **Note:** `jit_tier2_arm64.cpp` is guarded by `#if defined(__aarch64__) || defined(__arm64__)` and only compiles on ARM64 targets. The x86-64 codegen in `jit_tier2.cpp` is untouched — both backends share the same IR and optimization pipeline.

---

## Hot-Spot Profiler

**Class:** `HotSpotProfiler` (`jit_profiler.h`)

The profiler detects hot code by counting backward-jump executions (loop iterations) and method invocations.

### How It Works

1. Every backward jump (loop) and method call is recorded via `recordExecution(method_id, bytecode_offset)`.
2. When a location's execution count exceeds a threshold, it is marked "hot" and promoted to the next tier.
3. The profiler tracks **per-method** statistics (call count, total execution time) and **per-location** profiles (execution count, current tier).

### Thresholds

| Parameter | Value | Description |
|-----------|-------|-------------|
| `TIER1_COMPILATION_THRESHOLD` | 50 | Backward jumps to trigger Tier-1 |
| `TIER2_COMPILATION_THRESHOLD` | 50 | Tier-1 executions to trigger Tier-2 |
| `PROFILE_SAMPLE_INTERVAL` | 100 | Profiling sample frequency |
| `MAX_PROFILED_METHODS` | 10,000 | Max tracked methods |
| `MAX_PROFILED_LOOPS` | 5,000 | Max tracked loops |

### Warmup Detection

The profiler tracks a **warmup phase** (first 5 seconds or until Tier-2 compilations begin). During warmup, the JIT gathers type feedback and execution patterns before committing to aggressive optimizations.

---

## Tier-1: Lightweight Threaded Code

**Class:** `Tier1Compiler` (`jit_tier1.h`)

Tier-1 provides a fast first compilation by converting bytecode into **subroutine-threaded code** — a sequence of direct `CALL` instructions to pre-existing bytecode handler functions.

### Compilation Strategy

```
Bytecode:     OP_GET_LOCAL 0 | OP_CONSTANT 1 | OP_ADD | OP_SET_LOCAL 0
                    ↓                ↓             ↓           ↓
Threaded:     MOV RAX, &handler_get_local    MOV RAX, &handler_add
              CALL RAX                       CALL RAX
              MOV RAX, &handler_constant     MOV RAX, &handler_set_local
              CALL RAX                       CALL RAX
```

Each bytecode instruction becomes a `MOV RAX, imm64; CALL RAX` pair that invokes the interpreter's handler function directly, eliminating the dispatch overhead.

### Inline Caching

Tier-1 implements **monomorphic inline caches** for method dispatch:

- Each `OP_CALL` site gets a cache entry storing the expected method ID and handler address.
- On a **cache hit** (same method), dispatch is a direct `CALL` — no lookup needed.
- On a **cache miss**, a dynamic lookup is performed and the cache is updated.
- Hit/miss ratios are tracked per cache entry for profiling.

### Shallow Tracing

Tier-1 uses **shallow tracing** to safely profile both branches of conditionals without side effects. Instructions with side effects (`OP_SET_LOCAL`, `OP_SET_GLOBAL`, `OP_CALL`, `OP_THROW`) are wrapped in a `we_are_jitted()` guard that skips execution during trace recording, preventing state corruption.

### Code Cache

| Parameter | Value |
|-----------|-------|
| `TIER1_CODE_CACHE_SIZE` | 10 MB |
| `TIER1_FUNCTION_CACHE_CAPACITY` | 1,000 functions |

---

## Tier-2: Tracing JIT Compiler

**Class:** `Tier2Compiler` (`jit_tier2.h`)

Tier-2 is the aggressive optimizing compiler. It records **execution traces** (linear sequences of actually-executed instructions through a loop) and compiles them to optimized native x86-64 machine code.

### Compilation Pipeline

```
Bytecode → recordTrace() → IR (intermediate representation)
                                    ↓
                            optimizeTrace()
                              • Type specialization (guards)
                              • Loop unrolling
                              • Constant folding
                              • Dead code elimination
                              • Common subexpression elimination
                              • Store-load forwarding
                                    ↓
                            compileTrace() → Native x86-64
                                    ↓
                            executeTrace() → Direct execution
```

### Phase 1: Trace Recording

`recordTrace()` walks through bytecode starting at a loop entry point and records all instructions until hitting an `OP_LOOP` (backward jump) or `OP_RETURN`. This captures the **hot path** through the loop body.

- Nested control flow (jumps, conditionals) is tracked via depth counting.
- The trace is bounded by `MAX_TRACE_LENGTH` (5,000 instructions).

### Phase 2: Bytecode → IR Conversion

`convertToIR()` translates bytecode instructions into a typed intermediate representation. Key translations:

| Bytecode | IR Instruction | Notes |
|----------|----------------|-------|
| `OP_GET_LOCAL` / `OP_LOAD_LOCAL_0..3` | `LOAD_LOCAL` | Slot number in `operand1` |
| `OP_SET_LOCAL` | `STORE_LOCAL` | |
| `OP_GET_GLOBAL` | `LOAD_GLOBAL` | Resolved to direct `Value*` pointer at IR-build time |
| `OP_SET_GLOBAL` | `STORE_GLOBAL` | Also resolved to `Value*` |
| `OP_CONSTANT` / `OP_CONST_INT8` / `OP_CONST_ZERO` / `OP_CONST_ONE` | `LOAD_CONST` | Value pointer stored in `data` field |
| `OP_ADD` / `OP_ADD_INT` | `ADD` | Both generic and specialized map to same IR |
| `OP_LESS_JUMP` | `LESS` + `JUMP_IF_FALSE` | Fused opcodes are expanded |
| `OP_INC_LOCAL_INT` | `LOAD_LOCAL` + `LOAD_CONST(1)` + `ADD` + `STORE_LOCAL` | Super-instructions are expanded |
| `OP_INCREMENT_LOCAL` | Same 4-op expansion | |
| `OP_LOOP` | `LOOP_BACK` | Marks end of trace |

**Global variable resolution:** At IR-build time, `OP_GET_GLOBAL` and `OP_SET_GLOBAL` look up the global variable name in the VM's globals map and store a **direct `Value*` pointer** in the IR instruction's `data` field. This eliminates hash-map lookups at runtime — the JIT-compiled code reads/writes the `Value` struct directly via its memory address.

### Phase 3: Optimization Passes

Optimizations are applied in order of impact:

#### 1. Type Specialization (Guards)
Inserts `GUARD_TYPE` instructions at trace entry to verify runtime types match the profiled types. If a guard fails at runtime, execution falls back to the interpreter.

#### 2. Loop Unrolling
For very hot loops (execution count > `2 × TIER2_COMPILATION_THRESHOLD`), the loop body is duplicated `N` times with `UNROLL_MARKER` separators. The final `LOOP_BACK` jumps to the beginning of the unrolled body.

#### 3. Constant Folding & Dead Code Elimination
- `UNROLL_MARKER` instructions are stripped.
- Consecutive `LOAD_CONST` pairs are candidates for folding.

#### 4. Common Subexpression Elimination (CSE)
Instructions are hashed by `(opcode, operand1, operand2)`. Duplicate pure computations (`ADD`, `MULTIPLY`, `EQUAL`, `LESS`) are identified for potential reuse.

#### 5. Store-Load Forwarding
The pattern `STORE(X) / POP / LOAD(X)` is optimized by eliminating the `POP` and `LOAD` — the stored value remains available from the prior `STORE`.

### Phase 4: Native Code Generation

`compileTrace()` generates x86-64 machine code from the optimized IR. The generated code follows the **System V AMD64 ABI**.

#### Validation

Before compilation, the trace is validated:
- Only numeric operations are supported (non-numeric constants → bail out)
- Nested loops are rejected (single `LOOP_BACK` only)
- Unresolved globals → bail out
- Failed traces are recorded to avoid retrying

#### Register Allocation

**x86-64:**

```
RBP     = ExecutionFrame* (preserved across loop)
RBX     = Value* locals   (base pointer for local variable access)
R12-R15 = Cached global Value* addresses (top 4 most-accessed globals)
RAX     = Scratch register / integer cache for bitwise ops
RCX     = Second scratch for bitwise operand B
RDX     = Scratch for constants (avoids clobbering RAX integer cache)
XMM0-14 = Operand stack (max 15 slots, doubles in SSE2)
XMM15   = Scratch register for modulo and negation
```

**ARM64 (AArch64):**

```
X20     = ExecutionFrame* (callee-saved, = RBP on x86-64)
X19     = Value* locals   (callee-saved, = RBX on x86-64)
X21-X24 = Cached global Value* addresses (callee-saved, = R12-R15 on x86-64)
X9      = Scratch / integer cache for bitwise ops (= RAX on x86-64)
X1      = Temp for bitwise operand B and constant loading (= RCX on x86-64)
X0      = First argument (ExecutionFrame*), also temp
D0-D14  = Operand stack (D8-D14 are callee-saved, saved/restored in prologue/epilogue)
D15     = Scratch FP register (= XMM15 on x86-64)
```

**Global Register Caching:** The compiler analyzes all `LOAD_GLOBAL`/`STORE_GLOBAL` instructions in the trace, counts access frequency, and assigns the top 4 most-accessed global variables to callee-saved registers (R12–R15 on x86-64, X21–X24 on ARM64). This eliminates the `MOV RAX, imm64` (10 bytes on x86-64) or `MOVZ+MOVK` sequence (up to 16 bytes on ARM64) for every access of these hot global variables.

**Integer Register Cache:** For bitwise operation chains (`AND`, `OR`, `XOR`, `SHIFT`), the compiler tracks whether the integer scratch register (RAX on x86-64, X9 on ARM64) already holds the `int64` conversion of an operand-stack register. Consecutive bitwise operations skip the redundant `CVTTSD2SI` (x86-64) or `FCVTZS` (ARM64) conversion.

#### Code Shape

The generated native code has this structure:

<details>
<summary><b>x86-64</b></summary>

```asm
; ──── PROLOGUE ────
push rbx, rbp, r12, r13, r14, r15     ; save callee-saved
mov  rbp, rdi                          ; RBP = ExecutionFrame*
mov  rbx, [rbp+32]                     ; RBX = local_variables ptr
mov  r12, <global_addr_1>              ; cache hot globals
mov  r13, <global_addr_2>
...

; ──── LOOP START ────
loop_top:
    movsd  xmm0, [rbx + slot*16 + 8]  ; LOAD_LOCAL → SSE2 load
    movsd  xmm1, [rbx + slot*16 + 8]  ; LOAD_LOCAL
    ucomisd xmm0, xmm1                ; LESS comparison
    jae    exit_stub                   ; if not less, exit loop
    
    addsd  xmm2, xmm3                 ; ADD → SSE2 add
    movsd  [rbx + slot*16 + 8], xmm2  ; STORE_LOCAL → SSE2 store
    movsd  [r12 + 8], xmm4            ; STORE_GLOBAL via cached register
    
    jmp    loop_top                    ; LOOP_BACK

; ──── EXIT STUB ────
exit_stub:
    ; locals already synced (STORE_LOCAL writes to memory every iteration)
    pop  r15, r14, r13, r12, rbp, rbx ; restore callee-saved
    ret
```

</details>

<details>
<summary><b>ARM64 (AArch64)</b></summary>

```asm
; ──── PROLOGUE ────
stp  x30, x19, [sp, #-48]!           ; save LR + callee-saved GP regs
stp  x20, x21, [sp, #16]
stp  x22, x23, [sp, #32]
stp  d8,  d9,  [sp, #-56]!           ; save callee-saved FP regs (D8-D14)
stp  d10, d11, [sp, #16]
stp  d12, d13, [sp, #32]
str  d14,      [sp, #48]
mov  x20, x0                          ; X20 = ExecutionFrame*
ldr  x19, [x20, #32]                  ; X19 = local_variables ptr
movz x21, #<global_addr_1_lo>         ; cache hot globals
movk x21, #<global_addr_1_hi>, lsl 16
...

; ──── LOOP START ────
loop_top:
    ldr  d0,  [x19, #slot*16 + 8]    ; LOAD_LOCAL → FP load
    ldr  d1,  [x19, #slot*16 + 8]    ; LOAD_LOCAL
    fcmp d0, d1                        ; LESS comparison (sets NZCV)
    b.ge exit_stub                     ; if not less, exit loop

    fadd d2, d2, d3                    ; ADD → FP add
    str  d2, [x19, #slot*16 + 8]      ; STORE_LOCAL → FP store
    str  d4, [x21, #8]                 ; STORE_GLOBAL via cached register

    b    loop_top                      ; LOOP_BACK

; ──── EXIT STUB ────
exit_stub:
    ; restore callee-saved FP regs
    ldr  d14,      [sp, #48]
    ldp  d12, d13, [sp, #32]
    ldp  d10, d11, [sp, #16]
    ldp  d8,  d9,  [sp], #56
    ; restore callee-saved GP regs
    ldp  x22, x23, [sp, #32]
    ldp  x20, x21, [sp, #16]
    ldp  x30, x19, [sp], #48
    ret                                ; return via LR (X30)
```

</details>

#### Memory Layout

Locals are accessed as `Value` structs at `[RBX + slot * 16 + 8]`:
- Each `Value` is 16 bytes (8-byte type tag + 8-byte union)
- Offset `+8` reaches the `as.number` field (the double payload)

Globals are accessed through direct `Value*` pointers, either cached in R12–R15 or loaded via `MOV RAX, imm64`.

#### Executable Memory

Generated code is allocated and made executable via the `JITMemory` class (`jit_memory.h`):

| Platform | Allocation | Execution | Cache Coherency |
|----------|-----------|-----------|----------------|
| **Linux x86-64** | `mmap(PROT_READ\|PROT_WRITE)` | `mprotect(+PROT_EXEC)` | Not needed (unified cache) |
| **Linux ARM64** | `mmap(PROT_READ\|PROT_WRITE)` | `mprotect(+PROT_EXEC)` | `__builtin___clear_cache()` |
| **macOS ARM64** | `mmap(MAP_JIT)` | `pthread_jit_write_protect_np()` | `__builtin___clear_cache()` |
| **Windows** | `VirtualAlloc(MEM_COMMIT)` | `VirtualProtect(PAGE_EXECUTE_READWRITE)` | `FlushInstructionCache()` |

> **ARM64 note:** ARM64 has separate instruction and data caches (Harvard-style). After writing machine code to memory, `__builtin___clear_cache()` must be called to ensure the instruction cache sees the new code. macOS additionally enforces W^X (write XOR execute) via `MAP_JIT` + `pthread_jit_write_protect_np()` toggling.

### Code Cache

| Parameter | Value |
|-----------|-------|
| `TIER2_CODE_CACHE_SIZE` | 50 MB |
| `MAX_TRACE_LENGTH` | 5,000 instructions |
| `MAX_LOOP_TRACES` | 500 |

---

## JIT Manager

**Class:** `MultiTierJITManager` (`jit_manager.h`)

The manager orchestrates the entire JIT pipeline:

1. **Compilation Requests:** `requestCompilation()` decides whether to compile a method to Tier-1 or Tier-2 based on profiler data.
2. **Tier Transitions:** `transitionTier()` handles the state transition when code moves between execution tiers.
3. **Execution Dispatch:** `executeCompiledCode()` runs compiled code at the appropriate tier, with on-demand Tier-2 compilation if no trace exists.
4. **Monitoring:** Optional compilation event listeners track `TIER1_COMPILATION_TRIGGERED`, `TIER2_COMPILATION_COMPLETED`, `TIER_TRANSITION`, `COMPILATION_FAILED`, etc.
5. **Statistics:** Tracks compilation counts, compilation time, cache sizes, tier distribution (time spent in interpreter vs Tier-1 vs Tier-2).

### Tier Promotion Criteria

| Transition | Condition |
|------------|-----------|
| Interpreter → Tier-1 | Method call count ≥ `TIER1_COMPILATION_THRESHOLD` (50) |
| Tier-1 → Tier-2 | Call count ≥ `TIER2_COMPILATION_THRESHOLD` (50) AND total execution time > 10ms |

---

## Code Generators

### x86-64 Code Generator

**Class:** `X86_64CodeGen` (`jit_codegen.h`)

Low-level utility class that emits individual x86-64 instructions with correct encoding:

**General Purpose:**
- `MOV r64, r64` / `MOV r64, imm64` / `MOV r64, [mem]` / `MOV [mem], r64`
- `ADD r64, r64` / `CMP r64, r64` / `TEST r64, r64`
- `PUSH r64` / `POP r64` / `LEA r64, [mem]`
- `CALL rel32` / `CALL r64` / `RET`
- `JMP rel32` / `JE rel32`

**SSE2 Double Precision:**
- `ADDSD` / `SUBSD` / `MULSD` / `DIVSD` (arithmetic)
- `MOVSD xmm, [mem]` / `MOVSD [mem], xmm` (load/store)
- `UCOMISD xmm, xmm` (comparison, sets CPU flags)

**Encoding Utilities:**
- `emitRexPrefix()` — REX prefix for 64-bit operations and extended registers
- `encodeModRM()` — ModRM byte encoding (mod, reg, rm fields)
- `makeExecutable()` — Platform-specific memory protection for W^X

### ARM64 (AArch64) Code Generator

**Class:** `AArch64CodeGen` (`jit_codegen_arm64.h`)

Header-only code generator that emits 32-bit fixed-width ARM64 instructions:

**General Purpose:**
- `MOV Xd, Xn` (via `ORR Xd, XZR, Xn`) / `MOV Xd, #imm64` (via `MOVZ` + up to 3 `MOVK`)
- `LDR Xd, [Xn, #imm]` / `STR Xd, [Xn, #imm]` (unsigned scaled & unscaled offsets)
- `STP/LDP` pairs for prologue/epilogue (pre-index store, post-index load)
- `ADD Xd, Xn, #imm12` / `SUB Xd, Xn, #imm12`
- `RET` (return via X30/LR)

**FP Double Precision:**
- `FADD` / `FSUB` / `FMUL` / `FDIV` / `FNEG` (D-register arithmetic)
- `LDR Dd, [Xn, #imm]` / `STR Dd, [Xn, #imm]` (FP load/store)
- `FMOV Dd, Dn` / `FMOV Dd, Xn` (FP-FP and GP-to-FP moves)
- `FCMP Dn, Dm` (comparison, sets NZCV flags)

**Conversion:**
- `FCVTZS Xd, Dn` — FP double → signed int64 (for bitwise operations)
- `SCVTF Dd, Xn` — signed int64 → FP double (convert back after bitwise)

**Bitwise (GP):**
- `AND` / `ORR` / `EOR` (XOR) / `MVN` (NOT)
- `LSLV` (variable shift left) / `ASRV` (arithmetic shift right)

**Branch:**
- `B <offset>` — unconditional branch (±128 MB range)
- `B.cond <offset>` — conditional branch with FP condition codes (`GE`, `LT`, `GT`, `LE`, `EQ`, `NE`)
- Patch helpers: `patchB()` / `patchBCond()` for back-patching forward branches

---

## Optimization Feature Flags

Configurable in `jit_config.h`:

| Flag | Default | Description |
|------|---------|-------------|
| `ENABLE_INLINE_CACHING` | `true` | Monomorphic inline caches for Tier-1 dispatch |
| `ENABLE_LOOP_UNROLLING` | `true` | Loop body duplication in Tier-2 |
| `ENABLE_METHOD_INLINING` | `true` | Method inlining in Tier-2 |
| `ENABLE_SHALLOW_TRACING` | `true` | Side-effect-free tracing in Tier-1 |
| `ENABLE_TYPE_SPECIALIZATION` | `true` | Type guards for specialized code paths |
| `MAX_INLINING_DEPTH` | 3 | Maximum depth for recursive inlining |

---

## Current Status

The JIT infrastructure is **implemented but not yet connected to the VM execution loop**. The components exist as standalone, tested modules:

- ✅ Hot-spot profiler with threshold-based tier promotion
- ✅ Tier-1 threaded code compiler with inline caching
- ✅ Tier-2 tracing JIT with IR, optimization passes, and native **x86-64** codegen
- ✅ Tier-2 tracing JIT with native **ARM64 (AArch64)** codegen — same IR/optimization pipeline, separate backend
- ✅ x86-64 code generator with GPR + SSE2 support
- ✅ ARM64 code generator with GP + FP double-precision support
- ✅ Platform-specific executable memory management (Linux, macOS, Windows — including `MAP_JIT` for Apple Silicon)
- ✅ JIT manager with tier coordination and event monitoring
- ✅ Unit tests (`tests/jit_test.cpp`, `tests/jit_functionality_test.cpp`, `tests/jit_integration_test.cpp`)
- ⬚ VM integration (hooking the JIT into the interpreter's `OP_LOOP` / backward-jump dispatch)
- ⬚ On-stack replacement (OSR) for transitioning mid-execution
- ⬚ Deoptimization / guard failure fallback to interpreter

### Supported Operations (Tier-2 Native Codegen)

Both the x86-64 and ARM64 backends support the same set of IR operations. The Tier-2 compiler can generate native code for traces containing:

- **Locals:** `LOAD_LOCAL`, `STORE_LOCAL` (all slot numbers)
- **Globals:** `LOAD_GLOBAL`, `STORE_GLOBAL` (resolved to direct `Value*` pointers)
- **Constants:** Numeric constants only (`LOAD_CONST`)
- **Arithmetic:** `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `MODULO`
- **Bitwise:** `AND`, `OR`, `XOR`, `NOT`, `LEFT_SHIFT`, `RIGHT_SHIFT`
- **Comparison:** `LESS`, `GREATER`, `EQUAL`, `NOT_EQUAL`
- **Control flow:** `JUMP_IF_FALSE` (loop exit + internal conditionals), `JUMP` (forward), `LOOP_BACK`
- **Stack:** `POP`, `NEGATE`

Traces containing unsupported operations (method calls, string operations, object access, closures, exceptions) are rejected and marked as failed to avoid retry.

---

## Performance Monitoring

When monitoring is enabled (`initialize(true)`), the JIT manager emits `CompilationEvent` records for:

| Event | Description |
|-------|-------------|
| `TIER1_COMPILATION_TRIGGERED` | Tier-1 compilation started |
| `TIER1_COMPILATION_COMPLETED` | Tier-1 compilation finished |
| `TIER2_COMPILATION_TRIGGERED` | Tier-2 trace compilation started |
| `TIER2_COMPILATION_COMPLETED` | Tier-2 trace compilation finished |
| `TIER_TRANSITION` | Code moved from one tier to another |
| `COMPILATION_FAILED` | Compilation attempt failed |

Statistics available via `getStatistics()`:
- Total compilations per tier, failed compilations
- Total compilation time, total execution time
- Code cache sizes and hit ratios
- Time distribution across interpreter / Tier-1 / Tier-2
- Warmup duration
