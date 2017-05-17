import pymongo
import json
import tweepy
from textblob import TextBlob
import urllib2
from pprint import pprint


class My_MongoDB(object):
    ## Adds polarity to tweets that are already stored in MongoDB
    ## Not finished yet but won't need it anyway
    def __init__(self,database, collection):
        self.database = database
        self.collection = collection


    def connect_to_mongo(self):
        connection = pymongo.MongoClient()
        db = connection.self.database
        coll = db.self.collection
        return coll

    def add_polarity(self,collection):
        cursor = collection.find()
        tweets = json_normalize(list(cursor))
        tweets['polarity'] = ''
        for i in range(0, len(tweets['text'])):
            blob = TextBlob(tweets['text'][i])
            p = blob.polarity
            tweets['polarity'][i] = p


class MyListener(tweepy.StreamListener):
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self,status):
        try:
            connection = pymongo.MongoClient()
            db = connection.tweetsdb
            coll = db.tweets
            tweet = json.loads(status)
            
            blob = TextBlob(tweet['text'])
            polarity = blob.polarity
            subjectivity = blob.subjectivity
            tweet['Polarity'] = polarity
            tweet['Subjectivity'] = subjectivity

            coll.insert(tweet)


        except:
            print 'error!!'



TWITTER_KEY = '3156604010-jvQbB0JY4qWWiHcA1CymT1yimkzIHupm63ffA2j'
TWITTER_SECRET = 'i5CNIq3eTrAgn5x7i7hIapk6ghyfx2isNUSToAcFKipFL'
TWITTER_APP_KEY =  'qFna9qwaUFSR4H4LZqwmSGP9y'
TWITTER_APP_SECRET =  'NPRAFA0ipfHvVJztoE66uDt5dzPYcXSK9fVdabxDIA6lZbuvhH'

TRACK_TERMS = ['Corbyn','Theresa May','Labour','Conservatives','Tories', 'Lib Dems', 'Tim Farron','GeneralElection','Liberal Democrats']


auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

ML = MyListener()
stream = tweepy.Stream(auth=api.auth, listener=ML)
stream.filter(track=TRACK_TERMS)