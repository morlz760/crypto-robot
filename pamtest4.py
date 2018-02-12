#pam-v4.py

#pam will check your nominated exchanges and currency pairs, just fill out the below

import os
import sys
import json
import datetime

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

def style(s, style):
    return style + s + '\033[0m'

def green(s):
    return style(s, '\033[92m')

def blue(s):
    return style(s, '\033[94m')

print('')
print(green(('__-*-__-*-__RUNNING CRYPTO ROBOT__-*-__-*-__')))
print('')
print(blue(('----------time to make some money------------')))
print('')

#instanciate the exchange here
independentreserve = ccxt.independentreserve({})
btcmarkets = ccxt.btcmarkets({})

#add your exchanges below
exchange = [independentreserve, btcmarkets]

#add the symbols you want to check arb opps for here
symbols = ('ETH/AUD', 'BTC/AUD')

#this function will grab the market prices for each symbol on each exchange
def genMarketPrices():
	marketgroup = {}
	for y in exchange:
		bidasks = {}
		for x in symbols:
			orderbook = y.fetch_ticker(x)
			bidx = orderbook.get('bid')
			askx = orderbook.get('ask')
			bidasks[x+' bid'] = bidx
			bidasks[x+' ask'] = askx
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
	arbopps = ((findingmax[maxval] - findingmin[minval])/findingmin[minval])	
	minmaxpairs[sym] = [((maxval, findingmax[maxval])),((minval, findingmin[minval])), arbopps]
	return(minmaxpairs)

#this function passes different symbols into the findMaxMin function
def findopps():
	for x in symbols:
		print(findMaxMin(x))

#and here we run the function
findopps()