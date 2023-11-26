# NOTE: This script is part of the Fuser Custom Song Manager program. Its contents are here for reference and archival purposes.
# Do not run this script on its own unless you know what you are doing.

import struct
indata=open('Meta_yourlove9pm.uasset','rb').read()
offset=0
def structread(str,len):
    global offset
    retval=struct.unpack(str,indata[offset:offset+len])
    offset+=len
    return retval
#all offset+=number are always null and can be ignored

usig=structread("BBBB",4) #signature, always (193,131,42,158)
ver=structread("<I",4)[0] ^ 0xffffffff #version, xor'd with FFFFFFFF, result should be 6
offset+=16
fdiroffset=structread("<I",4)[0] #file directory offset?
unk1=structread("<I",4)[0]
pn=structread("<I",4)[0]
offset+=4
unk2=structread("B",1)[0] #should be 128
num_names=structread("<I",4)[0]
off_names=structread("<I",4)[0]
offset+=8
num_exp=structread("<I",4)[0]
off_exp=structread("<I",4)[0]
num_imp=structread("<I",4)[0]
off_imp=structread("<I",4)[0]
offset+=20
guidhash=structread("BBBBBBBBBBBBBBBB",16) #16 byte guid hash, probably not needed
unk3=structread("<I",4)[0] # 1
unk4=structread("<I",4)[0] # 1 or 2
unk5=structread("<I",4)[0] # same as number of names?
offset+=36
unk6=structread("<I",4)[0]
offset+=4
padding_offset=structread("<I",4)[0]
flen=structread("<I",4)[0] # file length + 4, but seems to sometimes be unknown length/offset
offset+=12
unk7=structread("<i",4)[0]
fdataoffset=structread("<I",4)[0]

names=[[]]*num_names
for name in range(num_names):
    strlen=structread("<I",4)[0]
    strdata=indata[offset:offset+strlen]
    offset+=strlen
    flags=structread("<I",4)[0]

    names[name]=(strlen,strdata,flags)
imports=[[]]*num_imp
for imp in range (num_imp):
    parent_nameid=names[structread("<Q",8)[0]][1][:-1]
    class_id=names[structread("<Q",8)[0]][1][:-1]
    parent_importid=structread("<I",4)[0]^0xffffffff
    nameid=names[structread("<I",4)[0]][1][:-1]
    unkid=structread("<I",4)[0]
    imports[imp]=[parent_nameid,class_id,parent_importid,nameid,unkid]
exports=[b'']*num_exp
for exp in range(num_exp):
    exports[exp]=indata[offset:offset+100]
    offset+=100
offset+=4
indatauexp=open('Meta_yourlove9pm.uexp','rb').read()
offsetuexp=0

def structreaduexp(str,len):
    global offsetuexp
    retval=struct.unpack(str,indatauexp[offsetuexp:offsetuexp+len])
    offsetuexp+=len
    return retval

uexp_data=[]


while offsetuexp<=len(indatauexp):
    nameid=names[structreaduexp("<Q",8)[0]][1][:-1]
    print(nameid)
    if nameid==b'None':
        try:
            nameid=names[structreaduexp("<Q",8)[0]][1][:-1]
        except:
            break
    classid=names[structreaduexp("<Q",8)[0]][1][:-1]
    
    print(nameid, classid)

    # quit once we hit IsStreamOptimized, we don't use this data (yet?)
    if (nameid == b'IsStreamOptimized'):
        break

    
    lendata=structreaduexp("<Q",8)[0]
    propdata=[]
    if classid==b'NameProperty':
        offsetuexp+=1
        name=names[structreaduexp("<I",4)[0]]
        nameunk=structreaduexp("<I",4)[0]
        propdata=[name,nameunk]
    elif classid==b'SoftObjectProperty':
        offsetuexp+=1
        name=names[structreaduexp("<I",4)[0]]
        value=structreaduexp("<Q",8)[0]
        propdata=[name,value]
    elif classid==b'TextProperty':
        offsetuexp+=1
        flag=structreaduexp("<i",4)[0]
        historytype=structreaduexp("<b",1)[0]
        strings=[]
        if historytype == -1:
            numstr=structreaduexp("<i",4)[0]
            for i in range(numstr):
                strlen=structreaduexp("<i",4)[0]
                if strlen<0:
                    strlen=strlen*-2
                    u16str=indatauexp[offsetuexp:offsetuexp+strlen]
                    strings.append(u16str)
                else:
                    strings.append(indatauexp[offsetuexp:offsetuexp+strlen])
                offsetuexp+=strlen
        propdata=[flag,historytype,strings]
    elif classid==b'EnumProperty':
        enumType=names[structreaduexp("<Q",8)[0]]
        offsetuexp+=1            
        enumValue=names[structreaduexp("<Q",8)[0]]
        propdata=[enumType,enumValue]
    elif classid==b'IntProperty':
        offsetuexp+=1
        propdata=structreaduexp("<i",4)[0]
    elif classid==b'ArrayProperty':
        aclass=names[structreaduexp("<Q",8)[0]][1][:-1]
        offsetuexp+=1
        num_values=structreaduexp("<I",4)[0]
        values=[]
        if aclass==b'ObjectProperty':
            for i in range(num_values):
                values.append(imports[structreaduexp("<I",4)[0]^0xffffffff])
        elif aclass==b'FloatProperty':
            for i in range(num_values):
                values.append(structreaduexp("<f",4)[0])
        elif aclass==b'SoftObjectProperty':
            for i in range(num_values):
                offsetuexp+=1
                name=names[structreaduexp("<I",4)[0]]
                value=structreaduexp("<Q",8)[0]
                values.append([name,value])
            offsetuexp-=1
        propdata=[aclass,num_values,values]
    elif classid==b'ObjectProperty':
        offsetuexp+=1
        propdata=imports[structreaduexp("<I",4)[0]^0xffffffff]
    elif classid==b'StructProperty':
        curoffset=offsetuexp
        structclass=names[structreaduexp("<Q",8)[0]][1][:-1]
        structvalues=[]
        if structclass==b'Transposes':
            offsetuexp+=1
            guid=indatauexp[offsetuexp:offsetuexp+16]
            offsetuexp+=16
            while offsetuexp<=curoffset+lendata:
                key=names[structreaduexp("<Q",8)[0]][1][:-1]
                offsetuexp+=8
                value=structreaduexp("<i",4)[0]
                offsetuexp+=9
                structvalues.append([key,value])
        propdata=structvalues
    elif classid==b'mReferencedChildAssets':
        reftype=names[structreaduexp("<Q",8)[0]][1][:-1]
        print(reftype)
        if reftype==b'HmxMidiFileAsset':
            print(names[structreaduexp("<Q",8)[0]])
            offsetuexp+=1
            print(names[structreaduexp("<I",4)[0]][1][:-1])
            print(imports[structreaduexp("<I",4)[0]^0xffffffff])
            print(imports[structreaduexp("<I",4)[0]^0xffffffff])
            print(structreaduexp("<i",4)[0])
            print(structreaduexp("<i",4)[0])
            print(structreaduexp("<i",4)[0])
            print(structreaduexp("<i",4)[0])
            print(structreaduexp("<i",4)[0])
    curdata=[nameid,classid,lendata,propdata]
    uexp_data.append(curdata)
    open('out2.bin','wb').write(indatauexp[offsetuexp:])
output=open('out.txt','w')
output.write('NAMES\n')
for thing in names:
    output.write(str(thing)+"\n")
output.write('\nIMPORTS\n')
for thing in imports:
    output.write(str(thing)+"\n")
output.write('\nEXPORTS\n')
for thing in exports:
    output.write(str(thing)+"\n")
output.write('\nUEXP\n')
for thing in uexp_data:
    output.write(str(thing)+"\n")
output.close()