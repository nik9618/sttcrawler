__all__ = ['marketSumParser','tickerParser','bidofferParser']
import config
import sys
from struct import *
from reading import *
import time
from datetime import datetime
import json
import os 

def getCurrentTime():
	return str(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3])

def marketSumParser(s):
	f = open(config.output+"marketSum", 'w')
	f.write(time.strftime('%Y/%m/%d'))
	f.write("\n")
	f.flush()
	while(True):
		size = s.recv(2)
		size = unpack('>H',size)[0]
		msg = s.recv(size)
		
		pos=0
		pos,service = readByte(msg,pos)
		
		if(service == 5):
			# print "Service : " + str(service)
			pos,conf = readByte(msg,pos)
			conf = parseConf(conf)
			# print conf
			pos,flag = readByte(msg,pos)

			total = {}
			pos, total['setIndex'] = readInt(msg,pos,config.DEFAULT_PRICE_DIGIT);
			pos, total['setHigh'] = readInt(msg,pos,config.DEFAULT_PRICE_DIGIT);
			pos, total['setLow'] = readInt(msg,pos,config.DEFAULT_PRICE_DIGIT);

			pos, total['setChange'] = readIOS(conf,msg,pos,config.DEFAULT_PRICE_DIGIT,unsigned=False);
			pos, total['setHighChange'] = readIOS(conf,msg,pos,config.DEFAULT_PRICE_DIGIT,unsigned=False);
			pos, total['setLowChange'] = readIOS(conf,msg,pos,config.DEFAULT_PRICE_DIGIT,unsigned=False);

			pos, total['setTotalValue'] = readInt(msg,pos,config.DEFAULT_PRICE_DIGIT);
			pos, total['setTotalVolume'] = readLong(msg,pos);

			pos, total['setGainers'] = readIOS(conf,msg,pos)
			pos, total['setLosers'] = readIOS(conf,msg,pos)
			pos, total['setUnchanged'] = readIOS(conf,msg,pos)

			pos, size = readByte(msg,pos)
			pos, total['setStatus'] = readString(msg,pos,size)
			total['time'] = getCurrentTime();

			f.write( json.dumps(total))
			f.write("\n")
			f.flush()
		else:
			# print "FROM SERVICE 5 :::: WRONG SERVICE > " + str(service)
			pass;
	return 
	
def tickerParser(s):
	f = open(config.output+"marketTick", 'a')
	f.write("#")
	f.write(time.strftime('%Y/%m/%d'))
	f.write("\n")
	f.write("#time\tintinstrumentType\tsignature\torderSide\ttrend\tinstrument\tprice\tchange\tseqID\tvolCount\tvolumes\n")
	f.flush()
	while(True):
		size = s.recv(2)
		size = unpack('>H',size)[0]
		msg = s.recv(size)
		
		pos = 0
		pos, service = readByte(msg,pos)
		if(service == 4):
			pos, conf = readByte(msg,pos)
			conf = parseConf(conf)
			pos, intinstrumentType = readByte(msg,pos)
			pos, signature = readByte(msg,pos)

			tickerSubType = (signature) & 0x0F
			orderSide = (signature>>4) & 0x01
			trend = (signature>>5) & 0x03
			isSum = (signature>>7) & 0x01

			if(tickerSubType == 0): tickerSubType='Common'
			elif(tickerSubType == 1): tickerSubType='Foriegn'
			elif(tickerSubType == 2): tickerSubType='ETF'
			elif(tickerSubType == 3): tickerSubType='DW'
			elif(tickerSubType == 4): tickerSubType='W'
			elif(tickerSubType == 5): tickerSubType='Convertible'
			elif(tickerSubType == 6): tickerSubType='Preferred'
			elif(tickerSubType == 7): tickerSubType='UnitTrust'

			if(orderSide == 0):
			    orderSide='B'
			elif(orderSide == 1):
			    orderSide='S'
			elif(orderSide == 2):
			    orderSide='S'
			elif(orderSide == 3):
			    orderSide='C'

			if(trend == 0):
			    trend='U'
			elif(trend == 1):
			    trend='-'
			elif(trend == 2):
			    trend='D'
			elif(trend == 3):
			    trend='N'

			if(intinstrumentType==0): # equity
				priceDigit = 2
			else:
			    pos,priceDigit = readByte(msg,pos)
			    
			total = {}
			pos, size = readSOB(conf,msg,pos);
			size=int(size)
			pos, instrument = readString(msg,pos,size)
			# f.write(instrument+"\t");
			# f.flush()
			pos, price = readIOS(conf,msg,pos,priceDigit,unsigned=False)
			# f.write(str(price)+"\t");
			# f.flush()
			pos, change = readIOS(conf,msg,pos,priceDigit,unsigned=False)
			# f.write(str(change)+"\t");
			# f.flush()
			pos, seqID = readInt(msg,pos)
			# f.write(str(seqID)+"\t");
			# f.flush()
			
			pos, volCount = readSOB(conf,msg,pos)
			# f.write(str(volCount)+"\t");
			# f.flush()
			volumns=[]
			for i in range(volCount):
				pos, volumn = readIOSV(conf,msg,pos)
				volumns.append(volumn);
			# f.write(str(volumns)+"\t");
			# f.flush()
			fstr = "%s\t%d\t%d\t%s\t%s\t%s\t%.2f\t%.2f\t%d\t%d" % (getCurrentTime(),intinstrumentType,signature,orderSide,trend,instrument,price,change ,seqID,volCount)
			for v in volumns:
				fstr += "\t" + str(v)
			fstr+="\n"

			f.write(fstr)
			f.flush()
			# sys.stdout.flush();
		else:
			# print "SERVICE TICKER ::::: WRONG SERVICE > " + str(service)
			pass;
	return

def bidofferParser(s,index,credentials,fr,to,insts):
	
	f = dict()
	if( not os.path.isdir(config.instoutput) ):
		os.makedirs(config.instoutput)
	
	while(True):
		size = s.recv(2)
		size = unpack('>H',size)[0]
		msg = s.recv(size)

		service = unpack('>B',msg[0])[0];
		if(service == 1):
			configByte = unpack('>B',msg[1])[0];

			conf = {};
			conf['iosV'] = (configByte>>3) & 1
			conf['loi'] = (configByte>>2) & 1
			conf['ios'] = (configByte>>1) & 1
			conf['sob'] = (configByte>>0) & 1

			pos=2;

			(pos,size) = readByte(msg,pos);
			(pos,instrument) = readString(msg,pos,size);
			(pos,instrumentType) = readByte(msg,pos);
			
			# index,credentials,fr,to
			if(config.validateSocket[index] == 0):
				config.validateSocket[index] = 1

			if(config.validateInstrument[instrument] == 0):
				config.validateInstrument[instrument] = 1	
			
			instSubtype = -1
			if(instrumentType==0): # 0 = equity
			    (pos,instSubType) = readByte(msg,pos,unsigned=False);

			priceDigit = config.DEFAULT_PRICE_DIGIT;
			settleDigit = config.DEFAULT_SETTLE_DIGIT;

			if (instrumentType==1 or instrumentType==2): # 1 = futures 2 = options
				(pos,priceDigit) = readByte(msg,pos);
				(pos,settleDigit) = readByte(msg,pos);

			(pos,flag) = readByte(msg,pos);

			hasInitMarket = (flag >> 5) & 1;
			hasInitIntraday = (flag >> 4) & 1;
			hasInitStat = (flag >> 3) & 1;
			hasSummary = (flag >> 2) & 1;
			hasBidOffer = (flag >> 1) & 1;
			hasProjected = (flag >> 0) & 1;

			# print hasInitMarket
			# print hasInitIntraday
			# print hasInitStat
			# print hasSummary
			# print hasBidOffer
			# print hasProjected
			# print "----"
			if(hasInitMarket == 1):
				(pos,previousClose) = readIOS(conf,msg,pos,priceDigit);
				(pos,high) = readIOS(conf,msg,pos,priceDigit);
				(pos,low) = readIOS(conf,msg,pos,priceDigit);
				(pos,ceiling) = readIOS(conf,msg,pos,priceDigit);
				(pos,floor) = readIOS(conf,msg,pos,priceDigit);
				if (instrumentType==1 or instrumentType==2): #--- is derivatives
					pos,spread = readIOS(conf,msg,pos,priceDigit);
					pos,previousSettle = readIOS(conf,msg,pos,priceDigit);
				# print "PSETTLE : " + str(previousSettle)

			if(hasInitIntraday == 1):
			    if (instrumentType ==0 or instrumentType ==1 or instrumentType ==2):
			        (pos,size) = readSOB(conf,msg,pos);
			        (pos,longInstName) = readString(msg,pos,size);
			        # print longInstName

			        if(instrumentType==0): # equity
			            pos,pe = readIOS(conf,msg,pos,config.PE_DIGIT);
			            pos,pbv = readIOS(conf,msg,pos,config.PBV_DIGIT);
			            pos,yield_ = readIOS(conf,msg,pos,config.YIELD_DIGIT);
			            pos,eps = readIOS(conf,msg,pos,config.EPS_DIGIT);
			            pos,w52High = readIOS(conf,msg,pos,config.W52_DIGIT);
			            pos,w52Low = readIOS(conf,msg,pos,config.W52_DIGIT);
			            pos,w52HighDate = readString(msg,pos,config.W_52_HIGH_LOW_DATE_LENGTH); #--------- string
			            pos,w52LowDate = readString(msg,pos,config.W_52_HIGH_LOW_DATE_LENGTH); #--------- string
			            pos,percentChg1W = readIOS(conf,msg,pos,config.PERCENT_CHANGE_WEEK_MONTH_DIGIT);
			            pos,percentChg1M = readIOS(conf,msg,pos,config.PERCENT_CHANGE_WEEK_MONTH_DIGIT);
			            pos,percentChg3M = readIOS(conf,msg,pos,config.PERCENT_CHANGE_WEEK_MONTH_DIGIT);
			            pos,size = readByte(msg,pos);
			            pos,currency = readString(msg,pos,size);
			            if (instSubtype==2 or instSubtype==3): #W and DW
			                pos,exercisePrice = readDouble(msg,pos);
			                pos,exerciseDate = readString(msg,pos,config.EXERCISE_DATE_LENGTH);
			                pos,isCallOptions = readByte(msg,pos);
			                if(isCallOption>0):
			                    optionsType = 'CALL';
			                else:
			                    optionsType = 'PUT';
			                pos,size = readByte(msg,pos);
			                pos,exerciseRatio = readString(msg,pos,size);

			                if (instSubtype==3): #DW
			                    pos,derivativesWarrantType = readString(msg,pos,config.DERIVATIVES_WARRANT_TYPE_LENGTH);
			                    pos,remainingDays = readIOS(conf,msg,pos);
			                    pos,lastTradingDate = readString(msg,pos,config.LAST_TRADING_DATE_LENGTH);
			                    pos,multiplier = readInt(msg,pos,config.MULTIPLER_DIGIT);
			            else:
			                if (instSubtype == 4):
			                    pos,aumSize = readInt(msg,pos,config.AUM_SIZE_DIGIT);
			        else:
			            if(instrumentType==1 or instrumentType==2 ): # futures and options 
			                pos,lifeHigh = readIOS(conf,msg,pos,config.W52_DIGIT);
			                pos,lifeLow = readIOS(conf,msg,pos,config.W52_DIGIT);
			                pos,lifeHighDate = readString(msg,pos,config.W_52_HIGH_LOW_DATE_LENGTH);
			                pos,lifeLowDate = readString(msg,pos,config.W_52_HIGH_LOW_DATE_LENGTH);
			                pos,remainingDays = readIOS(conf,msg,pos);
			                pos,lastTradingDate = readString(msg,pos,config.LAST_TRADING_DATE_LENGTH);
			                pos,size = readByte(msg,pos);
			                pos,underlying = readString(msg,pos,size);
			                pos,size = readByte(msg,pos);
			                pos,markettype = readString(msg,pos,size);
			                pos,initialMargin = readInt(msg,pos,config.INITIAL_MARGIN_DIGIT);
			                if (instrumentType==2):
			                    pos,isCallOptions = readByte(msg,pos);
			                    if(isCallOptions>0):
			                        optionsType = 'CALL';
			                    else:
			                        optionsType = 'PUT';
			                    pos,strikePrice = readIOS(conf,msg,pos,config.STRIKE_PRICE_DIGIT);
			    else:
			        #read index
			        pos,marketCap = readLOI(conf,msg,pos);
			        pos,pe = readIOS(conf,msg,pos,config.PE_DIGIT);
			        pos,pbv = readIOS(conf,msg,pos,config.PBV_DIGIT);
			        pos,yield_ = readIOS(conf,msg,pos,config.YIELD_DIGIT);

			if(hasInitStat==1):
			    if (instrumentType==0):
			        pos,dividendYield = readIOS(conf,msg,pos)

			if(hasSummary==1):
			    pos,lastDone = readIOS(conf,msg,pos,priceDigit);
			    pos,change = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			    pos,percentChange = readIOS(conf,msg,pos,config.PERCENT_DIGIT,unsigned=False);
			    pos,totalVolume = readLOI(conf,msg,pos);
			    if (instrumentType ==0 or instrumentType ==1 or instrumentType ==2):
			        pos,average = readIOS(conf,msg,pos,priceDigit);
			        pos,size = readByte(msg,pos);
			        pos,status = readString(msg,pos,size);
			        pos,percentBuy = readByte(msg,pos);
			        pos,percentSell = readByte(msg,pos);
			        if (instrumentType==0):
			            pos,totalValue = readLOI(conf,msg,pos)
			            pos,averageBuy = readIOS(conf,msg,pos,config.AVERAGE_DIGIT);
			            pos,averageSell = readIOS(conf,msg,pos,config.AVERAGE_DIGIT);
			            if (instSubtype==2 or instSubtype==3): 
			                pos,underlyingPrice = readIOS(conf,msg,pos,config.WARRANT_UNDERLYING_PRICE_DIGIT);
			                pos,theoricalPrice = readIOS(conf,msg,pos,config.THEORICAL_PRICE_DIGIT);
			                pos,impliedVolatility = readIOS(conf,msg,pos,config.IMPLIED_VOLATILLITY_DIGIT);
			                pos,delta = readIOS(conf,msg,pos,config.DELTA_DIGIT);
			                pos,theta = readInt(msg,pos,config.THETA_DIGIT);
			            else:
			                if (instSubtype==4): #etf
			                    pos,iNav = readInt(msg,pos,INAV_DIGIT);
			        else:
			            if (instrumentType ==1 or instrumentType ==2):
			                pos,underlyingPrice = readIOS(conf,msg,pos,priceDigit);
			                pos,openInterest = readIOS(conf,msg,pos);
			                pos,settlePrice = readIOS(conf,msg,pos,settleDigit);
			                pos,theoricalPrice = readIOS(conf,msg,pos,config.THEORICAL_PRICE_DIGIT);
			                if (instrumentType ==2):
			                    pos,impliedVolatility = readIOS(conf,msg,pos,config.IMPLIED_VOLATILLITY_DIGIT);
			                    pos,delta = readIOS(conf,msg,pos,config.DELTA_DIGIT);
			                    pos,theta = readInt(msg,pos,config.THETA_DIGIT);
			    else:
			        if (instrumentType==3):
			            pos,totalValue = readLOI(conf,msg,pos)

			if (hasBidOffer==1):
			    if (instrumentType ==0 or instrumentType ==1 or instrumentType ==2):
			        pos,bidAskFlagArray = readByte(msg,pos);
			        bidFlag = bidAskFlagArray & 0x0F;
			        askFlag = bidAskFlagArray >> 4;
			        pos,bidPrice1 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,bidPrice2 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,bidPrice3 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,bidPrice4 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,bidPrice5 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,askPrice1 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,askPrice2 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,askPrice3 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,askPrice4 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,askPrice5 = readIOS(conf,msg,pos,priceDigit,unsigned=False);
			        pos,bidVolume1 = readLOI(conf,msg,pos);
			        pos,bidVolume2 = readLOI(conf,msg,pos);
			        pos,bidVolume3 = readLOI(conf,msg,pos);
			        pos,bidVolume4 = readLOI(conf,msg,pos);
			        pos,bidVolume5 = readLOI(conf,msg,pos);
			        pos,askVolume1 = readLOI(conf,msg,pos);
			        pos,askVolume2 = readLOI(conf,msg,pos);
			        pos,askVolume3 = readLOI(conf,msg,pos);
			        pos,askVolume4 = readLOI(conf,msg,pos);
			        pos,askVolume5 = readLOI(conf,msg,pos);
			

			if(instrument not in f):
				f[instrument] = open(config.instoutput+instrument, 'a')
				f[instrument].write("#")
				f[instrument].write(time.strftime('%Y/%m/%d'))
				f[instrument].write("\n")
				f[instrument].write("#time\tpclose\tlast\tchg\tpchg\ttotalVol\tbidFlag\taskFlag\tbidv1\tbidv2\tbidv3\tbidv4\tbidv5\tbidp1\tbidp2\tbidp3\tbidp4\tbidp5\taskv1\taskv2\taskv3\taskv4\taskv5\taskp1\taskp2\taskp3\taskp4\taskp5\n")
				f[instrument].flush()
			
			fstr = ""
			fstr += "%s\t" % (getCurrentTime())
			fstr += "%.2f\t" % (previousClose)
			fstr += "%.2f\t" % (lastDone)
			fstr += "%.2f\t" % (change)
			fstr += "%.2f\t" % (percentChange)
			fstr += "%d\t" % (totalVolume)
			fstr += "%d\t" % (bidFlag)
			fstr += "%d\t" % (askFlag)

			fstr += "%d\t" % (bidVolume1)
			fstr += "%d\t" % (bidVolume2)
			fstr += "%d\t" % (bidVolume3)
			fstr += "%d\t" % (bidVolume4)
			fstr += "%d\t" % (bidVolume5)

			fstr += "%.2f\t" % (bidPrice1)
			fstr += "%.2f\t" % (bidPrice2)
			fstr += "%.2f\t" % (bidPrice3)
			fstr += "%.2f\t" % (bidPrice4)
			fstr += "%.2f\t" % (bidPrice5)
			
			fstr += "%d\t" % (askVolume1)
			fstr += "%d\t" % (askVolume2)
			fstr += "%d\t" % (askVolume3)
			fstr += "%d\t" % (askVolume4)
			fstr += "%d\t" % (askVolume5)

			fstr += "%.2f\t" % (askPrice1)
			fstr += "%.2f\t" % (askPrice2)
			fstr += "%.2f\t" % (askPrice3)
			fstr += "%.2f\t" % (askPrice4)
			fstr += "%.2f\t" % (askPrice5)
			
			fstr += "\n"
			f[instrument].write(fstr)
			f[instrument].flush()
			print "BID OFFER : "+instrument;
		else:
			# print "("+str(index)+")SERVICE BIDOFFER ::::: WRONG SERVICE > " + str(service)
			pass;
	return