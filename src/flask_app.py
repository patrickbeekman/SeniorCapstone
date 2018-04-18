# Hello, Flask!
from flask import Flask, render_template, request
from bokeh.embed import components
import pickle
import os
import tweets_data_analysis

app = Flask(__name__, static_folder="/home/patt/Documents/senior_year/SeniorCapstone/src/templates/img")

# Index page, no args
@app.route('/')
def index():
    #getPlots = tweets_data_analysis.TweetsDataAnalysis()
    #tweet_freq = getPlots.time_series_frequency_analysis()

    # Create all of my plots
    #tweet_freq_script, tweet_freq_div = components(tweet_freq)
    data_path = os.path.dirname(__file__) + "/../data/"
    with open(data_path + 'plot_components.p', 'rb') as fp:
        plot_components = pickle.load(fp)


    name = request.args.get("name")
    if name == None:
        name = "Patrick"
    return render_template("index.html", name=name,
                           tweet_freq_script=plot_components['time_series_script'], tweet_freq_div=plot_components['time_series_div'],
                           tweets_hourly_script=plot_components['tweets_hour_script'], tweets_hourly_div=plot_components['tweets_hour_div'],
                           hourly_emotion_script=plot_components['hourly_emotion_script'], hourly_emotion_div=plot_components['hourly_emotion_div'],
                           unNormalized_FavsRTs_script=plot_components['unNormalized_FavsRTs_script'], unNormalized_FavsRTs_div=plot_components['unNormalized_FavsRTs_div'],
                           normalized_FavsRTs_script=plot_components['normalized_FavsRTs_script'], normalized_FavsRTs_div=plot_components['normalized_FavsRTs_div'],
                           norm_FavsRTs_emotion_script=plot_components['norm_FavsRTs_emotion_script'], norm_FavsRTs_emotion_div=plot_components['norm_FavsRTs_emotion_div'],
                           emotions_word_ct_script=plot_components['emotions_word_ct_script'], emotions_word_ct_div=plot_components['emotions_word_ct_div'],
                           days_of_week_script=plot_components['days_of_week_script'], days_of_week_div=plot_components['days_of_week_div'],
                           favs_RTS_by_DoW_script=plot_components['favs_RTS_by_DoW_script'], favs_RTS_by_DoW_div=plot_components['favs_RTS_by_DoW_div'],
                           favs_RTs_by_DoW_normalized_script=plot_components['favs_RTs_by_DoW_normalized_script'], favs_RTs_by_DoW_normalized_div=plot_components['favs_RTs_by_DoW_normalized_div'])

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)

