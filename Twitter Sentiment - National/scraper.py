import settings
import tweepy
# import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import pyodbc
import sys


#db = dataset.connect(settings.CONNECTION_STRING)
conn = pyodbc.connect('DSN=kubricksql')
cursor = conn.cursor()

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        description = unicode(status.user.description)
        loc = unicode(status.user.location)
        text = unicode(status.text)
        coords = status.coordinates
        geo = status.geo
        name = unicode(status.user.screen_name)
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        retweeted = status.retweeted
        lang = status.lang
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
        truncated = status.truncated
        favourites = status.user.favourites_count
        following = status.user.friends_count
        userid = status.user.id_str
        userscreenname = status.user.screen_name
        usertotaltweets = status.user.statuses_count

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        try:
            query = 'insert into twitter.stage1.tweets (tweetid, userdesc, userlocation, coordinates, tweettext, geo, username, usercreated, userfollowers, created, retweetcount, polarity, subjectivity, retweeted, lang, truncated, favourites, following, userid, userscreenname, usertotaltweets) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'\

            cursor.execute(query,id_str, description, loc, coords, text, geo, name, user_created, followers, created, retweets, polarity, subjectivity, retweeted, lang, truncated, favourites, following, userid, userscreenname, usertotaltweets)
            cursor.commit()

        except: #ProgrammingError as err:
            #print description
            #print loc
            #print(err)
            e = sys.exc_info() [1]
            print e
            #print 'oops'

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)