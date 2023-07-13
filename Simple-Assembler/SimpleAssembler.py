"""Aryan Gupta-2021314 Tony Thomas -2021360 Harsh Bhardwaj-2021322"""
opcode={
    "add":"10000",
    "sub":"10001",
    "mov":"10010",
    "movr":"10011",
    "ld":"10100",
    "st":"10101",
    "mul":"10110",
    "div":"10111",
    "rs":"11000",
    "ls":"11001",
    "xor":"11010",
    "or":"11011",
    "and":"11100",
    "not":"11101",
    "cmp":"11110",
    "jmp":"11111",
    "jlt":"01100",
    "jgt":"01101",
    "je":"01111",
    "hlt":"01010"
}

registers={
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111"
}
from sys import stdout
file_output=stdout

def DecimalToBinary(num):
    bine="{0:b}".format(int(num))
    x=8-len(bine)
    bine='0'*x+bine
    return bine

def register_checker(reg,i):
    if reg not in registers.keys():
        file_output.write("Error, Use of Invalid Registers in line "+str(i))
        exit()

def all_variable_definition_at_beginning(stmts):
    for i in range(len(stmts)):
        count=0
        if stmts[i][0]=="var":
            if count ==1:
                file_output.write("Error, All the variable definitions are not made at the beginning of the assembly language, specifically "+stmts[i][0]+" in line "+str(i))
                exit()
        else:
            count=1

def immediate_checker(imm, i):
    if "$"!=imm[0]:
        file_output.write("Error, Immediate not provided, line "+str(i))
        exit()
    try :
        x=int(imm[1:])
        if(x>=256 or x<0):
            file_output.write("Error, The Immediate exceeds the limit from 0 to 255, line "+str(i))
            exit()
    except ValueError:
        file_output.write("Error, The immediate should be a whole number, line "+str(i))
        exit()

def typeA_checker(stmt,i):
    if len(stmt) != 4:
        file_output.write("Error, Invalid Number of Arguments for a Type-A Instruction in line "+str(i))
        exit()
    register_checker(stmt[1],i)
    register_checker(stmt[2],i)
    register_checker(stmt[3],i)
def typeB_checker(stmt,i):
    if len(stmt) != 3:
        file_output.write("Error, Invalid Number of Arguments for Type-B Instruction in line "+str(i))
        exit()
    register_checker(stmt[1],i)
    immediate_checker(stmt[2],i)
def typeC_checker(stmt,i):
    if len(stmt) != 3:
        file_output.write("Error, Invalid Number of Arguments for Type-C Instruction in line "+str(i))
        exit()
    register_checker(stmt[1],i)
    register_checker(stmt[2],i)
def typeD_checker(stmt,i):
    if len(stmt) != 3:
        file_output.write("Error, Invalid Number of Arguments for Type-D Instruction in line "+str(i))
        exit()
def typeE_checker(stmt,i):
    if len(stmt) != 2:
        file_output.write("Error, Invalid Number of Arguments for Type-E Instruction in line "+str(i))
        exit()
def typeF_checker(stmt,i):
    if len(stmt) != 1:
        file_output.write("Error, Invalid Number of Arguments for Type-E Instruction in line "+str(i))
        exit()

from sys import stdin
stmts=[]
for x in stdin:
    x=x.strip()
    if x=="\n" or x==" " or x=="":
        continue
    lst=x.split()
    stmts.append(lst)

#Editing in mov
for i in range(len(stmts)):
    if stmts[i][0] in ['mov','ls','rs']:
        try:
            if("$" not in stmts[i][2]):
                stmts[i][0]=stmts[i][0]+'r'
        except:
            file_output.write("Error, Immediate not provided in line "+str(i))
            exit()

#Edit and storing the label names
labels_lst={}
pc=0
for i in range(len(stmts)):
    if stmts[i][0][len(stmts[i][0])-1]==":":
        if len(stmts[i][0])==1:
            file_output.write("Error, Invalid statement in line "+str(i))
            exit()
        labels_lst[stmts[i][0][:-1]]=pc #storing labels
        stmts[i].remove(stmts[i][0])
        if len(stmts[i])==0:
            file_output.write("Error, Empty label in line "+str(i))
            exit()
    if stmts[i][0]!="var":
        pc+=1

for x in stmts:
    if(len(x)==0):
        stmts.remove(x)

if len(stmts)>256:
    file_output.write("Error, Number of Instructions exceeding the limit of 256")
    exit()

#Typos in Instruction Name
for i in range(len(stmts)):
    if stmts[i][0] not in opcode.keys() and stmts[i][0]!="var":
        file_output.write("Error, Typo in the instruction name or invalid declaration in line "+ str(i))
        exit()

instructions={}
mem_address=0
for i in range(len(stmts)) :
    if stmts[i][0]!="var":
        mem_address+=1

#creating a list of variables
all_variable_definition_at_beginning(stmts)
var_list={}
for i in range(len(stmts)):
    if stmts[i][0]=="var":
        var_list[stmts[i][1]]=mem_address
        mem_address+=1

#Checking if the variables or labels used in instructions is declared or not
for i in range(len(stmts)) :
    if stmts[i][0] in ['ld','st']:
        if stmts[i][2] not in var_list:
            file_output.write("Error, Use of an undefined variable in line "+str(i))
            exit()
    if stmts[i][0] in ['jmp','jlt','jgt','je']:
        if stmts[i][1] not in labels_lst.keys():
            file_output.write("Error, Use of an undefined label in line "+str(i))
            exit()

#Checking if hlt instruction is present or not, if present, it should be the last
is_hlt=False
for i in range(len(stmts)):
    if 'hlt' in stmts[i]:
        if i==len(stmts)-1:
            if(stmts[i][0]=='hlt' and len(stmts[i])==1):
                is_hlt=True
            else:
                file_output.write("Error, Illegal use of hlt instruction in line "+str(i))
                exit()
        else:
            file_output.write("Error, hlt must be the last instrucion in line "+str(i))
            exit()
if not(is_hlt):
    file_output.write("Error, missing hlt instruction")
    exit()

#if error-free
def get_mem_address_typeD(mem_address):
    return var_list[mem_address]

def get_mem_address_typeE(mem_address):
    return labels_lst[mem_address]

def typeA(stmt):
    return opcode[stmt[0]] + "0"*2 + registers[stmt[1]] + registers[stmt[2]] + registers[stmt[3]]
def typeB(stmt):
    x=opcode[stmt[0]] + registers[stmt[1]] + DecimalToBinary(int(stmt[2]))
    return x
def typeC(stmt):
    return opcode[stmt[0]] +"0"*5 + registers[stmt[1]] + registers[stmt[2]]
def typeD(stmt):
    x=opcode[stmt[0]] + registers[stmt[1]] + DecimalToBinary(int(get_mem_address_typeD(stmt[2])))
    return x
def typeE(stmt):
    x=opcode[stmt[0]]+ "0"*3 + DecimalToBinary(int(get_mem_address_typeE(stmt[1])))
    return x
def typeF(stmt):
    return opcode[stmt[0]]+ "0"*11

for i in range(len(stmts)):
    if('FLAGS' in stmts[i]):
        if(len(stmts[i])!=3 or stmts[i][0]!='movr' or stmts[i][1]!='FLAGS'):
            file_output.write("Error, Illegal use of FLAGS register in line "+str(i))
            exit()
        else:
            typeC_checker(stmts[i],i)
    if(stmts[i][0] in ['add','sub','mul','xor','or','and']):
        typeA_checker(stmts[i], i)
    elif(stmts[i][0] in ['mov','ls','rs']):
        typeB_checker(stmts[i], i)
    elif(stmts[i][0] in ['movr','div','not','cmp']):
        typeC_checker(stmts[i], i)
    elif(stmts[i][0] in ['ld','st']):
        typeD_checker(stmts[i], i)
    elif(stmts[i][0] in ['jmp','jlt','jgt','je']):
        typeE_checker(stmts[i], i)
    elif(stmts[i][0]=="hlt"):
        typeF_checker(stmts[i], i)

#Editing in immediate
for i in range(len(stmts)):
    if stmts[i][0] in ['mov','ls','rs']:
        if("$" in stmts[i][2]):
            stmts[i][2]=stmts[i][2][1:]

for i in range(len(stmts)):
    if(stmts[i][0] in ['add','sub','mul','xor','or','and']):
        file_output.write(typeA(stmts[i])+"\n")
    elif(stmts[i][0] in ['mov','ls','rs']):
        file_output.write(typeB(stmts[i])+"\n")
    elif(stmts[i][0] in ['movr','div','not','cmp']):
        file_output.write(typeC(stmts[i])+"\n")
    elif(stmts[i][0] in ['ld','st']):
        file_output.write(typeD(stmts[i])+"\n")
    elif(stmts[i][0] in ['jmp','jlt','jgt','je']):
        file_output.write(typeE(stmts[i])+"\n")
    elif(stmts[i][0]=="hlt"):
        file_output.write(typeF(stmts[i]))
file_output.close()