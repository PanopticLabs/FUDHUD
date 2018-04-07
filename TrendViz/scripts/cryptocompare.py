import urllib2
import json
import time
from datetime import datetime

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
       
def lookupPrice(timestring, symbol):
    if len(timestring) == 13:
        dt = datetime.strptime(timestring, "%Y-%m-%dT%H")
        unixtime = time.mktime(dt.timetuple())
    else:
        dt = datetime.strptime(timestring, "%Y-%m-%d")
        unixtime = time.mktime(dt.timetuple())

    unixtime = str(int(unixtime))

    url = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym=' + symbol + '&tsyms=BTC,USD,EUR,CAD&ts=' + unixtime

    request = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(request)

    data = json.load(response)
    return data
    #print json.dumps(j, indent=4, separators=(',', ': '))
