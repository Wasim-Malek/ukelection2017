import pymongo
import json
import tweepy
from textblob import TextBlob
import urllib2
from pprint import pprint


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

    def on_data(self, status):
        try:
            connection = pymongo.MongoClient()
            db = connection.twitter_db
            coll = db.twitter_collection_national
            tweet = json.loads(status)

            blob = TextBlob(tweet['text'])
            polarity = blob.polarity
            subjectivity = blob.subjectivity
            tweet['Polarity'] = polarity
            tweet['Subjectivity'] = subjectivity

            coll.insert(tweet)


        except:
            print 'error!!'


TWITTER_KEY = ''
TWITTER_SECRET = ''
TWITTER_APP_KEY = ''
TWITTER_APP_SECRET = ''

TRACK_TERMS = ['conservatives', 'theresa may', 'conservative party', 'theresamay', 'tories', 'tory', 'conservativeparty', 'theresa_may',
               'labour party', 'jeremy corbyn', 'jeremycorbyn', 'labour', 'labourparty', 'corbyn',
               'nicola sturgeon', 'nicolasturgeon', 'scottishnationalparty', 'scottish national party', 'snp',
               'tim farron', 'timfarron', 'liberal democrats', 'liberaldemocrats', 'libdems', 'libdem',
               'arlene foster', 'arlenefoster', 'democratic unionist party', 'democraticunionistparty', 'dup', 'DUPleader',
               'gerry adams', 'gerryadams', 'sinn fein', 'sinnfein', 'GerryAdamsSF',
               'leanne wood', 'leannewood', 'plaid cymru', 'plaid', 'plaidcymru',
               'Colum Eastwood', 'ColumEastwood', 'Social Democratic and Labour Party', 'SocialDemocraticandLabourParty', 'sdlp',
               'Robin Swann', 'RobinSwann', 'Ulster Unionist Party', 'UlsterUnionistParty', 'uup', 'robinswannuup',
               'Caroline Lucas', 'CarolineLucas', 'Jonathan Bartley','JonathanBartley', 'Green Party', 'GreenParty', 'jon_bartley',
               'Paul Nuttall', 'PaulNuttall', 'UK Independence Party', 'UKIndependenceParty', 'UKIP', 'paulnuttallukip', 'toriesout']

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

ML = MyListener()
stream = tweepy.Stream(auth=api.auth, listener=ML)
stream.filter(track=TRACK_TERMS)