#!/usr/bin/env python
import time, json, mysql.connector, urllib2, sys

with open('cred.json') as json_cred:
    cred = json.load(json_cred)

mysql_user = cred['mysql_user']
mysql_pass = cred['mysql_pass']
mysql_host = cred['mysql_host']
mysql_db = 'panoptic_fudhud'

cryptocompare_coins = {}
cryptocompare_translator = {
    'miota' : 'iot',
    'nano' : 'xrb',
    'ethos' : 'bqx'
}
#Still missing 'True Chain (TRUE)', 'WaykiChain (WICC)', 'Dew (DEW)', and 'Paypex (PAYX)'

current_time = time.strftime('%Y-%m-%d %H:00:00')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#
#Setup MySQL connection
#
connection = mysql.connector.connect(user=mysql_user, password=mysql_pass,
                              host=mysql_host,
                              database=mysql_db)


def queryMySQL(query, variables=None):
    conn = connection.cursor(dictionary=True, buffered=True)

    try:
        if variables is None:
            conn.execute(query)
        else:
            conn.execute(query, variables)

        try:
            result = conn.fetchall()
            connection.commit()
            return result
        except:
            result = conn.lastrowid
            connection.commit()
            return result
    except:
        e = sys.exc_info()
        print('SQL ERROR')
        print(e)
        return


def lookupCoins():
    global cryptocompare_coins
    url = 'https://www.cryptocompare.com/api/data/coinlist/'
    request = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(request)

    data = json.load(response)

    cryptocompare_coins = data['Data']
    return cryptocompare_coins

def getPriceStats(limit):
    coins = {}

    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=' + str(limit)
    request = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(request)

    coinmarketcap = json.load(response)
    for coin in coinmarketcap:
        symbol = coin['symbol'].lower()
        usd = coin['price_usd']
        btc = coin['price_btc']
        marketcap = coin['market_cap_usd']
        day_volume = coin['24h_volume_usd']
        hour_change = coin['percent_change_1h']
        day_change = coin['percent_change_24h']
        week_change = coin['percent_change_7d']
        last_update = coin['last_updated']


        coins[symbol] = {}
        coins[symbol]['usd'] = usd
        coins[symbol]['btc'] = btc
        coins[symbol]['marketcap'] = marketcap
        coins[symbol]['day_volume'] = day_volume
        coins[symbol]['hour_change'] = hour_change
        coins[symbol]['day_change'] = day_change
        coins[symbol]['week_change'] = week_change
        coins[symbol]['last_update'] = last_update

    return coins

def getSocialStats(symbol):
    global cryptocompare_coins

    try:
        symbol = cryptocompare_translator[symbol]
    except:
        pass

    if len(cryptocompare_coins) == 0:
        cryptocompare_coins = lookupCoins()

    try:
        coin_id = str(cryptocompare_coins[symbol.upper()]['Id'])
    except:
        try:
            coin_id = str(cryptocompare_coins[symbol.upper() + '*']['Id'])
        except Exception as e:
            return False

    url = 'https://www.cryptocompare.com/api/data/socialstats/?id=' + coin_id
    request = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(request)

    data = json.load(response)
    stats = {}
    if data['Data']['Twitter']['Points'] == 0:
        stats['twitter'] = {
            'Points' : 0,
            'followers' : 0,
            'following' : 0,
            'statuses' : 0,
            'link' : ''
        }
    else:
        stats['twitter'] = data['Data']['Twitter']

    if data['Data']['Reddit']['Points'] == 0:
        stats['reddit'] = {
            'Points' : 0,
            'subscribers' : 0,
            'comments_per_day' : 0,
            'comments_per_hour' : 0,
            'active_users' : 0,
            'link' : '',
            'posts_per_day' : 0,
            'posts_per_hour' : 0
        }
    else:
        stats['reddit'] = data['Data']['Reddit']

    if data['Data']['Facebook']['Points'] == 0:
        stats['facebook'] = {
            'link' : '',
            'talking_about' : 0,
            'likes' : 0,
            'Points' : 0
        }
    else:
        stats['facebook'] = data['Data']['Facebook']

    if data['Data']['CodeRepository']['Points'] == 0:
        stats['repository'] = {
            'open_pull_issues' : 0,
            'url' : '',
            'size' : 0,
            'fork' : 0,
            'stars' : 0,
            'closed_total_issues' : 0,
            'closed_issues' : 0,
            'closed_pull_issues' : 0,
            'open_total_issues' : 0,
            'last_update' : 0,
            'subscribers' : 0,
            'forks' : 0,
            'last_push' : 0,
            'open_issues' : 0
        }
    else:
        stats['repository'] = data['Data']['CodeRepository']['List'][-1]
        stats['repository']['Points'] = data['Data']['CodeRepository']['Points']

    return stats

coins = getPriceStats(200)
for key in coins:
    print(key)
    social = getSocialStats(key)
    if social:
        try:
            cryptocompare_key = cryptocompare_translator[key]
        except:
            cryptocompare_key = key

        try:
            coinID = cryptocompare_coins[cryptocompare_key.upper()]['Id']
            coinName = cryptocompare_coins[cryptocompare_key.upper()]['CoinName']
            imageURL = 'http://cryptocompare.com' + cryptocompare_coins[cryptocompare_key.upper()]['ImageUrl']
        except:
            try:
                coinID = cryptocompare_coins[cryptocompare_key.upper() + '*']['Id']
                coinName = cryptocompare_coins[cryptocompare_key.upper() + '*']['CoinName']
                imageURL = 'http://cryptocompare.com' + cryptocompare_coins[cryptocompare_key.upper() + '*']['ImageUrl']
            except Exception as e:
                print(cryptocompare_key.upper())
                print(e)
                break

        print(coinID)
        #print(cryptocompare_coins[key.upper()]['Id'])
        #print(cryptocompare_coins[key.upper()]['CoinName'])
        twitterURL = social['twitter'].get('link', '')
        redditURL = social['reddit'].get('link', '')
        facebookURL = social['facebook'].get('link', '')
        gitURL = social['repository'].get('url', '')

        result = queryMySQL("SELECT coinID FROM coins WHERE symbol=%s", (key, ))
        if len(result) == 0:
            coinID = queryMySQL("INSERT INTO coins(cryptocompareID, name, symbol, imageURL, twitterURL, redditURL, facebookURL, gitURL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (coinID, coinName, key, imageURL, twitterURL, redditURL, facebookURL, gitURL))
        else:
            for row in result:
                coinID = row['coinID']

        result = queryMySQL("SELECT priceStatID FROM priceStats WHERE coinID=%s AND datetime=%s", (coinID, current_time))
        if len(result) == 0:
            #print(coins[key]['marketcap'])
            queryMySQL("INSERT INTO priceStats(coinID, datetime, usd, btc, marketcap, dailyVolume, hourlyChange, dailyChange, weeklyChange, lastUpdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (coinID, current_time, coins[key]['usd'], coins[key]['btc'], coins[key]['marketcap'], coins[key]['day_volume'], coins[key]['hour_change'], coins[key]['day_change'], coins[key]['week_change'], coins[key]['last_update']))

        result = queryMySQL("SELECT socialStatID FROM socialStats WHERE coinID=%s AND datetime=%s", (coinID, current_time))
        if len(result) == 0:
            t_followers = social['twitter'].get('followers', 0)
            t_following = social['twitter'].get('following', 0)
            t_statuses = social['twitter'].get('statuses', 0)
            t_points = social['twitter'].get('Points', 0)
            r_subscribers = social['reddit'].get('subscribers', 0)
            r_active = social['reddit'].get('active_users', 0)
            r_pph = social['reddit'].get('posts_per_hour', 0)
            r_ppd = social['reddit'].get('posts_per_day', 0)
            r_cph = social['reddit'].get('comments_per_hour', 0)
            r_cpd = social['reddit'].get('comments_per_day', 0)
            r_points = social['reddit'].get('Points', 0)
            f_likes = social['facebook'].get('likes', 0)
            f_talking = social['facebook'].get('talking_about', 0)
            f_points = social['facebook'].get('Points', 0)
            g_stars = social['repository'].get('stars', 0)
            g_forks = social['repository'].get('forks', 0)
            g_subscribers = social['repository'].get('subscribers', 0)
            g_size = social['repository'].get('size', 0)
            g_lastupdate = social['repository'].get('last_update', 0)
            g_lastpush = social['repository'].get('last_push', 0)
            g_oti = social['repository'].get('open_total_issues', 0)
            g_cti = social['repository'].get('closed_total_issues', 0)
            g_opi =social['repository'].get('open_pull_issues', 0)
            g_cpi = social['repository'].get('closed_pull_issues', 0)
            queryMySQL("INSERT INTO socialStats(coinID, datetime, twitter_followers, twitter_following, twitter_statuses, twitter_points, reddit_subscribers, reddit_activeUsers, reddit_hourlyPosts, reddit_dailyPosts, reddit_hourlyComments, reddit_dailyComments, reddit_points, facebook_likes, facebook_talking, facebook_points, git_stars, git_forks, git_subscribers, git_size, git_lastUpdate, git_lastPush, git_openIssues, git_closedIssues, git_openPullIssues, git_closedPullIssues) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (coinID, current_time, t_followers, t_following, t_statuses, t_points, r_subscribers, r_active, r_pph, r_ppd, r_cph, r_cpd, r_points, f_likes, f_talking, f_points, g_stars, g_forks, g_subscribers, g_size, g_lastupdate, g_lastpush, g_oti, g_cti, g_opi, g_cpi))
