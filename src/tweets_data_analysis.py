import pandas as pd
import numpy as np
import json
import os
from pandas.io.json import json_normalize
from datetime import datetime
import matplotlib.pyplot as plt


class TweetsDataAnalysis:

    def max_favorites_of_tweets(self, data):
        fav_max = np.max(data.favorite_count)
        fav = data[data.favorite_count == fav_max].index[0]
        # Max FAVs:
        print("The tweet with the most likes is: \n{}".format(data['text'][fav]), "with", fav_max, "likes!")

    def max_retweets_of_tweets(self, data):
        rt_max = np.max(data.retweet_count)
        rt = data[data.retweet_count == rt_max].index[0]
        # Max FAVs:
        print("The tweet with the most retweets is: \n{}".format(data['text'][rt]), "with", rt_max, "retweets!")

    def graph_tweet_freq_per_month(self, data):
        # Want to show bar graph of number of joy vs sad for each month
        data.created_at = data.created_at.apply(lambda x: int(str(x)[0:10]))
        data.created_at = data.created_at.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')) # %H:%M:%S
        data.created_at = data.created_at.astype('datetime64[ns]')
        data['tone_name'].groupby(data.created_at.dt.month).count().plot(kind="bar", title='Count of tweets per month')
        plt.savefig(os.path.dirname(__file__) + "/../data/images/my_freq_per_month.png")

    def graph_emotions_per_month(self, data):
        # Want to show bar graph of number of joy vs sad for each month
        data.created_at = data.created_at.apply(lambda x: int(str(x)[0:10]))
        data.created_at = data.created_at.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')) # %H:%M:%S
        data.created_at = data.created_at.astype('datetime64[ns]')
        january_joy = data.loc[(data['created_at'].dt.month == 1) & (data.tone_name == "Joy")]
        print(january_joy)

    def get_flattened_data(self, filename, record_path, meta=[]):
        with open(filename) as f:
            data = json.load(f)
        data_flattened = pd.io.json.json_normalize(data, record_path=record_path, meta=meta)
        print(data_flattened.head())
        return data_flattened #self.convert_to_datetime(data_flattened)

    def convert_to_datetime(self, data):
        data.created_at = data.created_at.apply(lambda x: int(str(x)[0:10]))
        data.created_at = data.created_at.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')) # %H:%M:%S
        data.created_at = data.created_at.astype('datetime64[ns]')
        return data


def main():
    tda = TweetsDataAnalysis()

    data = tda.get_flattened_data(os.path.dirname(__file__) + "/../data/merged_analysis.json", 'tones', ['text', 'created_at', 'favorite_count', 'retweet_count'])
    #merged_analysis = pd.read_json(os.path.dirname(__file__) + "/../data/merged_analysis.json", orient='records')
    print(list(data.columns.values))
    # tda.max_favorites_of_tweets(data)
    # tda.max_retweets_of_tweets(data)
    # tda.graph_tweet_freq_per_month(data)
    tda.graph_emotions_per_month(data)


if __name__ == "__main__":
    main()