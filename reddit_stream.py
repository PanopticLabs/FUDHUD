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

def getCoins():
    #Get coinmarketcap data
    coins = {}
    coin_list = []
    coin_dict = {}
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=200'
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
        with open(os.path.join(script_dir, 'links.json')) as json_links:
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

                requests.post(panoptic_url+'subreddit', data={'name' : name, 'url' : subreddit, 'topic' : topic, 'token' : panoptic_token}).json()['data']

        #print(subreddits)
        for comment in reddit.subreddit(subreddits).stream.comments():
            #Get current date to check against the database and add to each row
            dt = time.strftime('%Y-%m-%d %H:%M:00', time.gmtime())

            comment_body = strip_non_ascii(comment.body)
            #print(comment_body)
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
                #print(sentiment)

                redditor = reddit.redditor(comment_author)

                userID = requests.post(panoptic_url+'user', data={'name' : comment_author, 'commentkarma' : str(redditor.comment_karma), 'linkkarma' : str(redditor.link_karma), 'token' : panoptic_token, 'data' : 'reddit'}).json()['data']
                #print(userID)
                requests.post(panoptic_url+'comment', data={'comment' : comment_unique, 'post' : comment_postUnique, 'parent' : comment_parentUnique, 'userid' : userID, 'unix' : comment_time, 'body' : comment_body, 'sentiment' : sentiment, 'token' : panoptic_token, 'data' : 'reddit'}).json()['data']

                topics = []
                for topic in coins['dict']:
                    if any(word in c.split() for word in coins['dict'][topic]):
                        #print(topic)
                        print('')
                        topics.append(topic)
                        #Post mention to api
                        requests.post(panoptic_url + 'mention', data={'datetime' : dt, 'topic' : topic, 'sentiment' : sentiment, 'token' : panoptic_token, 'data' : 'reddit'}).json()['data']

                #print('NOTIFYING!')
                commentObj = {'service' : 'redditstream', 'author' : comment_author, 'comment' : comment_body, 'post' : comment_postUnique, 'parent' : comment_parentUnique, 'link' : comment_link, 'topics' : topics}
                print(commentObj)
                notify_node(commentObj)
                #print('NOTIFIED!!')

    #except:
        #pass
    except BaseException as e:
        subject = 'Reddit Streamer MyListener Error'
        #mail.sendMail(subject, e)
        print("Error on_data: %s" % str(e))

while True:
    print('Starting Reddit Stream...')
    stream()
    time.sleep(60)
