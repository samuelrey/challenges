from collections import namedtuple
import csv
import os

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

Tweet = namedtuple('Tweet', 'id_str created_at text')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
API = tweepy.API(auth)


class UserTweets(object):
    """TODOs:
    - create a tweepy api interface
    - get all tweets for passed in handle
    - optionally get up until 'max_id' tweet id
    - save tweets to csv file in data/ subdirectory
    - implement len() an getitem() magic (dunder) methods"""
    def __init__(self, handle, max_id):
        self.handle = handle
        self.max_id = max_id
        self.output_file = '{}.{}'.format(os.path.join(DEST_DIR, self.handle),
                                          EXT)
        self.tweets = list(self._get_tweets())
        self._save_tweets()

    def _get_tweets(self):
        tweets = API.user_timeline(self.handle,
                                   count=NUM_TWEETS + 1,
                                   max_id=self.max_id)
        return (Tweet(t.id_str,
                      t.created_at,
                      t.text.replace('\n', '')) for t in tweets)

    def _save_tweets(self):
        with open(self.output_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(Tweet._fields)
            writer.writerows(self.tweets)

    def __len__(self):
        return len(self.tweets)

    def __getitem__(self, key):
        return self.tweets[key]


if __name__ == "__main__":

    for handle in ('pybites', 'techmoneykids', 'bbelderbos'):
        print('--- {} ---'.format(handle))
        user = UserTweets(handle)
        for tw in user[:5]:
            print(tw)
        print()
