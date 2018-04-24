import tweepy
import pandas as pd
import time
import sys
import os
import json

class TweepyGrabber:
    api = None

    def __init__(self):
        self.api = self.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])

    '''
        Connects to the twitter api taking in a consumer key and secret which can be gotten from
        creating a twitter app at: https://apps.twitter.com/
    '''
    def api_connect(self, consumer_key, consumer_secret):
        try:
            auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        except tweepy.TweepError as e:
            print(e)
            exit(1)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        return api

    '''
        Takes in a users screen name and will collect all the tweets in a users timeline
        aka tweets and retweets that you made. A max tweets has been added so you can
        specify a subset of tweets to get from the user. The tweets are saved in json
        format to the specified output path with filename.
    '''
    def get_users_timeline(self, screen_name, output_file_path, max_tweets=10000):
        all_tweets = []
        try:
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)
        except Exception as e:
            print("Error accessing usertimeline:", e.message)
        all_tweets.extend(new_tweets)
        # get the tweet id of the last tweet grabbed to know where to start grabbing
        # the next 200 tweets
        try:
            oldest = all_tweets[-1].id - 1
        except IndexError:
            # If the user has no tweets then just return
            return None
        print("Downloaded ", len(all_tweets), " so far =)")
        count = 0
        while len(new_tweets) > 0 and count <= max_tweets:
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            count+=200
            print("Downloaded ", len(all_tweets), " so far =)")

        with open(output_file_path, 'w') as file:
            json.dump([status._json for status in all_tweets], file)

    '''
        Takes in the output path as well as a user you would like their followers of.
        This returns a pandas Dataframe.
    '''
    def get_users_followers(self, output_path=None, screen_name="patrickbeekman"):
        users = []
        try:
            ids = []
            for page in tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).pages():
                ids.extend(page)
        except tweepy.TweepError:
            print("tweepy.TweepError")
            return None
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)
            return None

        for start in range(0, len(ids), 100):
            end = start + 100

            try:
                users.extend(self.api.lookup_users(ids[start:end]))

            except tweepy.RateLimitError:
                print("RateLimitError...waiting 900 seconds to continue")
                time.sleep(900)
                users.extend(self.api.lookup_users(ids[start:end]))

        users_df = pd.DataFrame([u._json for u in users])

        if output_path is not None:
            out_filename = output_path + screen_name + "_followers.json"
            users_df.to_json(out_filename)
        # with open(out_filename, 'w') as file:
        #     json.dump([u._json for u in users], file)
        return users_df

    '''
        Loops through a pandas Dataframe of users and saves all their followers
        to a new file @screenname_followers.json in the specified output_path.
    '''
    def get_followers_of_followers(self, users, output_path):

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        folder_files = os.listdir(output_path)
        should_continue = False

        if users is None:
            return

        for user in users.iterrows():
            sn = user[1]['screen_name']

            # Dont get private users and don't get if json file already saved
            if user[1]['protected'] is True:
                continue
            for f in folder_files:
                if f[1:f.find('_')] == sn:
                    should_continue = True
                    break
            if should_continue:
                should_continue = False
                continue

            print("collecting users from ", sn)
            this_users = self.get_users_followers(screen_name=sn)
            out_filename = output_path + "@" + sn + "_followers.json"
            this_users.to_json(out_filename)
            # with open(out_filename, 'w') as file:
            #     json.dump([u._json for u in this_users], file)

    '''
        Specify a search term as a string and the output path with filename.
        You can specify a max_tweets which is helpful for getting a subset of tweets.
    '''
    def get_search_results(self, search_term, output_file, max_tweets=10000):
        # Searching based on https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
        tweets_per_query = 100
        since_id = None
        max_id = -1
        tweet_count = 0
        all_tweets = []

        print("Downloading max {0} tweets".format(max_tweets))
        with open(output_file, 'w+') as f:
            while tweet_count < max_tweets:
                try:
                    if max_id <= 0:
                        if not since_id:
                            new_tweets = self.api.search(q=search_term, count=tweets_per_query)
                        else:
                            new_tweets = self.api.search(q=search_term, count=tweets_per_query,
                                                    since_id=since_id)
                    else:
                        if not since_id:
                            new_tweets = self.api.search(q=search_term, count=tweets_per_query,
                                                    max_id=str(max_id - 1))
                        else:
                            new_tweets = self.api.search(q=search_term, count=tweets_per_query,
                                                    max_id=str(max_id - 1),
                                                    since_id=since_id)
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    all_tweets.extend(new_tweets)
                    tweet_count += len(new_tweets)
                    print("Downloaded {0} tweets out of {1}".format(tweet_count, max_tweets))
                    max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break
        with open(output_file, 'w+') as file:
            json.dump([tweet._json for tweet in all_tweets], file)
        os.chmod(output_file, 0o777)

def main():
    grabber = TweepyGrabber()
    twitter_handle = "patrickbeekman"
    #grabber.get_users_timeline(twitter_handle, "@" + twitter_handle + "_tweets.json")
    # followers = grabber.get_users_followers(twitter_handle)
    # search_term = "North Carolina"
    # outfile = os.path.dirname(__file__) + "/../data/us_states/" + search_term.replace(' ', '_') + "_tweets.json"
    # grabber.get_search_results(search_term, outfile)

    path = os.path.dirname(__file__) + "/../data/"
    fllwrs = grabber.get_users_followers(output_path=path, screen_name="hrgwea")
    grabber.get_followers_of_followers(fllwrs, path + "../tests/flwrs_flwrs/")



if __name__ == "__main__":
    main()