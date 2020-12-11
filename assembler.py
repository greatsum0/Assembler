
"""
şu listi ['0','0','0','0','0','0'] şuna çeviriyor "000000" char ları concat ediyor string yapıyor yani
"""
def convert(s): 
    new = "" 
    for x in s: 
        new += str(x)  
    return new 

"""
r typeları vaktimiz oldukça ekleriz elif olarak
"""
def rType(instr):
    instr = instr.split()
    print(instr)
    word = ['0' for i in range(32)]

    if(instr[0] == "add"):
        word[0:6] = ['0','0','0','0','0','0']
        word[6:11] = bin(return_reg_num(instr[2])+int(instr[2][2]))[2:].zfill(5)
        word[11:16] = bin(return_reg_num(instr[3])+int(instr[3][2]))[2:].zfill(5)
        word[16:21] = bin(return_reg_num(instr[1])+int(instr[1][2]))[2:].zfill(5)
        word[21:26] = ['0','0','0','0','0']
        word[26:32] = ['1','0','0','0','0','0']
        
    return word

"""
    registerin baş harfine göre başladığı indexi dönüyor
"""
def return_reg_num(reg):

    print(reg)
    if(reg == "$sp"):
        return 29
    reg = reg[1]
    if(reg == 'z'):
        return 0
    elif(reg == 'v'):
        return 2
    elif(reg == 'a'):
        return 4
    elif(reg == 't'):
        return 8
    elif(reg == 's'):
        return 16
    elif(reg == 'k'):
        return 26
    elif(reg == 'g'):
        return 28
    elif(reg == 'f'):
        return 30
    elif(reg == 'r'):
        return 31
    

"""
eklenmesi gereken şey: gelen isntructionun tipine göre hangi fonksiyon çağırılcak
eğer eleman sayısı 4 se mesela r type olabilir 2 ise j olabilir gibi
i type için de bişeyler bulucaz artık

vakit olcukça bakılabilir
"""
f = open("assembly.txt","r")
code = f.read()
f.close()
instrs = code.split("\n")
f = open("output.txt","w")
for instr in instrs:#dosyadaki her instructionu alıp eçviriciye atıyor
    word = rType(instr)
    print(len(word))
    print(word)
    f.write(convert(word)+"\n")
f.close()

