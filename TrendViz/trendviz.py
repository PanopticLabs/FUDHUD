import sys
sys.path.insert(0, 'scripts')
import json

import googletrends
import plotly_twoline
import coinmarketcap


def getSymbol(coinname):
    with open('symbols.json') as json_data:
        symbols = json.load(json_data)
        symbol = symbols[coinname.lower()]
        return symbol


try:
    timescale = sys.argv[1]

    coin = sys.argv[2]
    term = coin.replace('-', ' ')
except Exception as e:
    print e
    raise

try:
    sym = getSymbol(coin)
    print 'Retrieved Symbol: ' + sym
except:
    #Download symbol data from coinmarketcap, current limit is set to top 200 coins
    coinlimit = 200

    print 'Downloading symbols for top ' + str(coinlimit) + ' coins...'
    coinmarketcap.downloadSymbols(coinlimit, 'symbols.json')
    try:
        sym = getSymbol(coin)
        print 'Retrieved Symbol: ' + sym
    except Exception as e:
        print e

try:
    print 'Gathering data from Google Trends and CryptoCompare...'
    googletrends.get_data(term, sym, timescale)
    print 'Complete'
    print 'Creating visualization...'
    plotly_twoline.plotGraph('csv/' + sym.lower() + '.csv', 'Date', term.title() + ' Trends', 'Historical Price (USD)', term.title() + ' Trends vs Price', term.title() + ' Trends', 'Historical Price (USD)')
except Exception as e:
    print e
