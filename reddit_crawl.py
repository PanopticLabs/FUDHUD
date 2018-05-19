#!/usr/bin/env python
import sys, json, re, time, calendar, mysql.connector, requests, urllib, praw, mail
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
        subject = 'Reddit Crawler SQL Error'
        mail.sendMail(subject, e)
        return

def getCoins():
    #Get coinmarketcap data
    cryptos = []
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=100'
    response = urllib.urlopen(url)
    coinmarketcap = json.loads(response.read())
    for coin in coinmarketcap:
        symbol = coin['symbol'].lower()
        cryptos.append(symbol)
        #print(cryptos)

    return cryptos

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

def crawl():
    #Retrieve URLs from JSON#########################################################
    with open("links.json") as json_links:
        links = json.load(json_links)
        reddit_links = links["reddit"]
    #################################################################################
    keywords = getCoins()

    for word in keywords:
        if word in reddit_links:
            subreddits = reddit_links[word]
            i = 0
            while i < len(subreddits):
                subreddit = subreddits[i]
                name = subreddit[25:]
                #print(name)
                result = queryMySQL("SELECT subredditID FROM reddit_subreddits WHERE url=%s", (subreddit,))
                if len(result) == 0:
                    subredditID = queryMySQL("INSERT INTO reddit_subreddits(name,url,topic) VALUES (%s,%s,%s)", (name,subreddit,word))
                else:
                    for row in result:
                        subredditID = row['subredditID']
                        queryMySQL("UPDATE reddit_subreddits SET name=%s, url=%s WHERE subredditID=%s", (name, subreddit, subredditID))

                #json_about = getJSON(subreddit + "/about")
                s = reddit.subreddit(name)
                try:
                    #t0 = time.time() # now (in seconds)
                    dt = time.strftime('%Y-%m-%d %H:00:00', time.gmtime())
                    t0 = calendar.timegm(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
                    #time1 = time.strftime('%Y-%m-%d %H:00:00', time.gmtime(t1))
                    t1 = t0 - 60*60

                    #print("Time0: %s" % str(t0))
                    #print("Time1: %s" % str(t1))
                    active_accounts = s.accounts_active
                    subscribers = s.subscribers
                    #print("Subscribers: %s" % str(subscribers))
                    #print("Active accounts: %s" % str(active_accounts))

                    #json_new = getJSON(subreddit + "/new")
                    new_posts = 0
                    for post in s.new(limit=100):
                        if post.created_utc >= t0:
                            continue
                        elif post.created_utc < t1:
                            break
                        else:
                            new_posts += 1

                    #print("New Posts: %s" % str(new_posts))
                    result = queryMySQL("SELECT activityID FROM reddit_activity WHERE datetime=%s AND subredditID=%s", (dt, subredditID))
                    if len(result) == 0:
                        activityID = queryMySQL("INSERT INTO reddit_activity(subredditID, datetime, subscribers, activeAccounts, newPosts) VALUES (%s, %s, %s, %s, %s)", (subredditID, dt, subscribers, active_accounts, new_posts))
                    else:
                        for row in result:
                            activityID = row['activityID']

                        queryMySQL("UPDATE reddit_activity SET subscribers=%s, activeAccounts=%s, newPosts=%s WHERE activityID=%s", (subscribers, active_accounts, new_posts, activityID))

                    fp_sentiment = 0
                    fp_count = 0

                    #posts = json_posts["data"]["children"]
                    for post in s.hot(limit=100):
                        if post.stickied == False:
                            global comment_count
                            global avg_sentiment
                            comment_count = 0
                            avg_sentiment = 0
                            adjusted_sentiment = 0
                            op_weight = 10 #op_weight is set arbitrarily. It is the importance placed on the sentiment of the original post when calculating the adjusted_sentiment

                            post_unique = post.id
                            #print(post_unique)
                            post_url = "https://www.reddit.com" + post.permalink
                            #print(post_url)
                            result = queryMySQL("SELECT postID, postSentiment FROM reddit_posts WHERE postUnique=%s", (post_unique, ))
                            if len(result) == 0:
                                post_title = post.title
                                post_title = strip_non_ascii(post_title)
                                #print(post_title)
                                post_author = str(post.author)
                                #print(post_author)
                                post_time = post.created_utc
                                #print(post_time)
                                user_result = queryMySQL("SELECT userID FROM reddit_users WHERE name=%s", (post_author, ))
                                if len(user_result) == 0:
                                    post_userID = queryMySQL("INSERT INTO reddit_users(name) VALUES (%s)", (post_author, ))
                                else:
                                    for row in user_result:
                                        post_userID = row['userID']
                                if post.is_self == True:
                                    #print('Selftext')
                                    post_text = post.selftext
                                    post_text = strip_non_ascii(post_text)
                                    analysis = tb(post_text)
                                    text_sentiment = analysis.sentiment.polarity
                                    analysis = tb(post_title)
                                    title_sentiment = analysis.sentiment.polarity

                                    post_sentiment = float(text_sentiment) + float(title_sentiment) / 2
                                    #print('Post Sentiment: %s' % str(post_sentiment))

                                else:
                                    #print('Link')
                                    post_text = post.url
                                    analysis = tb(post_title)
                                    post_sentiment = analysis.sentiment.polarity
                                    #print('Post Sentiment: %s' % str(post_sentiment))

                                #print(post_text)

                                post_id = queryMySQL("INSERT INTO reddit_posts(postUnique,subredditID, userID, unix, title, content, postSentiment) VALUES(%s, %s, %s, %s, %s, %s, %s)", (post_unique, subredditID, post_userID, post_time, post_title, post_text, post_sentiment))
                            else:
                                for row in result:
                                    post_id = row['postID']
                                    post_sentiment = row['postSentiment']

                            post_comments = post.num_comments
                            #print(post_comments)
                            post_score = post.score
                            #print(post_score)
                            post_ups = post.ups
                            #print(post_ups)
                            post_downs = post.downs
                            #print(post_downs)
                            post_crossposts = post.num_crossposts
                            #print(post_crossposts)
                            #print('')

                            queryMySQL("UPDATE reddit_posts SET comments=%s, score=%s, ups=%s, downs=%s, crossposts=%s, postSentiment=%s WHERE postID=%s", (post_comments, post_score, post_ups, post_downs, post_crossposts, post_sentiment, post_id))

                            total_sentiment = float(fp_sentiment) * fp_count
                            total_sentiment = float(total_sentiment) + float(post_sentiment)
                            fp_count += 1
                            fp_sentiment = float(total_sentiment) / fp_count


                    queryMySQL("UPDATE reddit_activity SET frontpageSentiment=%s WHERE activityID=%s", (fp_sentiment, activityID))

                except Exception as e:
                    subject = 'Reddit Post Crawler Error'
                    mail.sendMail(subject, e)
                    continue

                i += 1

        else:
            with open("links.json") as json_links:
                links = json.load(json_links)
                links['reddit'][word] = []

            jsonFile = open("links.json", "w+")
            jsonFile.write(json.dumps(links))
            jsonFile.close()

def crawlComments(comments, postID, parentID):
    global avg_sentiment
    global comment_count
    comment_postUnique = postID
    comment_parentUnique = parentID
    #print('Start Comment Crawler...')
    for comment in comments(limit=100):
        #print(dir(comment))
        replies = ""
        try:
            comment_unique = comment.id
            comment_body = comment.body
            #comment_body = comment_body.decode('utf-8')
            comment_body = strip_non_ascii(comment_body)
            #print('Body: %s' % comment_body)
            comment_author = comment.author
            comment_author = str(comment.author)
            comment_time = comment.created_utc
            comment_score = comment.score
            comment_ups = comment.ups
            comment_downs = comment.downs
            comment_controversiality = comment.controversiality
            #comment_depth = comment.depth

            analysis = tb(comment_body)
            sentiment = analysis.sentiment.polarity

            result = queryMySQL("SELECT commentID FROM reddit_comments WHERE commentUnique=%s", (comment_unique, ))
            if(len(result) == 0):
                #print("Post ID: %s" % str(comment_postID))
                #print("Parent ID: %s" % str(comment_parentID))
                user_result = queryMySQL("SELECT userID FROM reddit_users WHERE name=%s", (comment_author, ))
                if len(user_result) == 0:
                    comment_userID = queryMySQL("INSERT INTO reddit_users(name) VALUES (%s)", (comment_author, ))
                else:
                    for row in user_result:
                        comment_userID = row['userID']

                comment_id = queryMySQL("INSERT INTO reddit_comments(commentUnique, postID, parentUnique, userUnique, unix, body, sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s)", (comment_unique, comment_postUnique, comment_parentUnique, comment_userID, comment_time, comment_body, sentiment ))

            else:
                for row in result:
                    comment_id = row['commentID']

            queryMySQL("UPDATE reddit_comments SET score=%s, ups=%s, downs=%s, controversiality=%s WHERE commentID=%s", (comment_score, comment_ups, comment_downs, comment_controversiality, comment_id))
            comment_count = int(comment_count)
            total_sentiment = float(avg_sentiment) * comment_count
            total_sentiment = float(total_sentiment) + float(sentiment)
            comment_count += 1
            avg_sentiment = float(total_sentiment) / comment_count

            replies = comment.replies

            #print(comment_body)
            #print('Comment Sentiment: %s' % str(sentiment))
            #print('Avg Sentiment: %s' % str(avg_sentiment))
            #print('Count: %s' % str(comment_count))
            #print('')
            #print('')

        except Exception as e:
            subject = 'Reddit Comment Crawler Error'
            mail.sendMail(subject, e)
            continue

        if len(replies) != 0:
            crawlComments(replies, comment_postUnique, comment_unique)




#while True:
#    print('Crawling Reddit...')
#    crawl()
#    time.sleep(900)
crawl()
