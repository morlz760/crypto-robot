#pam-v4.py

#pam will check your nominated exchanges and currency pairs, just fill out the below

import os
import sys
import json
import datetime
import gspread
import codecs
from oauth2client.service_account import ServiceAccountCredentials
from apscheduler.schedulers.blocking import BlockingScheduler

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

#defining colours for when i print in the terminal
def style(s, style):
    return style + s + '\033[0m'

def green(s):
    return style(s, '\033[92m')

def blue(s):
    return style(s, '\033[94m')
def bold(s):
    return style(s, '\033[1m')

print('')
print(bold(green(('__-*-__-*-__RUNNING CRYPTO ROBOT__-*-__-*-__'))))
print('')
print(blue(('----------time to make some money------------')))
print('')

#bringing in the scheduler
sched = BlockingScheduler()

#setting up the google sheet
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('firstproject.json', scope)
client = gspread.authorize(creds)

#instanciate the exchange here
independentreserve = ccxt.independentreserve({})
btcmarkets = ccxt.btcmarkets({})
coinspot = ccxt.coinspot({
	})

#add your exchanges below
exchange = [btcmarkets, coinspot, independentreserve]

def instanciate(exchange):
	for x in exchange:
		x.load_markets()

#add the symbols you want to check arb opps for here
symtobechecked = ('BTC/AUD', 'LTC/AUD', 'ETH/AUD')

#this function will grab the market prices for each symbol on each exchange
def genMarketPrices():
	marketgroup = {}
	for y in exchange:
		bidasks = {}
		for x in symtobechecked:
			if x in y.symbols:
				orderbook = y.fetch_ticker(x)
				bidx = orderbook.get('bid')
				askx = orderbook.get('ask')
				bidasks[x+' bid'] = bidx
				bidasks[x+' ask'] = askx
			else:
				''
		marketgroup[y.id] = bidasks
	return(marketgroup)

#this function will select the max value and the min value based on the currency pair that is input and avaliable across your nominated exchanges
def findMaxMin(sym):
	marketprices = genMarketPrices()
	findingmax = {}
	findingmin = {}
	minmaxpairs = {}
	for x in marketprices:
		t = marketprices[x]
		for y in t:
			if y == sym+' bid':
				findingmax[x] = t[y]
			elif y == sym+' ask':
				findingmin[x] = t[y]
	maxval = max(findingmax)
	minval = min(findingmin)
	arbopps = format((((findingmax[maxval] - findingmin[minval])/findingmin[minval])*100), '.2f')
	minmaxpairs[sym] = [((maxval, findingmax[maxval])),((minval, findingmin[minval])), arbopps, datetime.datetime.now()]
	return(minmaxpairs)

#this function passes different symbols into the findMaxMin function and add the output to a list
def findopps():
	storage = []
	for x in symtobechecked:
		storage.append(findMaxMin(x))
	return storage

#and here we run the function and add it to our text file
def crypto_robot():
	instanciate(exchange)
	listofminmax = findopps()
	with codecs.open("entries.txt", "a", "utf-8") as my_file:  # better not shadow Python's built-in file
		for x in listofminmax:
			my_file.write(str(x) + "\n")

job = sched.add_job(crypto_robot, 'interval', minutes=15)

sched.start()








