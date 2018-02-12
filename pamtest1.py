#dwighttest1.py


import os
import sys
import json
import datetime

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

# return up to ten bidasks on each side of the order book stackw
independentreserve = ccxt.independentreserve({})
btcmarkets = ccxt.btcmarkets({})


exchange = [independentreserve, btcmarkets]

symbols = ('ETH/AUD', 'BTC/AUD')

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

marketprices = genMarketPrices()

def findopps(marketprices):
	findingmax = {}
	findingmin = {}
	minmaxpairs = {}
	sym = symbols[0]
	for x in marketprices:
		t = marketprices[x]
		print(t)
		for y in t:
			if y == sym+' bid':
				findingmax[x] = t[y]
			elif y == sym+' ask':
				findingmin[x] = t[y]
	maxval = max(findingmax)
	minval = min(findingmin)
	arbopps = ((findingmax[maxval] - findingmin[minval])/findingmin[minval])	
	minmaxpairs[sym] = [((maxval, findingmax[maxval])),((minval, findingmin[minval])), arbopps]
	print(minmaxpairs)

	

findopps(marketprices)