#dwighttest1.py


import os
import sys
import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

# return up to ten bidasks on each side of the order book stackw
independentreserve = ccxt.independentreserve({})
btcmarkets = ccxt.btcmarkets({})

sched = BlockingScheduler()

exchange = [independentreserve, btcmarkets]

symbols = ('ETH/AUD', 'BTC/AUD')

f = open('entries.txt', 'a')

@sched.scheduled_job('interval', minutes=15)
def k():
	for y in exchange:
		for x in symbols:
			orderbook = y.fetch_ticker(x)
			bidx = orderbook.get('bid')
			askx = orderbook.get('ask')
			spreadx = (askx - bidx) if (bidx and askx) else None
			tobewritten = (y.id, x, datetime.datetime.now(), 'market price', { 'bid': bidx, 'ask': askx, 'spread': spreadx })
			tobewritten = str(tobewritten)
			f.write(tobewritten)

sched.start()
