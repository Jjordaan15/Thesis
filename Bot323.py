import tweepy, time, sys
import random
import json 
import os
import argparse
from tweepy import Stream
from tweepy.streaming import StreamListener


from secrets import *
from Write import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

 #Construct the API instance
api = tweepy.API(auth) # create an API object

while True:

    filename = open('num1.txt', 'r')
    num = filename.readlines()
    filename.close()
    i = num[0]
    print(i + "  Start")

    try:
        filename = open('streamid' + str(i) + '.txt', 'r')
        t = filename.readlines()
        ids = []
        for t in t:
            t = t.replace('\n', '')
            ids.append(t)
        filename.close()

        for tweet_id in ids:

            print("Status ID: " + tweet_id)


            try:
                user = api.get_status(id=tweet_id)
                user.favorite()
                print("Tweet favorited")

                # this creates a break inbetween searches to make the following look more human
                TimeWait = random.randint(300, 1500)
                time.sleep(TimeWait)

            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(5)

        next_num = int(i) + 1
        print(str(next_num) + "end")
        filename = open('num1.txt', 'w')
        filename.write(str(next_num))
        filename.close()
        os.remove('streamid' + str(i) + '.txt')

    except:
        print("Waiting")
        time.sleep(300)

