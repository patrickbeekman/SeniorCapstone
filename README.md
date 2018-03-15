# SeniorCapstone

[![Build Status](https://travis-ci.org/patrickbeekman/SeniorCapstone.svg?branch=master)](https://travis-ci.org/patrickbeekman/SeniorCapstone)

An exploratory tone analysis of twitter data and how the emotions and frequency of tweets changes in respect to the months and seasons. 


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
  
