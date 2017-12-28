import sys, tweepy, textblob, json, re, time, mysql.connector, requests, urllib
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
mysql_db = cred['mysql_db']

#keywords = ['$btc', '$xbt', '$eth', '$omg', '$ltc', '$xmr', '$xrp', '$zec', '$xem', '$gnt', '$zrx', '$sc', '$fct', '$maid', '$gno', '$cvc', '$dcr', '$amp', '$rep']
#cryptos = ['$mod', '$salt', '$xel', '$miota', '$iota', '$cnd', '$neo', '$omg', '$wtc', '$bat', '$ark', '$lkk', '$cvc', '$fct', '$gtn', '$maid', '$storj', '$knc', '$zrx', '$eth', '$btc', '$gno', '$rep', '$sc', '$xmr', '$xem', '$ltc', '$zec', '$str']
cryptos = []

#Get coinmarketcap data
url = 'https://api.coinmarketcap.com/v1/ticker/?limit=100'
response = urllib.urlopen(url)
coinmarketcap = json.loads(response.read())
for coin in coinmarketcap:
    symbol = '$' + coin['symbol'].lower()
    cryptos.append(symbol)
    print(cryptos)

keywords = cryptos[:]

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
        print('SQL ERROR')
        print(e)
        return

def getAllColumns():
    conn = connection.cursor(dictionary=True, buffered=True)

    conn.execute("SELECT * FROM trends LIMIT 1")
    numColumns = len(conn.description)
    columns = [i[0] for i in conn.description]
    columns = remove_values_from_list(columns, 'id')
    columns = remove_values_from_list(columns, 'date')
    connection.commit()
    dbwords = columns

    return dbwords

def getPopularColumns(amount):
    yesterday = date.today() - timedelta(1)
    yesterday.strftime('%Y-%m-%d')
    result = queryMySQL("SELECT * FROM trends WHERE date=%s", (yesterday, ))
    for row in result:
        row.pop('id', 0)
        row.pop('date', 0)
        dbwords = row.keys()

    keywords = sorted(dbwords, key=row.__getitem__, reverse=True)
    keywords = keywords[:amount]
    return keywords

def notify_node(array):
    data = json.dumps(array)
    url = 'http://127.0.0.1:1337/'
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
        twitter_stream.filter(track=cryptos)
    except:
        pass


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            print("Starting...")
            tweet = json.loads(data)
            print("Checking tweet...")
            if(tweet['text'].startswith('RT ') is False): #Remove any retweets

                #Check if user is in our spam list
                result = queryMySQL("SELECT twitterID, name FROM spammers WHERE name=%s", (tweet['user']['screen_name'],))
                #If user is not in spam list, continue
                if len(result) == 0:
                    #Remove urls from tweet text (tweet urls are unique even if the text is identical)
                    text = re.sub(r"(?:\@|https?\://)\S+", "", tweet['text'])
                    #Hash text for comparison
                    textHash = hash(text)
                    #Check if hash is in the hash list
                    if textHash not in hashList:
                        print("Tweet Passes...")
                        #Since the hash isn't in the list, add it to the list
                        hashList.append(textHash)

                        print(json.dumps(tweet['user']['name'], indent=4, separators=(',', ': ')))
                        print(json.dumps(tweet['user']['screen_name'], indent=4, separators=(',', ': ')))
                        print(json.dumps(tweet['text'], indent=4, separators=(',', ': ')))

                        analysis = tb(tweet['text'])
                        sentiment = analysis.sentiment.polarity
                        print(sentiment)
                        print('')

                        #Check for new words
                        pattern = r'(?:^|\s)(\$[^\W\d_]+)'
                        search = re.findall(pattern, strip_non_ascii(tweet['text']))
                        search = [x.lower() for x in search]
                        newwords = list(set(search) - set(keywords))
                        print(newwords)
                        print('')
                        #Add the new words to our keyword list
                        #if (len(keywords) + len(newwords)) < 500:
                        keywords.extend(newwords)
                        #Get current date to check against the database and add to each row
                        today = time.strftime('%Y-%m-%d %H:00:00')
                        #print(today)
                        #Start count of topics mentioned, which deterimines whether a user gets added to spam
                        topicCount = 0;
                        topicLimit = 5;

                        for word in keywords:
                            if contains_word(tweet['text'], word):
                                topicCount += 1

                                word = word.lower()
                                #Check if the topic already in the table for today
                                result = queryMySQL("SELECT mentionID FROM crypto_mentions WHERE date=%s AND topic=%s", (today, word))
                                if len(result) == 0:
                                    mentionID = queryMySQL("INSERT INTO crypto_mentions (date, topic, mentions, sentiment) VALUES (%s, %s, %s, %s)", (today, word, 1, sentiment))
                                else:
                                    for row in result:
                                        mentionID = row['mentionID']

                                        result = queryMySQL("SELECT * FROM crypto_mentions WHERE mentionID=%s", (mentionID, ))
                                        for row in result:
                                            wordcount = row['mentions']
                                            totalSentiment = float(row['sentiment']) * wordcount
                                            totalSentiment = totalSentiment + sentiment

                                            wordcount += 1

                                            newSentiment = totalSentiment / wordcount

                                            queryMySQL("UPDATE crypto_mentions SET mentions=%s, sentiment=%s WHERE mentionID=%s", (wordcount, newSentiment, mentionID))


                        if topicCount > topicLimit:
                            #Add user to spam list
                            queryMySQL("INSERT INTO spammers (twitterID, name) VALUES (%s, %s)", (tweet['user']['id'], tweet['user']['screen_name']))
                            print('USER ADDED TO SPAM LIST FOR TOO MANY TOPICS')
                            print('')

                        #with open('python.json', 'a') as f:
                            #f.write(data)
                            #return True


                    else:
                        #Add user to spam list
                        queryMySQL("INSERT INTO spammers (twitterID, name) VALUES (%s, %s)", (tweet['user']['id'], tweet['user']['screen_name']))
                        print('USER ' + tweet['user']['screen_name'] + ' ADDED TO SPAM LIST FOR REPEAT TWEET: ' + tweet['text'])
                        print('')

                    result = queryMySQL("SELECT twitterID FROM spammers WHERE twitterID=%s", (tweet['user']['id'],))
                    if len(result) == 0:
                        print('USER NOT IN SPAM LIST')
                        result = queryMySQL("SELECT twitterID FROM crypto_users WHERE twitterID=%s", (tweet['user']['id'],))

                        tweetObj = {'service' : 'tweetstream', 'name' : tweet['user']['name'], 'screen_name'  : tweet['user']['screen_name'], 'pic' : tweet['user']['profile_image_url'], 'tweet' : tweet['text'].encode("utf-8")}

                        print(tweet['entities'])
                        if 'media' in tweet['entities']:
                            tweetMedia = tweet['entities']['media'][0]['media_url_https']
                            print(tweet['entities']['media'][0]['media_url_https'])
                            tweetObj['media'] = tweetMedia

                        notify_node(tweetObj)

                        if len(result) == 0:
                            print('USER NOT IN USERS LIST')
                            queryMySQL("INSERT INTO crypto_users (twitterID, name, screenName, description, location, timezone, followers, friends) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (tweet['user']['id'], tweet['user']['name'], tweet['user']['screen_name'], tweet['user']['description'], tweet['user']['location'], tweet['user']['time_zone'], tweet['user']['followers_count'], tweet['user']['friends_count']))

                    print('')
                    print('')
                    return True

                else:
                    print('')

        except BaseException as e:
            print("Error on_data: %s" % str(e))

        return True

    def on_error(self, status):
        print(status)
        return False


#keywords = getAllColumns()
#keywords = getMostPopular(400)

#print(sorted(data.items(), key=lambda x:x[1], reverse=True))
#print(data)

#queryMySQL("ALTER TABLE trends DROP $crypto")
#queryMySQL("ALTER TABLE trends ADD $crypto INT(10) UNSIGNED NOT NULL DEFAULT 0")
#queryMySQL("ALTER TABLE trends ALTER COLUMN $crypto SET DEFAULT 0")
hashList = []

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

while True:
    startStream()
    print('Restarting Twitter Stream...')
    time.sleep(60)
