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

import random

def randPpl():
    rand = random.randrange(100000000000,999999999999);
    chksum = 0;
    for i in range(12):
        at = (rand/(10**(11-i))) % 10
        # print at;
        chksum += at*(13-i)
    chksum = chksum%11
    return str(rand) + str((11 - chksum)%10)


# ----- Start crawling 
path='/Users/nik9618/Desktop/Library/chromedriver';
driver = webdriver.Chrome(path)
    
crid = 174

while(True):
    driver = webdriver.Chrome(path)
    username = "usr%.4d" % crid
    print username;
    print 'Main page loaded'

    pplid = randPpl();
    driver.get('https://click2win.settrade.com')
    
    sys.stdout.flush()
    time.sleep(0.2);

# ----- Login
    box = driver.find_element_by_name('txtLogin')
    time.sleep(0.2);
    box.clear();
    time.sleep(0.2);
    box.send_keys(username)
    time.sleep(0.2);
    box = driver.find_element_by_name('txtPassword')
    box.send_keys(username)
    elem = driver.find_element_by_class_name('input_login_submit-login');
    elem.click(); 
    
    print 'Logged In'
    sys.stdout.flush()
    time.sleep(0.2);

    alert = driver.switch_to_alert()
    alert.accept()
    
    box = driver.find_element_by_name('checkbox5')
    box.click()

    elem = driver.find_element_by_class_name('input_form_submit');
    elem.click(); 

    crid+=1;
    time.sleep(3);
    driver.close()
