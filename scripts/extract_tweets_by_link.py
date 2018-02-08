#  Script for extracting tweets by link
#  To run this script run `python scripts/extract_tweets_by_link.py -days=1` from the project root folder
import sys
sys.path.append('./common')

from twitter import TwitterAPI
from utils import get_last_day, check_data_directory

reload(sys)  # Reload for update the encoding
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
   print('Starting script - Extracting tweets by link\n')
   #  Opens a connection object with the Twitter API
   api = TwitterAPI()

   #  Get the last day for extraction
   selected_day = get_last_day();

   date_key = selected_day.date().strftime("%Y-%m-%d")

   check_data_directory();

   try:
      with open('./data/extracted-links-' + date_key + '.txt') as f:
         links = f.readlines()
   except BaseException as e:
      print("Error on_data: %s" % str(e))

   links = [link.strip() for link in links]

   tweets = api.get_linked_tweets(links)

   try:
      with open('./data/extracted-linked-tweets-' + date_key + '.txt', 'w') as f:
         for tweet in tweets:
            if (tweet and len(tweet) > 0):
               f.write(tweet + '\n')
   except BaseException as e:
      print("Error on_data: %s" % str(e))

   print('\nFinished script - Extracting tweets by link')
