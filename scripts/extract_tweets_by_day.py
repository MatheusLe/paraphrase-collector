#  Script for extracting tweets by day
#  To run this script run `python scripts/extract_tweets_by_day.py -days=2` from the project root folder
import sys
sys.path.append('./common')

from twitter import TwitterAPI
from utils import get_last_day, check_data_directory

reload(sys)  # Reload for update the encoding
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
   print('Starting script - Extracting tweets by day\n')
   #  Opens a connection object with the Twitter API
   api = TwitterAPI()

   #  Get selected users for the tweets extraction
   users = api.get_users()

   #  Get the last day for extraction
   last_day = get_last_day();

   #  Retrieves the tweets from the users between today and the last day to the past
   daily_tweets = api.get_tweets_by_day(users, last_day)

   check_data_directory();

   for key, day_tweets in daily_tweets.iteritems():
      try:
         with open('./data/extracted-tweets-' + key + '.txt', 'w') as f:
            for tweet in day_tweets['texts']:
               if (tweet and len(tweet) > 0):
                  f.write(tweet + '\n')
      except BaseException as e:
         print("Error on_data: %s" % str(e))

   print('\nFinished script - Extracting tweets by day')
