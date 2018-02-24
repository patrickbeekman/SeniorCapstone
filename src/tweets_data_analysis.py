import pandas as pd
import os
import json
import sys

class TweetsDataAnalysis:

    def hello(self):
        tone_analysis_path = os.path.dirname(__file__) + "/../data/analysis/"
        my_tweets_json = os.path.dirname(__file__) + "/../data/tweets.json"

        tone_analysis_json = [pos_json for pos_json in os.listdir(tone_analysis_path) if pos_json.endswith(".json")]

        all_data = []

        for js in tone_analysis_json:
            with open(os.path.join(tone_analysis_path, js)) as json_file:
                data = pd.read_json(json_file)
                all_data.append(data)

        all_data = pd.concat(all_data, axis=1)
        print(all_data['text'])
        #df = pd.read_json(os.path.dirname(__file__) + "/../data/analysis/tone_tweet_1.json")
        #print(df['text'])


    def rename_files(self):
        path = os.path.dirname(__file__) + "/../data/analysis/"
        l = [(x, "tone_tweet_" + x[11:-5].zfill(4) + ".json") for x in os.listdir(path) if
             x.startswith("tone_tweet_") and x.endswith(".json")]

        for oldname, newname in l:
            os.rename(os.path.join(path, oldname), os.path.join(path, newname))




def main():
    tda = TweetsDataAnalysis()
    #tda.hello()
    tda.rename_files()

if __name__ == "__main__":
    main()