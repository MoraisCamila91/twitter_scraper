from flask import Response
import requests
import json
import time

from handle_oauth import update_token

def get_tweet_by_user(user_id, start_date, end_date, max_results, token, pagination_token=None):    
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"

    headers={
            "Authorization": "Bearer {}".format(token['access_token']),
            "Content-Type": "application/json",
    }
    
    params = {
        "tweet.fields": "author_id,created_at",
        "max_results": max_results,
        "start_time": start_date,
        "end_time": end_date,
        # "exclude": "retweets,replies",
        "pagination_token": pagination_token
    }

    try:
        result = requests.get(url, headers=headers, params=params)
    
    except:
        error_response = {'message': 'Too Many Requests'}
        json_response = json.dumps(error_response)
        result = Response(json_response, status=429, mimetype='application/json')
    
    return result

def extract_info(result, trials, token):
    result_code = result.status_code
    
    if result_code == 200:
        trials = 3
        result_info = json.loads(result.text)

        if 'meta' in result_info.keys() and result_info['meta']['result_count'] == 0:
            return [], 'ZERO TWEETS', trials, result_code, token        
        
        elif 'errors' in result_info.keys() and result_info['errors'][0]['title'] == 'Not Found Error':
            return [], None, trials, result_code, token
        
        elif 'errors' in result_info.keys() and 'User has been suspended' in result_info['errors'][0]['detail']:
            return [], 'USER SUSPENDED', trials, result_code, token

        else:
            tweets = result_info['data']
            pagination_token = result_info['meta']['next_token'] if 'next_token' in result_info['meta'] else None
            return tweets, pagination_token, trials, result_code, token

    elif result_code == 401:
        token = update_token(token)
        return [], None, trials - 1, result_code, token

    elif result_code == 429:
        time.sleep(1*60)
        return [], None, trials - 1, result_code, token

    else:
        pass


def get_max_tweets_by_user(user_id, start_date, end_date, max_results, token):
    print("getting tweets from user {}".format(user_id))
    
    # first page
    trials = 3
    result_code = -1
    
    while result_code != 200 and trials > 0:
        result = get_tweet_by_user(user_id, start_date, end_date, max_results, token)
        tweets, pagination_token, trials, result_code, token = extract_info(result, trials, token)
    
    # pagination
    while pagination_token is not None and pagination_token not in ['ZERO TWEETS', 'USER SUSPENDED']:
        
        trials = 3
        result_code = -1
        
        while result_code != 200 and trials > 0:
            result = get_tweet_by_user(user_id, start_date, end_date, max_results, token, pagination_token)
            new_tweets, pagination_token, trials, result_code, token = extract_info(result, trials, token)

            if len(new_tweets) > 0:
                tweets = tweets + new_tweets
                
    if result_code == 200 or pagination_token in ['ZERO TWEETS', 'USER SUSPENDED']:
        return 'success', user_id, tweets, pagination_token, token
    
    else:
        return 'error', user_id, tweets, pagination_token, token
    