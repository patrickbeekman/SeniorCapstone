import pandas as pd
import numpy as np
import json
import os
from pandas.io.json import json_normalize
from datetime import datetime
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import tweepy
import tweepy_grabber


class TweetsDataAnalysis:

    def max_favorites_of_tweets(self, data):
        fav_max = np.max(data.favorite_count)
        fav = data[data.favorite_count == fav_max].index[0]
        # Max FAVs:
        print("The tweet with the most likes is: \n{}".format(data['text'][fav]), "with", fav_max, "likes!")

    def max_retweets_of_tweets(self, data):
        rt_max = np.max(data.retweet_count)
        rt = data[data.retweet_count == rt_max].index[0]
        # Max RTs:
        print("The tweet with the most retweets is: \n{}".format(data['text'][rt]), "with", rt_max, "retweets!")

    def graph_tweet_freq_per_month(self, data, filename):
        plt.figure(1)
        data['tone_name'].groupby(data.created_at.dt.month).count().plot(kind="bar", title='Count of tweets per month')
        plt.savefig(os.path.dirname(__file__) + "/../data/plots/" + filename)
        plt.close()

    def graph_joy_vs_sad_per_month(self, data, filename):
        data.set_index(data["created_at"], inplace=True)
        data["month"] = data['created_at'].apply(lambda x: x.strftime('%m'))
        joy_counts = data['month'][data.tone_name == "Joy"].value_counts().sort_index()
        sad_counts = data['month'][data.tone_name == "Sadness"].value_counts().sort_index()
        months1 = [1-.2,2-.2,3-.2,4-.2,5-.2,6-.2,7-.2,8-.2,9-.2,10-.2,11-.2,12-.2]
        months2 = [1,2,3,4,5,6,7,8,9,10,11,12]

        plt.figure(2)
        ax = plt.subplot(111)
        p1 = ax.bar(months1, joy_counts, width=.2, color='g', align='center')
        p2 = ax.bar(months2, sad_counts, width=.2, color='r', align='center')
        plt.ylabel('# Tweets')
        plt.title('All my tweets: Joy vs Sad by Month')
        plt.xticks(months2, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        plt.legend((p1[0], p2[0]), ('Joy', 'Sad'))
        plt.savefig(os.path.dirname(__file__) + "/../data/plots/" + filename)
        plt.close()

    def graph_joy_vs_sad_percent_stacked(self, data, filename, twitter_name):
        data.set_index(data["created_at"], inplace=True)
        data["month"] = data['created_at'].apply(lambda x: x.strftime('%m'))
        joy_counts = data['month'][data.tone_name == "Joy"].value_counts().sort_index()
        sad_counts = data['month'][data.tone_name == "Sadness"].value_counts().sort_index()
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.fill_series_with_zeros_if_data_missing(joy_counts)
        self.fill_series_with_zeros_if_data_missing(sad_counts)

        # Based on https://python-graph-gallery.com/13-percent-stacked-barplot/
        plt.figure(2)
        ax = plt.subplot(111)
        totals = [i + j for i, j in zip(joy_counts, sad_counts)]
        greenBars = [i / j * 100 for i, j in zip(joy_counts, totals)]
        redBars = [i / j * 100 for i, j in zip(sad_counts, totals)]

        barWidth = 0.85
        # Create green Bars
        plt.bar(months, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="Joy")
        # Create red Bars
        plt.bar(months, redBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth, label="Sad")
        plt.ylabel('# Tweets')
        plt.title(twitter_name + '\'s tweets: Joy vs Sad by Month')
        plt.xticks(months, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        plt.legend()
        plt.savefig(os.path.dirname(__file__) + "/../data/plots/" + filename)
        plt.close()

    def fill_series_with_zeros_if_data_missing(self, series):
        if len(series != 12):
            for i in range(12):
                if i+1 < 10:
                    index = '0' + str(i + 1)
                    try:
                        series[index]
                    except KeyError:
                        series[index] = 0
                        series.sort_index()
                else:
                    index = str(i+1)
                    try:
                        series[index]
                    except KeyError:
                        series[index] = 0
                        series.sort_index()

    def graph_other_emotions_per_month(self, data, filename):
        data["month"] = data['created_at'].apply(lambda x: x.strftime('%m'))
        analytical_counts = data['month'][data.tone_name == "Analytical"].value_counts().sort_index()
        tentative_counts = data['month'][data.tone_name == "Tentative"].value_counts().sort_index()
        fear_counts = data['month'][data.tone_name == "Fear"].value_counts().sort_index()
        confident_counts = data['month'][data.tone_name == "Confident"].value_counts().sort_index()
        anger_counts = data['month'][data.tone_name == "Anger"].value_counts().sort_index()
        months1 = [1-.4,2-.4,3-.4,4-.4,5-.4,6-.4,7-.4,8-.4,9-.4,10-.4,11-.4,12-.4]
        months2 = [1-.2,2-.2,3-.2,4-.2,5-.2,6-.2,7-.2,8-.2,9-.2,10-.2,11-.2,12-.2]
        months3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        months4 = [1+.2, 2+.2, 3+.2, 4+.2, 5+.2, 6+.2, 7+.2, 8+.2, 9+.2, 10+.2, 11+.2, 12+.2]
        months5 = [1+.4, 2+.4, 3+.4, 4+.4, 5+.4, 6+.4, 7+.4, 8+.4, 9+.4, 10+.4, 11+.4, 12+.4]
        self.fill_series_with_zeros_if_data_missing(analytical_counts)
        self.fill_series_with_zeros_if_data_missing(tentative_counts)
        self.fill_series_with_zeros_if_data_missing(fear_counts)
        self.fill_series_with_zeros_if_data_missing(confident_counts)
        self.fill_series_with_zeros_if_data_missing(anger_counts)

        plt.figure(3)
        ax = plt.subplot(111)
        p1 = ax.bar(months1, analytical_counts, width=.2, color='#cef442', align='center')
        p2 = ax.bar(months2, tentative_counts, width=.2, color='#ccb526', align='center')
        p3 = ax.bar(months3, fear_counts, width=.2, color='#c127cc', align='center')
        p4 = ax.bar(months4, confident_counts, width=.2, color='#26cc3e', align='center')
        p5 = ax.bar(months5, anger_counts, width=.2, color='#cc262f', align='center')
        plt.ylabel('# Tweets')
        plt.title('All my tweets: Other Emotions by Month')
        plt.xticks(months3, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('Analytical', 'Tentative', 'Fear', 'Confident', 'Anger'))
        plt.savefig(os.path.dirname(__file__) + "/../data/plots/" + filename)
        plt.close()

    def graph_pie_chart(self, data, filename, twitter_name):
        total = len(data.index)
        joy_counts = len(data[data.tone_name == "Joy"])
        sad_counts = len(data[data.tone_name == "Sadness"])
        analytical_counts = len(data[data.tone_name == "Analytical"])
        tentative_counts = len(data[data.tone_name == "Tentative"])
        fear_counts = len(data[data.tone_name == "Fear"])
        confident_counts = len(data[data.tone_name == "Confident"])
        anger_counts = len(data[data.tone_name == "Anger"])
        sizes = [joy_counts, sad_counts, analytical_counts, tentative_counts, fear_counts, confident_counts, anger_counts]
        sizes = [(x / total) * 100 for x in sizes]
        labels = 'Joy', 'Sadness', 'Analytical', 'Tentative', 'Fear', 'Confident', 'Anger'

        plt.figure(4)
        plt.title(twitter_name + ' Emotions Pie Chart')
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')
        plt.savefig(os.path.dirname(__file__) + "/../data/plots/" + filename)
        plt.close()

    def get_flattened_data(self, filename, record_path, meta=[]):
        with open(filename) as f:
            data = json.load(f)
        data_flattened = pd.io.json.json_normalize(data, record_path=record_path, meta=meta)
        #print(data_flattened.head())
        return data_flattened

    def convert_to_datetime(self, data):
        data.created_at = data.created_at.apply(lambda x: int(str(x)[0:10]))
        data.created_at = data.created_at.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')) # %H:%M:%S
        data.created_at = data.created_at.astype('datetime64[ns]')
        return data

    def graph_word_count_for_user(self, file_path):
        df = pd.read_json(file_path)
        # Removing common words: https://stackoverflow.com/questions/9953619/technique-to-remove-common-wordsand-their-plural-versions-from-a-string
        nltk.download("stopwords")
        s = set(stopwords.words('english'))
        myWords = {'RT', 'I', '.', 'The', 'like', 'I\'m', 'My', 'This', 'get', 'It\'s', 'Who', 'What', 'Where', 'When',
                 'Why', 'A', '`'}
        s.update(myWords)
        text_notflat = [filter(lambda w: not w in s, tweet.split()) for tweet in df['text']]
        word_counter = Counter(chain.from_iterable(text_notflat))
        most_common = word_counter.most_common(25)
        words = list(zip(*most_common))[0]
        values = list(zip(*most_common))[1]

        indexes = np.arange(len(words))
        width = 0.7
        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0.5, words)
        plt.xticks(rotation=90)
        plt.show()
        return word_counter




def main():
    tda = TweetsDataAnalysis()

    twitter_handle = "North_Carolina"

    #data = tda.get_flattened_data(os.path.dirname(__file__) + "/../data/us_states/" + twitter_handle + "_merged_analysis.json", 'tones', ['text', 'created_at', 'favorite_count', 'retweet_count', 'user'])

    # tda.convert_to_datetime(data)
    # tda.max_favorites_of_tweets(data)
    # tda.max_retweets_of_tweets(data)
    # tda.graph_tweet_freq_per_month(data, twitter_handle + 's_per_month.png')
    # #tda.graph_joy_vs_sad_per_month(data, 'my_tweets_joy_vs_sad_per_month.png')
    # tda.graph_joy_vs_sad_percent_stacked(data, twitter_handle + 's_tweets_joy_vs_sad_stacked_bar.png', twitter_handle)
    # #tda.graph_other_emotions_per_month(data, 'my_tweets_other_emotions_per_month.png')
    # tda.graph_pie_chart(data, twitter_handle + 's_pie_chart.png', twitter_handle)

    tda.graph_word_count_for_user(os.path.dirname(__file__) + "/../data/pbFollowers/users_tweets/patrickbeekman_tweets.json")


if __name__ == "__main__":
    main()