import tweepy_grabber
import tone_analyzer
import tweets_data_analysis
from watson_developer_cloud import WatsonException
import os

class Tweet_Driver:

    grabber = None
    analyzer = None
    analysis = None

    def start(self):
        self.grabber = tweepy_grabber.TweepyGrabber()
        self.analyzer = tone_analyzer.MyToneAnalyzer()
        self.analysis = tweets_data_analysis.TweetsDataAnalysis()

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

        current_files = os.listdir(os.path.dirname(__file__) + "/../data/us_states/")
        current_states = [f.split('_') for f in current_files]
        excluded_states = []
        for s in current_states:
            if s[1] == "tweets.json" or s[1] == "merged":
                try:
                    excluded_states.index(s[0])
                except ValueError:
                    excluded_states.append(s[0])
            else:
                try:
                    excluded_states.index(s[0] + " " + s[1])
                except ValueError:
                    excluded_states.append(s[0] + " " + s[1])
        count = 3
        for state in us_states:
            try:
                excluded_states.index(state)
            except ValueError:
                excluded_states.append(state)
                print("Starting: " + state)
                # tweepy_grabber stuff
                search_query = state
                outfile1 = os.path.dirname(__file__) + "/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"
                self.grabber.get_search_results(search_query, outfile1, 2500)

                # tone_analyzer stuff
                self.analyzer.incremental_send_all_tweets_to_text_json(self.analyzer.path_name("/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"),
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
                                                       self.analyzer.path_name("/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"),
                                                       self.analyzer.path_name("/../data/us_states/" + search_query.replace(' ', '_') + "_merged_analysis.json"))

                # tweets_data_analysis
                data = self.analysis.get_flattened_data(
                    os.path.dirname(__file__) + "/../data/us_states/" + search_query.replace(' ', '_') + "_merged_analysis.json", 'tones',
                    ['text', 'created_at', 'favorite_count', 'retweet_count'])

                count+=1
                self.analysis.convert_to_datetime(data)
                self.analysis.graph_pie_chart(data, search_query + 's_pie_chart.png', search_query)
                # reset the tone analyzer which creates a new connection to the service
                self.analyzer = tone_analyzer.MyToneAnalyzer()

def main():
    driver = Tweet_Driver()
    driver.start()

if __name__ == "__main__":
    main()
