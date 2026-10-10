Nand2Tetris · The Elements of Computing Systems, 2nd ed.

# Hack refresher: chapters 1 to 5

Everything you built before the assembler, from Nand to the Computer chip. Start with the checklist below. If you can do every item, start chapter 6. If not, open the chapter it points to.

[**✓**Ready for ch 6?](#ready) [**1**Boolean Logic](#ch1)[**2**Boolean Arithmetic](#ch2)[**3**Memory](#ch3)[**4**Machine Language](#ch4)[**5**Computer Architecture](#ch5)

Before chapter 6

## Ready for the assembler?

You have built the full Hack computer from Nand gates up: logic gates (ch1), the adder and ALU (ch2), registers, RAM and the program counter (ch3), the machine language spec (ch4), and the CPU, Memory and Computer chips (ch5). That machine runs only 16-bit binary words, so the next layer is the first piece of software, a translator from the human-readable Hack assembly you wrote in chapter 4 to the binary that your chapter 5 Computer loads into ROM. It closes Part I, and Part II then builds software on top of it.

- [ ] Ch 2 Be able to convert a non-negative decimal number to a fixed-width binary string, and say why 15 bits stop at 32767 (2^15 - 1) while a 16-bit word holds two's-complement values from -32768 to 32767.Chapter 6 treats an A-instruction constant as a decimal from 0 to 32767 that ends up as bits in a 16-bit word. You need to know the bit width and range without stopping to think.
- [ ] Ch 4 Be able to write the binary form of an A-instruction (@value): the top bit is 0 and the low 15 bits hold the value. Also know the three things the loaded A register can be: a data constant, the RAM address that M refers to, or the ROM address a jump goes to.Every @xxx line in chapter 6 means one of these three things. Which one it is affects what a name after @ stands for.
- [ ] Ch 4 Be able to split a C-instruction 'dest=comp;jump' into its parts, say which parts are optional (dest= and ;jump), and lay out its 16-bit binary form: 111 a c1..c6 d1 d2 d3 j1 j2 j3.Chapter 6 assumes you know this layout and repeats the encoding table (Figure 6.2) only as a reference. Knowing where each field sits in the word makes that table easy to read.
- [ ] Ch 2 Be able to explain the a-bit and the six c-bits: a=0 means the ALU's y input is A, a=1 means it is M (RAM\[A\]). The c-bits are the ALU control pins zx, nx, zy, ny, f, no from chapter 2. So 'D+A' and 'D+M' differ only in the a-bit.The comp table in chapter 6 is easier to read when you see it as ALU settings, not 28 random bit patterns. You also need to see why each comp has an A version and an M version.
- [ ] Ch 4 Be able to give the 3-bit dest code (d1=A, d2=D, d3=M, so 'AM' is 101 and 'AMD' is 111) and the 3-bit jump code (j1 means out\<0, j2 means out=0, j3 means out>0, so JGT=001, JEQ=010, JMP=111, and no jump is 000).These two small tables follow simple bit rules. If you remember the rules, the dest and jump encodings in chapter 6 are obvious.
- [ ] Ch 5 Be able to tell the two separate address spaces apart. ROM (instruction memory, 32K words) holds the program, and the PC indexes it from address 0. RAM (data memory) holds data, and A/M index it. Also know that the CPU treats a word whose top bit is 0 as an A-instruction and any other word as a C-instruction.Chapter 6 talks about where instructions sit in memory and where named values live. You need to know at once whether an address points into ROM or RAM.
- [ ] Ch 5 Be able to recite the Hack memory map: RAM 0-16383 is general data, 16384-24575 is the screen memory map (SCREEN), and 24576 is the keyboard register (KBD).Chapter 6 lists the predefined names and their addresses. Knowing the memory map tells you why SCREEN and KBD have those values.
- [ ] Ch 4 Be able to list the three kinds of symbols in Hack assembly. Predefined: R0-R15 = 0-15, SP/LCL/ARG/THIS/THAT = 0-4, SCREEN, KBD. Labels: written (LABEL), they mark a place in the code and produce no instruction. Variables: other @name symbols, which go to RAM starting at address 16.Chapter 6 assumes you already know these rules as a programmer. Have them fresh so you can focus on the new ideas in the chapter.
- [ ] Ch 4 Be able to read and write short Hack assembly programs with labels, variables and jumps, such as '@LOOP / 0;JMP', 'D;JGT', 'M=M+1', and the pointer and screen-loop patterns from project 4 (Mult, Fill).Chapter 6 uses an example program (Figure 6.1) and test programs (Add, Max, Rect, Pong). You need to follow what they do line by line.
- [ ] Ch 4 Be able to describe the file formats and tools. A .asm file is text with // comments, blank lines and indentation, and mnemonics are uppercase while labels and variables are case-sensitive. A .hack file is text where each line is sixteen '0'/'1' characters. A .hack file runs in the supplied CPU Emulator.Your input and output for the chapter 6 project are these two text formats. The CPU Emulator (and the supplied assembler) is how you will check results.

Ch 1

## Boolean Logic

[ ] Refreshed

Chapter 1 starts from one given gate, Nand, and builds the 15 gates that the later chips use. These are Not, And, Or, Xor, Mux and DMux; the 16-bit gates Not16, And16, Or16 and Mux16; and the multi-way gates Or8Way, Mux4Way16, Mux8Way16, DMux4Way and DMux8Way. The chapter also introduces the course HDL, test scripts (.tst/.cmp) and the hardware simulator. You use all three in every hardware chapter.

Keep this one idea

You can build any Boolean function from Nand gates only. Every chip has one interface (what it does) and many possible implementations (how it is wired from simpler chips). To use a chip as a part, you only need its interface.

Key concepts 19

Boolean function

A function that takes binary inputs (0/1) and returns a binary output. With n inputs, there are 2^n input rows and 2^(2^n) different functions. For 2 inputs, that gives 16 functions: And, Or, Nand, Nor, Xor, Equivalence, the two constants, and others (see the table below).

Notation

And is written x·y, Or is written x+y, and Not is written x with a bar over it. The prefix form is also used, for example And(Or(x,y), Not(z)).

Truth table vs. Boolean expression

There are two ways to define the same function. A truth table lists the output for each of the 2^n rows, and it is unique. Many different expressions can match one table. Example: f(x,y,z) = (x Or y) And Not(z) is 1 only when (x=1 or y=1) and z=0, which is rows 3, 5 and 7 of the table. You can always build the table from an expression, and you can always build an expression from a table (appendix 1 proves this). A simpler expression needs fewer gates. Example: Not(x And y) And (Not(x) Or y) And (Not(y) Or y) reduces to Not(x).

Universality of Nand

The set {And, Or, Not} can express any Boolean function. You can build each of these three from Nand, so Nand alone is enough. Nor alone is also enough. Nand(a,b) = Not(And(a,b)).

Gate / chip

A device that implements a Boolean function. The book uses the two words for the same thing and uses 'gate' for simple chips. You treat gates as black boxes, and the physics (transistors, silicon) is out of scope. In 1937, Claude Shannon's M.Sc. thesis used Boolean algebra to analyze the abstract behavior of logic gates.

Interface vs. implementation

The interface gives the chip name, the names of its input and output pins, and its behavior. There is only one interface, given as a truth table, an expression or a text description. The implementation is the internal wiring of parts, and many implementations can exist. The goal is to match the interface with as few parts as possible. Fewer parts means less cost, less energy and faster computation.

API style

The book specifies every chip in the same form: Chip name, Input, Output, Function and an optional Comment. Example: Chip name Nand; Input a, b; Output out; Function: if a==b==1 then out=0 else out=1. Appendix 4 lists the APIs of all the course chips.

Composite gate

A gate built from other gates. Example: And3(a,b,c) = And(And(a,b),c). After you build it, you can use it as a building block in other chips.

HDL (Hardware Description Language)

A text description of a chip. A CHIP block has a header (IN/OUT declarations, which form the interface) and a PARTS: section. Each part statement names a chip and connects its pins: PartName(partPin=myPinOrWire, ...). The left side of each '=' is a pin of the part. The right side is an input, output or internal pin of the chip you are building. In a supplied stub file, you write only under PARTS. You must not change the header.

Internal pins (wires)

An internal pin is created automatically the first time its name appears (example: Not(in=a, out=nota)). You can then use it as an input of other parts. A pin has fan-in 1, so only one source can drive it. A pin has unlimited fan-out, so one signal can feed any number of parts. In a diagram, fan-out is drawn as a fork. The width of an internal pin comes from the binding that creates it.

Hardware simulator

A program in nand2tetris/tools. It loads .hdl files, runs .tst test scripts, writes an .out file and compares that file line by line with the supplied .cmp file. It stops with an error message at the first line that does not match.

Test script (.tst)

A test script loads the chip and declares an output-list. Then it repeats a set of steps: set inputs, eval, output. A small gate can have an exhaustive test that tries every input combination. Larger chips cannot be tested exhaustively. You must be able to read test scripts, but you do not need to write them. Tip: if you delete the compare-to line, the test runs to the end and does not stop at the first mismatch.

Behavioral simulation / built-in chips

The simulator contains software (Java) versions of the course chips. You can use these chips before you build them. A built-in .hdl file has the same interface as your chip, but its PARTS section is replaced by 'BUILTIN Xxx;'. The matching Xxx.class file is in nand2tetris/tools/builtIn. Nand is always built-in, because it is the primitive gate.

Chip lookup rule

When the simulator meets a part Xxx, it first looks for Xxx.hdl in the current folder. If that file is not there, it uses tools/builtIn/Xxx.hdl. If neither file exists, it reports an error and stops. Trick: if your Mux.hdl is not finished, rename it to Mux1.hdl and the simulator uses the built-in Mux.

Multiplexer (Mux)

A selector with data inputs a and b and a select bit sel. If sel=0, out = a. If sel=1, out = b. The name comes from communications systems, where multiplexing sends several signals over one channel. Later chips use Mux to choose between data paths.

Demultiplexer (DMux)

The opposite of Mux. It sends in to output a when sel=0, or to output b when sel=1. The output that is not selected is 0.

Multi-bit (bus) gates

Not16, And16, Or16 and Mux16 apply the 1-bit gate to each bit position separately. Mux16 sends the same sel to all 16 one-bit Muxes. The design is the same for any width n (16, 32, 64).

Bit indexing

Bits are numbered from right to left. Bit 0 is the rightmost (least significant) bit, and bit 15 is the leftmost bit of a 16-bit value. In HDL, in\[5\] is one bit and in\[0..7\] is a sub-bus. Example: out\[3\]=in\[5\] sets bit 3 of out to bit 5 of in.

Multi-way gates

An m-way Or (Or8Way) outputs 1 if at least one of its m input bits is 1. It has no select input. An m-way Mux or DMux uses k = log2(m) select bits: 4-way uses sel\[2\] and 8-way uses sel\[3\]. With sel\[1\]sel\[0\] = 00, 01, 10, 11, the chip selects a, b, c, d. The project needs 16-bit multi-way Muxes (Mux4Way16, Mux8Way16) and 1-bit multi-way DMuxes (DMux4Way, DMux8Way). The book's only tip is 'think forks': build them as trees of smaller Mux or DMux chips.

Chips 16

| Chip | Interface | Behavior | Built from |
| --- | --- | --- | --- |
| Nand | IN a, b (1 bit each); OUT out (1 bit) | out = 0 only when a=1 and b=1. Otherwise out = 1. | Primitive, built into the simulator. You do not implement it. |
| Not | IN in; OUT out | Inverter: out is the opposite of in. | One Nand with both inputs connected to in: Nand(a=in, b=in, out=out). |
| And | IN a, b; OUT out | out = 1 only if a=1 and b=1. | A Nand, then a Not on its output. |
| Or | IN a, b; OUT out | out = 1 if a=1 or b=1, or both. | De Morgan: Or(a,b) = Not(And(Not a, Not b)), which equals Nand(Not a, Not b). |
| Xor | IN a, b; OUT out | out = 1 when exactly one input is 1 (a != b). | Or(And(a, Not b), And(Not a, b)), as in figure 1.7. A smaller version: And(Or(a,b), Nand(a,b)). |
| Mux | IN a, b, sel; OUT out | If sel=0, out = a. Otherwise out = b. | Or(And(a, Not sel), And(b, sel)). |
| DMux | IN in, sel; OUT a, b | sel=0: {a,b} = {in,0}. sel=1: {a,b} = {0,in}. | a = And(in, Not sel), b = And(in, sel). |
| Not16 | IN in\[16\]; OUT out\[16\] | out\[i\] = Not(in\[i\]) for i = 0..15. | 16 Not gates, one for each bit. |
| And16 | IN a\[16\], b\[16\]; OUT out\[16\] | out\[i\] = And(a\[i\], b\[i\]) for each bit. | 16 And gates. |
| Or16 | IN a\[16\], b\[16\]; OUT out\[16\] | out\[i\] = Or(a\[i\], b\[i\]) for each bit. | 16 Or gates. |
| Mux16 | IN a\[16\], b\[16\], sel (1 bit); OUT out\[16\] | If sel=0, out = a. Otherwise out = b. All 16 bits are selected together. | 16 Mux gates that share the same sel. |
| Or8Way | IN in\[8\]; OUT out (1 bit) | out = Or(in\[0\], in\[1\], ..., in\[7\]): 1 if any input bit is 1. | 7 Or gates in a chain or a tree. |
| Mux4Way16 | IN a\[16\], b\[16\], c\[16\], d\[16\], sel\[2\]; OUT out\[16\] | sel 00 -> a, 01 -> b, 10 -> c, 11 -> d. The selection copies all 16 bits. | Two Mux16 on sel\[0\] (one for a/b, one for c/d), then one Mux16 on sel\[1\]. |
| Mux8Way16 | IN a\[16\], b\[16\], c\[16\], d\[16\], e\[16\], f\[16\], g\[16\], h\[16\], sel\[3\]; OUT out\[16\] | sel 000 -> a, 001 -> b, ..., 111 -> h. | Two Mux4Way16 on sel\[0..1\] (one for a..d, one for e..h), then one Mux16 on sel\[2\]. |
| DMux4Way | IN in, sel\[2\]; OUT a, b, c, d (1 bit each) | Sends in to a, b, c or d for sel 00, 01, 10 or 11. The other outputs are 0. | One DMux on sel\[1\] splits in into the a/b half and the c/d half. Then one DMux on sel\[0\] for each half. |
| DMux8Way | IN in, sel\[3\]; OUT a, b, c, d, e, f, g, h (1 bit each) | Sends in to one of 8 outputs, chosen by sel (000 -> a ... 111 -> h). The other outputs are 0. | One DMux on sel\[2\], then two DMux4Way on sel\[0..1\]. |

Reference tables 7

Core 2-input truth tables

| a | b | And | Or | Nand | Nor | Xor |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |

All 16 Boolean functions of two variables (output column for xy = 00, 01, 10, 11)

| Name | Expression | 00 | 01 | 10 | 11 |
| --- | --- | --- | --- | --- | --- |
| Constant 0 | 0 | 0 | 0 | 0 | 0 |
| And | x·y | 0 | 0 | 0 | 1 |
| x And Not y | x·ȳ | 0 | 0 | 1 | 0 |
| x | x | 0 | 0 | 1 | 1 |
| Not x And y | x̄·y | 0 | 1 | 0 | 0 |
| y | y | 0 | 1 | 0 | 1 |
| Xor | x·ȳ + x̄·y | 0 | 1 | 1 | 0 |
| Or | x+y | 0 | 1 | 1 | 1 |
| Nor | Not(x+y) | 1 | 0 | 0 | 0 |
| Equivalence | x·y + x̄·ȳ | 1 | 0 | 0 | 1 |
| Not y | ȳ | 1 | 0 | 1 | 0 |
| If y then x | x+ȳ | 1 | 0 | 1 | 1 |
| Not x | x̄ | 1 | 1 | 0 | 0 |
| If x then y | x̄+y | 1 | 1 | 0 | 1 |
| Nand | Not(x·y) | 1 | 1 | 1 | 0 |
| Constant 1 | 1 | 1 | 1 | 1 | 1 |

Mux / DMux (short form of the truth table)

| sel | Mux out | DMux a | DMux b |
| --- | --- | --- | --- |
| 0 | a | in | 0 |
| 1 | b | 0 | in |

Multi-way selection (sel bits written high bit first)

| sel\[1\] sel\[0\] | Mux4Way16 out | DMux4Way output that gets `in` (others are 0) |
| --- | --- | --- |
| 0 0 | a | a |
| 0 1 | b | b |
| 1 0 | c | c |
| 1 1 | d | d |
| For the 8-way chips, sel\[2..0\] = 000..111 selects a..h. |  |  |

Pin names (you must use these exact names in part statements)

| Chip | Inputs | Outputs |
| --- | --- | --- |
| Nand, And, Or, Xor | a, b | out |
| Not | in | out |
| Mux | a, b, sel | out |
| DMux | in, sel | a, b |
| Not16 | in\[16\] | out\[16\] |
| And16, Or16 | a\[16\], b\[16\] | out\[16\] |
| Mux16 | a\[16\], b\[16\], sel | out\[16\] |
| Or8Way | in\[8\] | out |
| Mux4Way16 | a..d \[16\], sel\[2\] | out\[16\] |
| Mux8Way16 | a..h \[16\], sel\[3\] | out\[16\] |
| DMux4Way | in, sel\[2\] | a, b, c, d |
| DMux8Way | in, sel\[3\] | a..h |

Project 1 chip list (15 chips to implement; Nand is given)

| Group | Chips |
| --- | --- |
| Primitive | Nand (built-in) |
| Basic | Not, And, Or, Xor, Mux, DMux |
| 16-bit | Not16, And16, Or16, Mux16 |
| Multi-way | Or8Way, Mux4Way16, Mux8Way16, DMux4Way, DMux8Way |

Project files for each chip Xxx (nand2tetris/projects/01)

| File | Role |
| --- | --- |
| Xxx.hdl | Stub file with the interface given; you write the PARTS section |
| Xxx.tst | Test script (supplied) |
| Xxx.cmp | Expected output (supplied) |
| Xxx.out | Output that your chip produced; the simulator compares it with .cmp |

Code examples 9

Not from a single Nand: connect both inputs to the same signal hdl

```
CHIP Not {
    IN in;
    OUT out;
    PARTS:
    Nand(a=in, b=in, out=out);
}
```

Xor as in figure 1.7: internal wires nota, notb, w1, w2. Inputs a and b each feed two parts (fan-out). hdl

```
CHIP Xor {
    IN a, b;
    OUT out;
    PARTS:
    Not(in=a, out=nota);
    Not(in=b, out=notb);
    And(a=a, b=notb, out=w1);
    And(a=nota, b=b, out=w2);
    Or(a=w1, b=w2, out=out);
}
```

Or8Way as a tree: index the chip's own input bus bit by bit hdl

```
CHIP Or8Way {
    IN in[8];
    OUT out;
    PARTS:
    Or(a=in[0], b=in[1], out=o01);
    Or(a=in[2], b=in[3], out=o23);
    Or(a=in[4], b=in[5], out=o45);
    Or(a=in[6], b=in[7], out=o67);
    Or(a=o01, b=o23, out=o0123);
    Or(a=o45, b=o67, out=o4567);
    Or(a=o0123, b=o4567, out=out);
}
```

Mux4Way16 as a tree: sel\[0\] on the stage next to a..d, sel\[1\] on the last stage hdl

```
CHIP Mux4Way16 {
    IN a[16], b[16], c[16], d[16], sel[2];
    OUT out[16];
    PARTS:
    Mux16(a=a, b=b, sel=sel[0], out=ab);
    Mux16(a=c, b=d, sel=sel[0], out=cd);
    Mux16(a=ab, b=cd, sel=sel[1], out=out);
}
```

Mux8Way16 reuses Mux4Way16 and passes a 2-bit sub-bus of sel hdl

```
CHIP Mux8Way16 {
    IN a[16], b[16], c[16], d[16], e[16], f[16], g[16], h[16], sel[3];
    OUT out[16];
    PARTS:
    Mux4Way16(a=a, b=b, c=c, d=d, sel=sel[0..1], out=abcd);
    Mux4Way16(a=e, b=f, c=g, d=h, sel=sel[0..1], out=efgh);
    Mux16(a=abcd, b=efgh, sel=sel[2], out=out);
}
```

DMux4Way: the high bit splits first (next to in), then sel\[0\] (next to a..d) hdl

```
CHIP DMux4Way {
    IN in, sel[2];
    OUT a, b, c, d;
    PARTS:
    DMux(in=in, sel=sel[1], a=ab, b=cd);
    DMux(in=ab, sel=sel[0], a=a, b=b);
    DMux(in=cd, sel=sel[0], a=c, b=d);
}
```

Fragment (inside PARTS): split a part's output into sub-buses, and use the constants true/false. You cannot write x\[3\] when x is an internal wire. hdl

```
// x is a 16-bit IN pin of the chip being built
Not16(in=x, out[0..7]=lo, out[8..15]=hi);  // lo, hi: 8-bit internal wires
Mux16(a=x, b=false, sel=s, out=y);           // false = all 16 bits 0
Or8Way(in=lo, out=anyLo);                    // lo is already 8 bits wide
```

Built-in chip: same interface, but BUILTIN replaces PARTS hdl

```
CHIP Xor {
    IN a, b;
    OUT out;
    BUILTIN Xor;   // runs Xor.class from tools/builtIn
}
```

Exhaustive test script for a 2-input gate. Figure 1.7 shows only load and output-list before the set/eval/output steps; the supplied project scripts also contain output-file and compare-to. tst

```
load Xor.hdl,
output-file Xor.out,
compare-to Xor.cmp,
output-list a b out;
set a 0, set b 0, eval, output;
set a 0, set b 1, eval, output;
set a 1, set b 0, eval, output;
set a 1, set b 1, eval, output;
```

Gotchas 11

- In a part statement, the left side of '=' is always a pin of the part, and the right side is a pin or wire of your chip. 'a=a' is normal: the part's pin a gets your chip's input a.
- Use the part's exact pin names: Not uses in/out, And/Or/Xor use a/b/out, and DMux has outputs a/b (not out).
- Bit 0 is the rightmost (least significant) bit. A table written 'sel\[1\] sel\[0\]' shows the high bit first. Later chapters also refer to the bits of a Hack instruction by their positions, so this convention matters.
- In multi-way Mux and DMux trees, connect sel\[0\] to the stage next to the a/b/c/d pins. Connect the high bit to the stage next to the single in or out pin. If you swap them, outputs b and c change places.
- DMux sets the output that is not selected to 0. It does not keep its old value.
- The simulator never reports unconnected pins as errors; it sets them to 0. A misspelled wire, for example Foo(..., sum=sun), creates a new wire. Anything that reads the intended wire then gets 0. If an output is always 0, check your wire names.
- You can index the chip's own IN/OUT pins (in\[3\], a\[0..7\]) and the pins of a part. You cannot index an internal wire. To get part of a wire, take a sub-bus from the part's output, for example out\[0..7\]=lo.
- A pin has fan-in 1: only one source can drive it. Fan-out is unlimited.
- The simulator uses a local Xxx.hdl before the built-in chip. If the local file is broken, every chip that uses Xxx also fails. Rename or remove the file to use the built-in chip instead.
- Only the truth table is unique; many implementations are correct. Use as few parts as possible. Use chips that you already built, not raw Nands.
- Do not create helper chips. Project 1 HDL should use only the chips in this chapter. In a stub file, do not change anything above PARTS.

Self-check: answer first, then reveal 7

1. How do you build Not from Nand?

   Connect the same signal to both Nand inputs: Nand(in, in) = Not(in).
2. How many different Boolean functions of 2 variables exist, and why?

   16\. There are 2^2 = 4 input rows, and each row can output 0 or 1, so there are 2^4 = 16 functions.
3. Which input does Mux4Way16 output when sel = 10 (binary)?

   c. The mapping is 00=a, 01=b, 10=c, 11=d.
4. Which index is the most significant bit of a 16-bit value?

   Bit 15, the leftmost bit. Bit 0 is the rightmost bit.
5. The simulator meets part Foo, and there is no Foo.hdl in the project folder. What does it do?

   It uses tools/builtIn/Foo.hdl, which runs a Java implementation. If that file is also missing, it reports an error and stops.
6. You write Foo(..., sum=sun) by mistake and later use 'sum' as an input. What happens?

   There is no error. The simulator creates a new wire named sun. The wire 'sum' has no source, so it is always 0, and your chip gives wrong outputs.
7. What are the .tst, .cmp and .out files?

   .tst is the test script, .cmp is the expected output, and .out is the output that your chip produced. The simulator compares .out with .cmp and stops at the first line that does not match.

Ch 2

## Boolean Arithmetic

[ ] Refreshed

Chapter 2 uses the chapter 1 gates to build adders (HalfAdder, FullAdder, Add16, Inc16) and then the Hack ALU. The ALU takes two 16-bit inputs and 6 control bits, and it computes one of 18 documented functions. It is the computing core of the CPU. The same 6 bits come back in chapter 4 inside the binary form of Hack C-instructions.

Keep this one idea

Two's complement means signed numbers need no extra hardware. Subtraction is addition of the negation, and negation is 'flip all bits, then add 1'. So one adder plus some zero, negate and select stages can produce every arithmetic and logic function the Hack computer needs.

Key concepts 16

Which operations hardware must support

A general-purpose computer needs addition, sign conversion, subtraction, comparison, multiplication and division on signed integers. Chapter 2 builds hardware only for addition and sign conversion. The others are built on top of those two, some in hardware (subtraction in the ALU) and some in software (multiply and divide in the chapter 12 OS).

Binary (base 2) value

Bit i is worth 2^i. Bit 0 is the rightmost bit (the LSB). Example: 10011 = 16 + 2 + 1 = 19. With n bits and no sign you can count from 0 to 2^n - 1. In 8 bits that is 0..255.

Word size

The fixed number of bits the hardware uses for an integer. Common sizes are 8, 16, 32 and 64, which match the byte, short, int and long types. Hack uses 16 bits for data, registers, the ALU and instructions. To hold bigger values, high-level languages chain several words together, which is slow.

Binary addition and overflow

Add from right to left, one column at a time, and pass the carry into the next column. Book example in 4 bits: 1001 + 0101 = 1110, with no overflow. If the MSB column makes a carry, the book calls that overflow. Example: 1011 + 0111 = 10010. Hack ignores the carry, so the result is correct only in the lower n bits.

Two's complement

For n bits, the code for -x is the unsigned code of 2^n - x. In 4 bits, -7 is 16 - 7 = 9 = 1001. Check: 0111 + 1001 = 0000 after you drop the carry. n bits give 2^n values, from -2^(n-1) to 2^(n-1) - 1. For 16 bits that is -32768..32767. There is one more negative value than positive values, and 0 has only one code.

Sign bit

In two's complement the MSB gives the sign. MSB 0 means zero or positive. MSB 1 means negative. So the ALU's ng output is just out\[15\].

Negation rule

Fast method: -x = (!x) + 1. Flip every bit, then add 1. Hand method: scan from the right, keep all low 0s and the first 1 unchanged, then flip every bit to the left of that 1. A useful identity follows from this: !x = -x - 1.

Subtraction as addition

x - y = x + (-y), so the same adder works for positive, negative and mixed-sign operands. Book examples in 4 bits: 5 - 7 = 0101 + 1001 = 1110 = -2. And (-2) + (-3) = 1110 + 1101 = 11011. Drop the carry to get 1011 = -5.

Half-adder / Full-adder naming

A half-adder adds 2 bits. A full-adder adds 3 bits (a, b and a carry-in). In both, the 2-bit result is carry (MSB) followed by sum (LSB). The names come from how they are built: one full-adder is two half-adders plus one more gate (an Or).

Ripple-carry adder

An n-bit adder is a chain of full-adders. Each carry output feeds the carry input of the next higher bit. Bit 0 has no carry-in, so a half-adder is enough there. In HDL you describe all the bits as if they work at the same time. The carries do take time to ripple through, but the circuit settles within one clock cycle (chapter 3), so you can ignore timing here.

Carry lookahead (perspective only)

A faster adder design that works out the carries in advance instead of waiting for them to ripple. The book does not use it. Its goal is functionality, not speed, and the simulator does not allow the cyclic pin connections that lookahead needs.

ALU control pipeline

The six control bits act in a fixed order. (1) zx/zy: replace x or y with 0. (2) nx/ny: bitwise-NOT the result of step 1. (3) f: out = x+y if f=1, or x&y if f=0. (4) no: bitwise-NOT the output. Every step works on all 16 bits.

ALU status outputs zr, ng

zr = 1 exactly when out == 0 (a 16-bit equality test). ng = 1 exactly when out \< 0 (a two's complement test), which is the same as out\[15\] == 1. The CPU uses these two flags later. In chapter 4/5 they decide conditional jumps.

64 vs 18 functions

Six control bits give 2^6 = 64 combinations. Only 18 are documented and used by Hack, because those are enough for its instruction set. The other 46 still produce outputs, and some are even useful, but Hack never uses them.

Design method of the ALU

The designers first listed the operations they wanted, then worked backward to six simple bit manipulations. Each one is easy to build from basic gates. That is why so much functionality comes from so few parts.

Hardware vs software split

Building an operation into the ALU makes it faster but makes the hardware more expensive. Hack keeps the ALU minimal. It is integer-only, with no multiply, divide or floating point. The chapter 12 OS adds multiplication, division and other math (for example sqrt) as bitwise algorithms in software. For an expression like x\*12 + sqrt(y), the ALU does part of the work and OS routines do the rest.

Chips 5

| Chip | Interface | Behavior | Built from |
| --- | --- | --- | --- |
| HalfAdder | IN a, b (1 bit each); OUT sum, carry (1 bit each) | Adds two bits. sum = LSB of a+b = a XOR b. carry = MSB of a+b = a AND b. | One Xor and one And from chapter 1. The two outputs are exactly those two gates. |
| FullAdder | IN a, b, c (1 bit each); OUT sum, carry (1 bit each) | Adds three bits. sum = LSB of a+b+c = a XOR b XOR c. carry = MSB of a+b+c, which is 1 when at least two inputs are 1. | Two HalfAdders plus one Or. HA1(a,b) gives s1 and c1. HA2(s1,c) gives sum and c2. carry = c1 OR c2. Other designs that skip half-adders also work. |
| Add16 | IN a\[16\], b\[16\]; OUT out\[16\] | out = a + b in 16-bit two's complement. The carry out of bit 15 is dropped. The same chip works for nonnegative, negative and mixed-sign inputs. | Ripple chain: a HalfAdder for bit 0 (or a FullAdder with c=false), then 15 FullAdders. Each FullAdder takes the carry from the bit below it. The same design extends to any n. |
| Inc16 | IN in\[16\]; OUT out\[16\] | out = in + 1, with overflow ignored. The PC register (chapter 3) uses it to step to the next instruction. | Simplest version: Add16 with b set to the constant 1, so b\[0\]=true and b\[1..15\]=false. A dedicated incrementer can be more efficient, and there are several ways to build one. |
| ALU (Hack) | IN x\[16\], y\[16\], zx, nx, zy, ny, f, no (1 bit each); OUT out\[16\], zr (1 bit), ng (1 bit) | If zx then x=0. If nx then x=!x. If zy then y=0. If ny then y=!y. If f then out=x+y else out=x&y. If no then out=!out. zr=1 iff out==0. ng=1 iff out\<0. Overflow is ignored. | Build one zero/negate block and use it for x, y and out. Zeroing is a Mux16 with false. Conditional NOT is Not16 plus Mux16. And16 and Add16 feed a Mux16 controlled by f. zr = Not(Or(Or8Way(low byte), Or8Way(high byte))). ng = out\[15\]. |

Reference tables 5

Half-adder and full-adder truth tables (result = carry:sum)

| a | b | c | FA carry | FA sum | HA carry (c ignored) | HA sum |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 | 0 |

4-bit two's complement (negative codes are 16 - |x|; 16-bit works the same way: -32768..32767)

| bits | value | bits | value |
| --- | --- | --- | --- |
| 0000 | 0 | 1000 | -8 |
| 0001 | 1 | 1001 | -7 |
| 0010 | 2 | 1010 | -6 |
| 0011 | 3 | 1011 | -5 |
| 0100 | 4 | 1100 | -4 |
| 0101 | 5 | 1101 | -3 |
| 0110 | 6 | 1110 | -2 |
| 0111 | 7 | 1111 | -1 |

Useful 16-bit constants

| value | binary | hex |
| --- | --- | --- |
| 0 | 0000 0000 0000 0000 | 0x0000 |
| 1 | 0000 0000 0000 0001 | 0x0001 |
| -1 | 1111 1111 1111 1111 | 0xFFFF |
| 32767 (max) | 0111 1111 1111 1111 | 0x7FFF |
| -32768 (min) | 1000 0000 0000 0000 | 0x8000 |

Hack ALU: the 18 documented control settings (bit order zx nx zy ny f no)

| zx | nx | zy | ny | f | no | out |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 | 1 | 0 | -1 |
| 0 | 0 | 1 | 1 | 0 | 0 | x |
| 1 | 1 | 0 | 0 | 0 | 0 | y |
| 0 | 0 | 1 | 1 | 0 | 1 | !x |
| 1 | 1 | 0 | 0 | 0 | 1 | !y |
| 0 | 0 | 1 | 1 | 1 | 1 | -x |
| 1 | 1 | 0 | 0 | 1 | 1 | -y |
| 0 | 1 | 1 | 1 | 1 | 1 | x+1 |
| 1 | 1 | 0 | 1 | 1 | 1 | y+1 |
| 0 | 0 | 1 | 1 | 1 | 0 | x-1 |
| 1 | 1 | 0 | 0 | 1 | 0 | y-1 |
| 0 | 0 | 0 | 0 | 1 | 0 | x+y |
| 0 | 1 | 0 | 0 | 1 | 1 | x-y |
| 0 | 0 | 0 | 1 | 1 | 1 | y-x |
| 0 | 0 | 0 | 0 | 0 | 0 | x&y |
| 0 | 1 | 0 | 1 | 0 | 1 | x\|y |

Control bit meanings (applied in this order) and status outputs

| pin | effect |
| --- | --- |
| zx | x = 0 |
| nx | x = !x (after zx) |
| zy | y = 0 |
| ny | y = !y (after zy) |
| f | 1: out = x + y ; 0: out = x & y |
| no | out = !out |
| zr (output) | 1 iff out == 0 |
| ng (output) | 1 iff out \< 0 (i.e. out\[15\] == 1) |

Code examples 5

HalfAdder and FullAdder (FullAdder = 2 half-adders + Or) hdl

```
CHIP HalfAdder {
    IN a, b;
    OUT sum, carry;
    PARTS:
    Xor(a=a, b=b, out=sum);
    And(a=a, b=b, out=carry);
}

CHIP FullAdder {
    IN a, b, c;
    OUT sum, carry;
    PARTS:
    HalfAdder(a=a,  b=b, sum=s1,  carry=c1);
    HalfAdder(a=s1, b=c, sum=sum, carry=c2);
    Or(a=c1, b=c2, out=carry);
}
```

Add16 ripple chain (shown partially) and Inc16 via a constant hdl

```
// Add16 PARTS (pattern repeats up to bit 15)
HalfAdder(a=a[0], b=b[0], sum=out[0], carry=c0);
FullAdder(a=a[1], b=b[1], c=c0, sum=out[1], carry=c1);
FullAdder(a=a[2], b=b[2], c=c1, sum=out[2], carry=c2);
// ...
FullAdder(a=a[15], b=b[15], c=c14, sum=out[15]);  // final carry left unconnected = overflow dropped

// Inc16 PARTS
Add16(a=in, b[0]=true, b[1..15]=false, out=out);
```

ALU skeleton: zero/negate inputs, select with f, negate output, then the flags hdl

```
// x preprocessing
Mux16(a=x,  b=false, sel=zx, out=x1);
Not16(in=x1, out=notx1);
Mux16(a=x1, b=notx1, sel=nx, out=x2);

// y preprocessing (same block)
Mux16(a=y,  b=false, sel=zy, out=y1);
Not16(in=y1, out=noty1);
Mux16(a=y1, b=noty1, sel=ny, out=y2);

// f: choose between And and Add
And16(a=x2, b=y2, out=xandy);
Add16(a=x2, b=y2, out=xplusy);
Mux16(a=xandy, b=xplusy, sel=f, out=o1);

// no: conditional output negation; split bits for the flags here
Not16(in=o1, out=noto1);
Mux16(a=o1, b=noto1, sel=no,
      out=out, out[15]=ng, out[0..7]=lo, out[8..15]=hi);

// zr = NOT(any bit set)
Or8Way(in=lo, out=orlo);
Or8Way(in=hi, out=orhi);
Or(a=orlo, b=orhi, out=nonzero);
Not(in=nonzero, out=zr);
```

Trace by hand: control bits 001110 compute x-1 (the book's example with x = 27) text

```
x = 27 = 0000000000011011
zx=0,nx=0  -> x stays 27
zy=1       -> y = 0000000000000000   (y's original value does not matter)
ny=1       -> y = 1111111111111111   (= -1)
f=1        -> out = 27 + (-1) = 26
no=0       -> out = 0000000000011010 (26)
zr=0 (not zero), ng=0 (MSB is 0)
```

4-bit addition and subtraction by hand (the book's examples) text

```
  1001 (9)  +  0101 (5)  =  1110 (14)           no carry out
  1011      +  0111      = 10010 -> 0010        carry out dropped (overflow)

Signed (two's complement):
  5 - 7    = 0101 + 1001 = 1110         = -2
  -2 + -3  = 1110 + 1101 = 11011 -> 1011 = -5   (carry dropped)
  7 + -7   = 0111 + 1001 = 10000 -> 0000 = 0
```

Gotchas 10

- The book defines overflow as a carry out of the MSB. Hack drops that carry and raises no flag. Signed results that leave the range also wrap silently, even with no carry out. Example: 32767 + 1 = 0x7FFF + 0x0001 = 0x8000 = -32768.
- Negating -32768 (0x8000) gives -32768 again, because +32768 does not fit in 16 bits.
- Inside the ALU, zeroing comes before negating. So zx=1 with nx=1 makes x all ones (-1), not 0.
- Several rows rely on identities instead of doing the operation directly. x-y (010011) is computed as !(!x + y), and x+1 (011111) is computed as !(!x + (-1)). Both work because !a = -a - 1.
- In Nand2Tetris HDL you cannot take a slice of an internal pin (for example o1\[15\]). Split the bits where the pin is produced, as in out\[15\]=ng, out\[0..7\]=lo on the final Mux16. One part output can feed several names. You also cannot use a chip's OUT pin (such as out) as an input to another part. That is why the flags take their own copies of the bits.
- The constants true and false can drive a whole bus or a slice. b=false on a Mux16 gives 16 zeros. b\[0\]=true sets only bit 0.
- The ALU is combinational. It has no clock and no state. Registers and timing start in chapter 3.
- Project rules: do not copy chapter 1 .hdl files into the projects/02 folder. The simulator then uses the built-in versions, which are guaranteed correct and run faster. Use as few chip-parts as possible. Do not invent helper chips: use only chips from chapters 1 and 2.
- The ALU cannot multiply or divide, and it has no shift operation. Multiplication and division come later as OS software in chapter 12.
- Link to chapter 4 (not part of chapter 2): in a C-instruction, comp bits c1..c6 drive the ALU's zx nx zy ny f no, in that order. In the CPU the ALU's x input is D, and the extra 'a' bit chooses whether y is A or M. So a C-instruction's comp bits are exactly the ALU control rows in this chapter.

Self-check: answer first, then reveal 7

1. What 16-bit pattern represents -1, and what is the signed 16-bit range?

   1111111111111111 (0xFFFF). The range is -32768 to 32767.
2. Give two ways to compute -x in two's complement.

   (1) Flip every bit and add 1: -x = !x + 1. (2) From the right, keep all low 0s and the first 1, then flip every bit to the left of that 1.
3. How is a FullAdder built from HalfAdders?

   HA(a,b) gives s1 and c1. HA(s1,c) gives sum and c2. carry = Or(c1, c2).
4. List the six ALU control bits in order, with what each one does.

   zx: zero x. nx: NOT x. zy: zero y. ny: NOT y. f: 1 = add, 0 = And. no: NOT the output.
5. Which control bits give out = -1? x+y? x&y? x-1?

   -1: 111010. x+y: 000010. x&y: 000000. x-1: 001110.
6. How are the zr and ng flags computed?

   ng = out\[15\], the sign bit. zr = NOT(OR of all 16 output bits), built with two Or8Way gates, an Or and a Not.
7. Why does Hack need no special subtraction hardware, and what happens on overflow?

   In two's complement x - y = x + (-y), so the adder plus negation is enough. The carry out of the MSB is dropped and no flag is set, so results wrap modulo 2^16.

Ch 3

## Memory

[ ] Refreshed

Chapter 3 adds time to the hardware. It starts from one primitive clocked gate, the DFF. From it the chapter builds the Bit, the 16-bit Register, a family of RAM chips up to RAM16K, and the 16-bit Program Counter (PC). In chapter 5 these storage parts are combined with the ALU to build the Hack CPU and its memory.

Keep this one idea

Storage comes from feedback through a DFF. Bit is a DFF whose input comes from a Mux, so each cycle it either keeps its old value or takes a new one. Register, RAM and PC are all built on Bit. Addressing is only combinational logic around a bank of registers: a DMux sends load to one register, and a Mux picks which output to read. That logic does not wait for the clock, so a read at any address is effectively instant.

Key concepts 16

Combinational vs sequential chips

A combinational chip (And, Mux, Add16, ALU) computes its output only from its current inputs and has no memory. A sequential (clocked) chip also depends on inputs and outputs from earlier time units. Any chip that contains a DFF is sequential, whether the DFF is a direct part or sits inside another part.

Clock and cycle

A master clock is an oscillator that alternates between two phases, called 0-1, low-high, or tick-tock. One cycle runs from the start of a tick to the end of the next tock. Each cycle is one discrete time unit t. The same clock signal goes to every memory chip at the same time. Inside each chip it reaches the DFFs, and they commit a new state only at the end of the cycle.

Discrete time

Time is split into fixed-length cycles. State changes are observed only at cycle transitions, and anything that happens inside a cycle is ignored. This does two jobs. It hides the random delays of signal travel and computation. It also synchronizes all the chips in the system. Example from the book: a Not gate takes a moment to settle, but the cycle is longer than that, so at the cycle end it looks as if the gate answered instantly.

Cycle length trade-off

The cycle must be longer than the worst delay in the system: the longest wire travel between chips plus the slowest computation inside a chip. Shorter cycles make the computer faster. So the cycle is chosen to be slightly longer than that maximum delay. Modern clocks reach about one cycle per nanosecond. This is how the ALU can add x and y safely even when the two inputs arrive at different times: its output is valid by the end of the cycle.

Data flip-flop (DFF)

The primitive sequential gate. It has a 1-bit in, a 1-bit out and a clock input, drawn as a small triangle. Its behavior is out(t+1) = in(t): it outputs its input from the previous cycle. In the first cycle its output is undefined. A real DFF can be built from Nands, but that needs feedback loops between combinational gates, and the simulator cannot model those. So in Nand2Tetris the DFF is built in (tools/builtIn/DFF.hdl), and you do not build it.

Latched

All DFFs in the computer share one master clock. At the end of each cycle, every DFF outputs its input from the previous cycle. At all other times a DFF is latched: changes on its input do not affect its output.

Feedback loops

Combinational logic cannot use feedback. If you wire an output back to an input, the output depends on itself. A loop that passes through a DFF is fine. The DFF adds a one-cycle delay, so out(t+1) depends on out(t), not on itself. A typical sequential design is a block of DFF-based chips connected to combinational chips, with outputs fed back as inputs (figure 3.4).

Bit (1-bit register)

A DFF whose input comes from a Mux. The Mux picks the new in when load=1, and the DFF's own previous out when load=0. Result: if load(t) then out(t+1)=in(t), else out(t+1)=out(t). When load=0 the register is latched and in is ignored. Bit is the only Hack chip that uses a DFF directly. Every other memory chip uses DFFs through Bits.

Register (w-bit)

An array of w Bit chips that all share one load. Hack is a 16-bit platform, so its Register has in\[16\], load and out\[16\] and is built from 16 Bits. To read, look at out. To write v, put v on in and set load=1. out shows v from the next time unit on. A register keeps the last value written to it until you write another one.

RAMn (random access memory)

n 16-bit Registers plus addressing logic. Pins: in\[16\], load, address\[k\] with k = log2(n), and out\[16\]. Read: set address=m, and out shows register m right away, without waiting for the clock. Write: set address=m, in=v and load=1. Register m gets v, and out shows v from the next time unit on. Access time does not depend on the address or on the size of the RAM.

Registers have no physical address

No register stores its own address. Register m exists only because the combinational logic sends load to position m and reads the output of position m. Because that logic is combinational, access is nearly instant.

Hierarchical addressing

RAM64 is built from 8 RAM8s. A 6-bit address xxxyyy splits in two: xxx picks the RAM8, and yyy picks the register inside it. The same idea gives RAM512 (8 RAM64), RAM4K (8 RAM512) and RAM16K (4 RAM4K). RAM16K uses only 2 bits to pick a RAM4K, and the other 12 bits go to the RAM4K. Hack needs 16K (16384) 16-bit registers, so RAM16K is the last chip in the series.

Counter / Program Counter (PC)

A counter is a register that can add 1 to its value each time unit. The book names it PC because chapter 5 uses it as the Program Counter. Pins: in\[16\], load, inc, reset and out\[16\]. Priority: reset, then load, then inc. With none of them set, it keeps its value. For correct use, assert at most one control bit. The spec still defines what happens when more than one is set.

Project folders 03/a and 03/b

RAM8.hdl and RAM64.hdl are in projects/03/a. RAM512, RAM4K and RAM16K are in projects/03/b. When the simulator tests the b chips, it cannot find RAM64.hdl, so it uses the built-in RAM64. Otherwise it would create a software object for every part of a large RAM, which is slow and can use up all the memory on your computer.

Simulator clock control

In the hardware simulator you advance the clock by clicking a clock icon. Test scripts (.tst) advance it with the tick and tock commands.

Perspective: real flip-flops and real RAM

A real DFF is usually built in two steps. First, Nands in a feedback loop make a non-clocked bistable flip-flop that can hold 0 or 1. Then two of them are chained (master-slave): the first is set on tick and the second on tock. The book treats the DFF as a primitive instead. Modern memory chips often use other storage technologies, chosen for cost and performance. Building RAM recursively, as this chapter does, is elegant but not efficient, and faster designs exist.

Chips 9

| Chip | Interface | Behavior | Built from |
| --- | --- | --- | --- |
| DFF | in (1), out (1), clock (implicit) | out(t+1) = in(t). Undefined in the first cycle. | Primitive, built into the simulator (tools/builtIn/DFF.hdl). You do not implement it. |
| Bit | in (1), load (1) -> out (1) | if load(t) then out(t+1)=in(t) else out(t+1)=out(t) | Mux(a=dffOut, b=in, sel=load) feeds a DFF. The DFF output goes to out and back into the Mux's a input. |
| Register | in\[16\], load (1) -> out\[16\] | The 16-bit version of Bit. '=' acts on all 16 bits. It keeps its value until load=1, then shows in from the next cycle. | 16 Bit chips. Bit i uses in\[i\] and out\[i\], and all of them share load. |
| RAM8 | in\[16\], load (1), address\[3\] -> out\[16\] | 8 registers. Read: out = register\[address\], with no clock wait. Write: if load=1, register\[address\] gets in, and out shows it from the next cycle. | DMux8Way(in=load, sel=address) sends load to one of 8 Registers. All 8 Registers get the same in. Mux8Way16(sel=address) picks the output. |
| RAM64 | in\[16\], load (1), address\[6\] -> out\[16\] | RAMn behavior with 64 registers. | 8 RAM8. The high bits address\[3..5\] pick the RAM8 (DMux8Way for load, Mux8Way16 for out). The low bits address\[0..2\] go to every RAM8. |
| RAM512 | in\[16\], load (1), address\[9\] -> out\[16\] | RAMn behavior with 512 registers. | 8 RAM64. address\[6..8\] picks the RAM64, and address\[0..5\] goes to all of them. |
| RAM4K | in\[16\], load (1), address\[12\] -> out\[16\] | RAMn behavior with 4096 registers. | 8 RAM512. address\[9..11\] picks the RAM512, and address\[0..8\] goes to all of them. |
| RAM16K | in\[16\], load (1), address\[14\] -> out\[16\] | RAMn behavior with 16384 registers. This is the RAM size the Hack platform needs. | 4 RAM4K. address\[12..13\] picks one with DMux4Way and Mux4Way16. address\[0..11\] goes to all of them. |
| PC | in\[16\], load (1), inc (1), reset (1) -> out\[16\] | if reset(t): out(t+1)=0; else if load(t): out(t+1)=in(t); else if inc(t): out(t+1)=out(t)+1; else out(t+1)=out(t). | A Register with load=true. Its output feeds Inc16 (project 2) and loops back into a chain of Mux16s (project 1). The chain applies inc first, then load, then reset last, so reset wins. |

Reference tables 4

RAM family: sizes, address widths, construction (k = log2 n)

| Chip | Registers (n) | address bits (k) | Built from | Selector bits | Passed-down bits |
| --- | --- | --- | --- | --- | --- |
| RAM8 | 8 | 3 | 8 Register | address\[0..2\] | - |
| RAM64 | 64 | 6 | 8 RAM8 | address\[3..5\] | address\[0..2\] |
| RAM512 | 512 | 9 | 8 RAM64 | address\[6..8\] | address\[0..5\] |
| RAM4K | 4096 | 12 | 8 RAM512 | address\[9..11\] | address\[0..8\] |
| RAM16K | 16384 | 14 | 4 RAM4K | address\[12..13\] | address\[0..11\] |

Read vs write timing for a Register or RAM

| Operation | Set | Visible on out |
| --- | --- | --- |
| Read | address=m, load=0 | at once, in the same cycle (combinational) |
| Write | address=m, in=v, load=1 | from the next time unit (t+1) on |
| Hold | load=0 | the current value stays; in is ignored |

PC control priority (figure 3.8)

| reset | load | inc | out(t+1) |
| --- | --- | --- | --- |
| 1 | x | x | 0 |
| 0 | 1 | x | in(t) |
| 0 | 0 | 1 | out(t)+1 |
| 0 | 0 | 0 | out(t) |

Chips from chapters 1 and 2 reused here

| Need | Chip |
| --- | --- |
| choose new vs old value (Bit, PC) | Mux / Mux16 |
| send load to one register or sub-RAM | DMux8Way / DMux4Way |
| pick one register's or sub-RAM's output | Mux8Way16 / Mux4Way16 |
| add 1 in the PC | Inc16 |

Code examples 4

Bit: a Mux plus a DFF with a feedback loop. The loop is legal because it passes through the DFF. hdl

```
CHIP Bit {
    IN in, load;
    OUT out;
    PARTS:
    Mux(a=prev, b=in, sel=load, out=next);
    DFF(in=next, out=prev, out=out);   // one output can drive two wires
}
```

RAM8: a DMux sends load to one register, and a Mux reads one register's output. hdl

```
CHIP RAM8 {
    IN in[16], load, address[3];
    OUT out[16];
    PARTS:
    DMux8Way(in=load, sel=address, a=l0, b=l1, c=l2, d=l3, e=l4, f=l5, g=l6, h=l7);
    Register(in=in, load=l0, out=r0);
    Register(in=in, load=l1, out=r1);
    Register(in=in, load=l2, out=r2);
    Register(in=in, load=l3, out=r3);
    Register(in=in, load=l4, out=r4);
    Register(in=in, load=l5, out=r5);
    Register(in=in, load=l6, out=r6);
    Register(in=in, load=l7, out=r7);
    Mux8Way16(a=r0, b=r1, c=r2, d=r3, e=r4, f=r5, g=r6, h=r7, sel=address, out=out);
}
```

RAM64: the high 3 address bits pick a RAM8, and the low 3 bits go to every RAM8. RAM512 and RAM4K follow the same pattern. hdl

```
CHIP RAM64 {
    IN in[16], load, address[6];
    OUT out[16];
    PARTS:
    DMux8Way(in=load, sel=address[3..5], a=l0, b=l1, c=l2, d=l3, e=l4, f=l5, g=l6, h=l7);
    RAM8(in=in, load=l0, address=address[0..2], out=m0);
    RAM8(in=in, load=l1, address=address[0..2], out=m1);
    RAM8(in=in, load=l2, address=address[0..2], out=m2);
    RAM8(in=in, load=l3, address=address[0..2], out=m3);
    RAM8(in=in, load=l4, address=address[0..2], out=m4);
    RAM8(in=in, load=l5, address=address[0..2], out=m5);
    RAM8(in=in, load=l6, address=address[0..2], out=m6);
    RAM8(in=in, load=l7, address=address[0..2], out=m7);
    Mux8Way16(a=m0, b=m1, c=m2, d=m3, e=m4, f=m5, g=m6, h=m7, sel=address[3..5], out=out);
}
```

PC: the last Mux16 in the chain has the highest priority, so reset goes last. 'false' fills the whole 16-bit bus with 0. hdl

```
CHIP PC {
    IN in[16], load, inc, reset;
    OUT out[16];
    PARTS:
    Inc16(in=cur, out=plus1);
    Mux16(a=cur, b=plus1, sel=inc,   out=o1);
    Mux16(a=o1,  b=in,    sel=load,  out=o2);
    Mux16(a=o2,  b=false, sel=reset, out=o3);
    Register(in=o3, load=true, out=cur, out=out);
}
```

Gotchas 9

- A write needs a clock edge, but a read does not. After a write with load=1, out shows the new value only from the next time unit. A read shows the addressed register's value at once.
- In Nand2Tetris HDL you cannot use a chip's OUT pin as an input to another part. To feed an output back in, give the part a second output wire (out=prev, out=out) and use prev inside the chip.
- A pin can have only one source. So the naive Bit design, a DFF with its out wired straight back to in, does not work. It also has no load pin. A Mux has to choose between in and the old value.
- In HDL, address\[0\] is the least significant bit, and sub-buses are written low..high, for example address\[3..5\]. The book's xxxyyy split uses the high bits to pick the sub-chip. Any split works if you use the same bits for the DMux and the Mux.
- RAM16K is built from 4 RAM4K, not 8. Use DMux4Way and Mux4Way16 with the 2 bits address\[12..13\].
- In the PC, the order of the Mux16 chain sets the priority. The last Mux applied wins, so reset goes last. The inner Register's load can be always true, or the OR of the three control bits.
- Feedback through combinational logic alone is not allowed, because the output would depend on itself. Feedback is allowed only when it passes through a DFF, directly or inside a Bit, Register or RAM part.
- The DFF output, and so the output of any register, is undefined in the first cycle, before anything has been loaded.
- Keep the 03/a and 03/b folder split. If the simulator builds big RAMs out of your own lower-level RAM .hdl files, it can run very slowly or use up all the memory on your computer.

Self-check: answer first, then reveal 7

1. What is the DFF's behavior, written as an equation? What is its output in the first cycle?

   out(t+1) = in(t). In the first cycle the output is undefined.
2. Why must the clock cycle be longer than the worst-case delay in the system?

   State is observed only at the end of a cycle. Every combinational output must settle before then, for example the ALU result when its inputs arrive at different times. Otherwise a wrong value would be stored. The cycle is chosen to be just above the worst delay, because shorter cycles make the computer faster.
3. How do you build a Bit from a DFF, and why is the feedback loop allowed?

   Put a Mux in front of the DFF with sel=load, a=the DFF's own output and b=in. The loop is allowed because it passes through the DFF, which adds a one-cycle delay.
4. For RAMn, what is the width of address? Give the widths for RAM8 and RAM16K, and say what RAM16K is built from.

   k = log2(n). RAM8 has 3 bits. RAM16K has 14 bits and is built from 4 RAM4K.
5. Which project 1 chips handle a RAM8 write and a RAM8 read?

   Write: DMux8Way sends load to the one selected Register. All 8 Registers get the same in. Read: Mux8Way16 selects the addressed Register's output.
6. You set address=5, in=42 and load=1 in cycle t. When does out show 42?

   From cycle t+1 on. During cycle t, out still shows register 5's old value.
7. reset=1 and load=1 are set at the same time. What does the PC output in the next cycle? What if only inc=1 is set?

   With reset=1 and load=1 the output is 0, because reset has the highest priority. With only inc=1 it is out(t)+1.

Ch 4

## Machine Language

[ ] Refreshed

Chapter 4 builds no chips. It defines the Hack machine language. The chapter 5 hardware must execute this language, and your chapter 6 assembler must translate it. You learn the two instruction types (A and C), their exact 16-bit encodings, the symbol rules, memory-mapped I/O, and how to write small programs with loops and pointers.

Keep this one idea

Hack has only two instructions. `@value` loads a 15-bit number into A. `dest=comp;jump` makes the ALU compute from D and A (or from M = RAM\[A\]), stores the result in any of A, D and M, and can jump to ROM\[A\]. So every memory operation takes two instructions: first select the address with @, then act on it.

Key concepts 18

Machine language vs assembly language

Machine language is the binary form: 16 bits per instruction, written as text lines of '0' and '1' in .hack files. Assembly is the symbolic form of the same instructions, written in .asm files. An assembler translates assembly into binary. Each A- or C-instruction becomes exactly one 16-bit word. Label declarations are pseudo-instructions: they produce no word.

Hardware the language sees

Hack is a 16-bit computer. The book calls its design von Neumann architecture. It has two memories. ROM (instruction memory) is read-only and holds the program, which is loaded from outside. RAM (data memory) is read/write. Both are 16 bits wide and have a 15-bit address space, so each can address up to 32K words (0 to 32767). Line n of a .hack file goes into ROM\[n\], and counting starts at 0. Figure 4.2 is only a conceptual model: chapter 5 wires things somewhat differently.

Registers A, D and M

D is a plain 16-bit data register. A is both a data register and an address register. M is not a separate register. It is the name for RAM\[A\], the RAM word currently selected by A. Some value is always in A, so some RAM word is always selected (M) and some ROM word is always the current instruction. Selection takes effect immediately, within the same clock cycle. Changing A changes which word M means.

The dual role of A

After @xxx, A = xxx. This selects RAM\[xxx\] (M now means that word) and also ROM\[xxx\], a possible jump target. The next C-instruction uses only one of the two: either it works on M, or it jumps. Book rule: a C-instruction that refers to M should not jump, and a C-instruction that jumps should not refer to M. One address register controlling two memories keeps the hardware and the language small.

A-instruction (@xxx)

Binary form: 0vvvvvvvvvvvvvvv. Bit 15 is the opcode 0. The other 15 bits hold a non-negative number from 0 to 32767. xxx is a decimal constant or a symbol bound to such a value. It has three uses: (1) the only way for a program to enter a constant, (2) set A to an address before a C-instruction that uses M, (3) set A to a jump target before a C-instruction that jumps.

C-instruction (dest=comp;jump)

Binary form: 111a cccc ccdd djjj. Bit 15 = 1 is the opcode. Bits 14-13 are unused and set to 1 by convention. Then come the 7-bit comp field (the a-bit plus c1-c6), the 3-bit dest field and the 3-bit jump field. It answers three questions: what to compute, where to store it, and what to execute next. comp is required. If dest is empty, leave out '='. If jump is empty, leave out ';'.

comp field and the ALU

The ALU's first input always comes from D. Its second input comes from A when a=0 and from M when a=1. The six c-bits are the chapter 2 ALU control bits, in order zx, nx, zy, ny, f, no. Seven bits allow 128 codes, but the spec documents only 28 (18 with a=0 and 10 with a=1). A mnemonic like 'D+M' is one fixed string. The '+' does no arithmetic in the syntax.

dest field

d1 d2 d3 = store in A, store in D, store in M (RAM\[A\]). Any combination of zero to three bits can be set. Example: ADM=... writes the result to all three places.

jump field

j1 j2 j3 = jump if the ALU output is \<0, =0, >0. The test uses this instruction's comp result, not D. If the condition holds, the next instruction is ROM\[A\]. Otherwise execution continues in order. 000 = never jump and 111 = always jump. An unconditional jump is written 0;JMP: comp is required, so the convention is to compute 0 and ignore the result.

Symbols: predefined, labels, variables

Predefined: R0-R15 = 0-15 ('virtual registers'). SP, LCL, ARG, THIS, THAT = 0-4 (used in part II for the VM and compiler, so ignore them for now). SCREEN = 16384 (0x4000). KBD = 24576 (0x6000). Label: (NAME) binds NAME to the ROM address of the next instruction. Jumps may use a label before its declaration. Variable: any other symbol. Each new variable gets the next free RAM address: 16, 17, 18, ... By convention labels are UPPERCASE and variables are lowercase.

Why symbols matter

Symbols make code easier to write and debug. Code that mentions no physical addresses is also relocatable: it can be loaded into any free memory segment. The assembler maps each symbol to a real address.

Memory-mapped I/O

Screen: 256 rows x 512 black-and-white pixels. It is mapped to an 8K-word block that starts at SCREEN (RAM 16384-24575), with 32 words per row and the origin at the top-left corner. The pixel at (row, col) is bit col%16 (counted from the LSB) of RAM\[SCREEN + 32\*row + col/16\]. 1 = black and 0 = white. Keyboard: one word at KBD (RAM 24576). It holds the 16-bit code of the key currently pressed, or 0 when no key is pressed (codes are in appendix 5). Refresh loops outside the main platform keep the devices and their memory maps in sync.

Pointers

Arrays do not exist in machine language. To access \*(base+i), compute the address into A (for example A=D+M), then use M in the next instruction. This 'A=..., then use M' pattern is how the compiler will later implement every array access and every object field get/set.

Program termination

The CPU never stops by itself. After your last instruction it would keep fetching and running whatever is in ROM. End every program with an infinite loop: (END) @END 0;JMP.

Recommended workflow

Write goto-style pseudocode first. Trace it by hand with a few values. Then translate each pseudo-line into a few Hack instructions. Keep the pseudocode lines as comments in the .asm file.

Hack is a '1/2-address' language

A 16-bit word has no room for both an opcode and a 15-bit address. So each memory operation needs two instructions: an A-instruction for the address, then a C-instruction for the operation. Hack code is therefore mostly an alternation of @ lines and C lines. Macros like 'goto LOOP' could be added by having the assembler expand each one into its two instructions.

Syntax and file rules

.asm lines: A-instruction, C-instruction, label declaration (SYMBOL), // comment, or empty. Leading spaces and empty lines are ignored. The book's own programs and the supplied tools also accept a // comment after an instruction. Constants are decimal, 0 to 32767. A symbol is a sequence of letters, digits, \_ . $ : that does not start with a digit. Mnemonics must be uppercase, and symbols are case-sensitive. .hack lines: exactly 16 characters, each '0' or '1'.

Project 4 and the CPU emulator

Mult.asm: R2 = R0 * R1, assuming R0 >= 0, R1 >= 0 and R0\*R1 \< 32768. Fill.asm: an endless loop that blackens the whole screen while any key is held and clears it when no key is pressed. It is checked by eye, with no .cmp file. The CPU emulator loads .hack or .asm files (it has a built-in assembler) and shows ROM, RAM, A, D, PC, the ALU, the screen and keyboard input.

Reference tables 8

Instruction formats (bit 15 on the left)

| Type | Symbolic | Binary | Notes |
| --- | --- | --- | --- |
| A | `@xxx` | `0 vvvvvvvvvvvvvvv` | xxx = 0..32767, or a symbol |
| C | `dest=comp;jump` | `1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3` | bits 14-13 unused, set to 1 |

C-instruction bit positions

| Bits | 15 | 14-13 | 12 | 11-6 | 5-3 | 2-0 |
| --- | --- | --- | --- | --- | --- | --- |
| Field | opcode = 1 | unused = 11 | a | c1..c6 | d1 d2 d3 | j1 j2 j3 |

comp field: a-bit + c1..c6 (c-bits = ALU zx nx zy ny f no; first input = D, second = A or M)

| comp (a=0) | comp (a=1) | c1..c6 |
| --- | --- | --- |
| 0 |  | 101010 |
| 1 |  | 111111 |
| -1 |  | 111010 |
| D |  | 001100 |
| A | M | 110000 |
| !D |  | 001101 |
| !A | !M | 110001 |
| -D |  | 001111 |
| -A | -M | 110011 |
| D+1 |  | 011111 |
| A+1 | M+1 | 110111 |
| D-1 |  | 001110 |
| A-1 | M-1 | 110010 |
| D+A | D+M | 000010 |
| D-A | D-M | 010011 |
| A-D | M-D | 000111 |
| D&A | D&M | 000000 |
| D\|A | D\|M | 010101 |

dest field (d1 d2 d3 = A, D, M)

| dest | d1d2d3 | Stores ALU output in |
| --- | --- | --- |
| null | 000 | nowhere |
| M | 001 | RAM\[A\] |
| D | 010 | D |
| DM | 011 | D and RAM\[A\] |
| A | 100 | A |
| AM | 101 | A and RAM\[A\] |
| AD | 110 | A and D |
| ADM | 111 | A, D and RAM\[A\] |

jump field (j1 j2 j3 = out\<0, out=0, out>0)

| jump | j1j2j3 | Jump to ROM\[A\] if |
| --- | --- | --- |
| null | 000 | never |
| JGT | 001 | out > 0 |
| JEQ | 010 | out = 0 |
| JGE | 011 | out >= 0 |
| JLT | 100 | out \< 0 |
| JNE | 101 | out != 0 |
| JLE | 110 | out \<= 0 |
| JMP | 111 | always |

Predefined symbols

| Symbol | Value |
| --- | --- |
| R0..R15 | 0..15 |
| SP, LCL, ARG, THIS, THAT | 0, 1, 2, 3, 4 |
| SCREEN | 16384 (0x4000) |
| KBD | 24576 (0x6000) |
| user variables | allocated from 16 upward |

RAM as seen by a Hack program

| Address | Use |
| --- | --- |
| 0-15 | R0-R15 (also SP=0 ... THAT=4) |
| 16 upward | variables chosen by the assembler |
| 16384-24575 | screen memory map (8K words, 32 per row) |
| 24576 | keyboard memory map (1 word) |

Hand-encoded examples (useful for checking your chapter 6 output)

| Symbolic | Binary |
| --- | --- |
| @5 | 0000000000000101 |
| @7 | 0000000000000111 |
| D=M | 1111110000010000 |
| D=D-1 | 1110001110010000 |
| M=M+1 | 1111110111001000 |
| DM=M+1 | 1111110111011000 |
| D\|M | 1111010101000000 |
| D;JGT | 1110001100000001 |
| 0;JMP | 1110101010000111 |
| M=-1 | 1110111010001000 |

Code examples 8

Constant into RAM: RAM\[100\] = 17 (A is used first as data, then as an address) hack-asm

```
@17
D=A      // D = 17
@100
M=D      // RAM[100] = 17
```

Copy memory: RAM\[100\] = RAM\[200\] hack-asm

```
@200
D=M      // D = RAM[200]
@100
M=D      // RAM[100] = D
```

Arithmetic on virtual registers: R2 = R0 + R1 hack-asm

```
@R0
D=M      // D = RAM[0]
@R1
D=D+M    // D = RAM[0] + RAM[1]
@R2
M=D      // RAM[2] = D
```

Conditional branch: if (x > 0) goto POS hack-asm

```
@x
D=M      // D = x (a variable, e.g. RAM[16] if it is the first one)
@POS
D;JGT    // test the ALU output, which here is just D
// ... code for x <= 0 ...
(POS)
// ... code for x > 0 ...
```

Pointer loop: set arr\[0..n-1\] to -1, where the base address is in R0 and n is in R1 hack-asm

```
    @i
    M=0
(LOOP)
    @i
    D=M
    @R1
    D=D-M    // D = i - n
    @DONE
    D;JGE    // stop when i >= n
    @R0
    D=M      // D = base
    @i
    A=D+M    // A = base + i, so M = arr[i]
    M=-1
    @i
    M=M+1
    @LOOP
    0;JMP
(DONE)
    @DONE
    0;JMP
```

Keyboard polling: wait until a key is pressed hack-asm

```
(WAIT)
    @KBD
    D=M      // D = code of the pressed key, 0 if none
    @WAIT
    D;JEQ    // no key pressed: keep waiting
```

Blacken the 16 leftmost pixels of screen row 0, then halt hack-asm

```
@SCREEN
M=-1     // -1 = 1111111111111111, so all 16 pixels are black
(END)
@END
0;JMP    // halt: infinite loop
```

Negative constants: @ cannot take them, so compute them hack-asm

```
@5
D=-A     // D = -5
@x
M=D
```

Gotchas 14

- M always means RAM\[A\] for the current value of A. After A=D+M, M in the next instruction refers to the new address.
- Do not use M and a jump in the same C-instruction. A cannot point at a useful data word and a useful jump target at the same time.
- Jump conditions test the comp result of that same instruction, not D. 'D;JGT' tests D because comp is D. 'D=D-M;JGT' tests D-M.
- An A-instruction can only hold 0 to 32767, because bit 15 is the opcode. @-1 and @40000 are not allowed. To get a negative value, compute it, for example M=-1 or D=-A.
- Label declarations like (LOOP) produce no binary. The label's value is the ROM address of the next real instruction, not its line number in the source file.
- Labels mean ROM addresses and variables mean RAM addresses. Both are just numbers loaded with @. The next instruction decides how the number is used.
- Bit order: dest is A, D, M (d1, d2, d3). jump is \<0, =0, >0 (j1, j2, j3).
- The 2nd edition writes two-destination forms as DM, AM, AD and ADM. The 1st edition and older course and test files use MD and AMD, with the same bits (011 and 111). Expect to see both spellings.
- Each comp mnemonic is one fixed string. 'D+M' is in the spec table, but 'M+D' is not.
- Bits 14-13 of a C-instruction are 1 by convention, so every C-instruction starts with 111.
- Hack is case-sensitive. @foo and @Foo create two unrelated variables. Mnemonics must be uppercase.
- You cannot set a single screen pixel. Read the 16-bit word, change the bits with logic operations, and write the whole word back.
- Always end a program with an infinite loop. Otherwise the CPU runs whatever is in ROM after your code.
- Avoid writing A and jumping in the same instruction (for example A=M;JMP). The jump uses the value A had before this instruction, because the new A value is stored only at the end of the cycle. Use separate instructions.

Self-check: answer first, then reveal 7

1. How do you tell an A-instruction from a C-instruction in binary?

   Look at bit 15, the leftmost bit. 0 = A-instruction, and the other 15 bits are the value. 1 = C-instruction, with the layout 111a cccc ccdd djjj.
2. What decides whether comp reads A or M?

   The a-bit (bit 12). a=0 sends A to the ALU's second input. a=1 sends M (RAM\[A\]). The first input is always D.
3. Encode M=D+1 by hand.

   a=0, comp D+1 = 011111, dest M = 001, jump = 000. Result: 111 0 011111 001 000 = 1110011111001000.
4. If 'sum' is the second new variable in a program, which RAM address does it get? And what is LOOP's value for (LOOP)?

   sum = 17, because variables start at 16. LOOP is not a RAM address. It is the ROM address of the instruction right after (LOOP).
5. Which RAM word holds the pixel at row 3, column 40, and which bit?

   RAM\[16384 + 3\*32 + 40/16\] = RAM\[16384 + 96 + 2\] = RAM\[16482\]. Bit 40 % 16 = 8, counted from the LSB.
6. Why can't Hack do 'RAM\[x\] = RAM\[x\] + 1' in one instruction?

   A 16-bit word cannot hold an opcode and a 15-bit address together. You need @x to select the address and then M=M+1 to do the work.
7. How do you jump to LOOP only when D is not zero?

   @LOOP, then D;JNE (jump bits 101).

Ch 5

## Computer Architecture

[ ] Refreshed

Chapter 5 joins the ALU (ch. 2), the registers and PC (ch. 3) and basic gates (ch. 1) into the Hack computer, which runs the binary machine code from chapter 4. You build three chips. Memory is the data memory plus the screen and keyboard maps. CPU decodes and runs one 16-bit instruction per cycle. Computer is CPU + ROM32K + Memory. Chapter 6's assembler produces exactly the 16-bit words this hardware reads, so the instruction bit layout is the part to remember best.

Keep this one idea

A computer is a fetch-execute loop. The PC picks a word in instruction memory. The CPU splits that word into control bits that set up the ALU, the registers, memory and the next PC. A machine language is just the agreed meaning of each bit.

Key concepts 18

Stored program concept

The hardware is fixed and runs only a small, fixed set of simple instructions. The program sits in memory like data (software), not in the wiring. Load a different program and the same hardware does a different job.

von Neumann architecture

A CPU (ALU + registers + control unit) talks to a memory, takes data from input devices and sends data to output devices. Memory holds both the data and the instructions that work on it. Almost every real computer follows this model. Hack is a variant of it.

Instruction memory vs data memory

Instruction memory holds the binary program. Data memory holds variables, arrays and objects as plain binary words. Some machines share one address space for both. Others, like Hack, use two physically separate units. How a program gets into instruction memory is outside the architecture. It only has to be there when the CPU starts.

Harvard variant (what Hack uses)

Hack keeps instructions (ROM32K) and data (Memory) in two separate memories, each with its own address space. The CPU can fetch an instruction and read or write data in the same clock cycle. So there is a single-cycle fetch-execute and no instruction register. Advantages: easier and cheaper to build, often faster, and the instruction memory can be sized to a known program. Cost: less flexible, because spare data memory cannot hold code and spare code memory cannot hold data. This is why many embedded computers use it.

Why CPUs have registers

The ALU is a very fast combinational circuit. If every interim value went to the RAM (a separate chip) and back, the ALU would wait, which is called starvation. So CPUs have a few fast registers: data registers, address registers, a program counter and usually an instruction register. Typical CPUs have a few dozen. Hack has only three.

CPU registers in Hack

D holds data only. A holds data or an address. PC holds the address of the next instruction. A has three roles: a plain data value, the data-memory address that M refers to (M = RAM\[A\]), and the instruction-memory address of a jump target. A and D are ordinary 16-bit Registers. PC is the ch. 3 PC chip.

Control: decoding into micro-codes

An instruction is a package of bit fields. Each field tells one hardware part what to do. Decoding means pulling the fields apart and routing each one to its part (ALU, a register, memory, PC). Together, the parts carry out the instruction.

Fetch-execute cycle

Each cycle: the PC gives a ROM address, the ROM gives an instruction, and the CPU decodes and executes it. As a side effect, the CPU computes the next PC: 0 on reset, A if a jump is taken, otherwise PC+1. Hack does all of this in one clock cycle.

A- vs C-instruction inside the CPU

If the MSB is 0, it is an A-instruction. The whole word goes into A, so really a 15-bit value. If the MSB is 1, it is a C-instruction, read as 1 x x a c1..c6 d1 d2 d3 j1 j2 j3. The a and c bits are comp and set up the ALU input mux and the ALU. The d bits are dest: the load bits of A and D, and writeM. The j bits are jump: with the ALU's zr and ng flags they decide the PC load. The xx bits are ignored.

Memory-mapped I/O

Each I/O device gets a block of memory, its memory map. An output device always shows the state of its map (write a bit, a pixel changes). An input device always writes its state into its map (press a key, its code appears). Programs then do I/O with ordinary loads and stores. This needs agreed contracts: how the device data is laid out in memory, and which codes mean what. To add a device, give it a map and a base address (done by installer programs) and add a device driver to the OS.

Screen

256 rows x 512 columns of black-and-white pixels, 131,072 in all. The map is 8K (8192) 16-bit words, 32 words per row. Pixel (r, c) is bit c%16, counted from the LSB, of Screen\[r\*32 + c/16\], which is RAM address 16384 + r\*32 + c/16. So bit 0 is the leftmost pixel of its 16-pixel group. 1 = black, 0 = white.

Keyboard

One read-only 16-bit register, at address 24576 (0x6000) in Memory. It holds the code of the key pressed right now, or 0 if no key is pressed. There is no buffer. Codes come from the Hack character set (appendix 5). Printable characters use their ASCII codes. Special keys: 128 newline, 129 backspace, 130 left, 131 up, 132 right, 133 down, 134 home, 135 end, 136 page up, 137 page down, 138 insert, 139 delete, 140 esc, 141-152 F1-F12.

Booting / reset

The user sees only the screen, the keyboard and one input bit, reset. Set reset to 1, then to 0: the PC becomes 0 and the program in ROM runs from instruction 0. Programs always start at ROM address 0. In real machines, booting runs a ROM program that loads the OS kernel, which then runs other programs.

Combinational vs clocked outputs

outM and writeM come from combinational logic. They reflect the current instruction right away. addressM (from A) and pc (from PC) come from registers. They take their new values only at the next clock tick. When writeM = 0, outM can hold any value.

Hardware vs software trade-off

Any function the ALU leaves out, such as multiply, can be added later in software. Hardware is faster but costs more. Software is cheap but slower. Hack keeps the hardware minimal on purpose.

General-purpose vs single-purpose computers

General-purpose machines (PCs, phones) run many programs and switch between them. Single-purpose (embedded) machines run one program burned into ROM, as in cars, cameras and game cartridges. Both use the same core ideas: stored program, fetch-decode-execute, CPU, registers, counters.

Perspective: what real machines add

More registers, more data types, stronger ALUs and richer instruction sets. These differences are mostly quantitative, and the von Neumann model is the same. Real machines also have caches, pipelining, parallelism, instruction prefetching and faster I/O. Many send drawing commands to a GPU instead of setting pixel bits directly. Real displays use about 8 bits per primary colour per pixel instead of 1 bit. CISC (powerful, complex instructions) and RISC (simple CPU, small instruction set) are two rival ways to get speed. Hack belongs to neither camp.

Project 5 test programs

Add.hack computes 2 + 3 and stores the result in RAM\[0\]. Max.hack stores max(RAM\[0\], RAM\[1\]) in RAM\[2\]. Rect.hack draws a black rectangle at the top-left of the screen, 16 pixels wide and RAM\[0\] rows high. Each test script loads Computer, loads the program into its ROM32K and runs the clock for enough cycles.

Chips 6

| Chip | Interface | Behavior | Built from |
| --- | --- | --- | --- |
| Memory | IN in\[16\], address\[15\], load; OUT out\[16\] | The whole data address space, 32K addresses, of which 16K+8K+1 are used. 0-16383 goes to RAM16K. 16384-24575 goes to Screen at address minus 16384, so 16384 is Screen\[0\]. 24576 goes to Keyboard. Any other address is invalid. A read is combinational. A write (load=1) shows on out from the next time step. | Built-in RAM16K, Screen and Keyboard. Decode address\[13..14\]: 00 or 01 = RAM16K (address\[0..13\]), 10 = Screen (address\[0..12\]), 11 = Keyboard. Use DMux4Way to route load and Mux4Way16 to choose out. |
| CPU | IN instruction\[16\], inM\[16\], reset; OUT outM\[16\], writeM, addressM\[15\], pc\[15\] | A-instruction: A \<- instruction. C-instruction: the ALU computes f(D, A or M), and the result goes to every destination the d-bits name (A, D and/or M). For M: outM = ALU out and writeM = 1. Otherwise writeM = 0. Next PC: 0 if reset, A if the jump condition holds, else PC+1. addressM = A\[0..14\]. inM is RAM\[A\], supplied by Memory. | ALU (ch. 2), the built-in ARegister, DRegister and PC (ch. 3), two Mux16, and And/Or/Not gates for decoding and the jump test. Figure 5.8: ALU out feeds D, the A-input mux and outM. A out feeds the y-input mux, addressM and PC.in. reset goes straight to PC.reset. |
| ROM32K | IN address\[15\]; OUT out\[16\] | Read-only instruction memory of 32K 16-bit words. out = ROM\[address\], combinationally. Assumed to be preloaded with a Hack machine-language program. In the simulator, a test script loads a .hack text file into it. | Built-in. You do not build it. |
| Screen | IN in\[16\], address\[13\], load; OUT out\[16\] | Works exactly like an 8K RAM of 16-bit words: out = Screen\[address\], and with load=1 the word is set to in from the next time step. Side effect: it keeps a 256x512 black-and-white display refreshed from its bits. | Built-in. |
| Keyboard | OUT out\[16\] | A read-only 16-bit register. It outputs the code of the key pressed now, or 0 if none. | Built-in. |
| Computer | IN reset (no data outputs. The screen and keyboard are reached through Memory's Screen and Keyboard parts.) | The top-level chip. With reset=0 it runs the program stored in ROM32K. With reset=1 the program restarts. To start it, set reset to 1 and then to 0. | CPU + ROM32K + Memory. Wiring: CPU.pc to ROM.address. ROM.out to CPU.instruction. CPU.outM, addressM and writeM to Memory.in, address and load. Memory.out to CPU.inM. The external reset goes to CPU.reset. |

Reference tables 5

Hack data memory map (Memory chip)

| Range (decimal) | Hex | Device | Notes |
| --- | --- | --- | --- |
| 0 - 16383 | 0x0000 - 0x3FFF | RAM16K | general data (R0-R15 = 0-15 by convention) |
| 16384 - 24575 | 0x4000 - 0x5FFF | Screen (8K words) | symbol SCREEN = 16384. Memory address 16384 = Screen\[0\] |
| 24576 | 0x6000 | Keyboard (1 word, read-only) | symbol KBD = 24576 |
| 24577 - 32767 | 0x6001 - 0x7FFF | invalid | do not use |

C-instruction bit layout and where each field goes inside the CPU (bit 15 = MSB)

| Bits | Field | Wired to |
| --- | --- | --- |
| 15 | op-code (1 = C, 0 = A) | picks the mode and gates the side-effect signals |
| 14-13 | xx (not used, 1 by convention) | ignored |
| 12 | a | Mux16 select: ALU y = A (a=0) or inM (a=1) |
| 11-6 | c1..c6 | ALU zx, nx, zy, ny, f, no |
| 5 | d1 | load of A (from the ALU) |
| 4 | d2 | load of D |
| 3 | d3 | writeM |
| 2 | j1 | jump if out \< 0 (ng) |
| 1 | j2 | jump if out = 0 (zr) |
| 0 | j3 | jump if out > 0 (not zr and not ng) |

CPU control signals (isC = instruction\[15\], isA = not isC)

| Signal | Logic |
| --- | --- |
| A-register input mux | isC ? ALUout : instruction |
| loadA | isA OR (isC AND instruction\[5\]) |
| loadD | isC AND instruction\[4\] |
| writeM | isC AND instruction\[3\] |
| ALU x input | D (always) |
| ALU y input | instruction\[12\] ? inM : A |
| ALU zx..no | instruction\[11..6\] (gating optional, no side effects) |
| jump | (j1 AND ng) OR (j2 AND zr) OR (j3 AND NOT zr AND NOT ng) |
| PC load | isC AND jump (PC.in = A) |
| PC inc | 1 (load and reset have priority) |
| PC reset | CPU reset input |
| addressM | A\[0..14\] |
| pc | PC\[0..14\] |
| outM | ALU out |

Reminder: ALU control bits (from chapter 2). In the CPU, x = D and y = A or M.

| zx | nx | zy | ny | f | no | out |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 | 1 | 0 | -1 |
| 0 | 0 | 1 | 1 | 0 | 0 | x |
| 1 | 1 | 0 | 0 | 0 | 0 | y |
| 0 | 0 | 1 | 1 | 0 | 1 | !x |
| 1 | 1 | 0 | 0 | 0 | 1 | !y |
| 0 | 0 | 1 | 1 | 1 | 1 | -x |
| 1 | 1 | 0 | 0 | 1 | 1 | -y |
| 0 | 1 | 1 | 1 | 1 | 1 | x+1 |
| 1 | 1 | 0 | 1 | 1 | 1 | y+1 |
| 0 | 0 | 1 | 1 | 1 | 0 | x-1 |
| 1 | 1 | 0 | 0 | 1 | 0 | y-1 |
| 0 | 0 | 0 | 0 | 1 | 0 | x+y |
| 0 | 1 | 0 | 0 | 1 | 1 | x-y |
| 0 | 0 | 0 | 1 | 1 | 1 | y-x |
| 0 | 0 | 0 | 0 | 0 | 0 | x&y |
| 0 | 1 | 0 | 1 | 0 | 1 | x\|y |
| zr = 1 if out == 0. ng = 1 if out \< 0 (out\[15\] = 1). |  |  |  |  |  |  |

Chip interfaces at a glance

| Chip | Inputs | Outputs | Build or built-in |
| --- | --- | --- | --- |
| CPU | instruction\[16\], inM\[16\], reset | outM\[16\], writeM, addressM\[15\], pc\[15\] | build |
| Memory | in\[16\], address\[15\], load | out\[16\] | build |
| Computer | reset | - | build |
| ROM32K | address\[15\] | out\[16\] | built-in |
| Screen | in\[16\], address\[13\], load | out\[16\] | built-in |
| Keyboard | - | out\[16\] | built-in |
| RAM16K | in\[16\], address\[14\], load | out\[16\] | use built-in |
| ARegister / DRegister | in\[16\], load | out\[16\] | use built-in |
| PC | in\[16\], load, inc, reset | out\[16\] | use built-in |

Code examples 5

One possible CPU.hdl. The bits with side effects (d-bits, jump) are ANDed with isC, so an A-instruction's value bits never cause a write or a jump. hdl

```
CHIP CPU {
    IN  inM[16], instruction[16], reset;
    OUT outM[16], writeM, addressM[15], pc[15];
    PARTS:
    Not(in=instruction[15], out=isA);
    Not(in=isA, out=isC);

    // A register: instruction (A-instr) or ALU result (dest A)
    Mux16(a=instruction, b=aluOut, sel=isC, out=aIn);
    And(a=isC, b=instruction[5], out=destA);
    Or(a=isA, b=destA, out=loadA);
    ARegister(in=aIn, load=loadA, out=aOut, out[0..14]=addressM);

    // D register
    And(a=isC, b=instruction[4], out=loadD);
    DRegister(in=aluOut, load=loadD, out=dOut);

    // ALU: x = D, y = A or M (a-bit)
    Mux16(a=aOut, b=inM, sel=instruction[12], out=aOrM);
    ALU(x=dOut, y=aOrM,
        zx=instruction[11], nx=instruction[10], zy=instruction[9],
        ny=instruction[8],  f=instruction[7],  no=instruction[6],
        out=aluOut, out=outM, zr=zr, ng=ng);

    And(a=isC, b=instruction[3], out=writeM);

    // jump logic
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

Memory.hdl: address bits 14..13 pick the device. The keyboard has no load line, so DMux4Way's d output is left unconnected. hdl

```
CHIP Memory {
    IN  in[16], load, address[15];
    OUT out[16];
    PARTS:
    DMux4Way(in=load, sel=address[13..14], a=r0, b=r1, c=loadScr);
    Or(a=r0, b=r1, out=loadRam);
    RAM16K(in=in, load=loadRam, address=address[0..13], out=ramOut);
    Screen(in=in, load=loadScr, address=address[0..12], out=scrOut);
    Keyboard(out=kbdOut);
    Mux4Way16(a=ramOut, b=ramOut, c=scrOut, d=kbdOut,
              sel=address[13..14], out=out);
}
```

Computer.hdl: closing the fetch-execute loop (figure 5.9) hdl

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

Memory-mapped I/O in Hack assembly: while any key is held, blacken the first 16 pixels of row 0 asm

```
(LOOP)
    @KBD        // A = 24576
    D=M         // D = key code (0 if none)
    @LOOP
    D;JEQ       // no key -> keep polling
    @SCREEN     // A = 16384
    M=-1        // all 16 bits = 1 -> 16 black pixels
    @LOOP
    0;JMP
```

How one C-instruction drives the hardware: D;JGT text

```
D;JGT  ->  111 0 001100 000 001
           op+xx a c1..c6 ddd jjj
  isC=1. a=0 (y=A, ignored here). ALU computes x = D.
  ddd=000 -> loadA=0, loadD=0, writeM=0
  jjj=001 -> if D>0 (not zr and not ng) then PC=A else PC=PC+1
```

Gotchas 15

- A jump always goes to the address in A. So a jump takes two instructions: @TARGET, then comp;JUMP. The comp result only decides whether to jump, never where.
- The ch. 4 best-practice rule: a C-instruction that uses M should not jump, and one that jumps should not use M. One A selects both RAM\[A\] and ROM\[A\], so you should use it for one purpose only.
- Within one instruction, M and the jump target both use the A value from before the instruction. For example, AM=M+1 reads and writes RAM\[old A\], and the new A appears only at the next tick.
- An A-instruction loads the whole word into A. The MSB is 0, so the value has 15 bits (0-32767). You cannot write a negative constant with @. Load the positive value and negate it, e.g. @5 then D=-A.
- An A-instruction's value bits sit where the d and j fields would be. So loadD, writeM, the d1 part of loadA and the PC load must be ANDed with isC. Example: @8 has bit 3 set and would write to M without the gate. The a and c bits only steer the mux and ALU, so they need no gate.
- The xx bits (14-13) are ignored by the CPU. By convention they are 1, so C-instructions start with 111.
- outM and writeM are combinational and valid in the current cycle. addressM and pc come from registers and change only at the next tick. When writeM = 0, outM is undefined.
- A is 16 bits, but addressM and pc are 15 bits. Use sub-bus outputs: out\[0..14\]=addressM and out\[0..14\]=pc.
- PC priority is reset > load > inc. Tie inc to true. The CPU's reset input goes straight to PC.reset.
- The ALU's x is always D, and y is A or M (picked by the a-bit). So D-A and A-D have different comp codes.
- On the screen, the leftmost pixel of a 16-pixel group is bit 0 (the LSB), not the MSB. A row is 32 words, and row r starts at 16384 + 32\*r.
- Keyboard is read-only (no in or load pin) and shows only the key held now, with no buffer. If no key is held, the value is 0.
- Addresses above 24576 are invalid. The simple Mux4Way16 Memory above maps them to the keyboard, so programs must not use them.
- Hack is a Harvard machine. The program in ROM cannot be read or changed as data, and code in RAM cannot run.
- Use the built-in versions of ALU, registers, PC, RAM16K and gates. Your own versions work, but the built-ins show GUI state and are faster to simulate. No helper chips are needed.

Self-check: answer first, then reveal 7

1. What are the widths of the CPU's inputs and outputs, and why are addressM and pc 15 bits?

   instruction\[16\], inM\[16\], reset\[1\]. outM\[16\], writeM\[1\], addressM\[15\], pc\[15\]. Both memories have 32K = 2^15 addresses, so 15 bits are enough.
2. For the C-instruction 1110 0011 0001 1000 (binary), which ALU function runs, where does the result go, and is there a jump?

   a=0 and c=001100 give x, i.e. D. ddd=011 means D and M. jjj=000 means no jump. So it is MD=D: writeM=1, outM=D, D reloads its own value, and the next PC is PC+1.
3. Write the condition for loading the PC from A.

   isC AND ((j1 AND ng) OR (j2 AND zr) OR (j3 AND NOT zr AND NOT ng)).
4. Which RAM word holds the pixel at row 10, column 37, and which bit is it?

   16384 + 10\*32 + 37/16 = 16384 + 320 + 2 = 16706. The bit is 37 % 16 = 5, counted from the LSB.
5. When does the A register load, and where does its input come from in each case?

   On an A-instruction, the input is the instruction itself. On a C-instruction with d1=1, the input is the ALU output. A Mux16 selected by instruction\[15\] picks between them.
6. How does the Memory chip choose between RAM16K, Screen and Keyboard?

   By address bits 14-13. 00 or 01 goes to RAM16K (address\[0..13\]). 10 goes to Screen (address\[0..12\], so 16384 maps to Screen\[0\]). 11 goes to Keyboard (only 24576 is valid).
7. Why can Hack fetch and execute in one cycle when a single-memory von Neumann machine needs two?

   ROM32K and Memory have separate address inputs, so the instruction and the data are accessed at the same time. With one shared memory, the CPU must first fetch the instruction into an instruction register. Only then can the data address use the same memory address input.

Written from the book's chapters 1–5. Each chapter was drafted and then checked against the text and figures. Chapter 6 is not covered, so you can read it fresh. Your checkboxes are saved in this browser only.