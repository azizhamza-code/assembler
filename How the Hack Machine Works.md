# How the Hack Machine Works

*One mental model, from Nand to the seven software projects.*

The Hack computer has two instructions, three registers, and no multiply. Chapters 1 to 5 of *The Elements of Computing Systems* exist to make those two instructions execute once per clock tick. Chapters 6 to 12 exist to turn two instructions into something you would recognize as a program.

This post is the bridge between the two halves. It rebuilds the machine from the bottom up, but always toward one goal: a model you can hold in your head while you write an assembler, a VM translator, a compiler and an OS on top of it.

Everything here comes from chapters 1-5 — the refresher notes and the book. Nothing from chapter 6 onward is assumed. When the last section points forward to projects 6-12, it only tells you which part of the machine each project leans on.

---



## How to read this

Three passes, depending on what you need right now.

1. **Skim the boxes.** Every section has a bolded takeaway. The ten ideas below are the whole model; everything else is evidence.
2. **Read Part 5 (the traces) properly.** Hand-tracing one program cycle by cycle is what converts a pile of tables into a machine you understand.
3. **Keep the cheat sheet open** at the end while you work on projects 6-12. It is the encoding table, the memory map, and the CPU decode table on one screen.

---



## The ten ideas

If you remember nothing else, remember these. Each one is revisited below.

1. **Two primitives.** Nand gives you combinational logic (output depends only on inputs). DFF gives you time (output depends on the previous cycle). Everything in the machine is composition of those two.
2. **Interface vs. implementation.** You can use a chip without knowing its insides. Twelve layers of abstraction are only possible because of this one rule.
3. **A bus is 16 wires that move together.** Meaning is assigned by the operation, never stored in the bits. Two's complement is a reading convention, not hardware.
4. **The ALU is a pure function:** `out = f(x, y, zx, nx, zy, ny, f, no)`. No clock, no state, 18 useful settings out of 64.
5. **Memory = a Mux plus a DFF.** `load` is a select bit that decides "keep the old value" or "take the new one". Register, RAM and PC are all that same idea, repeated.
6. **Reads are combinational; writes are clocked.** This asymmetry is the reason a whole instruction fits in one clock cycle.
7. **Two memories, one address register.** ROM holds instructions, RAM holds data, and A points into both. That is why a C-instruction should not use `M` and jump at the same time.
8. **The instruction word is a wiring diagram.** Every bit field lands on a specific pin in the CPU. Decoding is routing, nothing more. This is the single most important idea for project 6.
9. **Memory operations take two instructions.** Address first with `@`, then act. The 16-bit word has no room for an opcode and a 15-bit address together.
10. **The program is data in ROM; the hardware never changes.** Same silicon, different bits, different job.

---



## The machine in 60 seconds

One loop, executed once per clock cycle:

```
                                                   reset
                                                     │
   next PC:  reset ? 0                               ▼
             jump  ? A                  ┌───────────────────────┐
             else  PC+1                 │        PC             │
        ┌───────────────────────────────└───────────┬───────────┘
        │                                        pc (15)
        │                                            │
        │                                            ▼
        │                              ┌───────────────────────────┐
        │                              │  ROM32K    32K x 16 words │
        │                              └─────────────┬─────────────┘
        │                                            │ instruction (16)
        │                                            ▼
        │                              ┌───────────────────────────┐
        └──────────────────────────────│           CPU             │
                                       │      A        D     ALU   │
                                       └───┬───────────────────▲───┘
                          addressM (15) ───┤                   │
                          outM (16)     ───┤                   │ inM (16)
                          writeM        ───▼                   │
                                       ┌───────────────────────────┐
                                       │         Memory            │
                                       │  RAM16K     0 - 16383     │
                                       │  Screen     16384 - 24575 │
                                       │  Keyboard   24576         │
                                       └───────────────────────────┘
```

Each cycle, in order:

1. `pc` addresses a word in **ROM32K**. The word appears on `instruction`.
2. The CPU looks at **bit 15**. `0` → A-instruction: copy the word into A. `1` → C-instruction: decode the fields.
3. For a C-instruction, the ALU computes from `D` and (`A` or `M`), the result is written to whatever `dest` names, and `writeM` may store it to RAM.
4. `addressM` comes from A, so the memory access targets `RAM[A]` — via the Memory chip, which routes to RAM, Screen or Keyboard.
5. The next PC is `0` if `reset` is high, `A` if the jump condition holds, otherwise `PC + 1`.
6. The clock ticks. Every register in the machine takes its new value simultaneously.

That is a computer. Everything below is why each step works.

---



# Part 1 — Logic without time (chapters 1-2)



## 1.1 One gate to build the world from

`Nand(a, b) = 0` only when both inputs are 1. From that single gate you can build `Not`, `And`, `Or`, `Xor`, `Mux`, `DMux`, and then 16-bit versions of all of them. This is not a curiosity: it means the physical layer only ever has to manufacture one thing well, and the rest is wiring.

The habit that matters is thinking in **interfaces**:

```
Chip name:  Xor
Input:      a, b
Output:     out
Function:   out = 1 when exactly one of a, b is 1
```

Two chips with the same interface are interchangeable. The simulator even exploits this: if `Mux.hdl` is missing from your folder, it silently uses the built-in `Mux`. Your whole career in this course is stacking interfaces.

> **Takeaway.** A chip is a promise about pins, not a circuit. That promise is what lets chapter 5 ignore chapter 1 completely.



## 1.2 The five gates that come back later

Most of chapter 1 is composition, but five parts reappear on every page of chapters 3 and 5. Worth knowing them cold.


| Gate                   | Behavior                                      | What it becomes later                                                               |
| ---------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------- |
| `Mux(a,b,sel)`         | `sel=0 → out=a`, `sel=1 → out=b`              | Every "keep or take" decision: register `load`, ALU input select, PC priority chain |
| `DMux(in,sel)`         | Routes `in` to one of two outputs, other is 0 | Write-enable broadcast: sends `load` to exactly one RAM row                         |
| `Not16 / And16 / Or16` | Bitwise, all 16 bits at once                  | ALU logic operations, screen pixel masking                                          |
| `Mux16`                | 16-bit Mux, one `sel` for all bits            | The ALU's `a`-bit path, the A register input, PC chain                              |
| `Mux8Way16 / DMux8Way` | 8-way trees of the above                      | RAM8's addressing: pick one register to write, one to read                          |


The two multi-way gates are worth stating as a rule, because the same rule becomes RAM addressing in chapter 3:

- `DMux8Way` takes one `load` bit and gives it to exactly one of eight registers. The other seven get 0.
- `Mux8Way16` takes eight register outputs and gives back the one the address selects.
- `sel[0]` goes to the stage next to the data pins; the high bit goes to the stage next to the single pin. Swap them and your outputs `b` and `c` trade places.



## 1.3 A bus is 16 wires wearing one name

`in[16]` is not a number. It is sixteen independent wires that the tools let you name as a group. Three rules follow, and all three cause bugs later:

- **Bit 0 is the rightmost bit** and the least significant one. Bit 15 is the leftmost and the sign bit under two's complement.
- **Slices are written low to high:** `address[3..5]` is three bits, and `address[3]` is the least significant of those three.
- **All 16 bits move together in a bus operation.** `Mux16(a=x, b=false, sel=s)` sends 16 zeros or 16 bits of x — never a mixture.

> **Takeaway.** Nothing in the hardware knows that bit 15 "means" a sign. The convention lives entirely in how the ALU and the jump logic read it.



## 1.4 Numbers without special hardware

Two's complement is the trick that lets one adder handle signed and unsigned arithmetic. For 16 bits:


| Value        | Binary                | Hex      |
| ------------ | --------------------- | -------- |
| 0            | `0000 0000 0000 0000` | `0x0000` |
| 1            | `0000 0000 0000 0001` | `0x0001` |
| -1           | `1111 1111 1111 1111` | `0xFFFF` |
| 32767 (max)  | `0111 1111 1111 1111` | `0x7FFF` |
| -32768 (min) | `1000 0000 0000 0000` | `0x8000` |


Facts you will use constantly:

- The range is `-32768 .. 32767`. There is one more negative value than positive ones, and zero has a single code.
- `-x` is `!x + 1`. Equivalently, and more usefully in code: `!x = -x - 1`.
- `x - y = x + (-y)`. Subtraction needs no hardware beyond negation.
- The carry out of bit 15 is **dropped**, silently. `32767 + 1` gives `0x8000` = `-32768`. There is no overflow flag in Hack, ever.
- Because an A-instruction has only 15 value bits, `@` can never express a negative number. You build negatives by computing them: `@5` then `D=-A`.

> **Takeaway.** Overflow is not detected because the machine does not care. Your later software (the OS in project 12) has to care on its own.



## 1.5 The ALU: six bits, eighteen functions

The Hack ALU takes two 16-bit inputs and six control bits, and produces one 16-bit result plus two flags. Its operation is a fixed pipeline:

```
x, y ──▶ [zx: x=0] ──▶ [nx: x=!x] ──┐
        [zy: y=0] ──▶ [ny: y=!y] ──┴──▶ [f: 1=add, 0=and] ──▶ [no: !out] ──▶ out
                                                                              ├──▶ zr = (out == 0)
                                                                              └──▶ ng = out[15]
```

Order matters: zeroing happens **before** negating, so `zx=1, nx=1` produces all-ones (`-1`), not zero.

The 18 documented settings (bit order `zx nx zy ny f no`):


| Setting  | out     | Setting  | out       | Setting  | out       |
| -------- | ------- | -------- | --------- | -------- | --------- |
| `101010` | 0       | `001111` | -D        | `000010` | D+A / D+M |
| `111111` | 1       | `110011` | -A / -M   | `010011` | D-A / D-M |
| `111010` | -1      | `011111` | D+1       | `000111` | A-D / M-D |
| `001100` | D       | `110111` | A+1 / M+1 | `000000` | D&A / D&M |
| `110000` | A / M   | `001110` | D-1       | `010101` | D         |
| `001101` | !D      | `110010` | A-1 / M-1 |          |           |
| `110001` | !A / !M |          |           |          |           |


Three things to notice, because they pay off in the assembler:

- **Every arithmetic operation is built from the adder plus negation.** `D-A` is encoded as `010011`, which is `!(!D + A)` — not a subtraction circuit. `D+1` is `011111` = `!(!D + (-1))`. Both rely on `!x = -x - 1`.
- `ng` **is literally** `out[15]`**.** A wire, not a comparison. `zr` is `NOT(OR of all 16 output bits)`, built from two `Or8Way`s.
- **The ALU has no shift, no multiply, no divide, and no memory.** Every one of those will be software you write in project 12.

> **Takeaway — and this is the seam between chapters.** The six control bits `zx nx zy ny f no` are, bit for bit, the `c1..c6` field of a C-instruction. Chapter 2 built the thing that chapter 4 will name, and chapter 5 will wire to the instruction word. When you write the assembler and look up `D+1 → 011111`, you are reading an ALU setting, not a magic string.

---



# Part 2 — Adding time (chapter 3)



## 2.1 Why the machine needs a clock at all

Combinational logic is instantaneous in the model and slow in reality. A `Not` gate takes a moment to settle; an `Add16` takes longer, and its carry ripples bit by bit from the right end. If you let signals feed back into the logic that produced them, the output would depend on itself and the circuit would oscillate.

The escape is to insert a delay you control, and to agree that **nobody looks at the wires except at the end of a cycle**. The master clock alternates tick/tock; one full cycle is one discrete time unit `t`. Every storage element in the machine commits its new value at the same instant.

That single decision does three jobs:

1. It hides propagation delay. The ALU's result is "instant" because you only sample it once the cycle is over.
2. It makes the cycle length a design choice: slightly longer than the worst-case delay in the machine. Shorter cycle, faster computer.
3. It makes feedback legal — as long as the feedback passes through a clocked element.



## 2.2 The DFF, and the only pattern you need

The data flip-flop is the primitive that adds time:

```
out(t+1) = in(t)          // first cycle: undefined
```

A raw DFF is useless on its own. Wire its output straight back to its input and you get a pin driven by two sources, which the HDL forbids anyway. So put a **Mux** in front of it:

```
CHIP Bit {
    IN in, load;
    OUT out;
    PARTS:
    Mux(a=prev, b=in, sel=load, out=next);
    DFF(in=next, out=prev, out=out);   // one output can drive two wires
}
```

```
load=1 → out(t+1) = in        (take the new value)
load=0 → out(t+1) = out(t)    (keep the old one; in is ignored)
```

**That is what memory is.** Not a special material — a Mux selecting between "new" and "old", with a DFF holding the loop. Every register, every RAM word, and the program counter are this pattern wearing different pins.

> **Takeaway.** `load` is a data input like any other. Storage is a selection, and selection is a Mux.



## 2.3 Register, RAM, PC: the same pattern three ways

**Register** = sixteen `Bit`s sharing one `load`. `load=1` writes all 16 bits; `load=0` freezes them. `=` in the spec means all 16 bits at once.

**RAMn** = n Registers plus addressing logic:

```
                 ┌──────────────┐
   load ────────▶│   DMux8Way   │──▶ l0 l1 l2 ... l7   (one write enable)
                 └──────────────┘
   in[16] ─────┬──▶ Register0 ──▶ r0
               ├──▶ Register1 ──▶ r1        ┌────────────┐
               └──▶ ...                   ─▶│ Mux8Way16  │──▶ out[16]
   address[2..0] ──────────────────────────▶└────────────┘
```

Two facts about this, both load-bearing:

- **No register knows its own address.** Register 5 is register 5 only because the `DMux` sends it the write enable for address 5, and the `Mux` picks its output for address 5. Addressing is pure combinational logic wrapped around a bank of identical cells.
- **Reads do not wait for the clock.** Set `address=m` and `out` shows register m in the same cycle. Only writes are clocked.

Bigger RAMs are the same picture, recursively:


| Chip   | Registers | Address bits | Built from  | Selector bits     | Passed down      |
| ------ | --------- | ------------ | ----------- | ----------------- | ---------------- |
| RAM8   | 8         | 3            | 8 Register  | `address[0..2]`   | —                |
| RAM64  | 64        | 6            | 8 RAM8      | `address[3..5]`   | `address[0..2]`  |
| RAM512 | 512       | 9            | 8 RAM64     | `address[6..8]`   | `address[0..5]`  |
| RAM4K  | 4096      | 12           | 8 RAM512    | `address[9..11]`  | `address[0..8]`  |
| RAM16K | 16384     | 14           | **4** RAM4K | `address[12..13]` | `address[0..11]` |


The high bits pick which sub-RAM to talk to; the low bits go to *all* of them at once, and each sub-RAM decides internally whether it is the target. Access time does not depend on the address or the size — hence "random access".

**The PC** is a Register whose next value is chosen by a priority chain:

```
CHIP PC {
    IN in[16], load, inc, reset;
    OUT out[16];
    PARTS:
    Inc16(in=cur, out=plus1);
    Mux16(a=cur, b=plus1, sel=inc,   out=o1);
    Mux16(a=o1,  b=in,    sel=load,  out=o2);
    Mux16(a=o2,  b=false, sel=reset, out=o3);   // last Mux wins
    Register(in=o3, load=true, out=cur, out=out);
}
```


| reset | load | inc | `out(t+1)`   |
| ----- | ---- | --- | ------------ |
| 1     | x    | x   | 0            |
| 0     | 1    | x   | `in(t)`      |
| 0     | 0    | 1   | `out(t) + 1` |
| 0     | 0    | 0   | `out(t)`     |


Note how priority is expressed: a **chain of Muxes**, where the last one applied overrides the earlier ones. Chapter 5 uses the same chain trick to sequence the CPU's next-PC decision, so this small chip is worth understanding properly rather than copying.

## 2.4 The timing rule that makes one cycle enough


| Operation | Set                           | Visible on `out`              |
| --------- | ----------------------------- | ----------------------------- |
| Read      | `address=m`, `load=0`         | immediately, same cycle       |
| Write     | `address=m`, `in=v`, `load=1` | from `t+1` onward             |
| Hold      | `load=0`                      | value unchanged; `in` ignored |


Reads are combinational; writes land on the tick. Hold onto that asymmetry — the entire single-cycle CPU depends on it. In Part 4 you will see one instruction do all of the following **within one cycle**: fetch, decode, compute, write RAM, and choose the next PC. It works because reading RAM costs nothing in time, and every state update happens at the same tick at the end.

> **Takeaway.** Combinational logic does the work; the clock only decides when the answer is believed.

---



# Part 3 — The contract: the Hack machine language (chapter 4)

Chapters 1-3 built a machine that can compute and remember. Chapter 4 is the agreement about what the bits in ROM **mean**. It is the shortest chapter and the one you will re-read most, because every project from 6 to 12 either produces or consumes this encoding.

## 3.1 Two instructions, and the 1/2-address problem

A 16-bit word cannot hold both an opcode and a 15-bit address. So Hack splits the work:

- `@value` — an *address* instruction. 15 bits of value.
- `dest = comp ; jump` — a *compute* instruction. No room for an address.

Which means every memory operation, and every jump, takes **two** instructions: one to put the address in A, one to act. Hack code therefore alternates `@` lines and C lines in a rhythm you will see echoed all the way up in the compiler:

```
@x          // A = address of x
M=M+1       // act on RAM[A]
```



## 3.2 A-instruction

```
0 v v v v v v v v v v v v v v v          bit 15 = 0, bits 14..0 = value (0..32767)
```

`@5` is `0000000000000101`. A is 16 bits, so `@5` really loads 16 bits — the top bit just happens to be 0. Three uses, and nothing else:

1. Introduce a constant into the program (the only way to do so).
2. Select a data address, so a following C-instruction can use `M` = `RAM[A]`.
3. Set a jump target, so a following C-instruction can jump to `ROM[A]`.

Because bit 15 is the opcode, `@-1` and `@40000` are impossible. Negative values are computed: `@5` then `D=-A`.

## 3.3 C-instruction

Written as 16 bits, most significant first:

```
1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
```


| Bits  | 15                      | 14-13               | 12                       | 11-6                       | 5-3           | 2-0              |
| ----- | ----------------------- | ------------------- | ------------------------ | -------------------------- | ------------- | ---------------- |
| Field | `1` (opcode)            | `11` (unused)       | `a`                      | `c1..c6`                   | `d1 d2 d3`    | `j1 j2 j3`       |
| Means | this is a C-instruction | ignored, convention | ALU `y` = A (0) or M (1) | comp: the ALU control bits | dest: A, D, M | jump: <0, =0, >0 |


`comp` is required. `dest=` and `;jump` are optional and simply omitted.

**The comp field.** The six `c` bits are the ALU control bits from Part 1, in the order `zx nx zy ny f no`. The ALU's `x` input is *always* `D`; the `a` bit picks whether `y` is `A` or `M`. There are 28 valid mnemonics (18 with `a=0`, 10 with `a=1`) out of 128 possible codes.


| comp (`a=0`) | comp (`a=1`) | `c1..c6` |     | comp (`a=0`) | comp (`a=1`) | `c1..c6` |
| ------------ | ------------ | -------- | --- | ------------ | ------------ | -------- |
| `0`          |              | `101010` |     | `D+1`        |              | `011111` |
| `1`          |              | `111111` |     | `A+1`        | `M+1`        | `110111` |
| `-1`         |              | `111010` |     | `D-1`        |              | `001110` |
| `D`          |              | `001100` |     | `A-1`        | `M-1`        | `110010` |
| `A`          | `M`          | `110000` |     | `D+A`        | `D+M`        | `000010` |
| `!D`         |              | `001101` |     | `D-A`        | `D-M`        | `010011` |
| `!A`         | `!M`         | `110001` |     | `A-D`        | `M-D`        | `000111` |
| `-D`         |              | `001111` |     | `D&A`        | `D&M`        | `000000` |
| `-A`         | `-M`         | `110011` |     | `D           | A`           | `D       |


Each mnemonic is **one fixed string**. `D+M` exists; `M+D` does not. The `+` does no parsing magic — it is part of a name that indexes a table.

**The dest field.** Bits in the order A, D, M — so `AM` is `101` and `AMD` is `111`. Any combination of zero to three destinations is legal.


| dest      | `d1d2d3` | Stores the ALU output in |
| --------- | -------- | ------------------------ |
| *(empty)* | `000`    | nowhere                  |
| `M`       | `001`    | `RAM[A]`                 |
| `D`       | `010`    | D                        |
| `DM`      | `011`    | D and `RAM[A]`           |
| `A`       | `100`    | A                        |
| `AM`      | `101`    | A and `RAM[A]`           |
| `AD`      | `110`    | A and D                  |
| `ADM`     | `111`    | A, D and `RAM[A]`        |


(The first edition wrote `MD` and `AMD`; the second writes `DM` and `ADM`. Same bits — expect to see both spellings in test files and in other people's code.)

**The jump field.** Bits in the order `<0`, `=0`, `>0`. The test applies to **this instruction's comp result**, never to `D` as such: `D;JGT` tests D because comp is `D`, while `D=D-M;JGT` tests `D-M`.


| jump      | `j1j2j3` | Jump to `ROM[A]` if |
| --------- | -------- | ------------------- |
| *(empty)* | `000`    | never               |
| `JGT`     | `001`    | out > 0             |
| `JEQ`     | `010`    | out = 0             |
| `JGE`     | `011`    | out >= 0            |
| `JLT`     | `100`    | out < 0             |
| `JNE`     | `101`    | out != 0            |
| `JLE`     | `110`    | out <= 0            |
| `JMP`     | `111`    | always              |


`comp` is mandatory, so an unconditional jump is written `0;JMP` — compute zero, then ignore it and jump. This is where the ALU's `zr` and `ng` flags get their purpose: they are the only two things a jump can test, which is exactly why the ALU exports them.

## 3.4 A's double life

After `@xxx`, A holds `xxx`, and `xxx` means **two** things at once: `RAM[xxx]` (data) and `ROM[xxx]` (a possible jump target). A C-instruction can use only one of them meaningfully, because A cannot point at a useful data word and a useful jump target at the same time.

The rule that follows is a real constraint on code you write and code your compiler will generate:

> **A C-instruction that reads or writes** `M` **should not jump. A C-instruction that jumps should not use** `M`**.**



## 3.5 Symbols: the assembler's job description

Three kinds of symbol, and knowing which is which is most of project 6:


| Kind           | Written                                                         | Value             | Notes                                                                                                            |
| -------------- | --------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Predefined** | `R0`-`R15`, `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `SCREEN`, `KBD` | fixed             | `R0..R15` = 0..15; `SP LCL ARG THIS THAT` = 0..4; `SCREEN` = 16384; `KBD` = 24576                                |
| **Label**      | `(LOOP)`                                                        | a **ROM** address | Pseudo-instruction: produces no binary. Binds to the address of the *next real instruction*, not the line number |
| **Variable**   | anything else after `@`                                         | a **RAM** address | Allocated from 16 upward, in order of first appearance                                                           |


Two consequences worth internalizing now:

- The chapter 4 rule "ignore `SP LCL ARG THIS THAT` for now" is a promise that Part II keeps. Those five symbols are pre-bound to RAM 0-4 because *the VM you build in projects 7-8 will use them as its stack pointer, its two frame bases, and the bases of the current object and array*. They are already in the language, waiting.
- Labels and variables are both just numbers loaded with `@`. The **next** instruction decides whether that number is being used as a jump target or as a data address. Nothing about the symbol itself says which.



## 3.6 The memory map

```
RAM[0..15]        R0..R15  (SP, LCL, ARG, THIS, THAT live at 0..4)
RAM[16..16383]    variables, arrays, objects, heap — yours to use
RAM[16384..24575] Screen   8K words, 256 rows x 512 pixels
RAM[24576]        Keyboard  one word, read-only
RAM[24577..32767] invalid  (the simple Memory chip aliases these to the keyboard)
```

The screen is bit-addressed inside 16-bit words, which is the single most error-prone piece of arithmetic in the whole course:

```
pixel (row, col) lives in  RAM[ 16384 + 32*row + col/16 ],  at bit  col % 16
1 = black, 0 = white, and bit 0 is the LEFTMOST pixel of its 16-pixel group
row 0 starts at 16384; each row is 32 words; there are 256 rows
```

There is no "set one pixel" instruction. You read the word, change bits with logic, and write the whole word back — which is exactly what `Screen.drawPixel` will have to do in project 12.

Keyboard is one read-only word holding the code of the key pressed **right now**, or 0. No buffer, no events. Codes are ASCII for printable characters; 128-140 are newline, backspace, arrows, home/end, page up/down, insert, delete, esc; 141-152 are F1-F12. Polling is the only technique available, which is why every Hack game has a loop reading `KBD`.

## 3.7 The four idioms

Every Hack program, and every line your compiler emits in project 11, is one of these patterns.

```
// 1. loop skeleton — "while (true)"
(LOOP)
    ...
    @LOOP
    0;JMP

// 2. conditional — "if (D > 0) goto POS"
    @POS
    D;JGT

// 3. pointer store — "*(base+i) = -1"   (arrays do not exist; addresses do)
    @i
    D=M          // D = i
    @R0
    A=D+M        // A = base + i  (A changes at the tick)
    M=-1         // so this M is RAM[base+i]

// 4. halt — the CPU never stops by itself
(END)
    @END
    0;JMP
```

Idiom 3 is the one to stare at. `A=D+M` computes an address *into A*, and the very next instruction's `M` refers to that new address. That single move is how every array access, every object field read, and every `push`/`pop` in the VM will be implemented.

> **Takeaway.** The language is small enough to hold entirely in your head: two instructions, three A-roles, three symbol kinds, one memory map. Everything else in Part II is a *convention layered on top of* `@` *and C-instructions*.

---



# Part 4 — The machine that keeps the contract (chapter 5)

Chapter 5 is only three chips: `Memory`, `CPU`, `Computer`. Everything before it was preparation.

## 4.1 Memory: one address space, three devices

The CPU sees a single 15-bit data address space. `Memory` splits it by looking at the top two bits:


| `address[14..13]` | Device   | Address passed down | Range         |
| ----------------- | -------- | ------------------- | ------------- |
| `00` or `01`      | RAM16K   | `address[0..13]`    | 0 - 16383     |
| `10`              | Screen   | `address[0..12]`    | 16384 - 24575 |
| `11`              | Keyboard | — (no address pin)  | 24576 only    |


```
CHIP Memory {
    IN  in[16], load, address[15];
    OUT out[16];
    PARTS:
    DMux4Way(in=load, sel=address[13..14], a=r0, b=r1, c=loadScr);
    Or(a=r0, b=r1, out=loadRam);          // 00 and 01 are both RAM16K
    RAM16K(in=in, load=loadRam, address=address[0..13], out=ramOut);
    Screen(in=in, load=loadScr, address=address[0..12], out=scrOut);
    Keyboard(out=kbdOut);
    Mux4Way16(a=ramOut, b=ramOut, c=scrOut, d=kbdOut,
              sel=address[13..14], out=out);
}
```

Note the duplicated `ramOut` input on the final Mux: `01` is not a distinct device, it is the upper half of RAM16K, so both selector values must return RAM. And because the Keyboard has no `load` pin, the `DMux4Way`'s `d` output is simply left unconnected — a write to 24576 silently does nothing.

> **Takeaway.** Memory-mapped I/O is not an instruction. It is an address decode. Writing to 16384 is a store instruction whose destination happens to be a display.



## 4.2 The CPU: where each bit goes

This is the heart of the post. The CPU is a decoder with one job: **route each bit of the instruction word to the pin it controls.**


| Bits  | Field    | Becomes                       | Effect this cycle                                      |
| ----- | -------- | ----------------------------- | ------------------------------------------------------ |
| 15    | opcode   | `isC` (`isA = !bit15`)        | Chooses the whole mode: A-instruction or C-instruction |
| 14-13 | unused   | nothing                       | Ignored. Convention says write `11`                    |
| 12    | `a`      | Mux16 select                  | ALU `y` input = A (`a=0`) or `inM` (`a=1`)             |
| 11-6  | `c1..c6` | ALU control pins              | `zx nx zy ny f no` — the chapter 2 settings            |
| 5     | `d1`     | `loadA` (with `isC`)          | Write the ALU output into A                            |
| 4     | `d2`     | `loadD` (with `isC`)          | Write the ALU output into D                            |
| 3     | `d3`     | `writeM` (with `isC`)         | Store the ALU output into `RAM[A]`                     |
| 2     | `j1`     | jump if `ng`                  | out < 0                                                |
| 1     | `j2`     | jump if `zr`                  | out = 0                                                |
| 0     | `j3`     | jump if not `zr` and not `ng` | out > 0                                                |


The control logic in full (`isC = instruction[15]`, `isA = !isC`):


| Signal           | Logic                                                |
| ---------------- | ---------------------------------------------------- |
| A register input | `isC ? aluOut : instruction` (a Mux16 on `isC`)      |
| `loadA`          | `isA OR (isC AND instruction[5])`                    |
| `loadD`          | `isC AND instruction[4]`                             |
| `writeM`         | `isC AND instruction[3]`                             |
| ALU `x`          | `D` — always, no choice                              |
| ALU `y`          | `instruction[12] ? inM : A`                          |
| ALU `zx..no`     | `instruction[11..6]`                                 |
| jump             | `(j1 AND ng) OR (j2 AND zr) OR (j3 AND !zr AND !ng)` |
| PC next          | `reset ? 0 : (isC AND jump) ? A : PC+1`              |
| `addressM`       | `A[0..14]` (15 bits)                                 |
| `pc`             | `PC[0..14]` (15 bits)                                |
| `outM`           | `aluOut` (combinational, valid this cycle)           |


**Why the** `AND isC` **gates exist.** On an A-instruction, bits 14..0 *are the value*. Those bit positions overlap the `dest` and `jump` fields exactly. Look at what that means:

```
@8  = 0000 0000 0000 1000     bit 3 = 1  → that is the writeM position
@16 = 0000 0000 0001 0000     bit 4 = 1  → that is the loadD position
```

Without the `isC` gate, `@8` would write to memory and `@16` would clobber D. The gate is not defensive coding; it is the reason the A-instruction encoding works at all. (The `a` and `c` bits need no gate — they only steer a Mux and the ALU, which have no side effects.)

Here is the whole CPU, abridged, with the gates visible:

```
CHIP CPU {
    IN  inM[16], instruction[16], reset;
    OUT outM[16], writeM, addressM[15], pc[15];
    PARTS:
    Not(in=instruction[15], out=isA);
    Not(in=isA, out=isC);

    // A: takes the instruction itself (A-instr) or the ALU result (dest A)
    Mux16(a=instruction, b=aluOut, sel=isC, out=aIn);
    And(a=isC, b=instruction[5], out=destA);
    Or(a=isA, b=destA, out=loadA);
    ARegister(in=aIn, load=loadA, out=aOut, out[0..14]=addressM);

    // D
    And(a=isC, b=instruction[4], out=loadD);
    DRegister(in=aluOut, load=loadD, out=dOut);

    // ALU: x = D always; y = A or M by the a-bit
    Mux16(a=aOut, b=inM, sel=instruction[12], out=aOrM);
    ALU(x=dOut, y=aOrM,
        zx=instruction[11], nx=instruction[10], zy=instruction[9],
        ny=instruction[8],  f=instruction[7],  no=instruction[6],
        out=aluOut, out=outM, zr=zr, ng=ng);

    And(a=isC, b=instruction[3], out=writeM);

    // jump: (j1&ng) | (j2&zr) | (j3&!zr&!ng), gated by isC
    Or(a=zr, b=ng, out=zrOrNg);
    Not(in=zrOrNg, out=pos);
    And(a=instruction[2], b=ng,  out=jlt);
    And(a=instruction[1], b=zr,  out=jeq);
    And(a=instruction[0], b=pos, out=jgt);
    Or(a=jlt, b=jeq, out=jle);
    Or(a=jle, b=jgt, out=jmp);
    And(a=isC, b=jmp, out=loadPC);
    PC(in=aOut, load=loadPC, inc=true, reset=reset, out[0..14]=pc);
}
```

Read that once more, slowly. `D;JGT` is not a command; it is `instruction[2]=1` meeting `ng=0` and `zr=0` meeting the PC's `load` pin. The PC is given `A` as its `in`, `inc=true` always, and the priority chain decides: `reset` beats `load` beats `inc`.

> **Takeaway.** The CPU has no notion of a "mnemonic". It has 16 wires and a routing. When you write your assembler in project 6, you are computing the bit pattern that makes these routes come out right — **the assembler is the inverse function of this table.**



## 4.3 Computer: closing the loop

```
CHIP Computer {
    IN reset;
    PARTS:
    ROM32K(address=pc, out=instr);
    CPU(instruction=instr, inM=memOut, reset=reset,
        outM=outM, writeM=writeM, addressM=addrM, pc=pc);
    Memory(in=outM, load=writeM, address=addrM, out=memOut);
}
```

Six wires each way. `pc` addresses ROM, `instr` feeds the CPU, `addrM`/`outM`/`writeM` go to Memory, `memOut` comes back as `inM`, `reset` restarts everything at ROM address 0.

**Why one cycle is enough.** Hack is a Harvard machine: `ROM32K` and `Memory` are physically separate, with separate address inputs. The CPU can fetch the next instruction and read or write data *in the same cycle*, so there is no instruction register and no fetch/decode/execute phasing.


|                     | Hack (Harvard, 2 memories)             | Classic von Neumann (1 memory)             |
| ------------------- | -------------------------------------- | ------------------------------------------ |
| Fetch + data access | same cycle                             | needs 2+ cycles or an instruction register |
| Hardware cost       | two memories                           | one memory, more control logic             |
| Flexibility         | code cannot be read or written as data | code and data share the space              |


The cost is real: you can never load a program from RAM, self-modify code, or run code generated at runtime. Hack does not need any of that, and it gets a single-cycle machine in exchange.

Also note what the CPU *cannot* do: it has no interrupt, no trap, no protected mode, and no way to stop. `reset` is the only external control, and a program ends by looping forever. That is why every Hack program, from `Add.asm` to the OS in project 12, ends in `(END) @END 0;JMP`.

---



# Part 5 — Trace it by hand

Tables are not understanding. Walking a program through the hardware cycle by cycle is. Do this once, properly, and the machine stops being a diagram.

## 5.1 The Add program, six cycles

```
ROM[0]  @2       0000000000000010
ROM[1]  D=A      1110110000010000
ROM[2]  @3       0000000000000011
ROM[3]  D=D+A    1110000010010000
ROM[4]  @0       0000000000000000
ROM[5]  M=D      1110001100001000
```

Starting state: `A=0, D=0, PC=0, RAM[0]=0`.


| t   | PC  | instruction | decoded as              | ALU does       | A (t+1) | D (t+1) | RAM write      | PC (t+1) |
| --- | --- | ----------- | ----------------------- | -------------- | ------- | ------- | -------------- | -------- |
| 1   | 0   | `@2`        | A-instr, value 2        | idle           | **2**   | 0       | —              | 1        |
| 2   | 1   | `D=A`       | `a=0`, comp A, dest D   | `(!0) & A` = 2 | 2       | **2**   | —              | 2        |
| 3   | 2   | `@3`        | A-instr, value 3        | idle           | **3**   | 2       | —              | 3        |
| 4   | 3   | `D=D+A`     | `a=0`, comp D+A, dest D | `2 + 3` = 5    | 3       | **5**   | —              | 4        |
| 5   | 4   | `@0`        | A-instr, value 0        | idle           | **0**   | 5       | —              | 5        |
| 6   | 5   | `M=D`       | `a=0`, comp D, dest M   | `5`            | 0       | 5       | **RAM[0] = 5** | 6        |


Three things this trace teaches that a table cannot:

- `D=A` **is not a copy circuit.** Its comp field is `110000` = `zx=1, nx=1, ...` which zeroes x, negates it to all-ones, ANDs with y=A, giving A. The general-purpose ALU does the copying as a side effect of `-1 & A`. Every comp mnemonic is a small proof like this.
- **A changes on cycles 1, 3 and 5; D only on 2 and 4.** State updates are sparse. Most cycles move one register.
- `loadA` **fires twice for different reasons.** On cycle 1 it fires because `isA=1`; on a `dest=A` C-instruction it would fire because `instruction[5]=1`. Two different routes to the same pin.



## 5.2 The gating proof, concretely

Recall bits 14..0 of an A-instruction sit exactly where the `dest` and `jump` fields live. Two words make the danger obvious:

```
@8  = 0000 0000 0000 1000
              bit 3 = 1  ← the d3 position, i.e. writeM
@16 = 0000 0000 0001 0000
              bit 4 = 1  ← the d2 position, i.e. loadD
```

Without `AND isC`:

- `@8` would set `writeM=1` and store a garbage ALU result into `RAM[8]`. Address 8 is `R8` — a register your program probably uses.
- `@16` would set `loadD=1` and destroy D with whatever the ALU happened to be computing.

With the gate, both are inert: `isC=0`, so `loadD=0` and `writeM=0`, and only `loadA` fires (through `isA`). This is why `loadA = isA OR (isC AND d1)` has an `OR` where the others have nothing: A must load on *both* instruction types, but for different reasons.

> **Takeaway.** Half of understanding the CPU is knowing which signals are gated by `isC` and why.



## 5.3 A loop: the PC takes A

```
        (LOOP)                        // binds LOOP to ROM address 0; emits nothing
ROM[0]      @i       0000000000010000 // i is the first variable ⇒ RAM[16]
ROM[1]      M=M+1    1111110111001000
ROM[2]      @LOOP    0000000000000000
ROM[3]      0;JMP    1110101010000111
```


| t   | PC  | instruction | what happens                                                   | PC (t+1) |
| --- | --- | ----------- | -------------------------------------------------------------- | -------- |
| 1   | 0   | `@i`        | A = 16                                                         | 1        |
| 2   | 1   | `M=M+1`     | `a=1` → y = `RAM[16]`; ALU `M+1`; `writeM=1` → `RAM[16] += 1`  | 2        |
| 3   | 2   | `@LOOP`     | A = 0                                                          | 3        |
| 4   | 3   | `0;JMP`     | comp `0` → out = 0 → `zr=1`; `j1j2j3=111` matches → `loadPC=1` | **0**    |


Two subtleties worth naming:

- `(LOOP)` produced **no binary**. It bound the symbol `LOOP` to the ROM address of the next real instruction — which is 0 here, the same value as `@0`.
- The jump condition tested `out`, which in `0;JMP` is the constant zero. `zr` is high, `j2=1`, so the PC loads A. A jump always goes to `ROM[A]`; the comp result only decides *whether*, never *where*.



## 5.4 The pointer store, and the one-cycle trap

```
    @i          // A = &i
    D=M         // D = i
    @R0
    A=D+M       // A = base + i     ← A is written at the END of this cycle
    M=-1        // this cycle's M is RAM[base+i]
```

Cycle by cycle: `A=D+M` computes `base+i` and loads it into A at the tick. In the *next* instruction, `M` resolves to `RAM[A]` = `RAM[base+i]`, so `M=-1` writes the array element. The address register and the data access are one cycle apart, always. That is the two-instruction rhythm from Part 3, seen from inside the CPU.

**The trap:** `A=D+M;JMP` does *not* jump to the new address. The jump logic reads A as it was *before* this instruction, because the new A is only stored at the tick. Use two instructions. The same applies to `AM=M+1` — the memory access uses the old A, and the new A appears next cycle.

## 5.5 One instruction, every part of the machine

`D;JGT` = `1110001100000001`. Read it against the CPU table:

```
111  0  001100  000  001
│    │  │       │    └── j1j2j3 = 001 → jump if ng=0 and zr=0  →  out > 0
│    │  │       └─────── d1d2d3 = 000 → loadA=0, loadD=0, writeM=0
│    │  └─────────────── c1..c6  = 001100 → the ALU setting for "D"
│    └────────────────── a = 0 → y = A  (unused here; only x matters)
└─────────────────────── opcode 1 → isC; bits 14-13 ignored
```

This one word, in one clock cycle: fetched from `ROM[PC]`, split into four fields, sent to the ALU (`x=D`), sent to the jump logic (`j1=1` with `ng`), and used to load the PC from A. No data is written anywhere. If `D <= 0`, the PC just increments and the next instruction runs instead.

## 5.6 A program you have already written

The chapter 4 `Fill` program is the same three ideas on loop:

```
(LOOP)
    @KBD            // A = 24576  → Memory routes this to the Keyboard, read-only
    D=M             // D = key code, 0 when nothing is pressed
    @BLACK
    D;JNE           // a key is down → blacken
    ... clear the screen words ...
    @LOOP
    0;JMP
(BLACK)
    @SCREEN         // A = 16384 → the first word of the screen map
    M=-1            // 16 pixels black in one store
    ...
```

Notice that nothing here is special-cased hardware. `@KBD / D=M` is an ordinary load whose address decode lands on a keyboard register. `@SCREEN / M=-1` is an ordinary store whose address decode lands on the display. **Input and output are just memory, at numbers you must remember.** Keep that in mind for project 9 (the Jack game) and project 12 (`Screen`, `Keyboard`, `Output`): all three are thin wrappers over this arithmetic.

### How to trace any program

1. Write the ROM addresses down the left margin, counting **only real instructions** (labels cost nothing).
2. Resolve every label to a ROM address and every variable to a RAM address.
3. Track four values: `A`, `D`, `PC`, and the RAM words you touch. Nothing else exists.
4. For each C-instruction, decode in this order: `a`-bit → `y`; `c1..c6` → the ALU operation; `d1d2d3` → what gets loaded; `j1j2j3` + `zr`/`ng` → the next PC.
5. When a jump is taken, the next PC is **A**, not the label's line number.
6. When a program misbehaves, compare your trace with the CPU emulator's A, D, PC and RAM panes. The first cycle they disagree is the bug.

---



# Part 6 — The inverse function, and the seven projects ahead



## 6.1 The one table that ties hardware to software


| The CPU **reads** this bit | Its wire does this       | Your assembler **writes** this bit      |
| -------------------------- | ------------------------ | --------------------------------------- |
| 15                         | Chooses A-mode or C-mode | `0` for `@x`, `1` for a C-instruction   |
| 14-13                      | Nothing                  | `11` by convention                      |
| 12                         | Selects ALU `y` = A or M | The `a`-bit implied by `D+A` vs `D+M`   |
| 11-6                       | Sets `zx nx zy ny f no`  | The 6 bits of the comp mnemonic         |
| 5                          | `loadA`                  | `1` if `A` appears in dest              |
| 4                          | `loadD`                  | `1` if `D` appears in dest              |
| 3                          | `writeM`                 | `1` if `M` appears in dest              |
| 2                          | Jump if `ng`             | `1` if the jump is `<0`, `!=0` or `<=0` |
| 1                          | Jump if `zr`             | `1` if the jump is `=0`, `>=0` or `<=0` |
| 0                          | Jump if `>0`             | `1` if the jump is `>0`, `>=0` or `!=0` |


Same table, read top-down by hardware and bottom-up by software. **An assembler is not a translator between two unrelated notations; it is the same table with the arrows reversed.** If you understand the CPU decode table, project 6 is bookkeeping.

## 6.2 Project 6 — the Assembler

**What it produces:** a text file where each line is exactly sixteen `0`/`1` characters, one per instruction, ready to load into `ROM32K`.

**The algorithm, in the order that avoids pain:**

1. **Pass 1 — collect labels, ignore everything else.** Walk the source, strip comments and whitespace, and count instructions. Maintain `romAddress = 0`; when you see `(NAME)`, record `NAME → romAddress` and emit nothing; for every A- or C-instruction, increment `romAddress`. This is why labels can be used before they are declared.
2. **Pass 2 — emit.** For each A-instruction: resolve the symbol, or allocate a variable if it is new (`nextRam++` starting at 16), then emit `0` + 15 bits. For each C-instruction: split `dest=comp;jump`, look up comp (which chooses the `a`-bit too), OR together the dest bits and the jump bits, and emit `111` + `a` + `comp` + `dest` + `jump`.
3. **Predefined symbols first.** `R0`-`R15`, `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `SCREEN`, `KBD` are bound before pass 1 and must never be allocated as variables.
4. **Write clean output.** One 16-character line per real instruction, no comments, no blank lines.

A skeleton that shows the shape (the tables are in the cheat sheet):

```python
predef = {"R%d"%i: i for i in range(16)}
predef.update({"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576})

lines = list(cleaned_lines(src))          # materialize: both passes walk the same lines

labels, rom = {}, 0
for line in lines:
    if line.startswith("("):  labels[line[1:-1]] = rom      # emits no instruction
    else:                     rom += 1

symtab, next_ram = dict(predef, **labels), 16
for line in lines:
    if line.startswith("("):  continue
    if line.startswith("@"):
        s = line[1:]
        if s.isdigit():       value = int(s)                # a literal, never a symbol
        elif s in symtab:     value = symtab[s]
        else:                 symtab[s] = next_ram; value = next_ram; next_ram += 1
        emit("0" + format(value, "015b"))
    else:
        dest, comp, jump = split_c_instruction(line)   # split on '=' first, then ';'
        emit("111" + a_bit(comp) + COMP[comp] + DEST[dest] + JUMP[jump])
```

**The bugs that catch everyone:**

- **Counting label lines as instructions** in pass 1. Every jump target after the first label is then off by one.
- **Splitting** `dest=comp;jump` **in the wrong order.** Split on `=` first, then on `;`. `D=D-M;JGE` has both; `0;JMP` has no `=`; `M=D` has no `;`.
- **Treating mnemonics as case-insensitive.** `d=m` is not an instruction, and `@foo` / `@Foo` are two different variables.
- **Allocating predefined symbols as variables**, which silently shifts every later variable by a few addresses.
- **Not checking for a numeric constant before the symbol table.** `@3` is a literal. Treat it as a name and you allocate a variable called `3`, shifting every later variable.
- **Forgetting that variables are allocated in order of first appearance across the whole file**, including forward references from earlier lines.



## 6.3 Projects 7-8 — the VM translator

Here is where the machine model pays off, because the VM is a deliberately tiny stack machine that must be *implemented in Hack assembly* — by the assembler you just wrote.

**Why a stack machine?** Because an expression like `(a+b)*(c-d)` has a tree shape, and a stack is the cheapest way to linearize a tree into instructions. The compiler (projects 10-11) emits stack code; the VM translator (7-8) turns stack code into Hack assembly; the assembler (6) turns that into bits.

**The five predefined symbols finally earn their keep.** Chapters 4-5 told you to ignore `SP`, `LCL`, `ARG`, `THIS`, `THAT`. They are the VM's fixed registers, pre-bound to RAM 0-4:


| Symbol | RAM | VM role                                                |
| ------ | --- | ------------------------------------------------------ |
| `SP`   | 0   | stack pointer: the address of the next free stack slot |
| `LCL`  | 1   | base of the current function's local segment           |
| `ARG`  | 2   | base of the current function's argument segment        |
| `THIS` | 3   | base of the current object (`this`)                    |
| `THAT` | 4   | base of the current array (`that`)                     |


And the VM's memory segments map onto addressing modes you already know:


| VM segment               | Hack address                  | Why                                     |
| ------------------------ | ----------------------------- | --------------------------------------- |
| `constant i`             | the literal `i`               | no memory at all                        |
| `local i` / `argument i` | `RAM[LCL+i]` / `RAM[ARG+i]`   | pointer plus offset — the `A=D+M` idiom |
| `this i` / `that i`      | `RAM[THIS+i]` / `RAM[THAT+i]` | same, for objects and arrays            |
| `temp i`                 | `RAM[5+i]`                    | fixed scratch                           |
| `pointer 0/1`            | `RAM[3]` / `RAM[4]`           | writes `THIS`/`THAT`                    |
| `static i`               | `RAM[16+i]`                   | one block per compiled file             |


**Three translations to have in your head** (project 7):

```
// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
```

```
// pop local 1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
```

```
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
```

Project 8 adds branching (`label`, `goto`, `if-goto`) and function call/return, which is where the frame layout matters: a call pushes the return address, then `LCL, ARG, THIS, THAT`, then points `ARG` at `SP-5-nArgs` and `LCL` at `SP`. Return restores all five and jumps to the saved address.

Note how much the VM leans on the timing rule from Part 2. `AM=M-1` touches memory *and* A in the same instruction: the store targets `RAM[A]` using A's value from before the instruction, while A itself takes its new value at the tick. One instruction, two effects, both committed at the end of the cycle. Every `push` and `pop` depends on that.

> **The mental model to carry into 7-8:** every VM command is 1-15 Hack instructions, and every one of them is an `@` line followed by a C line. You are writing a macro expander whose output happens to be a language you can now reason about bit by bit.



## 6.4 Project 9 — the Jack application

No new machine knowledge at all. You write a program in Jack (the high-level language), compile it with the **supplied** compiler, and run it on the **supplied** VM emulator. It is a checkpoint that the machine can host real software: sprites, game loops, keyboard polling.

Two connections back to chapters 1-5: the game loop is the `(LOOP) @LOOP 0;JMP` skeleton, and every visible pixel is still a bit in `RAM[16384..24575]` that your `Screen.drawPixel` will set by read-modify-write. The supplied OS hides that; project 12 makes you write it.

## 6.5 Projects 10-11 — the compiler

**Project 10** is a tokenizer and a recursive-descent parser that emits an XML view of the program's structure. No code generation. **Project 11** adds code generation: for every construct, emit VM code.

The machine model enters through the code generator:

- Every arithmetic operator becomes a VM `add`/`sub`/`and`/`or`/`not`/`neg`, which becomes the ALU setting you saw in Part 1. There is no other arithmetic available anywhere.
- Every `a[i]` becomes `push a; push i; add; pop pointer 1; push that 0` — the `A=D+M` pointer idiom, wrapped in VM commands.
- Every object field access `obj.field` becomes the same thing through `this`.
- Every `if`/`while` becomes `label`/`goto`/`if-goto`, which become `@LABEL / 0;JMP` and `@LABEL / D;JNE` after projects 7-8, and then 16-bit words after project 6.

When you write the code generator, you are choosing which of the four idioms from Part 3 to emit. That is the entire job.

## 6.6 Project 12 — the operating system

Seven or so Jack classes (`Math`, `String`, `Array`, `Memory`, `Screen`, `Keyboard`, `Output`, `Sys`) written in Jack, compiled by your own compiler. Here the consequences of the hardware choices become visible:

- **No multiply, no divide, no shift in the ALU.** `Math.multiply` is shift-and-add, `Math.divide` is repeated subtraction with shifting, `Math.sqrt` is a search. Every one of them is a loop over `+`, `-`, `&`, `|` and `!` — the only operations that exist in silicon.
- **RAM is 16K words, addresses 16..16383 are the whole playground.** `Memory.alloc` is a first-fit allocator over a heap that starts at 2048; `deAlloc` has to coalesce free blocks. Every object your compiler creates comes from this function.
- **The screen is bits in words.** `Screen.drawPixel` is `word = RAM[16384 + 32*row + col/16]`, set or clear bit `col%16` by masking, store back. `drawLine`, `drawRectangle` and `drawCircle` are all that operation in a loop.
- **No interrupts, no keyboard buffer.** `Keyboard.readChar` is a polling loop over `RAM[24576]`, waiting for a nonzero code and then waiting for zero so one keypress produces one character.
- `Sys.init` **sets** `SP = 256` and calls `Main.main` — the first thing that runs after reset, because ROM address 0 is whatever the OS loader put there.

> **The closing thought.** Nothing in projects 6-12 invents new hardware. Every one of them manipulates the same three registers, the same two memories, and the same 16-bit words you traced in Part 5. That is the point of building the machine first.



### The roadmap on one page


| Project            | You build                                                                  | Stands on                                                    | The hard part                                                     |
| ------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------- |
| **6** Assembler    | `.asm` → `.hack`                                                           | The CPU decode table (4.2)                                   | Two passes: labels are ROM addresses, variables are RAM addresses |
| **7** VM I         | Stack arithmetic + memory access → `.asm`                                  | `SP`/`LCL`/`ARG`/`THIS`/`THAT` = RAM 0-4, the `A=D+M` idiom  | Keeping the stack pointer contract exact                          |
| **8** VM II        | Branching + function call/return                                           | The frame layout and the PC's `load` pin                     | The 5-word frame; one wrong offset breaks every call              |
| **9** Jack app     | A program in Jack                                                          | Keyboard/screen polling, game loop                           | Design, not machine knowledge                                     |
| **10** Compiler I  | Tokenizer + parser → XML                                                   | Jack grammar                                                 | Recursive descent, lookahead for `<` vs `<`                       |
| **11** Compiler II | Jack → VM code                                                             | The four idioms (3.7), ALU operations                        | Expression evaluation order on the stack                          |
| **12** OS          | `Math`, `Memory`, `Screen`, `Keyboard`, `Output`, `Sys`, `String`, `Array` | Everything: no multiply in the ALU, RAM map, screen bit math | `Memory.alloc` and `Math.divide`                                  |


---



# Cheat sheet



## Instruction formats

```
A-instruction   0 vvvvvvvvvvvvvvv          bit 15 = 0; v = 0..32767 (decimal or symbol)

C-instruction   1 1 1 a c1c2c3c4c5c6 d1d2d3 j1j2j3

                bit 15        = 1
                bits 14-13    = 11   (unused, convention)
                bit 12        = a    ALU y = A (0) or M (1)
                bits 11-6     = comp c1..c6 = ALU zx nx zy ny f no
                bits 5-3      = dest d1 A, d2 D, d3 M
                bits 2-0      = jump j1 <0, j2 =0, j3 >0
```



## comp (28 valid mnemonics)


| `a=0` | `a=1` | bits     |     | `a=0` | `a=1` | bits     |
| ----- | ----- | -------- | --- | ----- | ----- | -------- |
| `0`   |       | `101010` |     | `D+1` |       | `011111` |
| `1`   |       | `111111` |     | `A+1` | `M+1` | `110111` |
| `-1`  |       | `111010` |     | `D-1` |       | `001110` |
| `D`   |       | `001100` |     | `A-1` | `M-1` | `110010` |
| `A`   | `M`   | `110000` |     | `D+A` | `D+M` | `000010` |
| `!D`  |       | `001101` |     | `D-A` | `D-M` | `010011` |
| `!A`  | `!M`  | `110001` |     | `A-D` | `M-D` | `000111` |
| `-D`  |       | `001111` |     | `D&A` | `D&M` | `000000` |
| `-A`  | `-M`  | `110011` |     | `D    | A`    | `D       |




## dest and jump


| dest     | bits  |     | jump     | bits  | condition |
| -------- | ----- | --- | -------- | ----- | --------- |
| *(none)* | `000` |     | *(none)* | `000` | never     |
| `M`      | `001` |     | `JGT`    | `001` | out > 0   |
| `D`      | `010` |     | `JEQ`    | `010` | out = 0   |
| `DM`     | `011` |     | `JGE`    | `011` | out >= 0  |
| `A`      | `100` |     | `JLT`    | `100` | out < 0   |
| `AM`     | `101` |     | `JNE`    | `101` | out != 0  |
| `AD`     | `110` |     | `JLE`    | `110` | out <= 0  |
| `ADM`    | `111` |     | `JMP`    | `111` | always    |




## Common instructions, pre-encoded

Use these to sanity-check your project 6 output.


| Symbolic              | Binary             | Hex      |
| --------------------- | ------------------ | -------- |
| `@0`                  | `0000000000000000` | `0x0000` |
| `@21`                 | `0000000000010101` | `0x0015` |
| `@i` (first variable) | `0000000000010000` | `0x0010` |
| `@SCREEN`             | `0100000000000000` | `0x4000` |
| `@KBD`                | `0110000000000000` | `0x6000` |
| `D=A`                 | `1110110000010000` | `0xEC10` |
| `D=M`                 | `1111110000010000` | `0xFC10` |
| `M=D`                 | `1110001100001000` | `0xE308` |
| `A=M`                 | `1111110000100000` | `0xFC20` |
| `A=D+M`               | `1111000010100000` | `0xF0A0` |
| `D=D+A`               | `1110000010010000` | `0xE090` |
| `D=D+1`               | `1110011111010000` | `0xE7D0` |
| `M=0`                 | `1110101010001000` | `0xEA88` |
| `M=1`                 | `1110111111001000` | `0xEFC8` |
| `M=-1`                | `1110111010001000` | `0xEE88` |
| `M=M+1`               | `1111110111001000` | `0xFDC8` |
| `M=M-1`               | `1111110010001000` | `0xFC88` |
| `AM=M-1`              | `1111110010101000` | `0xFCA8` |
| `D;JGT`               | `1110001100000001` | `0xE301` |
| `D;JEQ`               | `1110001100000010` | `0xE302` |
| `D;JNE`               | `1110001100000101` | `0xE305` |
| `D=D-M;JGE`           | `1111010011010011` | `0xF4D3` |
| `0;JMP`               | `1110101010000111` | `0xEA87` |




## Memory map


| Address     | Device          | Notes                                                  |
| ----------- | --------------- | ------------------------------------------------------ |
| 0-15        | `R0`-`R15`      | `SP`=0, `LCL`=1, `ARG`=2, `THIS`=3, `THAT`=4           |
| 16-16383    | variables, heap | assembler allocates from 16; OS heap starts at 2048    |
| 16384-24575 | Screen          | 8K words, 32 per row, 256 rows × 512 pixels            |
| 24576       | Keyboard        | read-only, code of the key held now, else 0            |
| 24577-32767 | invalid         | the simple Memory chip aliases these onto the keyboard |


```
pixel(row, col) → word 16384 + 32*row + col/16   (integer division)
                 → bit  col % 16                 (bit 0 = leftmost, 1 = black)
```



## CPU: bit → wire


| Bit   | Wire        | Effect                                                       |
| ----- | ----------- | ------------------------------------------------------------ |
| 15    | `isC`       | `0` = load the whole word into A; `1` = decode               |
| 14-13 | —           | ignored                                                      |
| 12    | Mux16 sel   | ALU `y` = A (0) or `inM` (1)                                 |
| 11-6  | ALU control | `zx nx zy ny f no`                                           |
| 5     | `loadA`     | with `isC`, A ← ALU out                                      |
| 4     | `loadD`     | with `isC`, D ← ALU out                                      |
| 3     | `writeM`    | with `isC`, `RAM[A]` ← ALU out                               |
| 2-0   | jump        | with `isC`, PC ← A when `(j1&ng) OR (j2&zr) OR (j3&!zr&!ng)` |


`x` is always D. `addressM = A[0..14]`, `pc = PC[0..14]`, `outM = aluOut` (combinational). PC priority: `reset > load > inc`.

## The ALU's 18 settings

`zx nx zy ny f no` → `out`

```
101010→0    111111→1    111010→-1   001100→D    110000→A/M
001101→!D   110001→!A/M 001111→-D   110011→-A/M 011111→D+1
110111→A+1/M+1  001110→D-1   110010→A-1/M-1
000010→D+A/D+M  010011→D-A/D-M   000111→A-D/M-D
000000→D&A/D&M  010101→D|A/D|M
zr = (out == 0)   ng = out[15]
```



## 16-bit constants


| Value            | Binary                | Hex      |
| ---------------- | --------------------- | -------- |
| 0                | `0000 0000 0000 0000` | `0x0000` |
| 1                | `0000 0000 0000 0001` | `0x0001` |
| -1               | `1111 1111 1111 1111` | `0xFFFF` |
| 16384 (`SCREEN`) | `0100 0000 0000 0000` | `0x4000` |
| 24576 (`KBD`)    | `0110 0000 0000 0000` | `0x6000` |
| 32767 (max)      | `0111 1111 1111 1111` | `0x7FFF` |
| -32768 (min)     | `1000 0000 0000 0000` | `0x8000` |




## The traps, in one list

1. `@` **takes 0-32767 only.** Bit 15 is the opcode. Negative constants must be computed (`@5 / D=-A`).
2. `M` **means** `RAM[A]` **for the current A.** After `A=D+M`, the *next* instruction's `M` is the new address.
3. **A jump goes where A points**, and A is read *before* this instruction's write. Never combine `A=...` with a jump.
4. **Do not use** `M` **and jump in the same instruction.** One A, two purposes.
5. **Jump conditions test this instruction's comp result**, not D. `D=D-M;JGT` tests `D-M`.
6. **Labels are ROM addresses; variables are RAM addresses.** A label produces no instruction — do not count its line.
7. **Screen bit 0 is the leftmost pixel** of its 16-pixel group, not the rightmost.
8. **Writes need a clock tick; reads do not.** After `load=1`, the new value appears next cycle.
9. **The A-instruction's value bits overlap the dest/jump fields** — that is exactly why `loadA`, `loadD`, `writeM` and the PC load are ANDed with `isC`.
10. `outM` **is meaningless when** `writeM=0`**.** Nothing is guaranteed about it.
11. **Hack has no interrupts, no halt, and no overflow flag.** Programs end in `(END) @END 0;JMP`.
12. **The ALU cannot multiply, divide or shift.** All of that is project 12 software.

---



# Self-check: can you rebuild the machine from memory?

Answer these without looking. If you can do all twelve, you have the model.

1. Why does `Nand` alone suffice, and what does `DFF` add that no combination of `Nand`-built combinational gates can?
2. What are the two inputs the ALU's `y` can take, and which bit chooses?
3. Why is `zx=1, nx=1` equal to `-1` rather than `0`?
4. Write `Bit` in one sentence: what does `load` actually do, structurally?
5. Why can RAM be read in the same cycle but not written in the same cycle?
6. The PC receives an instruction to do three contradictory things at once. How is priority implemented?
7. Explain to someone why `@8` would corrupt memory if `writeM` were not ANDed with `isC`.
8. Decode `1111000010100000` by hand: comp, dest, jump, and what happens to A, D and M.
9. A C-instruction reads `M` and has `j1j2j3 = 011`. Why is this a bad idea even though the encoding is legal?
10. Where does the value of `(LOOP)` come from, and how is it different in kind from the value of `@i`?
11. Which single bit of an A-instruction decides whether the following C-instruction acts on `RAM[A]` or jumps to `ROM[A]`?
12. Your compiler must generate `x = a[i]`. Which two-instruction pattern does it emit, and what does the second instruction's `M` refer to?

Answers

1. `{And, Or, Not}` is functionally complete and each of the three is a Nand wiring, so every Boolean function is reachable. `DFF` adds *time*: it makes an output depend on a previous cycle, which is what allows feedback and therefore state.
2. `A` or `M` (`inM`), chosen by instruction bit 12, the `a`-bit — which is also part of the comp field.
3. Zeroing is applied before negating in the ALU pipeline, so `x=0` becomes `!0` = all ones = `-1`.
4. `load` is the select input of a Mux that chooses between the incoming value and the chip's own previous output, with a DFF holding the result.
5. A read is a `Mux8Way16` over the register outputs — pure combinational logic, valid immediately. A write must change a DFF, and DFFs commit only at the clock edge.
6. As a chain of Mux16s where the last stage wins: `inc`, then `load`, then `reset`. Whatever the final Mux selects is what the register takes.
7. `@8` is `0000000000001000`; bit 3 is 1, and bit 3 is the `writeM` position of a C-instruction. Without `isC` gating, the CPU would treat the constant's bit as a store signal and write garbage to `RAM[8]`.
8. `1` = C-instruction, `11` ignored, `a=1`, `c=000010` = `D+M`, `d1d2d3=100` = dest A, `jjj=000` = no jump. So `A=D+M`: A takes the ALU result at the tick, D and M are unchanged.
9. A C-instruction that uses `M` reads `RAM[A]`, and a jump goes to `ROM[A]`. Both use the same A, so one of the two uses is almost certainly wrong. The convention is to avoid the combination.
10. `(LOOP)` is the ROM address of the next real instruction — the assembler counts instructions, not lines. `@i` is a *RAM* address allocated from 16 upward in order of first appearance.
11. None of them. The A-instruction only supplies a number; the *next* C-instruction decides whether A is an address for `M` or a jump target.
12. `@a` then `D=M` to get the base, `@i` then `A=D+M` to form the address, then `M=D` (or `D=M`) to act. The second instruction's `M` refers to `RAM[base+i]` because `A=D+M` landed at the previous tick.

---



# Where this came from

Chapters 1-5 of *The Elements of Computing Systems* (Nisan & Schocken, 2nd ed., MIT Press), cross-checked against the chapter-by-chapter refresher notes. Every hand-encoded instruction in the tables was verified programmatically, not typed from memory.

Next action: open the project 6 folder, write the pass-1 label collector, and check `@2 / D=A / @3 / D=D+A / @0 / M=D` against the six words encoded in Part 5.1.