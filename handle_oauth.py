import os
import re
import time
import base64
import hashlib
import requests

from requests_oauthlib import OAuth2Session

from keys import client_id, client_secret
from configuration import redirect_uri

# firefox_path = '/usr/bin/firefox'

def handle_oauth():
    # scopes = ["dm.read", "dm.write", "tweet.read", "users.read", "offline.access"]
    scopes = ["tweet.read", "users.read", "offline.access"]
    
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
    
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")
    
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
    
    auth_url = "https://twitter.com/i/oauth2/authorize"
    authorization_url, state = oauth.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    
    print("Visit the following URL to authorize your App on behalf of your Twitter handle in a browser:")
    print(authorization_url)

    authorization_response = input(
        "Paste in the full URL after you've authorized your App:\n"
    )
    
    token_url = "https://api.twitter.com/2/oauth2/token"
    
    auth = False
    
    token = oauth.fetch_token(
        token_url=token_url,
        authorization_response=authorization_response,
        auth=auth,
        client_id=client_id,
        include_client_id=True,
        code_verifier=code_verifier,
    )
    
    return token


def update_token(token):    
    trials = 3
    status_code = -1
    
    token_url = 'https://api.twitter.com/2/oauth2/token'

    data = {
        'refresh_token': token['refresh_token'],
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    while status_code != 200 and trials > 0:
        response = requests.post(token_url, data=data, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            token_data = response.json()
            return token_data

        else:
            trials -= 1
            print("Error obtaining access token:", response.status_code, response.text)
            print("Number of remaining trials: ", trials)
    
    raise Exception("Unable to update token.")