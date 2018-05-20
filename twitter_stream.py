#!/usr/bin/env python
import sys, tweepy, textblob, json, re, time, mysql.connector, requests, urllib, mail
from textblob import TextBlob as tb
from datetime import date, timedelta
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

with open('cred.json') as json_cred:
    cred = json.load(json_cred)

consumer_key = cred['consumer_key']
consumer_secret = cred['consumer_secret']
access_token = cred['access_token']
access_secret = cred['access_secret']

mysql_user = cred['mysql_user']
mysql_pass = cred['mysql_pass']
mysql_host = cred['mysql_host']
mysql_db = 'panoptic_fudhud'

#keywords = ['$btc', '$xbt', '$eth', '$omg', '$ltc', '$xmr', '$xrp', '$zec', '$xem', '$gnt', '$zrx', '$sc', '$fct', '$maid', '$gno', '$cvc', '$dcr', '$amp', '$rep']
#cryptos = ['$mod', '$salt', '$xel', '$miota', '$iota', '$cnd', '$neo', '$omg', '$wtc', '$bat', '$ark', '$lkk', '$cvc', '$fct', '$gtn', '$maid', '$storj', '$knc', '$zrx', '$eth', '$btc', '$gno', '$rep', '$sc', '$xmr', '$xem', '$ltc', '$zec', '$str']
cryptos = []
blacklist = set(['accepting new users', 'Binance registration', 'Register with Binance', 'on Binance with 50% discount trading fee'])

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
        hashsym = '#' + symbol
        symname = '$' + name
        hashname = '#' + name
        #Check that symbol does not use an ambiguous word
        shitlist = ['pay', 'sub', 'part', 'fun', 'bts', 'act', 'sky', 'link', 'elf', 'waves']
        if symbol in shitlist:
            coin_list.append(hashname)
            coin_list.append(symname)
            coin_list.append(topic)
            coin_dict[symbol] = [hashname, symname, topic]
        else:
            coin_list.append(hashname)
            coin_list.append(symname)
            coin_list.append(topic)
            coin_list.append(hashsym)
            coin_dict[symbol] = [hashname, symname, topic, hashsym]
        #print(cryptos)

    coins['list'] = coin_list
    coins['dict'] = coin_dict
    return coins


coins = getCoins()

#
#Setup MySQL connection
#
connection = mysql.connector.connect(user=mysql_user, password=mysql_pass,
                              host=mysql_host,
                              database=mysql_db)

dbwords = []

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
        #subject = 'Twitter SQL Error'
        #mail.sendMail(subject, e)
        return

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
    except Exception as e:
        subject = 'Twitter Stream Error'
        mail.sendMail(subject, e)
        pass


class MyListener(StreamListener):
    def on_data(self, data):
        count = 0
        try:
            #print("Starting...")
            tweet = json.loads(data)
            count += 1
            #print(json.dumps(tweet, indent=4, separators=(',', ': ')))
            #print("Checking tweet...")
            #Check if user is in our spam list
            result = queryMySQL("SELECT twitterID, name FROM twitter_spammers WHERE name=%s", (tweet['user']['screen_name'],))
            count += 1
            #If user is not in spam list, continue
            if len(result) == 0:
                count += 1
                status_link = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + str(tweet['id'])
                count += 1
                if(tweet['text'].startswith('RT ') is False): #Remove any retweets
                    count += 1
                    #Remove urls from tweet text (tweet urls are unique even if the text is identical)
                    text = re.sub(r"(?:\@|https?\://)\S+", "", tweet['text'])
                    count += 1
                    #Hash text for comparison
                    textHash = hash(text)
                    count += 1
                    #Check if hash is in the hash list
                    if (textHash not in hashList) and (not bool(blacklist.intersection(text))):
                        count += 1
                        print("Tweet Passes...")
                        count += 1
                        #Since the hash isn't in the list, add it to the list
                        hashList.append(textHash)
                        count += 1

                        #print(json.dumps(tweet['user']['name'], indent=4, separators=(',', ': ')))
                        #print(json.dumps(tweet['user']['screen_name'], indent=4, separators=(',', ': ')))
                        #print(json.dumps(tweet['text'], indent=4, separators=(',', ': ')))

                        analysis = tb(tweet['text'])
                        count += 1
                        sentiment = analysis.sentiment.polarity
                        count += 1
                        #print(sentiment)
                        #print('')

                        #Get current date to check against the database and add to each row
                        today = time.strftime('%Y-%m-%d %H:%M:00')
                        count += 1
                        #print(today)
                        #Start count of topics mentioned, which deterimines whether a user gets added to spam
                        topicCount = 0;
                        count += 1
                        topicLimit = 5;
                        count += 1

                        topics = []
                        count += 1
                        t = tweet['text'].lower()
                        count += 1
                        for topic in coins['dict']:
                            count += 1
                            if any(word in t.split() for word in coins['dict'][topic]):
                                #print(json.dumps(tweet['text'], indent=4, separators=(',', ': ')))
                                #print(topic)
                                topicCount += 1
                                topics.append(topic)

                                #word = word.lower()
                                #Check if the topic already in the table for today
                                result = queryMySQL("SELECT mentionID FROM twitter_mentions WHERE date=%s AND topic=%s", (today, topic))
                                if len(result) == 0:
                                    mentionID = queryMySQL("INSERT INTO twitter_mentions (date, topic, mentions, sentiment) VALUES (%s, %s, %s, %s)", (today, topic, 1, sentiment))
                                else:
                                    for row in result:
                                        mentionID = row['mentionID']

                                        result = queryMySQL("SELECT * FROM twitter_mentions WHERE mentionID=%s", (mentionID, ))
                                        for row in result:
                                            wordcount = row['mentions']
                                            totalSentiment = float(row['sentiment']) * wordcount
                                            totalSentiment = totalSentiment + sentiment

                                            wordcount += 1

                                            newSentiment = totalSentiment / wordcount

                                            queryMySQL("UPDATE twitter_mentions SET mentions=%s, sentiment=%s WHERE mentionID=%s", (wordcount, newSentiment, mentionID))


                        if topicCount > topicLimit:
                            #Add user to spam list
                            queryMySQL("INSERT INTO twitter_spammers (twitterID, name) VALUES (%s, %s)", (tweet['user']['id'], tweet['user']['screen_name']))
                            print('USER ADDED TO SPAM LIST FOR TOO MANY TOPICS')
                            print('')

                        #with open('python.json', 'a') as f:
                            #f.write(data)
                            #return True


                    else:
                        #Add user to spam list
                        queryMySQL("INSERT INTO twitter_spammers (twitterID, name) VALUES (%s, %s)", (tweet['user']['id'], tweet['user']['screen_name']))
                        print('USER ' + tweet['user']['screen_name'] + ' ADDED TO SPAM LIST FOR REPEAT TWEET: ' + tweet['text'])
                        print('')

                    result = queryMySQL("SELECT twitterID FROM twitter_spammers WHERE twitterID=%s", (tweet['user']['id'],))
                    if len(result) == 0:
                        print('USER NOT IN SPAM LIST')
                        result = queryMySQL("SELECT twitterID FROM twitter_users WHERE twitterID=%s", (tweet['user']['id'],))

                        tweetObj = {'service' : 'tweetstream', 'name' : tweet['user']['name'], 'screen_name'  : tweet['user']['screen_name'], 'pic' : tweet['user']['profile_image_url'], 'tweet' : tweet['text'].encode("utf-8"), 'link' : status_link, 'rt_count' : '0', 'fav_count' : '0', 'topics' : topics}

                        #print(tweet['entities'])
                        if 'media' in tweet['entities']:
                            tweetMedia = tweet['entities']['media'][0]['media_url_https']
                            #print(tweet['entities']['media'][0]['media_url_https'])
                            tweetObj['media'] = tweetMedia

                        notify_node(tweetObj)

                        if len(result) == 0:
                            print('USER NOT IN USERS LIST')
                            queryMySQL("INSERT INTO twitter_users (twitterID, name, screenName, description, location, timezone, followers, friends) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (tweet['user']['id'], tweet['user']['name'], tweet['user']['screen_name'], tweet['user']['description'], tweet['user']['location'], tweet['user']['time_zone'], tweet['user']['followers_count'], tweet['user']['friends_count']))

                    print('')
                    print('')
                    return True

                #if tweet is a retweet
                else:
                    try:
                        print('RETWEET')
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


            print('')
            return True

        except BaseException as e:
            subject = 'Twitter MyListener Error'
            content = 'Count ' + str(count) + ': ' + str(e)
            mail.sendMail(subject, content)
            #print("Error on_data: %s" % str(e))

        return True

    def on_error(self, status):
        print(status)
        return False

hashList = []
print(coins['list'])
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

while True:
    startStream()
    print('Restarting Twitter Stream...')
    time.sleep(60)
