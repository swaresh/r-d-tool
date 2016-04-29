#!/usr/bin/env python

from __future__ import print_function
import sys,os
import subprocess
import re



open('new_error_dump.txt', 'w').close()

target=open("new_error_dump.txt","w+")

l=[]
n=sys.argv[4]
def sh(script):
   # print('bash -c "%s"' % script)
    #os.system('bash -c "%s"' % script)
    proc=subprocess.Popen(['bash -c "' + script +'"'],stdout=subprocess.PIPE, shell=True)
    (out,err)=proc.communicate()
    return out.decode("utf-8").rstrip() 


def sh2(script):
   # print('bash -c "%s"' % script)
    #os.system('bash -c "%s"' % script)
    proc=subprocess.Popen(['bash -c "' + script +'"'],stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    (out,err)=proc.communicate()
    return err.decode("utf-8").rstrip() 

def sh1(script):
    os.system('bash -c "%s"' % script)

def returnline(fil,num):
    f=open(fil,"r")
    c=1
    for line in f:
        if(num==c):
            return line
        c=c+1

def mark(col,length):
    string=""
    for i in range(1,length+1):
        if(i==col-1):
            string=string+"~"
        elif(i==col+1):
            string=string+"~"
        elif(i==col):
            string=string+"^"
        else:
            string=string+" "
    string=string+"\n"
    return string           
 
f=open(sys.argv[2],"r")
d={}
for l in f:
    l.rstrip('\n')
    x=l.split(":")
    if(len(x)>1):
        x[1]=x[1].rstrip('\n')
        d[x[0]]=x[1]

msgfile=open(sys.argv[3],"r")
g={}
for l in msgfile:
    #print(l)
    l.rstrip('\n')
    x=l.split(":")
    if(len(x)>1):        
        x[1]=x[1].rstrip("\n")
        g[x[0]]=x[1]
        #print(g)



def check():
    global target 
    dumpfile=open("error_dump.txt","r")
    for line in dumpfile:
        
        flag=0
        line.rstrip("\n")
        list1=line.split(":")
        #print(list1)
        if(len(list1)==5):
            #msgfile=open("error_messages.txt","r")
            for k in g.keys():
                #list1[4].rstrip("\n")
               # print(list1[4])
                list1[4]=list1[4][:-1]
                if(k==list1[4]):
                    #print("yes"+list1[4])
                    string2=k
                    string3=g[k]
                    list2=re.findall(r"'(\w+)'", string2)
                    list3=re.findall(r"'(\w+)'", string3)
                    for i in range(0,len(list2)):
                        string3=string3.replace(list3[i],list2[int(list3[i])-1]) 
                    g[k]=string3
                    line1=line.replace(list1[4],g[k])
                    #print(line)
                    flag=1
                    #print(line)
                    target.write(line1)
            if(flag==0):
                #print(line)
                target.write(line)
        else:
            target.write(line)
            #print(line) 
            
outfile=open("outputfile.txt","w+")
sh1("clang++ -Wno-parentheses "+sys.argv[1]+" &>error_dump.txt")
check()
#for line in target:
 #   print(line)
#sh1("cat new_error_dump.txt")
#print(d)        



if(int(n[0])==1):
    #print("case1:")
    a=sh("bin/check-power "+sys.argv[1]+" -- -w 2>1 | grep "+sys.argv[1])			
    #print(a)
    if(a!=""):
        #sh("cat new_error_dump.txt")
        a=a.split(" ")
        for k in d.keys():
            if(a[3]==k):                       
                col=int(a[2])+1;
                target.write(sys.argv[1]+":"+a[1]+":"+str(col)+": warning: "+d[k]+"\n")
                line=returnline(sys.argv[1],int(a[1]))
                target.write(line)
                string=mark(col,len(line))
                target.write(string)
if(int(n[1])==1):
    #print("case2:")
    a=sh("bin/check-if "+sys.argv[1]+" -- -w 2>1 | grep "+sys.argv[1])
    if(a!=""):
        a=a.split(" ")
        for k in d.keys():
            if(a[3]==k):                       
                col=int(a[2])+1;
                target.write(sys.argv[1]+":"+a[1]+":"+str(col)+": warning: "+d[k]+"\n")
                line=returnline(sys.argv[1],int(a[1]))
                target.write(line)
                string=mark(col,len(line))
                target.write(string)
if(int(n[2])==1):
    #print("case3:")
    a=sh("bin/check-and-or "+sys.argv[1]+" -- -w 2>1 | grep "+sys.argv[1])
    if(a!=""):
        a=a.split(" ")
        for k in d.keys():
            if(a[3]==k):                       
                col=int(a[2])+1
                target.write(sys.argv[1]+":"+a[1]+":"+str(col)+": warning: "+d[k]+"\n")
                line=returnline(sys.argv[1],int(a[1]))
                target.write(line)
                string=mark(col,len(line))
                target.write(string)
if(int(n[3])==1):

    #print("case4:")
    a=sh("bin/check-division "+sys.argv[1]+" -- -w 2>1 | grep "+sys.argv[1])
    if(a!=""):
        a=a.split(" ")
        for k in d.keys():
            if(a[3]==k): 
                col=int(a[2])+1                      
                target.write(sys.argv[1]+" line:"+a[1]+":"+" warning: "+d[k]+"\n")
                line=returnline(sys.argv[1],int(a[1]))
                target.write(line)
                string=mark(col,len(line))
                target.write(string)
if(int(n[4])==1):
    #target=open("new_error_dump.txt","r")   
    #print("case5:")
    a=sh("bin/check-for "+sys.argv[1]+" -- -w 2>1 | grep "+sys.argv[1])
    #ff=open("new_error_dump.txt","r")
    target.seek(0, 0)
    #for line in target:
    #    print(line)
    #sh1("cat new_error_dump.txt")
    sh1("rm new_error_dump1.txt")
    sh1("cp new_error_dump.txt new_error_dump1.txt")
    target1=open("new_error_dump1.txt","w+")
    linecount=0
    linenum=0
    flag=0
    for line in target:
        #print("yes") 
        linecount=linecount+1
        #print(line) 
        line.rstrip("\n")
        list1=line.split(":")
        if(len(list1)==5):
            #print("len:5")
            list1[4]=list1[4][:-1]
            if(list1[4]==" for loop has empty body [-Wempty-body]"):
                linenum=linecount
                flag=1
                #print(linenum+"this is ln")
    target.seek(0, 0)                
    linecount=0
    for line in target:
        linecount=linecount+1
        if(linecount<linenum or linecount>(linenum+3)):
            target1.write(line)
    if(flag==1):    
        sh1("cp new_error_dump1.txt new_error_dump.txt")

    if(a!=""):
        a=a.split(" ")
        for k in d.keys():
            if(a[3]==k):
                col=int(a[2])+1;                       
                target.write(sys.argv[1]+" line:"+a[1]+":"+" warning: "+d[k]+"\n")
                line=returnline(sys.argv[1],int(a[1]))
                target.write(line)
                string=mark(col,len(line))
                target.write(string)
if(int(n[5])==1):
    open('clang-check-warnings.txt', 'w').close()

    checkfile=open("clang-check-warnings.txt","r+") 
    #checkfile1=open("clang-check-warnings1.txt","w") 
    #print("case6:")
    a=sh2("clang-check -analyze "+sys.argv[1]+" -- -DF00")
    if(a!=""):
        checkfile.write(a)
    for line in checkfile:
        line.rstrip("\n")
        if(line.find(':')!=-1):
            line=line.split(":",1)    
            target.write(sys.argv[1]+":"+line[1])   
        elif(line.find('warning generated')!=-1 or line.find("warnings generated")!=-1):
            continue    
        else:
            target.write(line)


#if(int(n[6])==1):
    
    #a=sh("clang-tidy -checks=* "+sys.argv[1]+" --")
#    print(a)
    #if(a!=""):
     #   if(a.find(':')!=-1):
      #      a=a.split(":",1)    
       #     print(sys.argv[1]+":"+a[1])   
       # else:
       #     print(a)

#sh1("cat new_error_dump.txt")


target.seek(0, 0) 
for line in target:
    if((line.find('warning')!=-1 or line.find('error')!=-1) and line.find('generated')!=-1):    
        flag1=1
    else:    
        print(line,end="")

               
