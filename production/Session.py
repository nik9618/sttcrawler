import config
import selenium
import selenium.webdriver.support.ui as UI
from selenium import webdriver;
import time
import urllib
import datetime
import hashlib
import re
import socket
import random

class Session():

	# self.username ='';
	# self.password ='';
	# self.driver = None;

	def __init__(self,username='',password=''):
		self.username = username
		self.password = password
		self.driver = webdriver.Chrome(config.seleniumpath)
		self.driver.get(config.url)
		time.sleep(1)
	
	def suicide(self):
		self.driver.quit();

	def login(self):
		userBox = self.driver.find_element_by_name('txtLogin')
		passBox = self.driver.find_element_by_name('txtPassword')
		userBox.clear()
		passBox.clear()
		userBox.send_keys(self.username)
		passBox.send_keys(self.password)
		elem = self.driver.find_element_by_class_name('input_login_submit-login');
		elem.click()
		time.sleep(1)
		self.getStreamingVar()
		
	def syncTime(self):
		self.driver.get(config.url + self.flashVar['fvSyncTimeURL'])
		servTime = self.driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")
		servTime = int(servTime[1]) #+ config.hourshift*60*60*1000
		servTime = servTime/1000
		self.difftime = time.time() - servTime
		# print self.difftime

	def getStreamingVar(self):
		# ------ Generate flash variables
		self.driver.get('view-source:'+config.url+'/realtime/streaming5/flash/StreamingPage.jsp')
		time.sleep(1)
		src = self.driver.page_source
		src = src[src.find('flashVar'):]
		src = src[src.find('{')+1:]
		src = src[0:src.find('}')]
		flashVar = {}
		src = src.split(",")
		for line in src:
			line = line.split(":")
			flashVar[urllib.unquote(line[0])] = urllib.unquote(line[1][1:-1])
		time.sleep(1);
		self.flashVar = flashVar
		self.syncTime()
		return flashVar

	def getInstrumentList(self):
		url = config.url + self.flashVar['fvDataProviderStrURL']
		key = datetime.datetime.fromtimestamp(time.time()+self.difftime).strftime('%d/%m/%Y') + "_" + self.flashVar['fvBrokerId']+"_"+self.flashVar['fvUserref']
		m = hashlib.md5()
		m.update(key)
		hs = m.hexdigest()
		# print "---- hash("+key +") = " + hs
		script = ""
		script = script + 'sc=\'\'; sc += \'<form id="dynForm" action="'+url+'" method="post">\';'
		script = script + 'sc += \'<input type="hidden" name="boardType" value="'+"equity"+'">\';'
		script = script + 'sc += \'<input type="hidden" name="APIVersion" value="'+config.APIVersion+'">\';'
		script = script + 'sc += \'<input type="hidden" name="subListName" value="">\';'
		script = script + 'sc += \'<input type="hidden" name="mainListName" value=".A">\';'
		script = script + 'sc += \'<input type="hidden" name="boardSubType" value="">\';'
		script = script + 'sc += \'<input type="hidden" name="service" value="12">\';'
		script = script + 'sc += \'<input type="hidden" name="q" value="'+hs+'">\';'
		script = script + 'sc += \'</form>\';'
		script = script + 'document.body.innerHTML += sc;'
		# print script;

		script = script + 'document.getElementById("dynForm").submit()';
		# driver.get('https://click2win.settrade.com'+flashVar['fvGenerateKeyURL'])
		self.driver.execute_script(script)
		# print "----"+ url
		text = self.driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")

		if text[0] == 'T':
		    category = text[6].split("^")
		    # print category
		    futures = [];
		    options = [];
		    equity  = [];
		    indexes = [];
		    for cate in category:
		        if cate == 'futuresAndUnderlying':
		            insts = text[7].split("^")
		            for inst in insts:
		                inst = inst.split("~")[0]
		                futures.append(inst);
		                
		        if cate == 'options':
		            insts = text[8].split("^")
		            for inst in insts:
		                inst = inst.split("~")[0]
		                options.append(inst);
		                
		        if cate == 'equity':
		            insts = text[9].split("^")
		            for inst in insts:
		                inst = inst.split("~")[0]
		                equity.append(inst);
		                
		    new_equity =[]
		    
		    reW = re.compile('^.*-W\d(\d*)$')
		    reDW = re.compile('^(.|..|...|....)\d\d(C|P)\d\d\d\d.$')
		    reF = re.compile('^.*-F$')
		    reP = re.compile('^.*-P$')
		    reQ = re.compile('^.*-Q$')
		      
		    for eq in equity:
		        if(reW.match(eq) or reDW.match(eq) or reF.match(eq) or reP.match(eq) or reQ.match(eq)):
		            #not simple
		            pass;
		        else:
		            new_equity.append(eq);
		    
		    equity = new_equity;
		    # print len(futures)
		    # print len(options)
		    # print len(equity)
		    # total = len(futures)+ len(options) + len(equity)
		    # print total

		    return (equity,futures,options)
		else:
			return None;

	def genKey(self):
		url = config.url + self.flashVar['fvGenerateKeyURL']
		key = datetime.datetime.fromtimestamp(time.time()+self.difftime).strftime('%d/%m/%Y') + "_" + self.flashVar['fvBrokerId']+"_"+self.flashVar['fvUserref']
		m = hashlib.md5()
		m.update(key)
		hs = m.hexdigest()
		print "hash("+key +") = " + hs
		script = ""
		script = script + 'sc=\'\'; sc += \'<form id="dynForm" action="'+url+'" method="post">\';'
		script = script + 'sc += \'<input type="hidden" name="time" value="'+str(int(time.time()+self.difftime))+'">\';'
		script = script + 'sc += \'<input type="hidden" name="clientType" value="'+self.flashVar['fvRealtimeClientType']+'">\';'
		script = script + 'sc += \'<input type="hidden" name="txtSETNET3" value="'+self.flashVar['fvSETNET3']+'">\';'
		script = script + 'sc += \'<input type="hidden" name="APIVersion" value="'+config.APIVersion+'">\';'
		script = script + 'sc += \'<input type="hidden" name="q" value="'+hs+'">\';'
		script = script + 'sc += \'</form>\';'
		script = script + 'document.body.innerHTML += sc;'
		script = script + 'document.getElementById("dynForm").submit()';
		self.driver.execute_script(script)
		src = self.driver.find_element_by_tag_name('body').text.split("\r")[0].split("|")
		self.key=src;
		return src

	def genSocket(self):
		key = self.genKey()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dns = socket.gethostbyname_ex(key[2])
		host = dns[2][0]
		port = int(key[3])
		conn = s.connect((host, port))
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		ss = self.flashVar['fvUserref']+"|"+self.flashVar['fvBrokerId']+"|"+key[1]+"|" + str(int(time.time()+self.difftime)) + "|"+self.flashVar['fvRealtimeClientType']+"|"+config.APIVersion+"\n"
		s.send(ss)
		print ss
		return s

	def marketSummarySocket(self):
		s = self.genSocket()
		s.send("REG|5\n")
		print "REG|5\n"
		return s

	def tickerSocket(self):
		s = self.genSocket()
		s.send("REG|4^N~N^N~N^E~D^E~D\n")
		print "REG|4^N~N^N~N^E~D^E~D\n"
		return s

	def bidofferSocket(self,insts):
		s = self.genSocket()
		ss = "REG|1^"
		for i in range(len(insts)):
			if(i == len(insts) - 1):
				ss+= insts[i]
			else:
				ss+= insts[i]+"~"

		ss += "^^"
		for i in range(len(insts)):
			if(i == len(insts) - 1):
				ss+= "M"
			else:
				ss+= "M~"
		ss += "\n"
		s.send(ss);
		print ss
		print self.key
		return s

if __name__ == '__main__':
	s=Session('usr0001','usr0001')
	s.login();
	s.getStreamingVar();
	s.getInstrumentList();
	# s.marketSummarySocket();
	# s.tickerSocket()
	# s.bidofferSocket(['AAV','AOT','VGI'])