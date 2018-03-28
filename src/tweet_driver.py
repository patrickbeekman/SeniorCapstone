import tweepy_grabber
import tone_analyzer
import tweets_data_analysis
import os

class Tweet_Driver:

    def start(self):
        grabber = tweepy_grabber.TweepyGrabber()
        analyzer = tone_analyzer.MyToneAnalyzer()
        analysis = tweets_data_analysis.TweetsDataAnalysis()

        search_query = "North Carolina"
        outfile1 = os.path.dirname(__file__) + "/../data/us_states/" + search_query.replace(' ', '_') + "_tweets.json"
        grabber.get_search_results(search_query, outfile1)



def main():
    driver = Tweet_Driver()
    driver.start()

if __name__ == "__main__":
    main()
