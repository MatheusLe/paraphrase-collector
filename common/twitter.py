__author__ = 'Matheus Leal'
__version__ = '1.0'
import tweepy
from tweepy import OAuthHandler
from utils import pre_process_text

USER_LIMIT = 10
TWEETS_BY_USER_LIMIT = 3000
consumer_key = 'uWSy8nx0CMLn47XhSS4E7Mf2A'
consumer_secret = 'busJy9IRWorNeRM4UnVmCLIKUdeTV06XGNlqPjcXCoNYBGUo3I'
access_token = '961434682960371713-pcWDFXULa73SOuqgUZmYdmANFAKxbGP'
access_secret = 'wjKf1rYEIBC7ztaNgvjwhsytJuTldNcSs9qjr90J4lPRm'

#  Handles Twitter API limit rates
def limit_handled(cursor):
   while True:
      try:
         yield cursor.next()
      except tweepy.RateLimitError:
         print('Rate Limit Error for Twitter API')
         time.sleep(15 * 60)

class TwitterAPI(object):
   def __init__(self):
      #  Authenticates with the Twitter API
      auth = OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_secret)
      self.api = tweepy.API(auth)

   # Get users linked to the application account
   def get_users(self):
      users = []
      for friend in tweepy.Cursor(self.api.friends).items(USER_LIMIT):
         print(' - Selected user: ' + friend.name)
         user = {}
         user['id'] = friend.id
         user['name'] = friend.name
         users.append(user)
      return users

   #  Retrieve all tweets by list of users between now and the last day to the past
   def get_tweets_by_day(self, users, last_day):
      daily_tweets = {};
      try:
         for user in users:
            n_tweets_by_user = 0
            for status in limit_handled(tweepy.Cursor(self.api.user_timeline, user_id=user['id']).items()):
               if (status.lang != 'pt'):
                  continue
               n_tweets_by_user += 1
               if (n_tweets_by_user > TWEETS_BY_USER_LIMIT):
                  print(' - Reached tweets by user limit: ' + user['name'] + ' with ' + str(n_tweets_by_user) + ' tweets')
                  break
               if (status.created_at.date() < last_day.date()):
                  print(' - Reached date limit: ' + user['name'] + ' with ' + str(n_tweets_by_user) + ' tweets')
                  break

               date_string = status.created_at.date().strftime("%Y-%m-%d")
               if (not date_string in daily_tweets):
                  daily_tweets[date_string] = {}
                  daily_tweets[date_string]['texts'] = set()
                  daily_tweets[date_string]['links'] = set()

               tweet = {}
               daily_tweets[date_string]['texts'].add(pre_process_text(status.text))
               daily_tweets[date_string]['links'].add(status.entities['urls'][0]['expanded_url'] if status.entities and status.entities['urls'] else None)
      except BaseException as e:
         print('Error while getting tweets by day: %s' % str(e))
      return daily_tweets

   def get_linked_tweets(self, urls):
      linked_tweets = set()
      try:
         for url in urls:
            print('Searching for url', url)
            search_string = url + ' +exclude:retweets'
            for status in limit_handled(tweepy.Cursor(self.api.search, q=search_string).items()):
               if (status.lang != 'pt'):
                  continue
               linked_tweets.add(pre_process_text(status.text))
      except BaseException as e:
         print('Error while getting linked tweets: %s' % str(e))

      return linked_tweets
