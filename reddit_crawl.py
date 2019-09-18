#!/usr/bin/env python
import os, sys, json, re, time, calendar, requests, urllib, praw, mail
from textblob import TextBlob as tb
from datetime import date, timedelta

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

##################################################################################
#Setup Reddit connection##########################################################
##################################################################################
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
    with open(os.path.join(script_dir, 'links.json')) as json_links:
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
                subredditID = requests.post(panoptic_url+'subreddit', data={'name' : name, 'url' : subreddit, 'topic' : word, 'token' : panoptic_token}).json()['data']
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
                    activityID = requests.post(panoptic_url+'activity', data={'subredditid' : subredditID, 'datetime' : dt, 'subscribers' : subscribers, 'activeaccounts' : active_accounts, 'newposts' : new_posts, 'data' : 'reddit', 'token' : panoptic_token}).json()['data']
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
                            result = getJSON(panoptic_url + 'post?data=reddit&post=' + post_unique)['data']
                            print(result)
                            if not result:
                                post_title = post.title
                                post_title = strip_non_ascii(post_title)
                                #print(post_title)
                                post_author = str(post.author)
                                #print(post_author)
                                post_time = post.created_utc
                                #print(post_time)
                                post_userID = requests.post(panoptic_url+'user', data={'name' : post_author, 'token' : panoptic_token, 'data' : 'reddit'}).json()['data']

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
                                post_id = requests.post(panoptic_url + 'post', data={'post' : post_unique, 'subredditid' : subredditID, 'userid' : post_userID, 'unix' : post_time, 'title' : post_title, 'content' : post_text, 'sentiment' : post_sentiment, 'data' : 'reddit', 'token' : panoptic_token}).json()['data']

                            else:
                                post_id = result['postID']
                                post_sentiment = result['postSentiment']

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

                            requests.put(panoptic_url + 'post', data={'postid' : post_id, 'comments' : post_comments, 'score' : post_score, 'ups' : post_ups, 'downs' : post_downs, 'crossposts' : post_crossposts, 'data' : 'reddit', 'token' : panoptic_token})

                            total_sentiment = float(fp_sentiment) * fp_count
                            total_sentiment = float(total_sentiment) + float(post_sentiment)
                            fp_count += 1
                            fp_sentiment = float(total_sentiment) / fp_count

                    requests.put(panoptic_url+'activity', data={'sentiment' : fp_sentiment, 'activityid' : activityID, 'data' : 'reddit', 'token' : panoptic_token})

                except Exception as e:
                    subject = 'Reddit Post Crawler Error'
                    #mail.sendMail(subject, e)
                    print(e)
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

            result = getJSON(panoptic_url + 'comment?data=reddit&comment=' + comment_unique)['data']

            if not result:
                #print("Post ID: %s" % str(comment_postID))
                #print("Parent ID: %s" % str(comment_parentID))
                comment_userID = requests.post(panoptic_url+'user', data={'name' : comment_author, 'token' : panoptic_token, 'data' : 'reddit'}).json()['data']
                comment_id = requests.post(panoptic_url+'comment', data={'comment' : comment_unique, 'post' : comment_postUnique, 'parent' : comment_parentUnique, 'userid' : comment_userID, 'unix' : comment_time, 'body' : comment_body, 'sentiment' : sentiment, 'token' : panoptic_token, 'data' : 'reddit'}).json()['data']
            else:
                comment_id = result['commentID']

            requests.put(panoptic_url+'comment', data={'commentID' : comment_id, 'score' : comment_score, 'ups' : comment_ups, 'downs' : comment_downs, 'controversiality' : comment_controversiality, 'token' : panoptic_token, 'data' : 'reddit'})
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
            #mail.sendMail(subject, e)
            print(e)
            continue

        if len(replies) != 0:
            crawlComments(replies, comment_postUnique, comment_unique)




#while True:
#    print('Crawling Reddit...')
#    crawl()
#    time.sleep(900)
crawl()
