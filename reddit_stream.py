#!/usr/bin/env python
import sys, json, re, time, calendar, mysql.connector, requests, urllib, praw
from textblob import TextBlob as tb
from datetime import date, timedelta

#################################################################################
#Setup MySQL connection##########################################################
#################################################################################
with open('cred.json') as json_cred:
    cred = json.load(json_cred)

mysql_user = cred["mysql_user"]
mysql_pass = cred["mysql_pass"]
mysql_host = cred["mysql_host"]
mysql_db = 'panoptic_fudhud'

connection = mysql.connector.connect(user=mysql_user, password=mysql_pass,
                              host=mysql_host,
                              database=mysql_db,
                              use_unicode=True,
                              charset="utf8")
#################################################################################
#Setup Reddit connection##########################################################
#################################################################################
reddit_useragent = cred["reddit_useragent"]
reddit_id = cred["reddit_id"]
reddit_secret = cred["reddit_secret"]
#reddit_user = cred["reddit_user"]
#reddit_pass = cred["reddit_pass"]

reddit = praw.Reddit(user_agent=reddit_useragent,
                 client_id=reddit_id, client_secret=reddit_secret)
#################################################################################
#################################################################################
#################################################################################

avg_sentiment = 0
comment_count = 0

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
        symbol = coin['symbol'].lower()
        topic = '$' + symbol
        #Check that symbol does not use an ambiguous word
        shitlist = ['pay', 'sub', 'part', 'fun']
        if symbol in shitlist:
            coin_list.append(name)
            coin_dict[symbol] = [name]
        else:
            coin_list.append(name)
            coin_list.append(symbol)
            coin_dict[symbol] = [name, symbol]
        #print(cryptos)

    coins['list'] = coin_list
    coins['dict'] = coin_dict
    return coins

def getJSON(url):
    time.sleep(2)
    response = requests.get(url, headers = {'User-agent': 'FUDHUD Crawler 0.1'})
    #print(response.headers)
    #print(response.headers['X-Ratelimit-Remaining'])
    #print(response.headers['X-Ratelimit-Reset'])
    return response.json()

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    newstring = ''.join(stripped)
    newstring = newstring[:4995] + (newstring[4995:] and '...')
    return newstring

def notify_node(array):
    data = json.dumps(array)
    url = 'https://fierce-forest-58606.herokuapp.com/'
    headers = {'Content-Type': 'application/json', 'Content-Length' : str(len(data))}
    res = requests.post(url, data=data, headers=headers)

def stream():
    try:
        #Retrieve URLs from JSON#########################################################
        with open("links.json") as json_links:
            links = json.load(json_links)
            reddit_links = links["reddit"]
        #################################################################################
        coins = getCoins()
        subreddits = ''
        for topic in reddit_links:
            #print(topic)
            for subreddit in reddit_links[topic]:
                #print(subreddit)
                name = subreddit[25:]
                if(subreddits == ''):
                    subreddits = name
                else:
                    subreddits = subreddits + '+' + name

                result = queryMySQL("SELECT subredditID FROM reddit_subreddits WHERE url=%s", (subreddit,))
                if len(result) == 0:
                    subredditID = queryMySQL("INSERT INTO reddit_subreddits(name,url,topic) VALUES (%s,%s,%s)", (name,subreddit,topic))
                else:
                    for row in result:
                        subredditID = row['subredditID']
                        queryMySQL("UPDATE reddit_subreddits SET name=%s, url=%s WHERE subredditID=%s", (name, subreddit, subredditID))

        #print(subreddits)
        for comment in reddit.subreddit(subreddits).stream.comments():
            #Get current date to check against the database and add to each row
            dt = time.strftime('%Y-%m-%d %H:%M:00')

            comment_body = strip_non_ascii(comment.body)
            print(comment_body)
            #print(dir(comment))
            c = comment_body.lower()
            if any(word in c.split() for word in coins['list']):
                comment_author = str(comment.author)
                comment_unique = comment.id
                comment_postUnique = comment.submission.id
                comment_parentUnique = comment.parent_id
                comment_time = comment.created_utc
                comment_link = 'https://www.reddit.com' + comment.permalink

                analysis = tb(comment_body)
                sentiment = analysis.sentiment.polarity
                print(sentiment)
                print('')

                user_result = queryMySQL("SELECT userID FROM reddit_users WHERE name=%s", (comment_author, ))
                if len(user_result) == 0:
                    comment_userID = queryMySQL("INSERT INTO reddit_users(name, comments) VALUES (%s, %s)", (comment_author, 1))
                else:
                    for row in user_result:
                        comment_userID = row['userID']
                        queryMySQL("UPDATE reddit_users SET comments=comments+1 WHERE userID=%s",(comment_userID, ))

                comment_id = queryMySQL("INSERT INTO reddit_comments(commentUnique, postUnique, parentUnique, userID, unix, body, sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s)", (comment_unique, comment_postUnique, comment_parentUnique, comment_userID, comment_time, comment_body, sentiment ))

                topics = []
                for topic in coins['dict']:
                    if any(word in c.split() for word in coins['dict'][topic]):
                        print(topic)
                        topics.append(topic)
                        result = queryMySQL("SELECT mentionID FROM reddit_mentions WHERE date=%s AND topic=%s", (dt, topic))
                        if len(result) == 0:
                            mentionID = queryMySQL("INSERT INTO reddit_mentions (date, topic, mentions, sentiment) VALUES (%s, %s, %s, %s)", (dt, topic, 1, sentiment))
                        else:
                            for row in result:
                                mentionID = row['mentionID']

                                result = queryMySQL("SELECT * FROM reddit_mentions WHERE mentionID=%s", (mentionID, ))
                                for row in result:
                                    wordcount = row['mentions']
                                    totalSentiment = float(row['sentiment']) * wordcount
                                    totalSentiment = totalSentiment + sentiment
                                    wordcount += 1
                                    newSentiment = totalSentiment / wordcount

                                    queryMySQL("UPDATE reddit_mentions SET mentions=%s, sentiment=%s WHERE mentionID=%s", (wordcount, newSentiment, mentionID))

                print('NOTIFYING!')
                commentObj = {'service' : 'redditstream', 'author' : comment_author, 'comment' : comment_body, 'post' : comment_postUnique, 'parent' : comment_parentUnique, 'link' : comment_link, 'topics' : topics}
                print(commentObj)
                notify_node(commentObj)
                print('NOTIFIED!!')

    #except:
        #pass
    except BaseException as e:
        print("Error on_data: %s" % str(e))

while True:
    print('Starting Reddit Stream...')
    stream()
    time.sleep(60)
