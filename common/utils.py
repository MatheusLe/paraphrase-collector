#utils.py
from datetime import datetime, timedelta
import argparse
import os, errno
import re
import HTMLParser

#  Set the last day from
def get_last_day():
    parser = argparse.ArgumentParser()
    parser.add_argument('-days', type=int, default=0)
    args = parser.parse_args()
    last_retrieval_day = datetime.today() - timedelta(days=args.days)
    return last_retrieval_day

def check_data_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def get_run_key():
   return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

def pre_process_text(text):
   text = HTMLParser.HTMLParser().unescape(text)
   text = text.replace('\n', ' ')
   return re.sub(r"http\S+", "", text)
