# Exploring emotional trends on Twitter
#### By: Patrick Beekman

## Project Overview
With this project I plan to expand my knowledge on exploratory data science and web development. Since I took a machine learning course over the summer I have been very interested in what data has to offer and I can explore the meaning behind the data. This interest has pushed me to start a side project of analyzing my friends tweets to find fun and insightful meaning, statistics and correlations. With this capstone I am going to move in a different direction and learn how to pursue more complex analyses and how to best visualize my findings. To display these visualizations an interactive website seems to make the most sense so anyone can view, examine and explore my findings on any computer with internet access. 

This Capstone is a research project to delve into how people on twitter react to certain people, events and the four seasons. I want to look at how users interact emotionally with other users, specifically within their direct network of twitter 'friends'. It would also be interesting to look at how people react to a single user or a single tweet, for example looking at all of the replies to one of Trump's controversial tweets or how twitter users view Trump as a whole. Since the age of smartphones and social networks such as Twitter there have only been two presidents and it would be intriguing to compare and contrast the emotional response of their tweets, possibly seeing if I could align emotions with certain important events. Examining the state of a large group of twitter users over a period of months to years is of interest to me to find a pattern between emotion and the four seasons, I would expect more people to be sad in the Winter and happier in the Summer.

Since this is a research project I am not gearing it towards anyone specific, this is an exploratory analysis of the data based on my interests and questions talked about above. There is no end user for my application, just a website to display my findings that hopefully answer my questions. One possible use for my project would possibly be to help predict approval ratings on the president or other politicians. 

### Features
- Essential
  - Interact directly with the twitter api through HTTP requests
  - Grab all tweets from a specific user
  - Grab all replies from a specific tweet
  - Find 'network' of friends to a variable degree, friends of degree 1 are immediate followers while degree 2 would be that plus all of those followers followers
  - Save tweets into a json file
  - Interact directly with IBM Watson's tone analyze through HTTP requests
  - Convert tweets into a readable format for the tone analyzer
  - Analyze a collection of tweets saved in a text file
  - Create a basic website (unstylized) using the MEAN stack (without the mongoDB part)
  - Display static visualizations on the website
    - Calendar view to show emotional trends over time
    - Histograms to show common words/emojis used in different emotional buckets
    - Graph to compare ages/sexes with the emotional buckets
- Want to have
  - Stylize the website with css
  - Display interactive visualizations on the website
  - Create a network graph visualization to show the relationships I (or some generic user) have with friends
  - Align certain important emotional events with Tweets from the presidents
- Bells and Whistles
  - Allow a user on the website to type in their username for personalized statistics
  - Digital Ocean (or AWS) hosted website
  - Embed tweets directly on the website
  - Explore new and more complex visualizations

## Similar Works
Researchers at stanford did something [similar](https://web.stanford.edu/~jesszhao/files/twitterSentiment.pdf) by analyzing the sentiment of users tweets about presidential candidates. In this study they focused on creating a machine learning model to analyze tweets and predict an emotion, while I will be using IBM Watsons tone analyzer to do this. The difference between these is that the model used in the study only predicts a single emotion while Watson returns the specific likelihood for each of the five emotions which can give more insight into my data. One interesting idea the study took into account was the use of looking at emojis after they found a large percentage of tweets included them. I want to include this concept into my analysis as well, I will create my own mapping of common emojis into emotional buckets. Another piece of interest from this paper is what tweets they collected to represent the whole of a populations opinion about the candidates. They just simply looked for a small sample of keywords and the candidates name. I do not think this is enough and I am going to look at the replies to a candidate's(or any generic user) tweets to find the emotional response to that tweet but with enough of these pooled together I hope to gain an overview of the publics opinion about a candidate(specific user).

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
I have never used IBM Watson's tone analyzer or any of IBM's other products. Fortunately they use an api with HTTP endpoints which should be easy for me to use because I learned how to do something similar with twitters api. I am still unsure on how to use and interpret the tone analyzer so I will create a small dummy project to analyze a short text file composed of 5 sentences with different tones.

My knowledge on data science is rudimentary at best right now and I know that this will not be enough to complete the project. I am not sure about the best practices for cleaning data, intuitively exploring the data for answers, visualizing or any other parts that may be useful/necessary to do during the process. To minimize this risk I will talk to Dr. Parry and Professor Waldon for advice and use the data science book I borrowed from Dr. Tashakori as a guide and reference.

Using Travis-CI as a tool for continuous integration is completely new to me, it is a very interesting tool that I have been eager to learn for a while. The first day of class I learned what it was, read through a guide and setup the basic foundation to check for unittests. This is fine for rudimentary development but there seem to be more complex ways to use the tool that would be useful for my project including not allowing merging or pushing to master without first passing the Travis-CI requirements. I plan on reading through some more of their very helpful documentation on [their website](https://docs.travis-ci.com/user/getting-started/) and talking to Professor Waldon if I get stuck. From what I understand once I get it all setup initially then I shouldn't run into many problems after the fact.

The last area of risk is my web development experience, I do not have much prior knowledge other than a small part of the project I did in my Database class. This is the single riskiest part of the project and the risk I am going to spend the most time and effort minimizing. To start I am going to read ahead through the MEAN stack book that I have bought for my Advanced Software Engineering course and create a website to simply display 'hello world!'. From there I will read through the rest of the book focusing in on the parts that seem most relevant to my project. If the website part of my project is confusing and proving to take too much time then I can always create a simple python GUI in place of the website.
