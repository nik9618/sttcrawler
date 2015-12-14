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
    
crid = 165

while(True):
    
    username = "usr%.4d" % crid
    print username;

    pplid = randPpl();

    driver.get('http://click2win.settrade.com/SETClick2WIN/Registration.jsp')
    print 'Main page loaded'
    sys.stdout.flush()
    time.sleep(1);

# # ----- Login
    box = driver.find_element_by_name('txtUsername')
    box.send_keys(username)
    box = driver.find_element_by_name('txtTmpPassword')
    box.send_keys(username)
    box = driver.find_element_by_name('txtTmpPasswordConfirm')
    box.send_keys(username)
    
    box = driver.find_element_by_name('txtBirthdate')
    box.click()
    options = box.find_elements_by_tag_name('option')
    options[1].click()
    box = driver.find_element_by_name('txtBirthmonth')
    box.click()
    options = box.find_elements_by_tag_name('option')
    options[1].click()
    box = driver.find_element_by_name('txtBirthyear')
    box.click()
    options = box.find_elements_by_tag_name('option')
    options[1].click()
    
    box = driver.find_element_by_css_selector("input[type='radio'][value='male']").click()

    box = driver.find_element_by_name('txtNameTh')
    box.send_keys('crawler')    
    box = driver.find_element_by_name('txtSurnameTh')
    box.send_keys(str(crid))    

    for i in range(0,13):
        box = driver.find_element_by_name('txtIdCard'+str(i))
        box.send_keys(pplid[i])    

    box = driver.find_element_by_name('txtProvince')
    box.click()
    options = box.find_elements_by_tag_name('option')
    options[1].click()
    
    box = driver.find_element_by_name('txtMobile')
    box.send_keys('081'+str(random.randrange(1000000,9999999)))
    box = driver.find_element_by_name('txtEmail')
    mail = "crawlerstt+%.4d@gmail.com" % crid
    box.send_keys(mail) 
    driver.execute_script("$('input[name=checkbox5]').attr('checked', true);")

    box = driver.find_element_by_name('captchaText')
    box.send_keys("")


    # selectByIndex(1);
    # # passBox = driver.find_element_by_name('txtPassword')
    # # userBox.clear()
    # # passBox.clear()
    # # userBox.send_keys(config['username'])
    # # passBox.send_keys(config['password'])
    # # elem = driver.find_element_by_class_name('input_login_submit-login');
    # # elem.click();
    # # print 'Logged In'
    # # sys.stdout.flush()
    # # time.sleep(3);

    crid+=1;
    time.sleep(5);
    # break;