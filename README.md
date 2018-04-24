# SeniorCapstone

[![Build Status](https://travis-ci.org/patrickbeekman/SeniorCapstone.svg?branch=master)](https://travis-ci.org/patrickbeekman/SeniorCapstone)

An exploratory analysis of a users followers to determine when and what to tweet about to maximize your tweets potential to gain the most amount of attention.
This tweet attention can be defined as the amount of favorites and retweets a tweet receives.

## Installation and Dependencies

This project use a python Flask app to display my findings. To get started you will first need to clone this repo to your workspace.
* You will then need to install [anaconda python 3.6](https://conda.io/docs/user-guide/install/index.html)
* You will then need to install these python packages, which you can easily install these with [python package manager pip](https://pip.pypa.io/en/stable/installing/).
  * Pandas ```pip install pandas```
  * Requests ```pip install requests```
  * Numpy ```pip install numpy```
  * Pymongo ```pip install pymongo```
  * tweepy ```pip install tweepy```
  * Flask ```pip install flask```
  * Bokeh ```pip install bokeh```
  * Watson Developer Cloud ```pip install --upgrade watson-developer-cloud```

## About and Usage

This application can be used at a very high level by:
1. Clone the repo
2. Navigate to repo/src (where flask_app.py is located)
3. Open up a terminal and execute ```python flask_app.py SCREEN_NAME``` replacing with the screen name of the twitter user you would like to analyze.
4. Now wait for the scripts to execute, Depending on the amount of followers the user has this can take a while. For about 200 followers it can take about [15-30 minutes initially**](#Note1).
5. Once the script has finished executing the website should now be viewable at localhost:5000/ in your favorite web browser.


<a id="Note1">**</a> Note that it will only take this long the first time you run this script on a user. The reason this process takes so long requires some understanding as to what the scripts are doing.
* Downloads all of the users followers from twitter
* Downloads ~2000 tweets for each of those followers
* Analyzes the tone of each tweet
* Aggregate all of the collected data
* Create the interactive plots of the data
* Send the plots to the Flask app which inserts them into the HTML
* And finally it hosts it locally so you can now view the finished product
Now hopefully you have a better idea of what this application is, how it works and how you can run this on any twitter user.
