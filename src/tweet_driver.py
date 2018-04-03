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

    def analyze_followers_of_followers(self, screen_name, data_folder):
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

        followers = self.grabber.get_users_followers(data_path, screen_name)
        self.grabber.get_followers_of_followers(followers, data_path)

        if not os.path.exists(data_path + "users_tweets/"):
            os.mkdir(data_path + "users_tweets/")
        # open up each file of followers accounts and grab 2000 of their tweets
        for file in current_files:
            with open(file) as f:
                users_followers = pd.DataFrame(f)
            for user in users_followers:
                users_tweets_path = data_path + "users_tweets/" + user['screen_name'] + "_tweets.json"
                self.grabber.get_users_timeline(user['screen_name'], users_tweets_path, max_tweets=2000)



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
    driver.analyze_search_term(us_states, 'us_states')

if __name__ == "__main__":
    main()
