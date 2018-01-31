# Exploring emotional trends on Twitter
#### By: Patrick Beekman

## Project Overview
With this project I plan to expand my knowledge on exploratory data science and web development. Since I took a machine learning course over the summer I have been very interested in what data has to offer and I can explore the meaning behind the data. This interest has pushed me to start a side project of analyzing my friends tweets to find fun and insightful meaning, statistics and correlations. With this capstone I am going to move in a different direction and learn how to pursue more complex analyses and how to best visualize my findings. To display these visualizations an interactive website seems to make the most sense so anyone can view, examine and explore my findings on any computer with internet access. 

This Capstone is a research project to delve into how people on twitter react to certain people, events and the four seasons. I want to look at how users interact emotionally with other users, specifically within their direct network of twitter 'friends'. It would also be interesting to look at how people react to a single user or a single tweet, for example looking at all of the replies to one of Trump's controversial tweets or how twitter users view Trump as a whole. Since the age of smartphones and social networks such as Twitter there have only been two presidents and it would be intriguing to compare and contrast the emotional response of their tweets, possibly seeing if I could align emotions with certain important events. Examining the state of a large group of twitter users over a period of months to years is of interest to me to find a pattern between emotion and the four seasons, I would expect more people to be sad in the Winter and happier in the Summer.

Since this is a research project I am not gearing*** it towards anyone specific, this is an exploratory analysis of the data based on my interests and questions talked about above. There is no end user for my application, just a website to display my findings that hopefully answer my questions. One possible use for my project would possibly be to help predict approval ratings on the president or other politicians. 

### Features
- Essential
  - Interact directly with the twitter api through HTTP requests
  - Grab all tweets from a specific user
  - Grab all replies from a specific tweet
  - Find 'network' of friends to a variable degree, friends of degree 1 are immediate followers while degree 2 would be that plus all of those followers followers
  - Save tweets into a json file
  - Interact directly with IBM Watsons tone analyze through HTTP requests
  - Convet tweets into a readable format for the tone analyzer
  - Analyze a collection of tweets saved in a text file
  - Create a basic website (unstylized) using the MEAN stack (without the mongoDB part)
  - Display static visualizations on the website
    - Calendar view to show emotional trends over time
    - Histograms to show common words/emojis used in different emotional buckets
    - Graph to compare ages/sexes with the emotional buckets
- Want to have
  - Stylize the website with css
  - Display interacive visualizations on the website
  - Create a network graph visualization to show the relationships I (or some generic user) have with friends
  - Align certain important emotional events with Tweets from the presidents
- Bells and Whistles
  - Allow a user on the website to type in their username for personalized statistics
  - Digital Ocean (or AWS) hosted website
  - Embed tweets directly on the website
  - Explore new and more complex visualizations

## Similar Works
Researchers at stanford did something [similar](https://web.stanford.edu/~jesszhao/files/twitterSentiment.pdf) by analyzing the sentiment of users tweets about presidental candidates. In this study they focused on creating a machine learning model to analyze tweets and predict an emotion, while I will be using IBM Watsons tone analyzer to do this. The difference between these is that the model used in the study only predicts a single emotion while Watson returns the specific likelihoods for each of the five emotions which can give more insight into my data. One interesting idea the study took into account was the use of looking at emojis after they found a large percentage of tweets included them. I want to include this concept into my analysis as well, I will create my own mapping of common emojis into emotional buckets. Another piece of interest from this paper is what tweets they collected to represent the whole of a populations opinion about the candidates. They just simply looked for a small sample of keywords and the candidates name. I do not think this is enough and I am going to look at the replies to a candidate's(or any generic user) tweets to find the emotional response to that tweet but with enough of these pooled together I hope to gain an overview of the publics opion about a candidate(specific user).

## Previous Experience
Over winter break I have been working on a small side project accessing the twitter api and collecting some tweets for a basic analysis. This project is useful because the knowledge learned from it will be the starting point for this project. This knowledge of interacting with an api through HTTP requests will also be applicable for using IBM Watsons tone analyzer. Other experience includes some basic web development with PHP to connect a webpage to a mysql backed which we did in my Database class. In my machine learning course over the summer I was formally introduced to python, data manipulation and visualization techniques. I was also introduced to some powerful python libraries such as pandas, numpy and matplotlib which all directly be used for this project.

## Technology
I will be using Travis-CI to handle the continuous integration of my project and set it up so that none of my feature branches can be merged into master without passing all its tests and code style requirements. The same will be done for commits directly to the master branch.
- Travis-CI
- [IBM Watson Tone Analyzer](https://www.ibm.com/watson/services/tone-analyzer/)
- python
- PEP8 checkstyle
- pip
- pytest
- ~~M~~EAN stack (Express, Angular, Node)
- matplotlib
- Pandas
- Numpy
- Github

## Risk Areas
I have never used IBM Watson's tone analyzer or any of IBM's other products. Fortunately they just have an api with HTTP endpoints that are standard and should be easy to access

never used ibm watson but Its just an api and i know how to access it with HTTP requests
website design knowledge is lacking so it will not be too crazy but at least the foundation will be there for me to expand on the knowledge I learn from this capstone project. Going to read the MEAN book for adv. software engineering and talk to my friend (webb) who knows web dev
not much experience with the whole of the data science pipeline, going to talk to Waldon and Parry for advice
Included in the data science pipeline would be visualizing the data which I do not have much practice other than in machine learning, I am in Parry's data visualization class right now
