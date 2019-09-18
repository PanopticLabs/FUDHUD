#!/usr/bin/env python
import os, sys, tweepy, textblob, json, re, time, requests, urllib, mail, subprocess
from textblob import TextBlob as tb
from datetime import date, timedelta
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

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
panoptic_url = 'https://api.panoptic.io/fudhud/'

#################################################################################
#Setup Twitter API###############################################################
#################################################################################
consumer_key = cred['consumer_key']
consumer_secret = cred['consumer_secret']
access_token = cred['access_token']
access_secret = cred['access_secret']
#################################################################################
#################################################################################
#################################################################################

def getCoins():
    #Get coinmarketcap data
    coins = {}
    coin_list = []
    coin_dict = {}
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=100'
    response = urllib.urlopen(url)
    coinmarketcap = json.loads(response.read())
    for coin in coinmarketcap:
        name = coin['name'].lower()
        name = name.replace(" ", "")
        symbol = coin['symbol'].lower()
        topic = '$' + symbol
        #hashsym = '#' + symbol
        #symname = '$' + name
        #hashname = '#' + name
        #Check that symbol does not use an ambiguous word
        shitlist = ['pay', 'sub', 'part', 'fun', 'bts', 'act', 'sky', 'link', 'elf', 'waves']
        if symbol in shitlist:
            #coin_list.append(hashname)
            #coin_list.append(symname)
            coin_list.append(topic)
            #coin_dict[symbol] = [hashname, symname, topic]
            coin_dict[symbol] = [topic]
        else:
            #coin_list.append(hashname)
            #coin_list.append(symname)
            coin_list.append(topic)
            #coin_list.append(hashsym)
            #coin_dict[symbol] = [hashname, symname, topic, hashsym]
            coin_dict[symbol] = [topic]
        #print(cryptos)

    coins['list'] = coin_list
    coins['dict'] = coin_dict
    return coins

def notify_node(array):
    data = json.dumps(array)
    url = 'https://fierce-forest-58606.herokuapp.com/'
    headers = {'Content-Type': 'application/json', 'Content-Length' : str(len(data))}
    res = requests.post(url, data=data, headers=headers)

def contains_word(s, w):
    s = s.lower()
    w = w.lower()
    return (' ' + w + ' ') in (' ' + s + ' ')

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def startStream():
    try:
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=coins['list'])
    #except IncompleteRead:
        # Oh well, reconnect and keep trucking
        #continue
    except Exception as e:
        subject = 'Twitter Stream Error'
        #mail.sendMail(subject, e)
        print(e)
        pass


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            tweet = json.loads(data)
            #print(json.dumps(tweet, indent=4, separators=(',', ': ')))
            try:
                user = tweet['user']
            except:
                print('No user!')
                return False

            #Check if user is in our spam list
            #result = queryMySQL("SELECT twitterID, name FROM twitter_spammers WHERE name=%s", (user['screen_name'],))
            result = requests.get(panoptic_url + 'spammers?data=twitter&name=' + user['screen_name']).json()['data']
            #If user is not in spam list, continue
            if not result:
                status_link = 'https://twitter.com/' + user['screen_name'] + '/status/' + str(tweet['id'])
                if(tweet['text'].startswith('RT ') is False): #Remove any retweets
                    #Remove urls from tweet text (tweet urls are unique even if the text is identical)
                    text = re.sub(r"(?:\@|https?\://)\S+", "", tweet['text'])
                    #Hash text for comparison
                    textHash = hash(text)
                    #Check if hash is in the hash list
                    if (textHash not in hashList) and (not bool(blacklist.intersection(text))):
                        #print("Tweet Passes...")

                        #Since the hash isn't in the list, add it to the list
                        hashList.append(textHash)

                        print(json.dumps(user['name'], indent=4, separators=(',', ': ')))
                        print(json.dumps(user['screen_name'], indent=4, separators=(',', ': ')))
                        print(json.dumps(tweet['text'], indent=4, separators=(',', ': ')))
                        print('')

                        analysis = tb(tweet['text'])
                        sentiment = analysis.sentiment.polarity
                        #print(sentiment)

                        #Get current date to check against the database and add to each row
                        datetime = time.strftime('%Y-%m-%d %H:%M:00', time.gmtime())
                        #print(datetime)
                        #Start count of topics mentioned, which deterimines whether a user gets added to spam
                        topicCount = 0;
                        topicLimit = 5;

                        topics = []
                        t = tweet['text'].lower()
                        for topic in coins['dict']:
                            if any(word in t.split() for word in coins['dict'][topic]):
                                #print(json.dumps(tweet['text'], indent=4, separators=(',', ': ')))
                                #print(topic)
                                topicCount += 1
                                topics.append(topic)

                                #Post mention to api
                                requests.post(panoptic_url + 'mention', data={'datetime' : datetime, 'topic' : topic, 'sentiment' : sentiment, 'token' : panoptic_token, 'data' : 'twitter'}).json()['message']

                        if topicCount > topicLimit:
                            #Add user to spam list
                            requests.post(panoptic_url+'spammers', data={'id' : user['id'], 'name' : user['screeen_name'], 'token' : panoptic_token, 'data' : 'twitter'}).json()['message']

                        #with open('python.json', 'a') as f:
                            #f.write(data)
                            #return True
                        else:
                            tweetObj = {'service' : 'tweetstream', 'name' : user['name'], 'screen_name'  : user['screen_name'], 'pic' : user['profile_image_url'], 'tweet' : tweet['text'].encode("utf-8"), 'link' : status_link, 'rt_count' : '0', 'fav_count' : '0', 'topics' : topics}

                            if 'media' in tweet['entities']:
                                tweetMedia = tweet['entities']['media'][0]['media_url_https']
                                #print(tweet['entities']['media'][0]['media_url_https'])
                                tweetObj['media'] = tweetMedia

                            notify_node(tweetObj)
                            requests.post(panoptic_url+'user', data={'twitterid' : user['id'], 'name' : strip_non_ascii(user['name']), 'screenname' : strip_non_ascii(user['screen_name']), 'description' : strip_non_ascii(user['description']), 'location' : user['location'], 'timezone' : user['time_zone'], 'followers' : user['followers_count'], 'friends' : user['friends_count'], 'token' : panoptic_token, 'data' : 'twitter'}).json()['data']

                    else:
                        #Add user to spam list
                        result = requests.post(panoptic_url+'spammers', data={'id' : user['id'], 'name' : user['screeen_name'], 'token' : panoptic_token, 'data' : 'twitter'}).json()['message']

                        #print('USER ' + user['screen_name'] + ' ADDED TO SPAM LIST FOR REPEAT TWEET: ' + tweet['text'])


                    return True

                #if tweet is a retweet
                else:
                    try:
                        #print('RETWEET')
                        #print(json.dumps(tweet, indent=4, separators=(',', ': ')))
                        topics = []
                        t = tweet['retweeted_status']['text'].lower()
                        for topic in coins['dict']:
                            if any(word in t.split() for word in coins['dict'][topic]):
                                #print(json.dumps(tweet['text'], indent=4, separators=(',', ': ')))
                                #print(topic)
                                topics.append(topic)

                        tweetObj = {'service' : 'tweetstream', 'name' : tweet['retweeted_status']['user']['name'], 'screen_name'  : tweet['retweeted_status']['user']['screen_name'], 'pic' : tweet['retweeted_status']['user']['profile_image_url'], 'tweet' : tweet['retweeted_status']['text'].encode("utf-8"), 'link' : status_link, 'rt_count' : tweet['retweeted_status']['retweet_count'], 'fav_count' : tweet['retweeted_status']['favorite_count'], 'topics' : topics}
                        #print(json.dumps(tweetObj, indent=4, separators=(',', ': ')))
                        notify_node(tweetObj)
                    except:
                        pass

            return True

        except BaseException as e:
            if str(e) == 'MySQL Connection not available.':
                #mail.sendMail('Twitter MyListener Error: MySQL Connection not available.','Restarting MySQL and Twitter Stream...')
                #Reset MySQL Connection
                subprocess.call('service mysql restart')
                return False
            #else:
                #subject = 'Twitter MyListener Error: ' + str(e)
                #mail.sendMail(subject, json.dumps(tweet, indent=4, separators=(',', ': ')))
            #print("Error on_data: %s" % str(e))

        return True

    def on_error(self, status):
        print(status)
        return False

#keywords = ['$btc', '$xbt', '$eth', '$omg', '$ltc', '$xmr', '$xrp', '$zec', '$xem', '$gnt', '$zrx', '$sc', '$fct', '$maid', '$gno', '$cvc', '$dcr', '$amp', '$rep']
#cryptos = ['$mod', '$salt', '$xel', '$miota', '$iota', '$cnd', '$neo', '$omg', '$wtc', '$bat', '$ark', '$lkk', '$cvc', '$fct', '$gtn', '$maid', '$storj', '$knc', '$zrx', '$eth', '$btc', '$gno', '$rep', '$sc', '$xmr', '$xem', '$ltc', '$zec', '$str']
cryptos = []
coins = getCoins()
dbwords = []
hashList = []
blacklist = set(['accepting new users', 'Binance registration', 'Register with Binance', 'on Binance with 50% discount trading fee'])
print(coins['list'])
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

while True:
    startStream()

    #mail.sendMail('Twitter Restart','Restarting Twitter Stream...')
    time.sleep(60)
