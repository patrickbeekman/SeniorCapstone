import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
import tweepy_grabber
import tweepy
import json
import pytest

grabber = tweepy_grabber.TweepyGrabber()


def test_good_api_connection():
    api = grabber.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])
    try:
        api.user_timeline(screenname="patrickbeekman", count=200)
        assert True
    except tweepy.TweepError as e:
        print(e)


def test_bad_api_connection():
    with pytest.raises(SystemExit) as e:
        api = grabber.api_connect(os.environ['TWEET_PUB'], "000000000")
        assert e.type == SystemExit


def test_user_not_exist_get_users_timeline():
    api = grabber.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])
    try:
        grabber.get_users_timeline("ponlejkdls", os.path.dirname(__file__) + "/../data/outfile.json")
        assert False
    except Exception:
        assert True


def test_success_get_users_timeline():
    api = grabber.api_connect(os.environ['TWEET_PUB'], os.environ['TWEET_PRI'])
    outputfile = os.path.dirname(__file__) + "/../data/longent.json"
    try:
        grabber.get_users_timeline("LongentUSA", outputfile)
    except Exception:
        assert False
    with open(outputfile) as file:
        data = json.load(file)
    os.remove(outputfile)
    assert len(data) > 0