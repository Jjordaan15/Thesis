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
        filename = open('stream' + str(i) + '.txt', 'r')
        t = filename.readlines()
        Handles = []
        for t in t:
            t = t.replace('\n', '')
            Handles.append(t)
        filename.close()

        for name in Handles:

            print("Twitter Handle: @" + name)


            try:
                user = api.get_user(screen_name=name)
                if not user.following:
                    api.create_friendship(screen_name=name)
                    print("Following @" +name )

                    # this creates a break inbetween searches to make the following look more human
                    TimeWait = random.randint(300, 1500)
                    time.sleep(TimeWait)
                else:
                    print("already following @" + name)

            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(5)

        next_num = int(i) + 1
        print(str(next_num) + "end")
        filename = open('num1.txt', 'w')
        filename.write(str(next_num))
        filename.close()
        os.remove('stream' + str(i) + '.txt')

    except:
        print("Waiting")
        time.sleep(300)

