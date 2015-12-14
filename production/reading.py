__all__ = ['parseConf','readLong','readIOSV','readLOI','readIOS','readSOB','readDouble','readInt','readByte','readString']

from struct import *
def parseConf(c):    
    conf = {};
    conf['iosV'] = (c>>3) & 1
    conf['loi'] = (c>>2) & 1
    conf['ios'] = (c>>1) & 1
    conf['sob'] = (c>>0) & 1
    return conf;

def readIOSV(conf,msg,p,d=0,unsigned=True):
    if(unsigned):
        if(conf['iosV'] == 1):
            pos=p; read=4; div=d; ans = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=2; div=d; ans = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
            
    else:
        if(conf['iosV'] == 1):
            pos=p; read=4; div=d; ans = unpack('>i',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=2; div=d; ans = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
            
    if(d==0):
        return (pos,int(ans))
    else:
        return (pos,ans)


def readLOI(conf,msg,p,d=0,unsigned=True):
    if(unsigned):
        if(conf['loi'] == 1):
            pos=p; read=8; div=d; ans = unpack('>Q',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=4; div=d; ans = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
    else:
        if(conf['loi'] == 1):
            pos=p; read=8; div=d; ans = unpack('>q',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=4; div=d; ans = unpack('>i',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
    if(d==0):
        return (pos,int(ans))
    else:
        return (pos,ans)

def readIOS(conf,msg,p,d=0,unsigned=True):
    if(unsigned):
        if(conf['ios'] == 1):
            pos=p; read=4; div=d; ans = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=2; div=d; ans = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read; 
    else:
        if(conf['ios'] == 1):
            pos=p; read=4; div=d; ans = unpack('>i',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=2; div=d; ans = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
    if(d==0):
        return (pos,int(ans))
    else:
        return (pos,ans)

def readSOB(conf,msg,p,d=0,unsigned=True):
    if(unsigned):
        if(conf['sob'] == 1):
            pos=p; read=2; div=d; ans = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=1; div=d; ans = unpack('>B',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
    else:
        if(conf['sob'] == 1):
            pos=p; read=2; div=d; ans = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            pos=p; read=1; div=d; ans = unpack('>b',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
    if(d==0):
        return (pos,int(ans))
    else:
        return (pos,ans)

def readDouble(msg,p):
    pos=p; read=8; ans = unpack('>d',msg[pos:pos+read])[0]; pos+=read;
    return (pos,ans)

def readLong(msg,p):
    pos=p; read=8; ans = unpack('>Q',msg[pos:pos+read])[0]; pos+=read;
    return (pos,ans)

def readInt(msg,p,d=0,unsigned=True):
    if(unsigned):
        pos=p; read=4;div=d; ans = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
    else:
        pos=p; read=4;div=d; ans = unpack('>i',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;

    if(d==0):
        return (pos,int(ans))
    else:
        return (pos,ans)

def readByte(msg,p,unsigned=True):
    if(unsigned):
        pos=p; read=1; ans = unpack('>B',msg[pos:pos+read])[0]; pos+=read;
    else:
        pos=p; read=1; ans = unpack('>b',msg[pos:pos+read])[0]; pos+=read;
    return (pos,ans)

def readString(msg,p,size):
    pos=p; read=size; ans = ''.join(msg[pos:pos+read]); pos+=read;
    return (pos,ans)