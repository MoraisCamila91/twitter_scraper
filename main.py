import pandas as pd

from keys import token, bad_keys
from configuration import SUCCESS_PATH, ERROR_PATH

from handle_oauth import handle_oauth
from get_tweets import get_max_tweets_by_user
from handle_csv import save_user_tweets, save_user_errors


### user infos
# import shelve
# from handle_users_info import get_info
# saves = shelve.open('saves')
# users_infos = {key: get_info(saves[key])
#                for key in saves.keys()
#                if key not in bad_keys}
# users_infos = {key: value
#                for key, value in users_infos.items()
#                if value['account_status'] is not None}

### user ids
# user_ids for testing purpose
# my_user_id = '1750230667101671424'
# elon_id = '44196397'

# df = pd.read_csv('../AWS/users_ideology.csv')[['id']]
df = pd.read_csv('../AWS/elite_id.csv')[['id']]
ids = [str(id) for id in df['id'].to_list()]

df_general_done = pd.read_csv('user_tweets.csv')[['user_id']]
ids_general_done = set(str(id) for id in df_general_done['user_id'].to_list())

df_done = pd.read_csv(SUCCESS_PATH)[['Unnamed: 0']]
ids_done = set(str(id) for id in df_done['Unnamed: 0'].to_list())

# df_fail = pd.read_csv(ERROR_PATH)[['Unnamed: 0']]
# ids_fail = set(str(id) for id in df_fail['Unnamed: 0'].to_list())

ids = [id for id in ids 
       if id not in ids_done and id not in ids_general_done]

print('Faltam ' + str(len(ids)) + ' tweeteiros')


### tweets configurations
# 01/10/2020 -> 01/01/2021 - data mining moment (TCC)
start_date = '2020-10-01T00:00:00.00Z'
end_date = '2021-01-01T00:00:00.00Z'
max_results = 100

### initial token
# token = handle_oauth()
# print(token)


def main():
    token2 = token
    # count_users = 0

    for user_id in ids:
        result_code, user_id, tweets, pagination_token, token2 = get_max_tweets_by_user(user_id, 
                                                                                       start_date, end_date, 
                                                                                       max_results,
                                                                                       token=token2)
        
        if result_code == 'success':
            save_user_tweets(user_id, tweets, pagination_token)
        else:
            save_user_errors(user_id, tweets, pagination_token)
        
        # count_users += 1

        # if count_users > 100:
        #     break

main()