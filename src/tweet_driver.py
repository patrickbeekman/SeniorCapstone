import tweepy_grabber
import tone_analyzer
import tweets_data_analysis
import pandas as pd
from watson_developer_cloud import WatsonException
import os

class Tweet_Driver:

    grabber = None
    analyzer = None
    analysis = None

    def __init__(self):
        self.grabber = tweepy_grabber.TweepyGrabber()
        self.analyzer = tone_analyzer.MyToneAnalyzer()
        self.analysis = tweets_data_analysis.TweetsDataAnalysis()

    def analyze_followers_of_user_create_plots(self, screen_name, data_folder):
        data_path = os.path.dirname(__file__) + "/../data/" + data_folder + "/"
        if not os.path.dirname(os.path.dirname(__file__) + "/../data/"):
            os.mkdir(os.path.dirname(__file__) + "/../data/")
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        # Collect the followers for the central user then collect all their followers
        # and save them to the specified folder.
        followers_path = data_path + "followers/"
        if not os.path.exists(followers_path):
            os.mkdir(followers_path)
        if not os.path.exists(followers_path + screen_name + "_followers.json"):
            followers = self.grabber.get_users_followers(followers_path, screen_name)
        #self.grabber.get_followers_of_followers(followers, followers_path)

        all_users_tweets_path = data_path + "users_tweets/"
        if not os.path.exists(all_users_tweets_path):
            os.mkdir(all_users_tweets_path)
        if not os.path.exists(data_path + "merged/"):
            os.mkdir(data_path + "merged/")
        if not os.path.exists(data_path + "analysis/"):
            os.mkdir(data_path + "analysis/")
        if not os.path.exists(data_path + "tweets_text/"):
            os.mkdir(data_path + "tweets_text/")


        # open up each file of followers accounts and grab 2000 of their tweets
        current_files = os.listdir(followers_path)
        for file in current_files:
            users_followers = pd.read_json(followers_path + file)
            for index, user in users_followers.iterrows():
                user_tweets_path = all_users_tweets_path + user['screen_name'] + "_tweets.json"
                if user['protected']:
                    continue

                if not os.path.exists(user_tweets_path):
                    self.grabber.get_users_timeline(user['screen_name'], user_tweets_path, max_tweets=2000)

                if os.path.exists(data_path + "merged/" + user['screen_name'] + "_merged_analysis.json"):
                    continue

                print("Starting: " + user['screen_name'])
                try:
                    self.analyzer.incremental_send_all_tweets_to_text_json(user_tweets_path, data_path + "tweets_text/")
                    self.analyzer.analyze_all_tweets_text_folder(data_path + "tweets_text/")
                    self.analyzer.create_single_file_tone_analysis(data_path + "analysis/",
                                                                   data_path + "all_analysis.json")
                except FileNotFoundError:
                    continue
                except WatsonException:
                    print("WatsonError!!!!")
                    self.analyzer = tone_analyzer.MyToneAnalyzer()
                    continue

                self.analyzer.attach_analysis_to_tweet(data_path + "all_analysis.json",
                                                       user_tweets_path,
                                                       data_path + "merged/" + user['screen_name'] + "_merged_analysis.json")
                self.analyzer.temp_file_cleanup(data_path + "analysis/",
                                                data_path + "tweets_text/")
        return self.analysis.create_components_to_json(data_path)

    def analyze_search_term(self, data, data_folder):
        data_path = os.path.dirname(__file__) + "/../data/" + data_folder + "/"
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        current_files = os.listdir(data_path)
        current_terms = [f.split('_') for f in current_files]
        excluded_terms = []
        for s in current_terms:
            if s[1] == "tweets.json" or s[1] == "merged":
                try:
                    excluded_terms.index(s[0])
                except ValueError:
                    excluded_terms.append(s[0])
            else:
                try:
                    excluded_terms.index(s[0] + " " + s[1])
                except ValueError:
                    excluded_terms.append(s[0] + " " + s[1])

        for entry in data:
            try:
                excluded_terms.index(entry)
            except ValueError:
                excluded_terms.append(entry)
                print("Starting: " + entry)
                # tweepy_grabber stuff
                search_query = entry
                outfile1 = os.path.dirname(__file__) + "/../data/" + data_folder + "/" + search_query.replace(' ', '_') + "_tweets.json"
                self.grabber.get_search_results(search_query, outfile1, 2500)

                # tone_analyzer stuff
                self.analyzer.incremental_send_all_tweets_to_text_json(self.analyzer.path_name("/../data/" + data_folder + "/" + search_query.replace(' ', '_') + "_tweets.json"),
                                                                       self.analyzer.path_name("/../data/tweets_text/"))
                try:
                    self.analyzer.analyze_all_tweets_text_folder(self.analyzer.path_name("/../data/tweets_text/"))
                except WatsonException as e:
                    # If error then just print, recreate/connect to analyzer and continue to next state
                    print("WatsonException")
                    print(e)
                    self.analyzer = tone_analyzer.MyToneAnalyzer()
                    continue
                self.analyzer.create_single_file_tone_analysis(self.analyzer.path_name("/../data/analysis/"),
                                                               self.analyzer.path_name("/../data/all_analysis.json"))
                self.analyzer.temp_file_cleanup(self.analyzer.path_name("/../data/analysis/"),
                                                self.analyzer.path_name("/../data/tweets_text/"))
                self.analyzer.attach_analysis_to_tweet(self.analyzer.path_name("/../data/all_analysis.json"),
                                                       self.analyzer.path_name("/../data/" + data_folder + "/" + search_query.replace(' ', '_') + "_tweets.json"),
                                                       self.analyzer.path_name("/../data/" + data_folder + "/" + search_query.replace(' ', '_') + "_merged_analysis.json"))

                # tweets_data_analysis
                data = self.analysis.get_flattened_data(
                    os.path.dirname(__file__) + "/../data/" + data_folder + "/" + search_query.replace(' ', '_') + "_merged_analysis.json", 'tones',
                    ['text', 'created_at', 'favorite_count', 'retweet_count'])

                self.analysis.convert_to_datetime(data)
                self.analysis.graph_pie_chart(data, search_query + 's_pie_chart.png', search_query)
                # reset the tone analyzer which creates a new connection to the service
                self.analyzer = tone_analyzer.MyToneAnalyzer()



def main():
    driver = Tweet_Driver()
    us_states = [
        'Alabama',
        'Alaska',
        'Arizona',
        'Arkansas',
        'California',
        'Colorado',
        'Connecticut',
        'Delaware',
        'Florida',
        'Georgia',
        'Hawaii',
        'Idaho',
        'Illinois',
        'Indiana',
        'Iowa',
        'Kansas',
        'Kentucky',
        'Louisiana',
        'Maine',
        'Maryland',
        'Massachusetts',
        'Michigan',
        'Minnesota',
        'Mississippi',
        'Missouri',
        'Montana',
        'Nebraska',
        'Nevada',
        'New Hampshire',
        'New Jersey',
        'New Mexico',
        'New York',
        'North Carolina',
        'North Dakota',
        'Ohio',
        'Oklahoma',
        'Oregon',
        'Pennsylvania',
        'Rhode Island',
        'South Carolina',
        'South Dakota',
        'Tennessee',
        'Texas',
        'Utah',
        'Vermont',
        'Virginia',
        'Washington',
        'West Virginia',
        'Wisconsin',
        'Wyoming'
    ]
    #driver.analyze_search_term(us_states, 'us_states')
    #driver.analyze_followers_of_user_create_plots('patrickbeekman', 'pbFollowers')
    analysis_path = os.path.dirname(__file__) + "/../data/pbFollowers/"
    #driver.analyzer.create_single_file_tone_analysis(analysis_path + "merged/", analysis_path + "single_file_merged.json")
    driver.analyze_followers_of_user_create_plots('LongentUSA', 'LongentFollowers')


if __name__ == "__main__":
    main()
