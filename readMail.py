import re;
import email, getpass, imaplib, os
import quopri;
from robobrowser import RoboBrowser

from selenium import webdriver;
import selenium
import selenium.webdriver.support.ui as UI

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# browser = RoboBrowser()
# browser.open('https://click2win.settrade.com/SETClick2WIN/Registration.jsp?mode=activate&usn=usr0024&curr=12012016&eusn=F8*eLpb%21pasSAOvbVn%21pCb5RjJI%24&uType=0')
# print browser.parsed
# exit()

detach_dir = '.' # directory where to save attachments (default: current)
user = 'crawlerstt@gmail.com'
pwd = 'jhzfiwpzausfgzrz'

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") 
    email_body = data[0][1]
    mail = email.message_from_string(email_body) 

    if ( mail["From"] == 'noreplyclick2win@settrade.com' ) :
		email_body = email_body.replace("\n","")
		# print email_body
		raw_body=data[0][1]
		raw_body=quopri.decodestring(raw_body)
		raw_body=raw_body.decode('iso-8859-1').encode('utf-8')
		# print raw_body
		url =  raw_body.split("\n")[29]
		print url
		# ----- Start crawling 
		path='/Users/nik9618/Desktop/Library/chromedriver';
		driver = webdriver.Chrome(path)
		driver.get(url)
		driver.close()


		
		# reg = r'http.*'
		# match = re.match(reg, raw_body)
		# print match
		# item = match.group(0)
		# print item
		# item2 = match.group(2)
		# reQ = re.compile('^http://')
		# if(reQ.match(eq)):
		# 	pass

