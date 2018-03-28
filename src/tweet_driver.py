import tweepy_grabber
import tone_analyzer
import tweets_data_analysis
import os

class Tweet_Driver:

    def start(self):
        grabber = tweepy_grabber.TweepyGrabber()
        analyzer = tone_analyzer.MyToneAnalyzer()
        analysis = tweets_data_analysis.TweetsDataAnalysis()

        # tweepy_grabber stuff
        search_query = "North Carolina"
        outfile1 = os.path.dirname(__file__) + "/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"
        grabber.get_search_results(search_query, outfile1, 5000)

        # tone_analyzer stuff
        analyzer.incremental_send_all_tweets_to_text_json(analyzer.path_name("/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"),
                                                          analyzer.path_name("/../data/tweets_text/"))
        analyzer.analyze_all_tweets_text_folder(analyzer.path_name("/../data/tweets_text/"))
        analyzer.create_single_file_tone_analysis(analyzer.path_name("/../data/analysis/"),
                                                  analyzer.path_name("/../data/all_analysis.json"))
        analyzer.temp_file_cleanup(analyzer.path_name("/../data/analysis/"),
                                   analyzer.path_name("/../data/tweets_text/"))
        analyzer.attach_analysis_to_tweet(analyzer.path_name("/../data/all_analysis.json"),
                                          analyzer.path_name("/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"),
                                          analyzer.path_name("/../data/us_states/" + search_query.replace(' ', '_') + "_merged_analysis.json"))

        # tweets_data_analysis
        data = analysis.get_flattened_data(
            os.path.dirname(__file__) + "/../data/us_states/" + search_query + "_merged_analysis.json", 'tones',
            ['text', 'created_at', 'favorite_count', 'retweet_count'])

        analysis.convert_to_datetime(data)
        analysis.graph_pie_chart(data, search_query + 's_pie_chart.png', search_query)


def main():
    driver = Tweet_Driver()
    driver.start()

if __name__ == "__main__":
    main()
