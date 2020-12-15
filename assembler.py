def loadregs():
    d = {}
    with open("registers.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = int(val)
    f.close()
    return d

def loadinstr():
    d = {}
    with open("instructions.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    f.close()
    return d

def reg2bin(reg):
    return bin(registers.get(reg))[2:].zfill(5)

registers = loadregs()
instructions = loadinstr()

f= open("assembly.txt","r")
code = f.read()
f.close()
instrs = code.split("\n")
f = open("output.txt","w")

for instr in instrs:
    word = instr.split(" ")
    regs = reg2bin(word[2])
    regs = regs + reg2bin(word[3])
    regs = regs + reg2bin(word[1])
    target_instr = instructions.get(word[0])
    result = target_instr[0:6]+regs+target_instr[21:32]
    f.write(result+"\n")
    
f.close()