'''
tweet_grabber.py
A direct way to access the twitter RESTful api to grab twitter data
'''

import base64
import requests
import json
import os
import pandas as pd
import numpy as np


class TweetGrabber:

    def __init__(self):
        self.base_url = 'https://api.twitter.com/'

    def check_status(self, status_code):
        """
        Checks whether the response status is successful or not
        :param status_code: The status code we are checking
        :return: True if it is 200 (aka. successful) False otherwise and print an error message
        """
        if status_code == 200:
            return True
        else:
            print('Error: authorization failed with status ' + str(status_code))
            return False

    def get_user_timeline(self, token, username):
        """
        grabs all of the tweets from a users timeline and returns them in a python array
        :param token: The bearer token to access the api
        :param username: The username of the users timeline you want to get
        :return: A python array of all the users tweets
        """
        search_params = {
            'screen_name': str(username),
            'count': 100
        }
        tweet_data = self.query(token, search_params, '1.1/statuses/user_timeline.json')
        len_new = 100
        while len_new >= 1:
            print(str(len(tweet_data)))
            search_params = {
                'screen_name': str(username),
                'since_id': tweet_data[len(tweet_data) - 1]['id'],
                'count': 100
            }
            new_data = self.query(token, search_params, '1.1/statuses/user_timeline.json')
            len_new = len(new_data)
            tweet_data += new_data

        return tweet_data

    def save_to_json(self, data, filename):
        """
        Saves the json formatted data from a python list of json tweets
        :param data: a python list of json formatted tweets
        :param filename: the filename to save to
        """
        with open(filename, "a", encoding='utf8') as outfile:
            json.dump(data, outfile, indent=4)

    def query(self, bearer_tok, params, endpoint):
        """
        Performs a query on the twitter RESTful api using params and an endpoint
        :param bearer_tok: The bearer token that we got from a successful authorization
        :param params: A map object of the parameters we will be on the api
        :param endpoint: The endpoint location we will access on the api
        :return: All the requested information in json format
        """
        headers = {
            'Authorization': 'Bearer {}'.format(bearer_tok)
        }

        api_path = self.base_url + endpoint
        resp = requests.get(api_path, headers=headers, params=params)

        if self.check_status(resp.status_code):
            tweets_q = resp.json()
            return tweets_q
        else:
            return None

    def authorize(self, filename):
        """
        Authorizes the user application and connects to the RESTful twitter api
        :param filename: The name of the file containing the public/private keys this file should
                         have a single line of documentation \n public key \n private key
        :return: The bearer token for api requests
        """
        keys_file = open(filename, 'r')
        keys_file.readline()  # skip the first line of comments
        public_key = keys_file.readline().rstrip()
        if public_key == "":
            return "No public key"
        private_key = keys_file.readline().rstrip()
        if private_key == "":
            return "No private key"

        # Format the public:private and then encode using base64
        key_secret = '{}:{}'.format(public_key, private_key).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')

        # twitter api url
        base_url = 'https://api.twitter.com/'
        # the authorization endpoint
        auth_url = '{}oauth2/token'.format(base_url)

        # Header info for the authorization
        auth_headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        auth_data = {
            'grant_type': 'client_credentials'
        }

        # Was the authorization successful (aka. 200)
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

        if self.check_status(auth_resp.status_code):
            return auth_resp.json()['access_token']
        else:
            return None


def main():
    tg = TweetGrabber()
    bearer_token = tg.authorize(os.path.dirname(__file__) + '/../keys.txt')
    print(bearer_token)
    tweets = None
    if bearer_token is not None:
        tweets = tg.get_user_timeline(bearer_token, 'patrickbeekman')

    json_filename = os.path.dirname(__file__) + "/../tweets.json"

    os.remove(json_filename)
    tg.save_to_json(tweets, json_filename)

    df = pd.read_json(json_filename)
    print(list(df))

if __name__ == "__main__":
    main()