import tweepy
import time
import os
import json

class TweepyGrabber:
    api = None

    def __init__(self):
        self.api = self.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])

    def api_connect(self, consumer_key, consumer_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth)
        return api

    def get_users_timeline(self, screen_name, output_file_name):
        all_tweets = []
        try:
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)
        except Exception as e:
            print("Error accessing usertimeline:", e.message)
        all_tweets.extend(new_tweets)
        # get the tweet id of the last tweet grabbed to know where to start grabbing
        # the next 200 tweets
        oldest = all_tweets[-1].id - 1
        print("Downloaded ", len(all_tweets), " so far =)")

        while len(new_tweets) > 0:
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            print("Downloaded ", len(all_tweets), " so far =)")

        json_file_path = os.path.dirname(__file__) + "/../data/" + output_file_name

        with open(json_file_path, 'w') as file:
            json.dump([status._json for status in all_tweets], file)

    def get_users_followers(self, screen_name):
        ids = []
        for page in tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
            time.sleep(5)

        followers = [user for user in self.api.lookup_users(user_ids=ids)]
        return followers

def main():
    grabber = TweepyGrabber()
    twitter_handle = "_sydalee"
    #grabber.get_users_timeline(twitter_handle, "@" + twitter_handle + "_tweets.json")
    followers = grabber.get_users_followers("patrickbeekman")
    print("hi")

if __name__ == "__main__":
    main()