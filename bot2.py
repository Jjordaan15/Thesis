import tweepy, time, sys
import random
import json 
import os
import argparse
from urllib3.exceptions import ProtocolError
import shapely.geometry
from tweepy import Stream
from tweepy.streaming import StreamListener

from secrets import *

#========================================================================================

filename=open('Common.txt','r')
t=filename.readlines()
trending_words = []
for t in t:
    t = t.replace('\n','')
    trending_words.append(t)
filename.close()
print(trending_words)

print('#========================================================================================')

#========================================================================================

with open('zaf.json') as f: # https://github.com/datasets/geo-countries/
    gj = json.load(f)

bbox = shapely.geometry.shape(gj).buffer(0.025)

#========================================================================================

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

 #Construct the API instance
api = tweepy.API(auth) # create an API object

geo_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
geo_auth.set_access_token(access_token, access_secret)
geo_api = tweepy.API(geo_auth)

#========================================================================================
 
class MyListener(StreamListener):

    def __init__(self):
        self.__run_time__ = time.monotonic()

        self.__trend_stream__ = None
        super().__init__()

    def on_status(self, status):
        if self.is_geolocal(status):
            filename = open('num.txt', 'r')
            num = filename.readlines()
            filename.close()
            num = num[0]
            print(num + "  Start")

            with open('stream'+ num +'.txt', 'a') as f:
                f.write(status.user.screen_name + "\n")
                print(status)
                if self.__run_time__ + 300 < time.monotonic():
                    self.__run_time__ = time.monotonic()
                    next_num = int(num) + 1
                    print(str(next_num) + "end")
                    filename = open('num.txt', 'w')
                    filename.write(str(next_num))
                    filename.close()

            with open('streamid'+ num +'.txt', 'a') as f:
                f.write(str(status.id) + "\n")
                print(status)


    def is_geolocal(self, status):
        if status.place:
            pb = shapely.geometry.shape({'type': status.place.bounding_box.type, 'coordinates': status.place.bounding_box.coordinates})
            if bbox.contains(pb.centroid): return True
        if status.coordinates:
            if bbox.contains(shapely.geometry.shape(status.coordinates)): return True

        return False

    def on_error(self, status):
        print(status)
        return True

    def on_exception(self, exception):
        print(exception)
        return True


while True:
    try:
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=trending_words)

    except (ProtocolError, AttributeError):
        continue