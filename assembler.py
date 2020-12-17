import os

def load_regs():
    d = {}
    with open("registers.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = int(val)
    f.close()
    return d

def load_instr():
    d = {}
    with open("instructions.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    f.close()
    return d

def load_labels():
    d = {}
    with open("labels.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    f.close()
    return d

def reg2bin(reg):
    return bin(registers.get(reg))[2:].zfill(5)

def bin2hex(binary):
    return "0x"+hex(int(binary, 2))[2:].zfill(8)

def format_word(instr):
    instr = instr.replace(":","",1)
    instr = instr.replace(","," ",2)
    instr = instr.replace("("," ",1)
    instr = instr.replace(")"," ",1)
    return instr

def label_writer(word):
    label_file = open("labels.txt","a+")
    label_file.write(word[0]+" "+str(address)+"\n")
    label_file.close()

def r_type(instr):
    i=0
    if(len(instr)>4):
        i+=1
    word = rtype
    word = word.replace("op",instructions[instr[0+i]][:6])
    word = word.replace("rd",reg2bin(instr[1+i]))
    word = word.replace("rs",reg2bin(instr[2+i]))
    word = word.replace("rt",reg2bin(instr[3+i]))
    word = word.replace("sh",reg2bin("$zero"))
    word = word.replace("fn",instructions[instr[0+i]][26:])
    return word

def i_type1(instr):
    i=0
    if(len(instr)>4):
        i+=1
    word = itype1
    word = itype1.replace("op",instructions[instr[0+i]][:6])
    word = word.replace("rt",reg2bin(instr[1+i]))
    word = word.replace("off",bin(int(instr[2+i]))[2:].zfill(16))
    word = word.replace("rs",reg2bin(instr[3+i]))
    return word

def i_type2(instr):
    i=0
    if(len(instr)>4):
        i+=1
    
    
    offset = int(abs(current_address-address)/4)-1
    print("current address: ",current_address)
    word = itype2
    word = itype2.replace("op",instructions[instr[0+i]][:6])
    word = word.replace("rt",reg2bin(instr[2+i]))
    word = word.replace("rs",reg2bin(instr[1+i]))
    if(instr[0+i][0] == "b"):
        word = word.replace("addr",bin(int(offset))[2:].zfill(16))
    elif(instr[i+3] in labels):
        word = word.replace("addr",bin(int(int(labels[instr[i+3]])/4))[2:].zfill(16))
    elif(int(instr[i+3])<0):
        val = bin(-int(instr[i+3][1:])+(1<<int(instr[i+3][1:])))
        word = word.replace("addr",val[2:].zfill(16))
    elif(int(instr[i+3])>=0):
        word = word.replace("addr",bin(int(int(instr[3+i])/4))[2:].zfill(16))
    else:
        val = bin(int(int(instr[i+3])/4))
        word = word.replace("addr",val[2:].zfill(16))
    
    return word

def j_type(instr):
    i=0
    if(len(instr)>4):
        i+=1
    word = jtype
    word = jtype.replace("op",instructions[instr[0+i]][:6])
    if(instr[i+1] in labels):
        word = word.replace("addr",bin(int(int(labels[instr[i+1]])/4))[2:].zfill(26))
    elif(instr[i+1][0]=="$"):
        word = word.replace("addr",reg2bin(instr[i+1]))
        word = word+bin(0)[2:].zfill(15)
        word = word+instructions[instr[0+i]][26:]
    else:
        word = word.replace("addr",bin(int(int(instr[1+i])/4))[2:].zfill(26))
    return word


address = 0
current_address = 0
labels = None
rtype = None
itype1 = None
itype2 = None
jtype = None
registers = load_regs()
instructions = load_instr()

f= open("test.src","r")
code = f.read()
instrs = code.split("\n")
f.close()
ff = open("output.obj","w")



def main():
    global address
    global labels
    global instrs
    global rtype
    global itype1
    global itype2
    global jtype
    global current_address
    j=0

    for instr in instrs:
        if(len(instr)!=0 and instr[0] != "#"):
            i=0
            if(len(instr)>4):
                i+=1
            word = format_word(instr)
            word = word.split()
            print(word)
            d = {"blt":"bne", "ble":"beq","bgt":"bne","bge":"beq"}
            if(word[i+0] in d):
                del instrs[j]
                if(i==1):
                    label = word[0]+": "
                else:
                    label=""
                instrs.insert(j,label+"slt $a0, "+word[i+1]+", "+word[i+2])
                instrs.insert(j+1, d.get(word[i+0])+" $a0, $zero, " +word[i+3])
        j+=1

        

    for instr in instrs:
        if(len(instr)!=0 and instr[0] != "#"):

            word = format_word(instr)
            dollar = word.count("$")
            word = word.split()
            if(dollar == 3 and len(word)>4):
                label_writer(word)
            elif(dollar == 2 and len(word)>4):
                label_writer(word)
            elif((dollar == 1 or dollar == 0)and len(word)>2):
                label_writer(word)
        address+=4
    labels = load_labels()
    os.remove("labels.txt")

    for instr in instrs:
        if(len(instr)!=0 and instr[0] != "#"):
            print(instr)
            print(current_address)
            rtype = "oprsrtrdshfn"
            itype1 = "oprsrtoff"
            itype2 = "oprsrtaddr"
            jtype= "opaddr"
            instr = format_word(instr)
            dollar = instr.count("$")
            instr = instr.split()
            if(dollar == 3):
                ff.write(bin2hex(r_type(instr))+"\n")
            elif(dollar == 2 and instr[-1][0] == "$"):
                ff.write(bin2hex(i_type1(instr))+"\n")
            elif(dollar == 2):
                ff.write(bin2hex(i_type2(instr))+"\n")
            elif(dollar == 1 or dollar == 0):
                ff.write(bin2hex(j_type(instr))+"\n")
            current_address += 4
    ff.close()


if __name__ == "__main__":
    main()