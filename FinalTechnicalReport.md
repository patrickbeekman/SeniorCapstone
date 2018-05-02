<H1 align="center">How to maximize your tweet potential</H1>
<p align="center">
By Patrick Beekman
April 25, 2018
</p>

---
## Abstract
Write my abstract here

**Keywords:** Python, Data Visualization, Twitter, Data Analysis, Bokeh

## Table of Contents
* [Introduction](#Intro)
* [Design, Development and Testing](#DDT)
  * [Design](#Design)
  * [Development](#Development)
  * [Testing](#Testing)
* [Results](#Results)
* [Conclusions and Future Work](#Conclusion)
* [References](#References)

---
<a name="Intro"/>

## Introduction

### Problem, Objective and Users
Twitter can be a wild and confusing place with a plethora of information readily available. The problem is that twitter is constantly being flooded with noise, often times making it difficult for your tweets to stand out and gain attention. That was the inspiration for this project, I have studied the best times to tweet, emotions and keywords that should be used to maximize the potential of your tweets and give it the most attention. The goal of this project was to create a simple way for users to analyze the trends of their followers and easily interpret the graphs to determine how to maximize the potential of their next tweet. The application needed to be easy to use because the users of this are not expected to know programming, only to have some basic knowledge of using computers. This application is meant for small business social media marketers so they can get a better idea about the trends of their followers and gear their tweets toward them. Increasingly businesses are using twitter to communicate with their customers/users, but with each new follower it becomes harder to appeal to your followers hence the need for my application. Other users of my application include general twitter users who have something important to say and want to ensure it makes the largest impact on their followers. One example my application could be used is if a user had thoughts or a story to contribute to the #metoo campaign, they may want to make sure as many people hear what they have to say as possible. 

### Relevant Background Information
Unsurprisingly enough twitter does something similar to my application except they have approached the problem from the other side. Instead of your twitter timeline (tweets from all your followers) being displayed chronologically they actually tailor it so tweets they think you will like appear closer to the top of your timeline[1](https://help.twitter.com/en/using-twitter/twitter-timeline). Twitter does this in an attempt to increase the amount of engagements each tweet receives, they define an engagement as the ”total number of times a user interacted with a Tweet. Clicks anywhere on the Tweet, including Retweets, replies, follows, likes, links, cards, hashtags, embedded media, username, profile photo, or Tweet expansion”[2](https://help.twitter.com/en/managing-your-account/using-the-tweet-activity-dashboard). If users are getting more impressions on their tweets they are then likely to use twitter more which is what twitter wants so they can increase their ad revenue. My project approaches from the other side and strives to maximize the potential impressions for a single tweet which in turn can help the user gain more attention on twitter and grow their business or spread a message to their followers. While my application is different from twitter's algorithm it is impossible for them to not overlap. For example the time that a tweet is sent may not be an accurate measure in my analysis because twitter will choose where to place the tweet in a users timeline affecting the time that it is seen by the users followers.

### Problem Scope and features
This project gives the user an overview of the general trends found in their followers. It specifically looks at the trends of when favorites and retweets happen throughout a day and how that relates to the tone of the tweet, the day of the week and the amounts of tweets per hour. It will also show you some keywords found in popular tweets of your followers split by emotion. The user can analyze these graphs on the website themselves to determine an ideal time and content for their tweet. It gives the user an easy way to aggregate all of their followers and view interactive visualizations of these general trends. My application does not give the user a single perfect time and content to tweet about. My application does not take into account replies to tweets, link clicks or other tweet engagement [2](https://help.twitter.com/en/managing-your-account/using-the-tweet-activity-dashboard) information that twitter takes into account for their timeline placement algorithm. It does not guarantee more engagement from your followers but simply tries to increase the likelihood that they will favorite or retweet your tweet. 

<a name="DDT"/>

## Design, Development and Testing

<a name="Design"/>

### Design

#### Software Modules
< Insert UML Diagram here >
This application was built across five classes to handle the different subsystems of logic. The five classes and how they relate to each other can be seen in UML diagram above [Figure 1.1](#Fig1.1). An integral piece to the application is the secrets.json file found in the /data/ folder, it should contain the users Twitter and IBM Watson API keys. More Information on how to get these keys keys can be found in the [Installation and Dependencies section of the Readme](LINK TO README SECTION). The TweepyGrabber class handles the connection to the twitter api as well as downloading users followers and tweets. The ToneAnalyzer class handles the connection to the IBM tone analyzer api, analyzing the tone of tweets, and merging this analysis back with the original tweet object. The TweetsDataAnalysis class handles all of the data cleaning, analysis and plotting. The TweetDriver class controls the logic of how those three classes connect with each other, it also passes all of the plot components up to the FlaskApp script. The FlaskApp script simple handles creating the flask application, adding the plots javascript objects to the pages HTML and finally rendering the HTML site.
< Insert application logic diagram here >
The logic flow of my application can be seen above in [Figure 1.2](#Fig1.2). Each color defines a different class where that logic takes place. The application starts when the flask app is run with the twitter screen name as an input parameter and the page is requested in a browser. The FlaskApp object then creates a TweetDriver object to control most of the applications logic flow. The TweetDriver class creates a TweepyGrabber object thus connecting to the Twitter api, note this will only connect if you have the correct keys inside the ./data/secrets.json file see [Readme for help](LINK TO README SECTION). The TweetDriver class then handles the input and feeds it into the TweepyGrabber object to start downloading all of the followers for that user. After that finishes the TweetDriver will get a response containing a list of the users followers, at which point it will download a max of 2,000 tweets for each follower and save this to ./data/SCREENNAME/users_tweets/. Next the TweetDriver class will create a ToneAnalyzer object which connects to IBM Watson’s tone analyzer API, pending that you have added your keys to the ./data/secrets.json file. The ToneAnalyzer then parses through each file of users tweets extracting the text into hundred tweet groupings (max per api request) to be sent for tone analysis to the api. These tone analysis’s are then merged back together into the original tweet object and again saved to ./data/SCREENNAME/merged/. Once the TweetDriver knows that this has been done for each follower it will ask the TweetsDataAnalysis object to aggregate all of the followers merged analysis files together. After aggregation the TweetsDataAnalysis then creates a multitude of plots saving each to ./data/SCREENNAME/plot_components.p. The logic is then pushed back up to the FlaskApp which adds the plot components to the index HTML page and renders everything. The user can now view the resultant HTML page at http://localhost:5000/. 

#### Libraries Used

| Library | Use |
| ------ | --- |
| Pandas | Made data analysis easy with datetime objects and grouping functionality. Allowed for easy manipulation, reading and writing of json files. |
| Numpy | Useful for data crunching in the TweetsDataAnalysis class. |
| Tweepy | Quickly and easily connect and use the Twitter api. |
| Flask | A quick and simple way to display my plots and analysis on a webpage. |
| Bokeh | Created all the plots, allowed easy embedding and gave the plots their interactiveness. |
| Watson Developer Cloud | A simple way to connect to the watson api in lieu of HTTP requests. |

<a name="Development"/>

### Development
The development of this project has been a roller coaster ride of productivity and confusion. This was in large part because I did not have a solid project idea until six weeks before the end of the semester. Not having a clear and defined goal didn’t seem like much of a risk at the time but should have been addressed and resolved before moving on. I had a vague direction to follow where I knew that I wanted do data analysis on tweets and display my findings on a website. That is where development started with the setup and creation of a simple single page MEAN stack website within the first two weeks. This was a risk for me because I have never done web development before, I thought by setting it up and getting a large part out of the way early it would reduce the risk later on, I later realized this was not the case. Once that was set up I could start working on what I was actually going to display on the site, the twitter analytics.

To start the analytics I first had to download all the data from twitter which was a quick and easy process because of the abundance of resources online. Then came time for the tone analysis of my tweets, at this point I still did not have a clear goal but thought the tones of tweets was interesting and wanted to explore the tweets with that in mind. Using IBM Watson’s api was new to me and a known risk, fortunately the documentation was really helpful and I quickly got this working on a small sample of the downloaded tweets. The first hurdle came when I realized the quirks and limitations of IBM Watson’s api. Three weeks later I was able to analyze all of my tweets and merge the tone analysis back with the original tweet objects. 

At this point I still did not know what question I wanted to ask about the collected data and spent a couple of weeks exploring the data. I finally figured out what I wanted to do with my project and settled on analyzing the best times and content to tweet. From here I hastily transitioned to brainstorming some visualizations I wanted and with the help of the [Bokeh library](BOKEH) was able to quickly feed my data in and get the graphs I wanted. Once I had some visualizations I then needed to display them on my MEAN stack website, this turned out to be a huge pain that I could not figure out. With time running short I scraped the whole MEAN stack and replaced it with a python flask app. The flask application was easy to understand, implement and embed my plots in. I transitioned and got a working website with my plots in a single night, which is much quicker and less of a pain than the bulky MEAN stack. The last two weeks of the project were then just finalizing my code and adding some new visualizations.

<a name="Testing"/>

### Testing
Creating and keeping up with tests was a challenge for me throughout the project development. I used [pytest](https://docs.pytest.org/en/latest/) to automate the testing framework as well as [Travis continuous integration](https://travis-ci.org/) to keep my github repository clean and functional. I did not follow the agile methodology of test first drive development, mainly because I was unsure what any of my code would look like beforehand. I often times found myself having to program in debug mode and try out multiple things before moving on to the next piece of code.
I started my testing on the TweepyGrabber class which turned out to be harder than I initially thought. It was difficult because I had to write tests that would check for good and bad api connections, as well as finding twitter users to run my tests on. For example testing that my application handles users who have never tweeted, I couldn’t just pick a random user who had never tweeted and hoped that they never did tweet while my test existed. I ended up having to create some basic twitter accounts to simulate these specific users. One of the test twitter accounts got marked as a bot which I had to verify that it was not, for now it is safe but who knows if twitter will mark it as a bot in the future and delete the account. 
Other testing was done on the ToneAnalyzer class which I ran into similar issues specifically with the api requests and reaching api quotas. Testing other methods was easier because I could create test json files and feed those into my methods. I mainly tested the helper methods and less so the control flow methods. For example I tested the method that would parse the tweet object and return a string of cleaned tweets instead of the method that looped through the users tweets and called this method.
I did not test the TweetDriver class for a similar reason stated above because it was just controlling the logic flow of the application. I did not test the TweetsDataAnalysis class either because all of the methods were used to create my visualizations which was not easy to test or defined some basic control flow of creating all the plots. The plotting methods either created the visual that I wanted or it did not, if it didn’t I would know and fix what was necessary. The FlaskApp class was also not tested because of its bare bones nature and time limitations.

<a name="Results"/>

## Results
Write results here.

<a name="Conclusion"/>

## Conclusions and Future Work
Conclusion.

<a name="References"/>

## References
refs.
