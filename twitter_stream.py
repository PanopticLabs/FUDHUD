import sys, tweepy, textblob, json, re, time, mysql.connector, requests
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
keywords = ['$mod', '$salt', '$xel', '$miota', '$iota', '$cnd', '$neo', '$omg', '$wtc', '$bat', '$ark', '$lkk', '$cvc', '$fct', '$gtn', '$maid', '$storj', '$knc', '$zrx', '$eth', '$btc', '$gno', '$rep', '$sc', '$xmr', '$xem', '$ltc', '$zec']

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

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            tweet = json.loads(data)
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
                        keywords.extend(newwords)
                        #Get current date to check against the database and add to each row
                        today = time.strftime('%Y-%m-%d')
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
        return True


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

twitter_stream = Stream(auth, MyListener())
#twitter_stream.filter(follow=["372670289", "242988022", "2491780596", "4809119178", "857324455906955265", "2755711470", "2603525726", "188200785", "16825716", "4883282427", "2545340341", "2474001188", "4469439315", "15076390", "30077085", "354847710", "2939964463", "2445396642", "2207466804", "2199095514", "3102352966", "886832413", "427683064", "2646838458", "3014374765", "16186995", "2350970786", "2331297668", "4812598373", "2436257148", "494067493", "2261759419", "16722167", "548531623", "488068087", "2984516592", "2445577221", "2775995436", "2309818874", "570690894", "2153022625", "4919234126", "170783148", "15276283", "1333467482", "2655088121", "2796556901", "352518189", "2307692107", "4041496403", "2242726506", "19701628", "19537263", "2313884124", "2432540773", "309366491", "2225300413", "2553526670", "2493846643", "915465450", "2331238783", "187978594", "2358139032", "2270186526", "1383414554", "1329957756", "2476252142", "246754333", "2477083290", "2244340904", "3091902905", "2697847370", "3376411193", "2211174856", "1221931562", "2262119468", "842418386260922369", "13334762", "2809829401", "2216869699", "14182218", "756197344241127424", "1431204614", "877570089813454848", "740282661973950464", "2396594216", "19794115", "2884021535", "2353870874", "8496762", "2232729908", "2435734063", "1490943313", "3460030275", "2240969400", "357312062", "2290258379", "2740618784", "2783445143", "1125663272", "1572687990", "705812309495713797", "2521555771", "384457179", "253442629", "4491162742", "314533520", "308357575", "307605837", "2384348287", "782353732562452480", "1404222906", "574032254", "2317907780", "8371802", "776936941275246592", "2977110796", "581589763", "3438073289", "2279681898", "2799211554", "2800803747", "3183487161", "17577230", "700195467", "2434800834", "125304737", "852220046143365121", "2221699733", "495974881", "56249443", "2256561481", "1414582549", "2207129125", "43976252", "32461891", "618709104", "2481574266", "354764655", "1416245712", "1064700308"])
twitter_stream.filter(track=keywords)
