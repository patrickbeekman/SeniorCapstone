# TweetMaximizer

[![Build Status](https://travis-ci.org/patrickbeekman/SeniorCapstone.svg?branch=master)](https://travis-ci.org/patrickbeekman/SeniorCapstone)

An application to analyze the trends of your followers so you can maximize the potential of your tweets. My analysis looks at when and you should tweet about so you can gain the largest amount of favorites and retweets. This can be useful for businesses and advertisers who want to ensure each of their tweets makes the largest impact on their followers to help grow the businesses image on twitter. While useful for businesses it is also a great tool for twitter users who have something important to say and want to make sure the news gets spread! For example you may have something important to add to the #metoo campaign so you can use this application to find the best times to tweet and some keywords/emotional tones you may want to think about while drafting your tweet.

<a name="installation-and-dependencies"/>

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
1. [Clone/Download the repository](https://services.github.com/on-demand/github-cli/clone-repo-cli)
2. Navigate to wherever you cloned/downloaded the repository and go into the src folder where flask_app.py is located.
3. Open up a terminal at the location navigated to in step 2 and execute ```python flask_app.py SCREEN_NAME``` replacing the screen name with the twitter user you would like to analyze. (the screen name is the @name not the other one)
4. Now wait for the script to execute, Depending on the amount of followers the user has this can take a while. For about 200 followers it can take about [15-30 minutes initially**](#Note1).
5. Once the script has finished executing the website should now be viewable at localhost:5000/ in your favorite web browser.

## Developer Instructions

### Setting up developer environment
Setup developer environment? Huh?
* Code style checking is done with [PEP8](https://www.python.org/dev/peps/pep-0008/) and handled automatically with the [Python Pycharm IDE](https://www.jetbrains.com/pycharm/).

### Testing
All tests were written using [pytest](https://docs.pytest.org/en/latest/).
* Follow the [installation and dependencies section](#installation-and-dependencies)
* Clone the repository
* Open a terminal and navigate to the repository
* Run ```pytest``` in the terminal

### Contribution
This project is not open source although anyone is free to fork or download my application and modify it however you see fit.

## Resources

* [Project proposal](ProjectProposal.md)
* [Final Technical Report](FinalTechnicalReport.md)

## Notes

<a id="Note1">**</a> Note that it will only take this long the first time you run this script on a user. The reason this process takes so long requires some understanding as to what the scripts are doing. Below describes the process:
* Downloads all of the users followers from twitter
* Downloads ~2000 tweets for each of those followers
* Analyzes the tone of each tweet
* Aggregate all of the collected data
* Create the interactive plots of the data
* Send the plots to the Flask app which inserts them into the HTML
* And finally it hosts it locally so you can now view the finished product
Now hopefully you have a better idea of what this application is, how it works and how you can run this on any twitter user.
