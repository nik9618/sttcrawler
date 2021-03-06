import config
import re
from robobrowser import RoboBrowser
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
		self.browser = RoboBrowser()
		
	def login(self):
		self.browser.open('https://click2win.settrade.com/LoginRepOnRole.jsp?txtLogin='+self.username+'&txtPassword='+self.password+'&txtSecureKey=NONE&txtDefaultPage=%2FSETClick2WIN%2FSelectUserLeague.jsp&txtLoginPage=SETClick2WIN/index.jsp&txtBrokerId=089&txtSystem=ITP&txtRole=INTERNET&tmpUsername=&tmpPassword=')
		form = self.browser.get_forms()[0]
		self.browser.submit_form(form)
		form = self.browser.get_forms()[0]
		self.browser.submit_form(form)
		self.getStreamingVar()
		
	def syncTime(self):
		self.browser.open(config.url + self.flashVar['fvSyncTimeURL'])
		servTime = self.browser.select('p')[0].get_text().split("|")
		servTime = int(servTime[1]) #+ config.hourshift*60*60*1000
		servTime = servTime/1000
		self.difftime = time.time() - servTime
		# print self.difftime

	def getStreamingVar(self):
		# ------ Generate flash variables
		self.browser.open(config.url+'/realtime/streaming5/flash/StreamingPage.jsp')		
		src = self.browser.select('html')[0]
		src = src.get_text().encode('utf-8').split("\n")
		for i in src:
			if(i.find('flashVar')== -1 ): continue;
			i = i[i.find('flashVar'):]
			i = i[i.find('{')+1:]
			i = i[0:i.find('}')]
			src = i;
			break;
		flashVar = {}
		print src
		src = src.split(",")
		for line in src:
			line = line.split(":")
			flashVar[urllib.unquote(line[0])] = urllib.unquote(line[1][1:-1])
		
		self.flashVar = flashVar
		self.syncTime()
		return flashVar

	def getInstrumentList(self):
		url = config.url + self.flashVar['fvDataProviderStrURL']
		key = datetime.datetime.fromtimestamp(time.time()+self.difftime).strftime('%d/%m/%Y') + "_" + self.flashVar['fvBrokerId']+"_"+self.flashVar['fvUserref']
		m = hashlib.md5()
		m.update(key)
		hs = m.hexdigest()
		# print "hash("+key +") = " + hs
		params = "boardType=equity&"
		params += "APIVersion="+config.APIVersion+"&"
		params += "subListName=&"
		params += "mainListName=.A&"
		params += "boardSubType=&"
		params += "service=12&"
		params += "q="+hs
		self.browser.open(url +"?"+params);
		text = self.browser.select('p')[0].get_text().split("|")

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
		    
		    reNW = re.compile('^.*-W$')
		    reW = re.compile('^.*-W\d(\d*)$')
		    reDW = re.compile('^(.|..|...|....)\d\d(C|P)\d\d\d\d.$')
		    reF = re.compile('^.*-F$')
		    reP = re.compile('^.*-P$')
		    reQ = re.compile('^.*-Q$')
		      
		    for eq in equity:
		        if(reNW.match(eq) or reW.match(eq) or reDW.match(eq) or reF.match(eq) or reP.match(eq) or reQ.match(eq)):
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
		    # equity = equity[1:100]
		    # futures = futures[1:100]
		    # options = []
		    return (equity,futures,options)
		else:
			return None;

	def genKey(self):
		url = config.url + self.flashVar['fvGenerateKeyURL']
		key = datetime.datetime.fromtimestamp(time.time()+self.difftime).strftime('%d/%m/%Y') + "_" + self.flashVar['fvBrokerId']+"_"+self.flashVar['fvUserref']
		m = hashlib.md5()
		m.update(key)
		hs = m.hexdigest()
		# print "hash("+key +") = " + hs
		
		params = "time="+str(int(time.time()+self.difftime))+"&"
		params += "clientType="+self.flashVar['fvRealtimeClientType']+"&"
		params += "txtSETNET3="+self.flashVar['fvSETNET3']+"&"
		params += "APIVersion="+config.APIVersion+"&"
		params += "q="+hs

		self.browser.open(url +"?"+params);
		src = self.browser.select('p')[0].get_text().split("|")
		self.key=src;
		return src

	def genSocket(self):
		key = self.genKey()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print key;
		dns = socket.gethostbyname_ex(key[2])
		host = dns[2][0]
		port = int(key[3])
		conn = s.connect((host, port))
		# s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		ss = self.flashVar['fvUserref']+"|"+self.flashVar['fvBrokerId']+"|"+key[1]+"|" + str(int(time.time()+self.difftime)) + "|"+self.flashVar['fvRealtimeClientType']+"|"+config.APIVersion+"\n"
		s.send(ss)
		# print ss
		return s

	def marketSummarySocket(self):
		s = self.genSocket()
		s.send("REG|5\n")
		# print "REG|5\n"
		return s

	def tickerSocket(self):
		s = self.genSocket()
		s.send("REG|4^N~N^N~N^E~D^E~D\n")
		# print "REG|4^N~N^N~N^E~D^E~D\n"
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
		# print self.key
		return s

if __name__ == '__main__':
	s=Session('usr0001','usr0001')
	s.login();
	# s.genKey();
	# print s.getInstrumentList();
	# s.marketSummarySocket();
	# s.tickerSocket()
	# s.bidofferSocket(['AAV','AOT','VGI'])