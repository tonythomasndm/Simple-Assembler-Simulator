"""Aryan Gupta-2021314 Tony Thomas-2021360 Harsh Bhardwaj-2021322"""
registers={
    "000":0,
    "001":0,
    "010":0,
    "011":0,
    "100":0,
    "101":0,
    "110":0,
    "111":"0"*16
}
mem_address={}
for i in range(256):
    mem_address[i]="0"*16

def DecimalToBinary(num):
    binary="{0:b}".format(int(num))
    x=16-len(binary)
    binary='0'*x+binary
    return binary

def BinaryToDecimal(binary):
    i=len(binary)-1
    num=0
    for x in binary:
        num=num+int(x)*pow(2,i)
        i-=1
    return num

def overflowCheckerandHandler(num):
    global registers
    global flag_count
    while(num>=65536):
        registers["111"]="0"*12+"1000"
        flag_count=2
        num=num-65536
    return num

from itertools import cycle
from sys import stdout
file_output=stdout
from sys import stdin
import matplotlib.pyplot as plt
import numpy as np

stmts=[]
mem_addrs_counter=0
for stmt in stdin:
    stmt=stmt.strip()
    if stmt==" " or stmt=="\n" or stmt=="":
        continue
    mem_address[mem_addrs_counter]=stmt
    mem_addrs_counter+=1
    stmts.append(stmt)

count=0
jump_count=0
flag_count=0
program_counter=0
program_counter_new=0
memaddressgraph=[]
cyclenumbergraph=[]
cyclenumber=1
while(program_counter<len(stmts)):
    stmt=stmts[program_counter]
    opcode=stmt[:5]
#typeA_operations
    if opcode in ["10000","10001","10110","11010","11011","11100"]:
        reg1=stmt[7:10]
        reg2=stmt[10:13]
        reg3=stmt[13:]
    #addition
        if opcode == "10000":
            registers[reg3]=overflowCheckerandHandler(registers[reg1]+registers[reg2])
    #subtraction
        elif opcode == "10001":
            value=registers[reg1]-registers[reg2]
            if value>=0:
                registers[reg3]=value
            else:
                registers["111"]="0"*12+"1000"
                registers[reg3]=0
                flag_count=2
    #multiplicatipon
        elif opcode =="10110":
            registers[reg3]=overflowCheckerandHandler(registers[reg1]*registers[reg2])
    #bitwise_XOR_operation
        elif opcode =="11010":
            registers[reg3]=registers[reg1]^registers[reg2]
    #bitwise_OR_operation
        elif opcode =="11011":
            registers[reg3]=registers[reg1]|registers[reg2]
    #bitwise_AND_operation
        elif opcode =="11100":
            try:
                registers[reg3]=int(registers[reg1])&int(registers[reg2])
            except:
                raise Exception(" Reg1 :",registers[reg1],type(registers[reg1]),"and Reg2 :",registers[reg2],type(registers[reg2]))

#typeB_operations
    elif opcode in ["10010","11000","11001"]:
        reg1=stmt[5:8]
        imm=BinaryToDecimal(stmt[8:])
    #move immediate
        if opcode == "10010":
            registers[reg1]=imm
    #right-shift operation
        elif opcode == "11000":
            value=int(registers[reg1])>>imm
            if value<0:
                registers[reg1]=0
            else:
                registers[reg1]=value
    #left-shift operation
        elif opcode == "11001":
            x=registers[reg1]<<imm
            if (x>=65536):
                registers[reg1]=x-65536
            else:
                registers[reg1]=x
#typeC_operations
    elif opcode in ["10011","10111","11101","11110"]:
        reg1=stmt[10:13]
        reg2=stmt[13:]
    #move register
        if opcode == "10011":
            if reg2=="111":
                registers[reg2]=BinaryToDecimal(registers[reg1])
                registers['111']='0'*16
            else:
                registers[reg2]=registers[reg1]
    #divide
        elif opcode == "10111":
            registers["000"]=registers[reg1]//registers[reg2]
            registers["001"]=registers[reg1]%registers[reg2]
    #bitwise_NOT_operations
        elif opcode == "11101":
            x=DecimalToBinary(registers[reg1])
            s=''
            for bit in x:
                if bit=='0':
                    s=s+'1'
                else:
                    s=s+'0'
            registers[reg2]=BinaryToDecimal(s)
    #comparison
        elif opcode == "11110":
            flag_count=2
            value= int(registers[reg1])-int(registers[reg2])
            if value >0:
                registers["111"]="0"*12+"0010"
            elif value == 0:
                registers["111"]="0"*12+"0001"
            elif value <0 :
                registers["111"]="0"*12+"0100"
#typeD_operations
    elif opcode in ["10100","10101"]:
        reg1=stmt[5:8]
        mem_addrs=BinaryToDecimal(stmt[8:])
    #load
        if opcode == "10100":
            registers[reg1]=BinaryToDecimal(mem_address[mem_addrs])
    #store
        elif opcode == "10101":
            mem_address[mem_addrs]=DecimalToBinary(registers[reg1])
        memaddressgraph.append(mem_addrs)
        cyclenumbergraph.append(cyclenumber)
#typeE_operations
    elif opcode in ["11111","01100","01101","01111"]:
        mem_addrs=BinaryToDecimal(stmt[8:])
    #unconditional jump
        if opcode == "11111":
            program_counter_new=mem_addrs
            jump_count=1
    #jump if less than
        elif opcode == "01100":
            if registers["111"]=="0"*12+"0100":
                program_counter_new=mem_addrs
                jump_count=1
    #jump if equal
        elif opcode == "01111":
            if registers["111"]=="0"*12+"0001":
                program_counter_new=mem_addrs
                jump_count=1
    #jump if greater than
        elif opcode =="01101":
            if registers["111"]=="0"*12+"0010":
                program_counter_new=mem_addrs
                jump_count=1
#typeF_operation-halt
    elif opcode in ["01010"]:
        count=1
    if flag_count!=2:
        registers['111']='0'*16
    file_output.write(str(DecimalToBinary(program_counter))[8:]+" "+str(DecimalToBinary(registers["000"]))+" "+str(DecimalToBinary(registers["001"]))+" "+str(DecimalToBinary(registers["010"]))+" "+str(DecimalToBinary(registers["011"]))+" "+str(DecimalToBinary(registers["100"]))+" "+str(DecimalToBinary(registers["101"]))+" "+str(DecimalToBinary(registers["110"]))+" "+registers["111"]+"\n")
    memaddressgraph.append(program_counter)
    cyclenumbergraph.append(cyclenumber)
    cyclenumber+=1
    program_counter+=1
    flag_count=0
    if flag_count==2:
        registers['111']='0'*16
    if jump_count==1:
        program_counter=program_counter_new
        jump_count=0
    if count==1:
        break

for mem_addrs in mem_address:
    file_output.write(mem_address[mem_addrs]+"\n")
file_output.close()

x=np.array(cyclenumbergraph)
y=np.array(memaddressgraph)
plt.scatter(x,y)
#plt.show()