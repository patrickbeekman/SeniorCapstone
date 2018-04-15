import pandas as pd
import numpy as np
import json
import os
from pandas.io.json import json_normalize
import datetime
import time
import math
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt
import nltk
import random
import operator
from nltk.corpus import stopwords
from bokeh.plotting import figure, output_file, show
from bokeh.models.annotations import Title
from bokeh.models.glyphs import VBar
from bokeh.layouts import gridplot
from bokeh.transform import factor_cmap
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    DataRange1d,
    LinearAxis,
    LinearColorMapper,
    Plot,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
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
        data_flattened = pd.io.json.json_normalize(data, record_path=record_path, meta=meta, errors='ignore')
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
    def count_localised_time(self, times, file, offset=0):
        real_times = times / 1000
        morning = 0
        mid_day = 0
        late_night = 0
        standardized_times = []
        if offset is None:
            offset = 0
        for time in real_times:
            new_time = datetime.datetime.fromtimestamp(time + offset)
            standardized_times.append(new_time)
            if 5 <= new_time.hour <= 11:
                morning+=1
            elif 23 <= new_time.hour <= 24 or 0 <= new_time.hour <= 5:
                late_night+=1
            else:
                mid_day+=1
        return morning, mid_day, late_night, standardized_times

    def count_sad_happy_four_seasons(self, tone_names, std_times):
        seasons = {'spring_sad':0, 'summer_sad':0, 'fall_sad':0, 'winter_sad':0,
                   'spring_joy':0, 'summer_joy':0, 'fall_joy':0, 'winter_joy':0}
        for index, tone in tone_names.iteritems():
            if tone != 'Joy' and tone != 'Sadness':
                continue
            month = pd.to_datetime(std_times.iloc[index]).month
            if month in range(3, 5+1):
                # spring
                if tone == 'Joy':
                    seasons['spring_joy'] += 1
                elif tone == 'Sadness':
                    seasons['spring_sad'] += 1
            elif month in range(6, 8+1):
                #summer
                if tone == 'Joy':
                    seasons['summer_joy'] += 1
                elif tone == 'Sadness':
                    seasons['summer_sad'] += 1
            elif month in range(9, 11+1):
                #fall
                if tone == 'Joy':
                    seasons['fall_joy'] += 1
                elif tone == 'Sadness':
                    seasons['fall_sad'] += 1
            else:
                #winter
                if tone == 'Joy':
                    seasons['winter_joy'] += 1
                elif tone == 'Sadness':
                    seasons['winter_sad'] += 1
        return seasons

    def create_X_matrix(self, folder_path, output_file_path):
        X = pd.DataFrame(columns=['screen_name', 'joy', 'sad', 'analytical',
                                  'tentative', 'fear', 'confident', 'anger',
                                  'tot_tweets', 'morning', 'mid_day', 'late_night',
                                  'spring_sad', 'summer_sad', 'fall_sad', 'winter_sad',
                                  'spring_joy', 'summer_joy', 'fall_joy', 'winter_joy'])
        counter = 0
        all_files = os.listdir(folder_path)
        tot_files = len(all_files)
        for file in all_files:
            print('{:.2%}'.format(counter/tot_files))
            df = self.get_flattened_data(folder_path + file, 'tones', ['created_at', 'user', 'source'])
            X.loc[counter] = None
            try:
                total = df['user'][0]['statuses_count']
            except ValueError:
                total = 0
            except IndexError:
                continue
            try:
                sn = df['user'][0]['screen_name']
            except ValueError:
                sn = None

            X.loc[counter]['tot_tweets'] = total
            X.loc[counter]['screen_name'] = sn
            counts, total = self.get_tone_counts(df)
            #tone_percentages = [(x / total) * 100 for x in counts]
            X.loc[counter]['joy'] = counts[0] #tone_percentages[0]
            X.loc[counter]['sad'] = counts[1] #tone_percentages[1]
            X.loc[counter]['analytical'] = counts[2] #tone_percentages[2]
            X.loc[counter]['tentative'] = counts[3] #tone_percentages[3]
            X.loc[counter]['fear'] = counts[4] #tone_percentages[4]
            X.loc[counter]['confident'] = counts[5] #tone_percentages[5]
            X.loc[counter]['anger'] = counts[6] #tone_percentages[6]

            morning, mid_day, late_night, std_times = self.count_localised_time(df['created_at'], file, df['user'][0]['utc_offset'])
            X.loc[counter]['morning'] = morning
            X.loc[counter]['mid_day'] = mid_day
            X.loc[counter]['late_night'] = late_night
            s = pd.Series(std_times, index=df.index, name='std_times')

            seasons = self.count_sad_happy_four_seasons(df['tone_name'], s)
            # attach the seasons to X
            X.loc[counter]['spring_sad'] = seasons['spring_sad']
            X.loc[counter]['summer_sad'] = seasons['summer_sad']
            X.loc[counter]['fall_sad'] = seasons['fall_sad']
            X.loc[counter]['winter_sad'] = seasons['winter_sad']
            X.loc[counter]['spring_joy'] = seasons['spring_joy']
            X.loc[counter]['summer_joy'] = seasons['summer_joy']
            X.loc[counter]['fall_joy'] = seasons['fall_joy']
            X.loc[counter]['winter_joy'] = seasons['winter_joy']

            # analyze tone of each users tweets and attach back
            # determine how to find total number of tweets for season.
            # can I look at the tones for each season?
            # When looking at time of day for tweets take into account 'utc_offset'
            counter+=1
        X.to_pickle(output_file_path)
        return X

    def create_boxplot(self, data_path, save_path):
        df = pd.read_pickle(data_path)
        df = df.apply(pd.to_numeric, errors='ignore')
        descriptive_stats = df.describe()
        df_emotions = df[['joy', 'sad', 'analytical', 'tentative', 'fear', 'confident', 'anger']]
        plt.figure()
        df_emotions.plot.box()
        plt.title("Emotions boxplots")
        plt.savefig(save_path + "emotions_boxplot.png")
        plt.clf()

        df_time_of_day = df[['morning', 'mid_day', 'late_night']]
        plt.figure()
        df_time_of_day.plot.box()
        plt.title("Time of day boxplots")
        plt.savefig(save_path + "timeOfDay_boxplot.png")
        plt.clf()

        df_seasons = df[['spring_sad', 'spring_joy', 'summer_sad', 'summer_joy',
                         'fall_sad', 'fall_joy', 'winter_sad', 'winter_joy']]
        plt.figure()
        df_seasons.plot.box()
        plt.title("Joy/Sad broken down by season")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(save_path + "joy_sad_Seasons_boxplot.png")
        print("hello")


    def time_series_frequency_analysis(self):
        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/merged/"
        dir_files = os.listdir(data_path)

        counts_of_tweets = {}

        for filename in dir_files:
            df = pd.read_json(data_path + filename)
            df = df.set_index(df['created_at'])
            p = df.groupby(pd.TimeGrouper("D"))
            freq_of_tweets = p['created_at'].count()
            freq_dict = freq_of_tweets.to_dict()
            for key, value in freq_dict.items():
                try:
                    counts_of_tweets[key.to_datetime()] += value
                except KeyError:
                    counts_of_tweets[key.to_datetime()] = value
            # index like freq_dict.get(pd.Timestamp('2018-01-31'))

        dates = np.fromiter(counts_of_tweets.keys(), dtype='datetime64[us]')
        counts = np.fromiter(counts_of_tweets.values(), dtype=float)

        # window_size = 30
        # window = np.ones(window_size) / float(window_size)
        # counts_avg = np.convolve(counts, window, 'same')

        # output to static HTML file
        tweet_freq_plot_path = data_path + "../plots/Tweet_freq_by_day.html"
        output_file(tweet_freq_plot_path, title="Tweet frequency of my followers")

        # create a new plot with a a datetime axis type
        p = figure(width=800, height=350, x_axis_type="datetime")

        # add renderers
        p.circle(dates, counts, size=4, color='blue', alpha=0.8)
        # p.line(dates, counts_avg, color='grey')

        p.title.text = "Tweet Frequency of @patrickbeekman's followers"
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = '# of Tweets'

        show(p)

        print("Frequency of tweets graph created!")


    def time_series_day_of_week_plot(self):
        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/merged/"
        dir_files = os.listdir(data_path)

        counts_of_tweets = {}

        for filename in dir_files:
            df = pd.read_json(data_path + filename)
            df = df.set_index(df['created_at'])
            temp = pd.DatetimeIndex(df['created_at'])
            df['weekday'] = temp.weekday_name
            p = df.groupby(df['weekday'])
            freq_of_tweets = p['created_at'].count()
            freq_dict = freq_of_tweets.to_dict()
            for key, value in freq_dict.items():
                try:
                    counts_of_tweets[key] += value
                except KeyError:
                    counts_of_tweets[key] = value
            # index like freq_dict.get(pd.Timestamp('2018-01-31'))

        #dates = np.fromiter(counts_of_tweets.keys(), dtype=object)
        #counts = np.fromiter(counts_of_tweets.values(), dtype=float)

        # output to static HTML file
        tweet_freq_plot_path = data_path + "../plots/Tweet_freq_day_of_week.html"
        output_file(tweet_freq_plot_path)

        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        counts_of_week = [counts_of_tweets[days_of_week[0]], counts_of_tweets[days_of_week[1]],
                          counts_of_tweets[days_of_week[2]], counts_of_tweets[days_of_week[3]],
                          counts_of_tweets[days_of_week[4]], counts_of_tweets[days_of_week[5]],
                          counts_of_tweets[days_of_week[6]]]

        source = ColumnDataSource(data=dict(days_of_week=days_of_week, counts_of_week=counts_of_week))

        hover = HoverTool(tooltips=[
            ('days_of_week', '@days_of_week'),
            ('counts_of_week', '@counts_of_week'),
        ])

        p = figure(x_range=days_of_week, plot_height=350, toolbar_location=None, title="Freq of Tweets by Day of Week", tools=[hover])
        p.vbar(x='days_of_week', top='counts_of_week', width=0.9, source=source,
               line_color='white', fill_color=["#ff0000", "#ff4000", "#ff8000", "#ffbf00", "#ffsff00", "#bfff00", "#80ff00"])

        show(p)


    def tweets_per_hour_plot(self, emotion=None, color="#b3de69"):
        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/merged/"
        dir_files = os.listdir(data_path)

        counts_of_tweets = {}

        for filename in dir_files:
            #df = pd.read_json(data_path + filename)
            df = self.get_flattened_data(data_path+filename, 'tones', ['user', 'created_at'])
            if emotion is not None:
                try:
                    df = df[df.tone_name == emotion]
                except AttributeError:
                    continue
            df['created_at'] = df['created_at']/1000
            offset = 0
            try:
                offset = df['user'][0]['utc_offset']
            except (IndexError, KeyError):
                offset = 0
            if offset is None:
                offset = 0
            #df['std_time'] = df['created_at'] + pd.TimedeltaIndex(df['offset'], unit='s')
            df['std_time'] = df['created_at'] + offset
            df['std_time'] = [datetime.datetime.fromtimestamp(x) for x in df['std_time']]
            df = df.set_index(df['std_time'])
            temp = pd.DatetimeIndex(df['std_time'])
            df['hour'] = temp.hour
            p = df.groupby(df['hour'])
            freq_of_tweets = p['std_time'].count()
            freq_dict = freq_of_tweets.to_dict()
            for key, value in freq_dict.items():
                try:
                    counts_of_tweets[key] += value
                except KeyError:
                    counts_of_tweets[key] = value

        hours = np.fromiter(counts_of_tweets.keys(), dtype=float)
        hours+=1
        numTweets = np.fromiter(counts_of_tweets.values(), dtype=float)

        # output to static HTML file
        if emotion is None:
            hourly_freq_plot_path = data_path + "../plots/Hourly_freq_plot.html"
            output_file(hourly_freq_plot_path)

        source = ColumnDataSource(data=dict(hours=hours, numTweets=numTweets))

        hover = HoverTool(tooltips=[
            ('hours', '@hours'),
            ('numTweets', '@numTweets'),
        ])

        xdr = DataRange1d()
        ydr = DataRange1d()
        plot = Plot(x_range=xdr, y_range=ydr, plot_width=500, plot_height=500,
                    h_symmetry=False, v_symmetry=False, min_border=0, tools=[hover])

        glyph = VBar(x="hours", top="numTweets", bottom=0, width=0.5, fill_color=color)
        plot.add_glyph(source, glyph)

        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')

        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')

        t = Title()
        if emotion is not None:
            t.text = "(" + emotion + ") Number of Tweets by Hour"
        else:
            t.text = "(all emotions) Number of Tweets by Hour"
        plot.title = t
        plot.xaxis.axis_label = 'Hours'
        plot.yaxis.axis_label = 'Number of Tweets'

        if emotion is not None:
            return plot
        else:
            show(plot)


    def hourly_plot_by_emotion(self):

        emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Analytical', 'Tentative', 'Confident']
        colors = ['#ffff4d', '#668cff', '#ff3333', '#e67300', '#5cd65c', '#ff33ff', '#00ff00']

        plots = []
        for index, emotion in enumerate(emotions):
            plots.append(self.tweets_per_hour_plot(emotion=emotion, color=colors[index]))

        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/plots/"
        output_file(data_path + "multiple_emotions_by_hour.html")

        grid = gridplot(plots, ncols=3, plot_width=350, plot_height=350)
        show(grid)

    def normalized_num_favs_retweets_by_hour(self, emotion=None, normalize=True):
        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/merged/"
        dir_files = os.listdir(data_path)

        counts_of_favs = {}
        counts_of_rts = {}

        for filename in dir_files:
            # df = pd.read_json(data_path + filename)
            df = self.get_flattened_data(data_path+filename, 'tones', ['user', 'text', 'text_x', 'created_at', 'favorite_count', 'retweet_count'])
            if len(df) == 0:
                continue
            try:
                df = df[df.text_x.str.startswith('RT') == False]
            except AttributeError:
                try:
                    df = df[df.text.str.startswith('RT') == False]
                except AttributeError:
                    continue
            if emotion is not None:
                try:
                    df = df[df.tone_name == emotion]
                except AttributeError:
                    continue
            df['created_at'] = df['created_at']/1000
            offset = 0
            try:
                offset = df['user'].iloc[0]['utc_offset']
            except (IndexError, KeyError):
                offset = 0
            try:
                fllwrs = df['user'].iloc[0]['followers_count']
            except (IndexError, KeyError):
                fllwrs = 1
            if offset is None:
                offset = 0
            #df['std_time'] = df['created_at'] + pd.TimedeltaIndex(df['offset'], unit='s')
            df['std_time'] = df['created_at'] + offset
            df['std_time'] = [datetime.datetime.fromtimestamp(x) for x in df['std_time']]
            df = df.set_index(df['std_time'])
            temp = pd.DatetimeIndex(df['std_time'])
            df['hour'] = temp.hour
            p = df.groupby(df['hour'])
            if not normalize:
                fllwrs = 1
            fav_counts = (p['favorite_count'].sum()/fllwrs).to_dict()
            rt_counts = (p['retweet_count'].sum()/fllwrs).to_dict()
            for key, value in fav_counts.items():
                if math.isnan(value):
                    continue
                try:
                    counts_of_favs[key] += value
                except KeyError:
                    counts_of_favs[key] = value
            for key2, value2 in rt_counts.items():
                if math.isnan(value2):
                    continue
                try:
                    counts_of_rts[key2] += value2
                except KeyError:
                    counts_of_rts[key2] = value2

        favs = np.array(list(counts_of_favs.items()), dtype=float)
        favs = sorted(favs, key=lambda x: x[0])
        rts = np.array(list(counts_of_rts.items()), dtype=float)
        rts = sorted(rts, key=lambda x: x[0])

        # output to static HTML file
        if emotion is None:
            if normalize:
                hourly_freq_plot_path = data_path + "../plots/Normalized_Hourly_favs_rts_plot.html"
            else:
                hourly_freq_plot_path = data_path + "../plots/Hourly_favs_rts_plot.html"
            output_file(hourly_freq_plot_path)

        favs_source = ColumnDataSource(dict(hours=[x[0] for x in favs], favorites=[y[1] for y in favs]))
        rts_source = ColumnDataSource(dict(hours=[x[0] for x in rts], retweets=[y[1] for y in rts]))

        hover = HoverTool(tooltips=[
            ('hours', '@hours'),
            ('favorites', '@favorites'),
            ('retweets', '@retweets'),
        ])

        if normalize:
            normText = '(Normalized by # of Followers)'
        else:
            normText = ''

        if emotion is None:
            title = 'Number of Fav\'s and RT\'s by Hour' + normText
        else:
            title = '(' + emotion + ') Number of Fav\'s/RT\'s by Hour ' + normText

        fig = figure(plot_width=500, plot_height=500, tools=[hover], title=title,
                     x_axis_label='Hours', y_axis_label=normText + ' Amount of Fav\'s/RT\'s')

        fig.line(x='hours', y='favorites', source=favs_source, line_width=3,
                 line_color='#e0b61d', legend='Favorites')
        fig.line(x='hours', y='retweets', source=rts_source, line_width=3,
                 line_color='#20a014', legend='Retweets')
        fig.legend.location = "top_left"

        if emotion is None:
            show(fig)
        else:
            return fig

    def normalized_favs_rts_plot_by_emotion(self):

        emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Analytical', 'Tentative', 'Confident']
        #colors = ['#ffff4d', '#668cff', '#ff3333', '#e67300', '#5cd65c', '#ff33ff', '#00ff00']

        plots = []
        for emotion in emotions:
            plots.append(self.normalized_num_favs_retweets_by_hour(emotion=emotion))

        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/plots/"
        output_file(data_path + "favs_rts_multiple_emotions_by_hour.html")

        grid = gridplot(plots, ncols=3, plot_width=350, plot_height=350)
        show(grid)

    def word_choice_by_emotion_barchart(self, emotion):
        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/merged/"
        dir_files = os.listdir(data_path)

        most_common_words = {}

        for filename in dir_files:
            df = self.get_flattened_data(data_path+filename, 'tones', ['user', 'text', 'text_x', 'created_at', 'favorite_count', 'retweet_count'])
            try:
                df = df[df.tone_name == emotion]
            except AttributeError:
                continue
            df = df.sort_values(by=['favorite_count', 'retweet_count'], ascending=False)
            df_subset = df[:np.min([len(df), 250])]
            # Somehow sort the tweets by favorite count
            # Removing common words: https://stackoverflow.com/questions/9953619/technique-to-remove-common-wordsand-their-plural-versions-from-a-string
            #nltk.download("stopwords")
            s = set(stopwords.words('english'))
            myWords = {'RT', 'I', '.', 'The', 'like', 'I\'m', 'My', 'This', 'get', 'It\'s', 'Who', 'What', 'Where', 'When',
                     'Why', 'A', '`', '&amp;', '-'}
            s.update(myWords)
            try:
                text_notflat = [filter(lambda w: not w in s, tweet.split()) for tweet in df_subset['text_x']]
            except AttributeError:
                try:
                    text_notflat = [filter(lambda w: not w in s, tweet.split()) for tweet in df_subset['text']]
                except AttributeError:
                    continue
            word_counter = Counter(chain.from_iterable(text_notflat))
            most_common = word_counter.most_common(100)
            try:
                words = list(zip(*most_common))[0]
                values = list(zip(*most_common))[1]
            except IndexError:
                continue
            for i in range(len(words)):
                if math.isnan(values[i]):
                    continue
                try:
                    most_common_words[words[i]] += values[i]
                except KeyError:
                    most_common_words[words[i]] = values[i]

        sorted_x = sorted(most_common_words.items(), key=operator.itemgetter(1), reverse=True)
        #print(sorted_x)
        #print(len(sorted_x))

        hourly_freq_plot_path = data_path + "../plots/emotion_word_count_plot.html"
        output_file(hourly_freq_plot_path)

        hover = HoverTool(tooltips=[
            ('words', '@words'),
            ('amounts', '@amounts'),
        ])

        words = [x[0] for x in sorted_x[:25]]
        amounts = [x[1] for x in sorted_x[:25]]

        source = ColumnDataSource(data=dict(words=words, amounts=amounts))

        p = figure(x_range=words, y_range=(0, max(amounts)+100), plot_height=350, title=emotion + " Word Counts",
                   toolbar_location=None, tools=[hover])

        p.vbar(x='words', top='amounts', width=0.9, source=source)

        p.xgrid.grid_line_color = None
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.xaxis.major_label_orientation = math.pi / 2

        show(p)


    def plot_heatmap(self):
        data_path = os.path.dirname(__file__) + "/../data/pbFollowers/merged/"
        dir_files = os.listdir(data_path)
        data = pd.read_csv(data_path+"../unemployment_data.csv")

        data['Year'] = data['Year'].astype(str)
        data = data.set_index('Year')
        data.drop('Annual', axis=1, inplace=True)
        data.columns.name = 'Month'

        years = list(data.index)
        months = list(data.columns)

        # reshape to 1D array or rates with a month and year for each row.
        df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()

        print("hello")



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

    #tda.graph_word_count_for_user(os.path.dirname(__file__) + "/../data/pbFollowers/users_tweets/patrickbeekman_tweets.json")
    # tda.create_X_matrix(os.path.dirname(__file__) + "/../data/pbFollowers/merged/",
    #                     os.path.dirname(__file__) + "/../data/pbFollowers/X_matrix.pkl")
    # tda.create_boxplot(os.path.dirname(__file__) + "/../data/pbFollowers/X_matrix.pkl",
    #                    os.path.dirname(__file__) + "/../data/pbFollowers/plots/")


    # tda.time_series_frequency_analysis()
    # tda.time_series_day_of_week_plot()
    # tda.tweets_per_hour_plot()
    #tda.hourly_plot_by_emotion()
    # tda.plot_heatmap()
    # tda.normalized_num_favs_retweets_by_hour(normalize=True)
    # tda.normalized_favs_rts_plot_by_emotion()
    tda.word_choice_by_emotion_barchart('Joy')


if __name__ == "__main__":
    main()