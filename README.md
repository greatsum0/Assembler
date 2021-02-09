# MIPS Assembler

Hello everyone. This project is a fun project about MIPS assembly language. 


## What is MIPS Assembly Language ?

MIPS (Microprocessor without Interlocked Pipeline Stages) is an assembly language of the MIPS processors.
Since many embedded systems run on the MIPS processor, the MIPS assembly language is a handy language to understand. Knowing how to code in this language provides a better grasp of the lower level of how these programs work.

## What Is the Aim of This Project ?

This project aims to convert MIPS assembly code into machine code.

## What are pseudo-instructions ?

Pseudo instructions are instructions that consist of 1 or more instructions. For instance: 

```
blt $t0, $t1, exit

```
C-ish meaning 
```
if (t0 < t1)
    pc++
else
    *branch*
```

```
slt $at, $t0, $t1 
bne $at, $zero, exit
```
C-ish meaning 
```
if($t0 < $t1)
    $at = 1
else
    $at = 0

if ($at != $zero) 
    pc++
else
    branch*
```

In this example we can see that blt instruction(branch less than) translates into slt(set less than) and bne(branch not equal) meaning:

# How to Run the Code

Batch mode: python assembler.py -s source -o output
interactive mode: python assembler -i 'MIPS instruction'

debug mode: append -d to the arguments to see PC and instructions  

example run: python assembler.py -s source.src -o output.obj -d        
example run: python assembler.py -s source.src -o output.obj
example run: python assembler.py -i 'addi $s1, $s0, -1'

# What is instructions.txt

Text file that contains skeleton of the instructions.

# What is registers.txt

Text file that contains registers and their corresponding values.
