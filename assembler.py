    import os
import sys
import argparse

def input_arguments():
    """
    Takes the input from terminal and returns a parse dictionary for arguments
    
    Parameters
    ----------
    NONE
    """
    parser = argparse.ArgumentParser(description="This is an assembler")
    parser.add_argument("-s" ,"--source", type= str, nargs= 1,
                        help="source code to be converted to machine language")
    parser.add_argument("-o", "--object", type= str, nargs = 1,
                        help="output file to be saved")
    parser.add_argument("-i", "--interactive", type= str, nargs = 1,
                        help="interactive code converter")

    global args
    args = vars(parser.parse_args())
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return args

def load_regs():
    """
    It reads register from file.
    
    Parameters
    ----------
    NONE
    """
    d = {}
    with open("registers.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = int(val)
    f.close()
    return d

def load_instr():
    """
    It reads instructions from file.
    
    Parameters
    ----------
    NONE
    """
    d = {}
    with open("instructions.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    f.close()
    return d

def load_labels():
    """
    It reads labels and their addresses from file.
    
    Parameters
    ----------
    NONE
    """
    d = {}
    with open("labels.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    f.close()
    return d

def reg2bin(reg):
    """
    It gets reg and convert it and return its binary equivalent.
    
    Parameters
    ----------
    reg 
    """
    return bin(registers.get(reg))[2:].zfill(5)

def bin2hex(binary):
    """
    It gets binary and convert it and return its hexadecimal equivalent.
    
    Parameters
    ----------
    binary
    """
    return "0x"+hex(int(binary, 2))[2:].zfill(8)

def format_word(instr):
    """
    It gets instr and convert it to readable format. Then, returns it.
    
    Parameters
    ----------
    instr
    """
    instr = instr.replace(":","",1)
    instr = instr.replace(","," ",2)
    instr = instr.replace("("," ",1)
    instr = instr.replace(")"," ",1)
    return instr

def label_writer(word):
    """
    It writes the label and its address to a file.
    
    Parameters
    ----------
    NONE
    """
    label_file = open("labels.txt","a+")
    label_file.write(word[0]+" "+str(address)+"\n")
    label_file.close()

def twos_complement(instr):
    """
    returns twos complement of an negative value
    
    Parameters
    ----------
    instr negative number as stirng
    """
    val = bin(-int(instr[1:])+(2*int(instr[1:])))[2:]
    val = val.replace("1","a")
    val = val.replace("0","b")
    val = val.replace("a","0")
    val = val.replace("b","1")
    temp_len = len(val)
    val = bin(int(val,2)+1)[2:].zfill(temp_len)
    val = val.rjust(8-len(val) + len(val), '1')
    val = val.zfill(16)
    return val

def r_type(instr):
    """
    converts r type mips instruction into hex value
    
    Parameters
    ----------
    instr: instruction
    """
    i=0
    if(len(instr)>4):
        i+=1
    word = rtype
    word = word.replace("op",instructions[instr[0+i]][:6])
    word = word.replace("rd",reg2bin(instr[1+i]))
    if(instr[0+i]=='sll' or instr[0+i]=='srl'):
        word = word.replace("rs",reg2bin("$zero"))
        word = word.replace("rt",reg2bin(instr[2+i]))
        valu = bin(int(instr[3+i]))[2:].zfill(5)
        word = word.replace("sh",valu)
    else:
        word = word.replace("rs",reg2bin(instr[2+i]))
        word = word.replace("rt",reg2bin(instr[3+i]))
        word = word.replace("sh",reg2bin("$zero"))
    word = word.replace("fn",instructions[instr[0+i]][26:])
    return word

def i_type1(instr):
    """
    converts i type mips instruction into hex value
    
    Parameters
    ----------
    instr: instruction
    """
    i=0
    if(len(instr)>4):
        i+=1
    word = itype1
    word = itype1.replace("op",instructions[instr[0+i]][:6])
    word = word.replace("rs",reg2bin(instr[3+i]))
    word = word.replace("rt",reg2bin(instr[1+i]))
    word = word.replace("off",bin(int(instr[2+i]))[2:].zfill(16))
    
    return word

def i_type2(instr):
    """
    converts i type mips instruction into hex value
    
    Parameters
    ----------
    instr: instruction
    """
    i=0
    if(len(instr)>4):
        i+=1
    word = itype2
    word = itype2.replace("op",instructions[instr[0+i]][:6])
    word = word.replace("rt",reg2bin(instr[1+i]))
    word = word.replace("rs",reg2bin(instr[2+i]))
    if(instr[0+i][0] == "b"):
        label_address = int(labels.get(instr[i+3]))
        label_offset = int((label_address-current_address-4)/4)
        if(label_offset <0):
            val = bin(-int(abs(label_offset))+(1<<int(abs(label_offset))))[2:]
            val = val.rjust(16-len(val) + len(val), '1')
            val = val[-16:]
            word = word.replace("addr",val)
        else:
            word = word.replace("addr",bin(label_offset)[2:].zfill(16))
    elif(int(instr[i+3])<0):
        
        word = word.replace("addr",twos_complement(instr[i+3]))
    elif(int(instr[i+3])>=0):
        word = word.replace("addr",bin(int(int(instr[3+i])))[2:].zfill(16))
    else:
        val = bin(int(int(instr[i+3])/4))
        word = word.replace("addr",val[2:].zfill(16))
    
    return word

def j_type(instr):
    """
    converts j type mips instruction into hex value
    
    Parameters
    ----------
    instr: instruction
    """
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

def handle_pseudo():
    """
    converts pseudo code into real mips instructions and replaces it in the instructions list
    
    Parameters
    ----------
    instr: NONE
    """
    j=0
    for instr in instrs:
        if(len(instr)!=0 and instr[0] != "#"):
            
            word = format_word(instr)
            word = word.split()
            i=0
            if(len(word)>4):
                i+=1
            d = {"blt":"bne", "ble":"beq","bgt":"bne","bge":"beq","move":"add"}
            if(word[i+0] in d):
                del instrs[j]
                if(i==1):
                    label = word[0]+": "
                else:
                    label=""

                if(word[i+0]=='move'):
                    instrs.insert(j,label+d.get(word[i+0])+" "+word[i+1]+", "+word[i+2]+", $zero")
                else:
                    instrs.insert(j,label+"slt $at, "+word[i+1]+", "+word[i+2])
                    instrs.insert(j+1, d.get(word[i+0])+" $at, $zero, " +word[i+3])
                    
        j+=1 

def handle_labels():
    """
    calculates the corresponding label addresses for instructions 
    
    Parameters
    ----------
    instr: instruction
    """
    global address
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

def translate(ff):
    """
    translates MIPS instruction into hex value with correspoınding type 
    
    Parameters
    ----------
    ff: file output stream
    """
    global instrs
    global current_address
    global rtype
    global itype1
    global itype2
    global jtype
    
    for instr in instrs:
        if(len(instr)!=0 and instr[0] != "#"):
            print("PC: "+str(current_address)+"--> "+instr)
            rtype = "oprsrtrdshfn"
            itype1 = "oprsrtoff"
            itype2 = "oprsrtaddr"
            jtype= "opaddr"
            instr = format_word(instr)
            instr = instr.split()
            i=0
            if(len(instr)>4):
                i+=1    
            r_types = ["add","addu","sub","subu","and","or","nor","slt","sltu","sll","srl"]
            i_type1s = ["lw","sw"]
            i_type2s = ["beq","bne","addi","addiu","andi","ori","slti","sltiu","lui"]
            j_types =["j","jal","jr"]

            if(instr[0+i] in r_types):
                if(ff != None):
                    ff.write(bin2hex(r_type(instr))+"\n")
                else:
                    print(bin2hex(r_type(instr)))
            elif(instr[0+i] in i_type1s):
                if(ff != None):
                    ff.write(bin2hex(i_type1(instr))+"\n")
                else:
                    print(bin2hex(i_type1(instr)))
            elif(instr[0+i] in i_type2s):
                if(ff != None):
                    ff.write(bin2hex(i_type2(instr))+"\n")
                else:
                    print(bin2hex(i_type2(instr)))
            elif(instr[0+i] in j_types):
                if(ff != None):
                    ff.write(bin2hex(j_type(instr))+"\n")
                else:
                    print(bin2hex(j_type(instr)))
            current_address += 4

def main():
    """
    It's main part where we will decide if we read a file our get an input as an interactive session.
    If it is interactive, we will skip label and file operation and directly handle it.
    
    Parameters
    ----------
    """
    global args
    global address
    global labels
    global instrs
    global rtype
    global itype1
    global itype2
    global jtype
    global current_address
    global instructions
    global registers

    registers = load_regs()
    instructions = load_instr()
    args = input_arguments()

    if(args["interactive"] == None):
        inputfile = args["source"][0]
        outputfile = args["object"][0]

        f= open(inputfile,"r")
        code = f.read()
        instrs = code.split("\n")
        f.close()
        ff = open(outputfile,"w")
        handle_pseudo()
        handle_labels()
        labels = load_labels()
        os.remove("labels.txt")
        translate(ff)
        ff.close()

    else:
        instrs = []
        instrs.append(args["interactive"][0])
        handle_pseudo()
        translate(None)

"""
GLOBALS
"""
address = 4194304
current_address = 4194304
labels = None
rtype = None
itype1 = None
itype2 = None
jtype = None
args = None
instrs = None
instructions = None
registers = None


if __name__ == "__main__":
    main()