
# coding: utf-8

# In[1]:

#!/usr/bin/env python

import sys;
import time;
import json;
from selenium import webdriver;
import selenium
import selenium.webdriver.support.ui as UI
import re;
import socket
import urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime
import hashlib
from struct import *

#----- Configuration

conf={}
conf['username'] = 'crawler001'
conf['password'] = 'crawler001'
conf['url']      = 'https://click2win.settrade.com'
conf['APIVersion']      = '1'
conf['hourshift']      = 15 # from server to thai timezone +7 

# ----- Start crawling 
path='/Users/nik9618/Desktop/Library/chromedriver';
driver = webdriver.Chrome(path)
driver.get(conf['url'])
print 'Main page loaded'
sys.stdout.flush()
time.sleep(1);

# ----- Login
userBox = driver.find_element_by_name('txtLogin')
passBox = driver.find_element_by_name('txtPassword')
userBox.clear()
passBox.clear()
userBox.send_keys(conf['username'])
passBox.send_keys(conf['password'])
elem = driver.find_element_by_class_name('input_login_submit-login');
elem.click();
print 'Logged In'
sys.stdout.flush()
time.sleep(3);


# In[2]:


# ------ Generate flash variables
driver.get('view-source:'+conf['url']+'/realtime/streaming5/flash/StreamingPage.jsp')
# print 'view-source:'+conf['url']+'/realtime/streaming5/flash/StreamingPage.jsp'
print 'Streaming Opened'
sys.stdout.flush()
time.sleep(1)
src = driver.page_source
src = src[src.find('flashVar'):]
src = src[src.find('{')+1:]
src = src[0:src.find('}')]
flashVar = {}
src = src.split(",")
for line in src:
	line = line.split(":")
	flashVar[urllib.unquote(line[0])] = urllib.unquote(line[1][1:-1])
print 'Flash Variable Generated'
sys.stdout.flush()
time.sleep(1);


# In[3]:

driver.get(conf['url'] + flashVar['fvSyncTimeURL'])
time = driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")

thaiTime = int(time[1]) + conf['hourshift']*60*60*1000
thaiTime = thaiTime/1000

print 'time synchronized'
print time


# In[4]:

url = conf['url'] + flashVar['fvGenerateKeyURL']
key = datetime.datetime.fromtimestamp(thaiTime).strftime('%d/%m/%Y') + "_" + flashVar['fvBrokerId']+"_"+flashVar['fvUserref']
m = hashlib.md5()
m.update(key)
hs = m.hexdigest()
print "hash("+key +") = " + hs
script = ""
script = script + 'sc=\'\'; sc += \'<form id="dynForm" action="'+url+'" method="post">\';'
script = script + 'sc += \'<input type="hidden" name="time" value="'+time[1]+'">\';'
script = script + 'sc += \'<input type="hidden" name="clientType" value="'+flashVar['fvRealtimeClientType']+'">\';'
script = script + 'sc += \'<input type="hidden" name="txtSETNET3" value="'+flashVar['fvSETNET3']+'">\';'
script = script + 'sc += \'<input type="hidden" name="APIVersion" value="'+conf['APIVersion']+'">\';'
script = script + 'sc += \'<input type="hidden" name="q" value="398b4ac3e846f9529519de0e8f0567c3">\';'
script = script + 'sc += \'</form>\';'
script = script + 'document.body.innerHTML += sc;'
# print script;

script = script + 'document.getElementById("dynForm").submit()';
# driver.get('https://click2win.settrade.com'+flashVar['fvGenerateKeyURL'])
# 
driver.execute_script(script)
src = driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")
print src


# In[5]:

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns = socket.gethostbyname_ex(src[2]);
host = dns[2][0];
port = int(src[3])
conn = s.connect((host, port))

# print conn
print src[2]
# print dns
print host
print port
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


# In[6]:

ss = flashVar['fvUserref']+"|"+flashVar['fvBrokerId']+"|"+src[1]+"|" + str(int(time[1])+3313) + "|gen5sc1|1\n"
print s.send(ss)
print ss;


# In[7]:

# print s.send("REG|5\n")
print s.send("REG|4^N~N^N~N^E~D^E~D\n")
# print s.send("REG|1^^^M\n")
# print s.send("REG|3^^\n")
# print s.send("REG|5\n")
# print s.send("REG|4^^N~N^^E~D\n")
# print s.send("REG|1^^^M\n")
# print s.send("REG|3^^\n")
# print s.send("REG|5\n")

# print s.send("REG|3^^\n")


# In[247]:

# size = s.recv(2)
# size = unpack('>H',size)[0]
# msg = s.recv(size)
# print msg


# In[248]:

# service = unpack('>B',msg[0])[0];
# config = unpack('>B',msg[1])[0];
# signature = unpack('>B',msg[1])[0];
# intinstrumentType = unpack('>B',msg[1])[0];
# print intinstrumentType
# public static const NO_TYPE:InstrumentType = new InstrumentType("No Type", -1);
# public static const EQUITY:InstrumentType = new InstrumentType("Equity", 0);
# public static const FUTURES:InstrumentType = new InstrumentType("Futures", 1);
# public static const OPTIONS:InstrumentType = new InstrumentType("Options", 2);
# public static const INDEX:InstrumentType = new InstrumentType("Index", 3);

# tickerSubType = TickerSubType.lookUpFromFeed(instrumentType, subArray[0]);  D OR E 
# orderSide = OrderSide.lookUpFromFeed(subArray[1]); S B H C
# trend = Trend.lookUpFromFeed(subArray[2]); up still down
# isSum = (subArray[3] == 1); ???
#4121

# tickerSubType = signature & 0x0F
# orderSide = (signature & 0x10) >> 4 
# trend = (signature & 0x60) >> 5
# isSum = (signature & 0x80) >> 7

# if(tickerSubType == 0):
#     tickerSubType='E'
# else:
#     tickerSubType='D'

# if(orderSide == 0):
#     orderSide='Buy'
# elif(orderSide == 1):
#     orderSide='Sell'
# elif(orderSide == 2):
#     orderSide='Short'
# elif(orderSide == 3):
#     orderSide='Cover'
    
# if(trend == 0):
#     trend='Up'
# elif(trend == 1):
#     trend='-'
# elif(trend == 2):
#     trend='Down'
# elif(trend == 3):
#     trend='NoData'
    
# print "tickerType= " + tickerSubType
# print "orderSide= " + orderSide
# print "trend= " + trend
# print "isSum= " + str(isSum)

# if(tickerSubType=='E'):
#     pos=3
#     total = {}
#     read=1; div=0; size = unpack('>B',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# #     print size
#     read=1; div=0; size = unpack('>B',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
#     size=int(size)
# #     print size
#     read=size; div=0; instrument = ''.join(msg[pos:pos+read]); pos+=read;
# #     print instrument
#     read=2; div=2; price = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# #     print price
#     read=2; div=2; change = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# #     print change
#     read=4; div=0; seqID = int(unpack('>I',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;
# #     print seqID
#     read=1; div=0; volCount = int(unpack('>B',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;
# #     print volCount
#     # print pos
#     # print len(msg)
#     read=2; div=0; volumn = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# #     print volumn

# print str(instrument)+"\t"+str(price)+"\t" + str(change) + "\t"+str(volCount)+"\t"+ str(volumn)


# In[161]:

# service = unpack('>B',msg[0])[0];
# config = unpack('>B',msg[1])[0];
# flag = unpack('>B',msg[2])[0];

# print "service : "+ str(service);
# print "config : "+ str(config);
# print "flag : "+ str(flag);

# pos=3
# total = {}
# read=4; div=2; total['setIndex'] = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=4; div=2; total['setHigh'] = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=4; div=2; total['setLow'] = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;

# read=2; div=2; total['setChange'] = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=2; div=2; total['setHighChange'] = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=2; div=2; total['setLowChange'] = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;

# read=4; div=2; total['setTotalValue'] = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=8; div=0; total['setTotalVolume'] = unpack('>Q',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;

# read=2; div=0; total['setGainers'] = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=2; div=0; total['setLosers'] = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
# read=2; div=0; total['setUnchanged'] = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;

# read=1; div=0; size = unpack('>B',msg[pos:pos+read])[0]; pos+=read;
# read=size; div=0; total['setStatus'] = ''.join(msg[pos:pos+read]); pos+=read;

# print total


# In[ ]:




# In[ ]:




# In[ ]:

while(True):
    size = s.recv(2)
    size = unpack('>H',size)[0]
    msg = s.recv(size)
    #print msg
    service = unpack('>B',msg[0])[0];
    config = unpack('>B',msg[1])[0];
    intinstrumentType = unpack('>B',msg[2])[0];

    
    if(intinstrumentType==0): # equity
        signature = unpack('>B',msg[3])[0];
        
        tickerSubType = (signature) & 0x0F
        orderSide = (signature>>4) & 0x01
        trend = (signature>>5) & 0x03
        isSum = (signature>>7) & 0x01
        
        iosV = config>>3 & 1
        loi = config>>2 & 1
        ios = config>>1 & 1
        sob = config>>0 & 1

        if(tickerSubType == 0): tickerSubType='Common'
        elif(tickerSubType == 1): tickerSubType='Foriegn'
        elif(tickerSubType == 2): tickerSubType='ETF'
        elif(tickerSubType == 3): tickerSubType='DW'
        elif(tickerSubType == 4): tickerSubType='W'
        elif(tickerSubType == 5): tickerSubType='Convertible'
        elif(tickerSubType == 6): tickerSubType='Preferred'
        elif(tickerSubType == 7): tickerSubType='UnitTrust'

        if(orderSide == 0):
            orderSide='Buy'
        elif(orderSide == 1):
            orderSide='Sell'
        elif(orderSide == 2):
            orderSide='Short'
        elif(orderSide == 3):
            orderSide='Cover'

        if(trend == 0):
            trend='Up'
        elif(trend == 1):
            trend='-'
        elif(trend == 2):
            trend='Down'
        elif(trend == 3):
            trend='NoData'

        pos=4
        total = {}
        read=1; div=0; size = unpack('>B',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        size=int(size)
        read=size; div=0; instrument = ''.join(msg[pos:pos+read]); pos+=read;

        if(ios == 0):
            read=2; div=2; price = unpack('>H',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
            read=2; div=2; change = unpack('>h',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
        else:
            read=4; div=2; price = unpack('>I',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
            read=4; div=2; change = unpack('>i',msg[pos:pos+read])[0]/pow(10.,div); pos+=read;
            
        read=4; div=0; seqID = int(unpack('>I',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;

        if(sob==0):
            read=1; div=0; volCount = int(unpack('>B',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;
        else:
            read=2; div=0; volCount = int(unpack('>H',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;
        
        volumns=[]
        for i in range(volCount):
            if(iosV==0):
                read=2; div=0; volumn = int(unpack('>H',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;
            else:
                read=4; div=0; volumn = int(unpack('>I',msg[pos:pos+read])[0]/pow(10.,div)); pos+=read;
            volumns.append(volumn);

        # print "tickerType= " + tickerSubType
        # print "orderSide= " + orderSide
        # print "trend= " + trend
        # print "isSum= " + str(isSum)
        print str(seqID)+"\t"+str(instrument)+"\t"+str(price)+"\t" + str(change) + "\t"+str(volCount)+"\t"+ str(volumns)


# In[ ]:



