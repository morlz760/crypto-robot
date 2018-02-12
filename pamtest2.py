#dwighttest1.py


import os
import sys
import json
import datetime

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

print(' ----- RUNNING CRYPTO ROBOT ----- ')

independentreserve = ccxt.independentreserve({})
btcmarkets = ccxt.btcmarkets({})


exchange = [independentreserve, btcmarkets]

symbols = ('ETH/AUD', 'BTC/AUD')

def genMarketPrices():
	marketgroup = {}
	for x in symbols:
		bidasks = {}
		for y in exchange:
			orderbook = y.fetch_ticker(x)
			bidx = orderbook.get('bid')
			askx = orderbook.get('ask')
			bidasks[y.id+' bid'] = bidx
			bidasks[y.id+' ask'] = askx
		marketgroup[x] = bidasks
	return(marketgroup)

marketprices = genMarketPrices()

def findopps(marketprices):
	findingmax = []
	for x in marketprices:
		t = marketprices[x]
		for y in t:
			if y == 'ETH/AUD bid':
				findingmax.append(t[y])
	print(max(findingmax))
print(marketprices)




'ETH/AUD': {'independentreserve bid': 1180.0, 'independentreserve ask': 1190.9, 'btcmarkets bid': 1177.08, 'btcmarkets ask': 1188.98}
