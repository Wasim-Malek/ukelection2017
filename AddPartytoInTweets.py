import os
import sys
from tweepy import API
from tweepy import OAuthHandler
import string
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
import tweepy
import pymongo
import json
import tweepy
from textblob import TextBlob
import urllib2
from pprint import pprint

TRACK_TERMS = ['conservatives', 'theresa may', 'conservative party', 'theresamay', 'tories', 'tory', 'conservativeparty', 'theresa_may','#votetory', '#toriesout','#VoteConservative',
               'labour party', 'jeremy corbyn', 'jeremycorbyn','labour manifesto', 'labour', 'labourparty', 'corbyn', '@uklabour', '#jc4pm', '#corbyn4pm', '#forthemany', '#strongandstable','#Votelabour',
               'nicola sturgeon', 'nicolasturgeon', 'scottishnationalparty', 'scottish national party', 'snp','#VoteSNP',
               'tim farron', 'timfarron','lib dem manifesto', 'liberal democrats', 'liberaldemocrats', 'libdems', 'libdem','#Votelibdem','#Votelibdems',
               'arlene foster', 'arlenefoster', 'democratic unionist party', 'democraticunionistparty', 'dup', 'DUPleader','#VoteDUP',
               'gerry adams', 'gerryadams', 'sinn fein', 'sinnfein', 'GerryAdamsSF','VoteSF','#VoteSinnFein',
               'leanne wood', 'leannewood', 'plaid cymru', 'plaid', 'plaidcymru','#VotePlaid',
               'Colum Eastwood', 'ColumEastwood', 'Social Democratic and Labour Party', 'SocialDemocraticandLabourParty', 'sdlp','#VoteSDLP',
               'Robin Swann', 'RobinSwann', 'Ulster Unionist Party', 'UlsterUnionistParty', 'uup', 'robinswannuup','#VoteUUP',
               'Caroline Lucas', 'CarolineLucas', 'Jonathan Bartley','JonathanBartley', 'Green Party', 'GreenParty', 'jon_bartley','#VoteGreen2017','#VoteGreen',
               'Paul Nuttall', 'PaulNuttall', 'UK Independence Party', 'UKIndependenceParty', 'UKIP', 'paulnuttallukip','#VoteUKIP']



def get_twitter_auth():
    """Setup Twitter authentication"""

    try:
        TWITTER_KEY = '3156604010-jvQbB0JY4qWWiHcA1CymT1yimkzIHupm63ffA2j'
        TWITTER_SECRET = 'i5CNIq3eTrAgn5x7i7hIapk6ghyfx2isNUSToAcFKipFL'
        TWITTER_APP_KEY = 'qFna9qwaUFSR4H4LZqwmSGP9y'
        TWITTER_APP_SECRET = 'NPRAFA0ipfHvVJztoE66uDt5dzPYcXSK9fVdabxDIA6lZbuvhH'
    except KeyError:
        sys.stderr.write('Error with authentication keys')
        sys.exit(1)
    auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
    auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

    return auth

def get_twitter_client():
    """Setup Twitter API client.
    Return: tweepy.API object"""

    auth = get_twitter_auth()
    client = API(auth)

    return client

class CustomListener(StreamListener):
    """Custom StreamListener for streaming Twitter Data"""
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")



    def on_data(self, status):
        try:
            connection = pymongo.MongoClient()
            db = connection.tweetsdb
            coll = db.nationaltweets
            tweet = json.loads(status)

            blob = TextBlob(tweet['text'])
            polarity = blob.polarity
            subjectivity = blob.subjectivity
            tweet['Polarity'] = polarity
            tweet['Subjectivity'] = subjectivity

            def Party_Seperator(tweet):
                '''Adds an extra field for the party which the tweet was about

                Returns the tweet with an extra field with the list of mentioned parties'''
                result = list()

                # TRACK TERMS FOR EACH PARTY
                Partys = ['labour', 'Conservative', 'libDem', 'Ukip', 'Green', 'SNP']
                Labour = ['labour party', 'jeremy corbyn', 'jeremycorbyn','labour manifesto', 'labour', 'labourparty', 'corbyn',
                          '@uklabour',
                          '#jc4pm', '#corbyn4pm', '#forthemany', '#strongandstable', '#Votelabour']
                Conservative = ['conservatives', 'theresa may', 'conservative party', 'theresamay', 'tories',
                                'tory',
                                'conservativeparty', 'theresa_may', '#votetory', '#toriesout', '#VoteConservative']
                LibDem = ['tim farron', 'timfarron','lib dem manifesto', 'liberal', 'democrats', 'liberaldemocrats', 'libdems', 'libdem',
                          '#Votelibdem', '#Votelibdems']
                Ukip = ['Paul', 'Nuttall', 'PaulNuttall', 'UK Independence Party', 'UKIndependenceParty', 'UKIP',
                        'paulnuttallukip', '#VoteUKIP']
                Green = ['Caroline Lucas', 'CarolineLucas', 'Jonathan Bartley', 'JonathanBartley', 'Green Party',

                         'GreenParty', 'jon_bartley', '#VoteGreen2017', '#VoteGreen']
                SNP = ['nicola sturgeon', 'nicolasturgeon', 'scottishnationalparty', 'scottish national party',
                       'snp',
                       '#VoteSNP']
                Party_track_terms = [Labour, Conservative, LibDem, Ukip, Green, SNP]

                Tweet_Contents = tweet['text'].split(' ')

                total = range(0, len(Party_track_terms))

                for i in total:
                    if (len(filter(lambda x: x.lower() in [x.lower() for x in Party_track_terms[i]],
                                   Tweet_Contents)) > 0):
                        result.append(Partys[i])

                def unique_list(seq):
                    '''makes list unique by removing duplicates'''
                    checked = []
                    for e in seq:
                        if e not in checked:
                            checked.append(e)
                    return checked

                tweet['Party'] = ','.join(unique_list(result))

                return tweet

            tweet = Party_Seperator(tweet)

            coll.insert(tweet)
        except  BaseException as e:
            sys.stderr.write('Error on data')
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write('Rate limit exceeded')
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True



if __name__ == '__main__':
    auth = get_twitter_auth()
    twitter_stream = Stream(auth, CustomListener())
    twitter_stream.filter(track=TRACK_TERMS)





