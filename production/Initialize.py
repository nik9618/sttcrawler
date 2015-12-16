#-- configuration
import config
import time
import math
from Session import Session
import numpy as np
from workerparser import *
import threading


#-- load user list
users=[];
with open(config.path+'settings/userlist.txt', 'r') as f:
	fs = f.readlines()
	for i in fs:
		i=i.split("\n")[0].split("\t");
		users.append({'user':i[0],'pwd':i[1]})
print "Account list loaded"
lgIdx = 0;

#-- list stocks and derivatives
s = Session(users[lgIdx]['user'],users[lgIdx]['pwd'])
lgIdx +=1;
s.login()
tmpInstList = s.getInstrumentList()

# #-- load instrument list
instList = [];
for j in tmpInstList:
	for i in j:
		instList.append(i)


# #-- truncated for speeding up developement
# instList =instList[0:150];
# #-- end truncation

# index,credentials,fr,to
s = Session(users[lgIdx]['user'],users[lgIdx]['pwd'])
s.login()
socketMktSum = s.marketSummarySocket();
mktsumThread = threading.Thread(target=marketSumParser,args=(socketMktSum,))
mktsumThread.start()
lgIdx+=1

s = Session(users[lgIdx]['user'],users[lgIdx]['pwd'])
s.login()
socketTicker = s.tickerSocket();
tickerThread = threading.Thread(target=tickerParser,args=(socketTicker,))
tickerThread.start()
lgIdx+=1

# ---bypass for speeding up development
# np.save('tmpInstList.txt', instList)
# instList=np.load('tmpInstList.txt.npy')
# print len(instList)
# ---end bypass

#-- CrowdLogin
s = Session(users[lgIdx]['user'],users[lgIdx]['pwd'])
totalSocket = [];
config.validateSocket= dict();
config.validateInstrument= dict();
for i in instList:
	config.validateInstrument[i] = 0;

def worker(index,credentials,fr,to):
	try:
		config.validateSocket[index] = 0;
		s = Session(credentials['user'], credentials['pwd'])
		s.login()
		socketBidOffer = s.bidofferSocket(instList[fr:to])
		bidofferParser(socketBidOffer,index,credentials,fr,to)
	except:
		print "ERROR" + str(index) +" -- "+str(credentials)+" -- "+str(instList[fr:to])
		time.sleep(1)
		worker(index,credentials,fr,to)
	return;

threads = []
i = 0;
n_thread = math.ceil(float(len(instList))/config.max_streaming_concurrent);
# print n_thread

while True:
	to_work = []
	for j in range(i,i+config.n_concurrent):
		if(j>=n_thread): break
		to_work.append((j,users[lgIdx],j*config.max_streaming_concurrent,(j+1)*config.max_streaming_concurrent))
		lgIdx+=1;
	i=i+config.n_concurrent;
	if(len(to_work)==0):
		break;

	for w in to_work:
		print w
		t = threading.Thread(target=worker,args=w)
		threads.append(t)
		t.start()
	time.sleep(3);

# ---- validate connections
time.sleep(30);
while(True):
	print config.validateInstrument
	print config.validateSocket
	time.sleep(10)
# email perhaps



