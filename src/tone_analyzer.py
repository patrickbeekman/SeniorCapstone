import pandas as pd
import os
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonException
from watson_developer_cloud import WatsonInvalidArgument
# install with - from watson_developer_cloud import ToneAnalyzerV3

class MyToneAnalyzer():

    #def __init__(self):

    def create_connection(self, version_num):
        try:
            tone_analyzer = ToneAnalyzerV3(
                username=os.environ['TONE_U'],
                password=os.environ['TONE_P'],
                version=version_num)
        except WatsonInvalidArgument as e:
            print(e)
            exit(0)
        return tone_analyzer

    def analyze_json_file(self, analyzer, filename):
        with open(filename) as tone_json:
            try:
                tone_resp = analyzer.tone(tone_json.read())
            except WatsonException as e:
                print("WatsonException", e)
                exit(0)
        return tone_resp

    def strip_text_from_json(self, filename, newfilename=""):
        df = pd.read_json(filename)
        tweet_text = df['text']
        hundred_tweets = ""
        for tweet in tweet_text:
            s_tweet = tweet.strip().replace('.','')
            s_tweet += '..'
            hundred_tweets += " " + s_tweet
        print(hundred_tweets)
        d = {'text': [hundred_tweets]}
        new_df = pd.DataFrame(data=d).to_json(orient='records')[1:-1]
        with open('file_name.json', 'w') as f:
            f.write(new_df)


def main():
    ta = MyToneAnalyzer()
    analyzer = ta.create_connection('2018-02-07')

    filename_tone = os.path.dirname(__file__) + "/../test_text.json"
    tone_resp = ta.analyze_json_file(analyzer, filename_tone)
    #print(json.dumps(tone_resp, indent=2))

    filename_tweet = os.path.dirname(__file__) + "/../small_tweets.json"
    ta.strip_text_from_json(filename_tweet)
    print(json.dumps(ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/file_name.json")))

if __name__ == "__main__":
    main()