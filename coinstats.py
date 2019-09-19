#!/usr/bin/env python
import os, time, json, requests, sys

#################################################################################
#Get relative path###############################################################
#################################################################################
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]

#################################################################################
#Retrieve authentication variables###############################################
#################################################################################
with open(os.path.join(script_dir, 'cred.json')) as json_cred:
    cred = json.load(json_cred)

#################################################################################
#Setup Panoptic API##############################################################
#################################################################################
panoptic_token = cred['panoptic_token']
#panoptic_url = 'https://api.panoptic.io/fudhud/'
panoptic_url = 'http://localhost/panoptic.io/api/fudhud/'



cryptocompare_coins = {}
cryptocompare_translator = {
    'ethos' : 'bqx'
}
#Still missing 'True Chain (TRUE)', 'WaykiChain (WICC)', 'Dew (DEW)', and 'Paypex (PAYX)'

current_time = time.strftime('%Y-%m-%d %H:00:00', time.gmtime())

def getJSON(url):
    response = requests.get(url, headers = {'User-agent': 'FUDHUD Crawler 0.1'})
    return response.json()

def lookupCoins():
    global cryptocompare_coins
    url = 'https://www.cryptocompare.com/api/data/coinlist/'
    response = getJSON(url)
    cryptocompare_coins = response['Data']
    return cryptocompare_coins

def getPriceStats(limit):
    coins = {}

    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=' + str(limit)
    coinmarketcap = getJSON(url)
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
    data = getJSON(url)
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
#print(json.dumps(coins, indent=4, separators=(',', ': ')))
count = 0
for key in coins:
    print(key)

    cryptocompareID = ''
    coin_name = ''
    image_url = ''

    social = getSocialStats(key)

    try:
        cryptocompare_key = cryptocompare_translator[key]
    except:
        cryptocompare_key = key

    try:
        cryptocompareID = cryptocompare_coins[cryptocompare_key.upper()]['Id']
        coin_name = cryptocompare_coins[cryptocompare_key.upper()]['CoinName']
        image_url = 'http://cryptocompare.com' + cryptocompare_coins[cryptocompare_key.upper()]['ImageUrl']
    except:
        try:
            cryptocompareID = cryptocompare_coins[cryptocompare_key.upper() + '*']['Id']
            coin_name = cryptocompare_coins[cryptocompare_key.upper() + '*']['CoinName']
            image_url = 'http://cryptocompare.com' + cryptocompare_coins[cryptocompare_key.upper() + '*']['ImageUrl']
        except Exception as e:
            #print(cryptocompare_key.upper())
            print(e)


    if (coin_name != ''):
        count += 1

        if social:
            #print(cryptocompare_coins[key.upper()]['Id'])
            #print(cryptocompare_coins[key.upper()]['CoinName'])
            twitter_url = social['twitter'].get('link', '')
            reddit_url = social['reddit'].get('link', '')
            facebook_url = social['facebook'].get('link', '')
            git_url = social['repository'].get('url', '')

            #Post coin data
            coinID = requests.post(panoptic_url+'coin', data={'token' : panoptic_token,
                                                              'cryptocompareid' : cryptocompareID,
                                                              'name' : coin_name,
                                                              'symbol' : key,
                                                              'imageurl' : image_url,
                                                              'twitterurl' : twitter_url,
                                                              'redditurl' : reddit_url,
                                                              'facebookurl' : facebook_url,
                                                              'giturl' : git_url
                                                            }).json()['data']

            #Post price stats
            requests.post(panoptic_url+'stat', data={'token' : panoptic_token,
                                                     'data' : 'price',
                                                     'coinid' : coinID,
                                                     'datetime' : current_time,
                                                     'usd' : coins[key]['usd'],
                                                     'btc' : coins[key]['btc'],
                                                     'marketcap' : coins[key]['marketcap'],
                                                     'dailyvolume' : coins[key]['day_volume'],
                                                     'hourlychange' : coins[key]['hour_change'],
                                                     'dailychange' : coins[key]['day_change'],
                                                     'weeklychange' : coins[key]['week_change'],
                                                     'lastupdate' : coins[key]['last_update']
                                                    }).json()['data']
            #Post social stats
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

            requests.post(panoptic_url+'stat', data={'token' : panoptic_token,
                                                     'data' : 'social',
                                                     'coinid' : coinID,
                                                     'datetime' : current_time,
                                                     'twitterfollowers' : t_followers,
                                                     'twitterfollowing' : t_following,
                                                     'twitterstatuses' : t_statuses,
                                                     'twitterpoints' : t_points,
                                                     'redditsubscribers' : r_subscribers,
                                                     'redditactiveusers' : r_active,
                                                     'reddithourlyposts' : r_pph,
                                                     'redditdailyposts' : r_ppd,
                                                     'reddithourlycomments' : r_cph,
                                                     'redditdailycomments' : r_cpd,
                                                     'redditpoints' : r_points,
                                                     'facebooklikes' : f_likes,
                                                     'facebooktalking' : f_talking,
                                                     'facebookpoints' : f_points,
                                                     'gitstars' : g_stars,
                                                     'gitforks' : g_forks,
                                                     'gitsubscribers' : g_subscribers,
                                                     'gitsize' : g_size,
                                                     'gitlastupdate' : g_lastupdate,
                                                     'gitlastpush' : g_lastpush,
                                                     'gitopenissues' : g_oti,
                                                     'gitclosedissues' : g_cti,
                                                     'gitopenpullissues' : g_opi,
                                                     'gitclosedpullissues' : g_cpi
                                                    }).json()['data']
