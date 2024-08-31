import os
import csv
from configuration import SUCCESS_PATH, ERROR_PATH

def save_user_tweets(user_id, tweets, pagination_token=None):
    keys = ['user_id', 'text', 'created_at', 'id', 'author_id']

    with open(SUCCESS_PATH, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        
        existing_file = os.path.isfile(SUCCESS_PATH) and os.path.getsize(SUCCESS_PATH) > 0
        
        if not existing_file:
            writer.writeheader()

        if len(tweets) == 0:
            tweets = [{'text': None, 
                       'created_at': None, 
                       'id': None, 
                       'author_id': None}]

        for tweet in tweets:
            tweet['user_id'] = user_id
            
            edited_tweet = {key: tweet.get(key, None) for key in keys}

            if pagination_token in ['ZERO TWEETS', 'USER SUSPENDED', 'USER NOT FOUND']:
                tweet['text'] = pagination_token

            writer.writerow(edited_tweet)
            
def save_user_errors(user_id, tweets, pagination_token):
    keys = ['user_id', 'pagination_token', 'text', 'created_at', 'id', 'author_id']

    with open(ERROR_PATH, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        
        existing_file = os.path.isfile(ERROR_PATH) and os.path.getsize(ERROR_PATH) > 0
        
        if not existing_file:
            writer.writeheader()
        
        if len(tweets) == 0:
            tweets = [{'text': None, 
                       'created_at': None, 
                       'id': None, 
                       'author_id': None}]

        for tweet in tweets:
            tweet['user_id'] = user_id
            tweet['pagination_token'] = pagination_token
            
            edited_tweet = {key: tweet.get(key, None) for key in keys}
            writer.writerow(edited_tweet)