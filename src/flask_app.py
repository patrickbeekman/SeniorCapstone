# Hello, Flask!
from flask import Flask, render_template, request
from bokeh.embed import components
import tweets_data_analysis

app = Flask(__name__)

# Index page, no args
@app.route('/')
def index():
    getPlots = tweets_data_analysis.TweetsDataAnalysis()
    tweet_freq = getPlots.time_series_frequency_analysis()
    tweet_freq_script, tweet_freq_div = components(tweet_freq)

    name = request.args.get("name")
    if name == None:
        name = "Edward"
    return render_template("index.html", name=name,
                           tweet_freq_script=tweet_freq_script, tweet_freq_div=tweet_freq_div)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)

