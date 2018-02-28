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

    def grab_emotion_per_month(self, data):
        print(list(data.columns.values))

        #t_tones = pd.Series(data=data.tone_name, index=data.created_at)
        # Want to show bar graph of number of joy vs sad for each month
        data.created_at = data.created_at.apply(lambda x: int(str(x)[0:10]))
        data.created_at = data.created_at.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')) # %H:%M:%S
        #print(data.created_at)
        data.created_at = data.created_at.astype('datetime64[ns]')
        #print(data)
        month_vs_count = data['tone_name'].groupby(data.created_at.dt.month).count().plot(kind="bar", title='Count of tweets per month')
        #month_vs_count.xticks(plt.arange(12), plt.calendar.month_name[1:13], rotation=17 )
        plt.savefig(os.path.dirname(__file__) + "/../data/images/my_freq_per_month.png")
        #plt.show()

    def get_flattened_data(self, filename, record_path, meta=[]):
        with open(filename) as f:
            data = json.load(f)
        data_flattened = pd.io.json.json_normalize(data, record_path=record_path, meta=meta)
        print(data_flattened.head())
        return data_flattened


def main():
    tda = TweetsDataAnalysis()

    data = tda.get_flattened_data(os.path.dirname(__file__) + "/../data/merged_analysis.json", 'tones', ['text', 'created_at', 'favorite_count', 'retweet_count'])
    #merged_analysis = pd.read_json(os.path.dirname(__file__) + "/../data/merged_analysis.json", orient='records')
    print(list(data.columns.values))
    tda.max_favorites_of_tweets(data)
    tda.max_retweets_of_tweets(data)
    tda.grab_emotion_per_month(data)


if __name__ == "__main__":
    main()