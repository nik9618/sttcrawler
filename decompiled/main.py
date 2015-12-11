#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys;
import time;
import json;
from selenium import webdriver;
import selenium
import selenium.webdriver.support.ui as UI
import re;
import socket               # Import socket module
import urllib

#----- Configuration
path='/Users/nik9618/Desktop/Library/chromedriver';

conf={}
conf['username'] = 'crawler001'
conf['password'] = 'crawler001'


# #----- Start crawling 
driver = webdriver.Chrome(path)
driver.get('https://click2win.settrade.com')
print 'Main page loaded'
sys.stdout.flush()
time.sleep(1);

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
time.sleep(1)

driver.get('view-source:https://click2win.settrade.com/realtime/streaming5/flash/StreamingPage.jsp')
print 'Streaming Opened'
sys.stdout.flush()
time.sleep(1)

src = driver.page_source;
src = src[src.find('flashVar'):]
src = src[src.find('{')+1:]
src = src[0:src.find('}')]

flashVar = {}
src = src.split(",")
for line in src:
	line = line.split(":")
	flashVar[urllib.unquote(line[0])] = urllib.unquote(line[1][1:-1])


driver.get('https://click2win.settrade.com'+flashVar['fvGenerateKeyURL'])
src = driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")

driver.get('https://click2win.settrade.com'+flashVar['fvSyncTimeURL'])
time = driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")


# for key in flashVar:
# 	print key + "\t" + urllib.unquote(flashVar[key])
#-------- socket realtime --------
print 'start socket'
s = socket.socket()
dns = socket.gethostbyname_ex(src[2]);
host = dns[2][0];
port = int(src[3])
s.connect((host, port))
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# authenticate
s.send(flashVar['fvUserref'] + "|" + flashVar['fvBrokerId'] + "|" + src[1] + "|" + time[2] + "|" + flashVar['fvRealtimeClientType'] + "|1\n")
s.send(flashVar['fvUserref'] + "|" + flashVar['fvBrokerId'] + "|" + "wcgfd" + "|" + time[2] + "|" + flashVar['fvRealtimeClientType'] + "|1\n")
# market summary
s.send("REG|1^^^M\n")
s.send("REG|3^^\n")
s.send("REG|5\n")
s.send("REG|4^N~N^N~N^E~D^E~D\n")

print 'start reading'
while True:
	x = ''
	x = s.recv(1024);
	if(x!= ''):
		print x



# 7575997|089|OWfUQzTC4MP4fyk2inIr6w==|1449626605405|gen5sc1|1

# s.listen(5)                 # Now wait for client connection.
# # while True:
#    c, addr = s.accept()     # Establish connection with client.
#    print 'Got connection from', addr
#    c.send('')
#    c.close()                # Close the connection

