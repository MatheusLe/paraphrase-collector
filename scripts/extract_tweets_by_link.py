#  Script for extracting tweets by link
#  To run this script run `python scripts/extract_tweets_by_link.py -days=1` from the project root folder
__author__ = 'Matheus Leal'
__version__ = '1.0'
import sys
sys.path.append('./common')

from twitter import TwitterAPI
from utils import get_last_day, check_data_directory, get_run_key

reload(sys)  # Reload for update the encoding
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
   old_stdout = sys.stdout
   check_data_directory('./logs');
   log_file = open("./logs/log_extract_tweets_by_link_" + get_run_key() + ".log ","w")
   sys.stdout = log_file
   print('Starting script - Extracting tweets by link\n')
   #  Opens a connection object with the Twitter API
   api = TwitterAPI()

   #  Get the last day for extraction
   selected_day = get_last_day();

   date_key = selected_day.date().strftime("%Y-%m-%d")

   check_data_directory('./data');

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
   sys.stdout = old_stdout
   log_file.close()
