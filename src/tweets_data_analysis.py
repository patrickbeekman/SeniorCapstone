import pandas as pd
import numpy as np
import json
import os
from pandas.io.json import json_normalize
import datetime
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
        sizes, total = self.get_tone_counts(data)
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

    def graph_word_count_for_user(self, file_path, screen_name, save_path):
        df = pd.read_json(file_path)
        # Removing common words: https://stackoverflow.com/questions/9953619/technique-to-remove-common-wordsand-their-plural-versions-from-a-string
        nltk.download("stopwords")
        s = set(stopwords.words('english'))
        myWords = {'RT', 'I', '.', 'The', 'like', 'I\'m', 'My', 'This', 'get', 'It\'s', 'Who', 'What', 'Where', 'When',
                 'Why', 'A', '`'}
        s.update(myWords)
        text_notflat = [filter(lambda w: not w in s, tweet.split()) for tweet in df['text']]
        word_counter = Counter(chain.from_iterable(text_notflat))
        most_common = word_counter.most_common(50)
        words = list(zip(*most_common))[0]
        values = list(zip(*most_common))[1]
        
        indexes = np.arange(len(words))
        width = 0.7
        plt.clf()
        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0.5, words)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.title("Top Word Counts of " + screen_name)
        plt.savefig(save_path)
        plt.close()
        return word_counter

    '''
        Gets the tone counts from a dataframe of tweets,
        this also returns the totals so that you can caluclate percentages.
        Returns: Joy, Sad, Analytical, Tentative, Fear, Confident, Anger
    '''
    def get_tone_counts(self, df):
        total = df.shape[0]
        joy_counts = len(df[df.tone_name == "Joy"])
        sad_counts = len(df[df.tone_name == "Sadness"])
        analytical_counts = len(df[df.tone_name == "Analytical"])
        tentative_counts = len(df[df.tone_name == "Tentative"])
        fear_counts = len(df[df.tone_name == "Fear"])
        confident_counts = len(df[df.tone_name == "Confident"])
        anger_counts = len(df[df.tone_name == "Anger"])
        counts = [joy_counts, sad_counts, analytical_counts, tentative_counts, fear_counts, confident_counts, anger_counts]

        return counts, total

    '''
        Converts the times to local time based on offset and then counts
        up the number of tweets occuring during the 3 periods of the day.
        morning=5-11, mid-day=11-23, night=23-5
    '''
    def count_localised_time(self, times, offset):
        real_times = times / 1000
        morning = 0
        mid_day = 0
        late_night = 0
        for time in real_times:
            new_time = datetime.datetime.fromtimestamp(time + offset)
            if 5 <= new_time.hour <= 11:
                morning+=1
            elif 23 <= new_time.hour <= 24 or 0 <= new_time.hour <= 5:
                late_night+=1
            else:
                mid_day+=1
        return morning, mid_day, late_night

    def create_X_matrix(self, folder_path):
        X = pd.DataFrame(columns=['screen_name', 'joy', 'sad', 'analytical',
                                  'tentative', 'fear', 'confident', 'anger', 'tot_winter',
                                  'tot_spring', 'tot_summer', 'tot_fall', 'tot_tweets',
                                  'morning', 'mid_day', 'late_night'])
        counter = 0
        for file in os.listdir(folder_path):
            df = self.get_flattened_data(folder_path + file, 'tones', ['created_at', 'text_x', 'favorite_count', 'retweet_count', 'user', 'source'])
            X.loc[counter] = None
            X.loc[counter]['tot_tweets'] = df['user'][0]['statuses_count']
            X.loc[counter]['screen_name'] = df['user'][0]['screen_name']
            counts, total = self.get_tone_counts(df)
            tone_percentages = [(x / total) * 100 for x in counts]
            X.loc[counter]['joy'] = tone_percentages[0]
            X.loc[counter]['sad'] = tone_percentages[1]
            X.loc[counter]['analytical'] = tone_percentages[2]
            X.loc[counter]['tentative'] = tone_percentages[3]
            X.loc[counter]['fear'] = tone_percentages[4]
            X.loc[counter]['confident'] = tone_percentages[5]
            X.loc[counter]['anger'] = tone_percentages[6]

            morning, mid_day, late_night = self.localising_time(df['created_at'], df['user'][0]['utc_offset'])
            X.loc[counter]['morning'] = morning
            X.loc[counter]['mid_day'] = mid_day
            X.loc[counter]['late_night'] = late_night
            # analyze tone of each users tweets and attach back
            # determine how to find total number of tweets for season.
            # can I look at the tones for each season?
            # When looking at time of day for tweets take into account 'utc_offset'
            counter+=1





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

    # tda.graph_word_count_for_user(os.path.dirname(__file__) + "/../data/pbFollowers/users_tweets/patrickbeekman_tweets.json")
    tda.create_X_matrix(os.path.dirname(__file__) + "/../data/pbFollowers/merged/")

if __name__ == "__main__":
    main()