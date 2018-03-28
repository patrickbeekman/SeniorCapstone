# SeniorCapstone

[![Build Status](https://travis-ci.org/patrickbeekman/SeniorCapstone.svg?branch=master)](https://travis-ci.org/patrickbeekman/SeniorCapstone)

An exploratory tone analysis of twitter data and how the emotions and frequency of tweets changes in respect to the months and seasons. 

My Tweets: Happy vs Sad per month            |  Tones by percentage of all my tweets
:-------------------------:|:-------------------------:
![Happy vs Sad](/data/plots/my_tweets_joy_vs_sad_stacked_bar.png)  |  ![Pie chart](/data/plots/my_tweets_pie_chart.png) 

## Installation

This project uses the MEAN stack for the web development and python with its related dependencies to hanlde the exploratory data analysis. To get started you will first need to clone this repo to your workspace.
* You will first need to install [anaconda python 3.6](https://conda.io/docs/user-guide/install/index.html)
* You will then need to install these python packages, which you can easily install these with [python package manager pip](https://pip.pypa.io/en/stable/installing/).
  * Pandas ```pip install pandas```
  * Requests ```pip install requests```
  * Numpy ```pip install numpy```
  * Pymongo ```pip install pymongo```
  * tweepy ```pip install tweepy```
  * Watson Developer Cloud ```pip install --upgrade watson-developer-cloud```
* For the web development stuff you will need to use [node package manager(npm) to install all dependencies](https://nodejs.org/en/) which comes downloaded with node.
  * Then navigate to the root directory of this project and from the terminal run ```npm install```. This will install all of the web dependencies needed to run the server.
  * To test that this is setup correctly you should be able to run ```node server.js``` from the root directory of the project, you should then be able to navigate to [http://localhost:8080/](http://localhost:8080/) to view the web app.
  
## Usage

The bulk of the usage of the application in its current state is done through the three python scripts ```tweepy_grabber.py, tone_analyzer.py and tweets_data_analysis.py``` which will grab all the tweets from a specific user and analyze the emotion of each tweet visualizing it on some nice plots that can be found in ```/project_root/data/plots/```.
1. You will first need to create a twitter account and then create a [twitter app here](https://apps.twitter.com/)
   1. Once created open the app and click on 'Keys and Access Tokens'
   2. Under the title 'Application Seetings' copy and paste your 'Consumer Key' (like username) and your 'Consumer Secret' (like password).
2. Open the file ```tweepy_grabber.py```
   1. In the main method's call to api_connect() replace the parameters with your Consumer Key and Secret as strings
   2. In the call to get_users_timelines() replace the second parameter with the @ handle name of the twitter user you would like to save all of their tweets. The third variable is the file name of a json file containing all the tweets. **Remeber the name of this file it will be used in step 4**
   3. You can now run the script, the file containing all of the tweets should be saved at ```/project_root/data/```
3. Next we will be interacting with IBM Watson's Tone analyzer so you will need to [create a free account](https://console.bluemix.net/registration/?target=%2Fdeveloper%2Fwatson%2Fcreate-project%3Fservices%3Dtone_analyzer%26hideTours%3Dtrue&cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmca1%3D000000OF%26cm_mmca2%3D10000409).
   1. Once logged in navigate to [browse all IBM cloud services](https://console.bluemix.net/developer/watson/services).
   2. Select Tone analyzer and add service, then you will name it and click 'Create Project'
   3. You should now be on the page for your newly created project at which point click 'Service Credentials' located on the lefthand side and select 'view credentials'. If no credentials then simply add 'New Credential'.
   4. You will want to save these credentials as they will be used in the next step.
4. Open the file ```tone_analyzer.py```
   1. Scroll to the main method at the bottom
   2. Edit the parameters of the create_connection() method call to use your username and password as string values. The third param is just for version purposes and can be changed if wanted.
   3. We will have to do is change the first parameter of the ```incremental_send_all_tweets_to_text_json()``` method to be the path to your json file of the tweets from step 2.
   4. Next also change the second parameter of the ```attach_analysis_to_tweet()``` method to the path of the json file from step 2.
   5. Now we should be able to run the script and it will analyze the emotion of each tweet and merge the tone with the original json of all the tweets. This file will be very helpful for the data analysis next. If you didnt change anything else in the script it should be saved ```/project_root/data/merged_analysis.json```
5. Open the file ```tweets_data_analysis.py```
   1. If you didn't change the filepath of the merged analysis then you can just run the script as is. Your plots will be created and saved to ```/project_root/data/plots/```
      * If you did change the filepath then edit the first parameter of the ```get_flattened_data()``` method call to be the new filepath.
