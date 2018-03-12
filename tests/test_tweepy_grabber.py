import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
import tweepy_grabber
import tweepy
import json

grabber = tweepy_grabber.TweepyGrabber()


def test_good_api_connection():
    api = grabber.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])
    try:
        api.user_timeline(screenname="patrickbeekman", count=200)
        assert True
    except tweepy.TweepError as e:
        print(e)


def test_bad_api_connection():
    api = grabber.api_connect(os.environ['TWEET_PUB'], "000000000")
    try:
        api.user_timeline(screenname="patrickbeekman", count=200)
        assert False
    except tweepy.TweepError:
        assert True

def test_bad_get_users_timeline():
    api = grabber.api_connect(os.environ['TWEET_PUB'], "000000000")
    try:
        grabber.get_users_timeline(api, "patrickbeekman", "outfile.json")
        assert False
    except Exception:
        assert True

def test_user_not_exist_get_users_timeline():
    api = grabber.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])
    try:
        grabber.get_users_timeline(api, "ponlejkdls", "outfile.json")
        assert False
    except Exception:
        assert True

def test_success_get_users_timeline():
    api = grabber.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])
    try:
        grabber.get_users_timeline(api, "donaldglover", "donald.json")
    except Exception:
        assert False
    outputfile = os.path.dirname(__file__) + "/../data/donald.json"
    with open(outputfile) as file:
        data = json.load(file)
    os.remove(outputfile)
    assert len(data) > 0