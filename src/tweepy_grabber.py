import tweepy
import time
import sys
import os
import json

class TweepyGrabber:
    api = None

    def __init__(self):
        self.api = self.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])

    def api_connect(self, consumer_key, consumer_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
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
        users = []
        try:
            ids = []
            for page in tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).pages():
                ids.extend(page)
        except tweepy.TweepError:
            print("tweepy.TweepError=")
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)

        for start in range(0, len(ids), 100):
            end = start + 100

            try:
                users.extend(self.api.lookup_users(ids[start:end]))

            except tweepy.RateLimitError:
                print("RateLimitError...waiting 1000 seconds to continue")
                time.sleep(1000)
                users.extend(self.api.lookup_users(ids[start:end])._json)

        return users

def main():
    grabber = TweepyGrabber()
    twitter_handle = "_sydalee"
    #grabber.get_users_timeline(twitter_handle, "@" + twitter_handle + "_tweets.json")
    followers = grabber.get_users_followers("patrickbeekman")
    print("hi")

if __name__ == "__main__":
    main()