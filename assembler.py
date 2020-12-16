import re

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

def bin2hex(binary):
    return hex(int(binary, 2))

registers = loadregs()
instructions = loadinstr()

f= open("assembly.txt","r")
code = f.read()
f.close()
instrs = code.split("\n")
f = open("output.txt","w")

def r_type(word):
    i=0
    if(len(word)>4):
        i+=1
    regstr = reg2bin(word[i+2])
    regstr = regstr + reg2bin(word[i+3])
    regstr = regstr + reg2bin(word[i+1])
    target_instr = instructions.get(word[i+0])
    result = target_instr[0:6]+regstr+target_instr[21:32]
    return result

def i_type(word):
    i=0
    if(len(word)>4):
        i+=1
    regstr = reg2bin(word[i+1])
    regstr = regstr + reg2bin(word[i+3])
    regstr = regstr + bin(int(word[i+2]))[2:].zfill(16)
    target_instr = instructions.get(word[i+0])
    result = target_instr[0:6]+regstr
    return result

def j_type(word):
    i=0
    if(len(word)>2):
        i+=1
    regstr = bin(word[i+1]).zfill(26)
    target_instr = instructions.get(word[i+0])
    result = target_instr[0:6]+regstr
    return result

def format_word(instr):
    instr = instr.replace(":","",1)
    instr = instr.replace(","," ",2)
    instr = instr.replace("("," ",1)
    instr = instr.replace(")"," ",1)
    return instr

def main():
    for instr in instrs:
        if(len(instr)!=0):
            word = format_word(instr)
            dollar = word.count("$")
            word = word.split()
            print(word)
            if(dollar == 3):
                f.write(bin2hex(r_type(word))+"\n")
            elif(dollar == 2 and word[-1][0] == "$"):
                f.write(bin2hex(i_type(word))+"\n")
            elif(dollar == 1 or dollar == 0):
                f.write(bin2hex(j_type(word))+"\n")
    f.close()


if __name__ == "__main__":
    main()