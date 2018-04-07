import urllib
import json

def downloadSymbols(limit, filepath):
    #Get coinmarketcap data
    coins = {}

    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=' + str(limit)
    response = urllib.urlopen(url)
    coinmarketcap = json.loads(response.read())
    for coin in coinmarketcap:
        name = coin['name'].lower()
        name = name.replace(" ", "-")
        symbol = coin['symbol'].lower()

        coins[name] = symbol

    with open(filepath, 'w') as outfile:
        json.dump(coins, outfile)
