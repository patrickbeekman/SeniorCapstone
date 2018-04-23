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
    try:
        grabber.get_users_timeline("ponlejkdls", os.path.dirname(__file__) + "/../data/outfile.json")
        assert False
    except Exception:
        assert True


def test_success_get_users_timeline():
    outputfile = os.path.dirname(__file__) + "/../data/longent.json"
    try:
        grabber.get_users_timeline("LongentUSA", outputfile)
    except Exception:
        assert False
    with open(outputfile) as file:
        data = json.load(file)
    os.remove(outputfile)
    assert len(data) > 0

def test_get_users_timeline_no_tweets():
    outputfile = os.path.dirname(__file__) + "/../data/donald.json"
    try:
        ret = grabber.get_users_timeline("donaldglover", outputfile)
        if ret is None:
            assert True
    except Exception:
        assert False

def test_get_users_followers_not_exist():
    outputfile = os.path.dirname(__file__) + "/../data/test.json"
    ret = grabber.get_users_followers(outputfile, "ponlejkdls")
    assert ret is None

def test_get_users_followers_good():
    outputfile = os.path.dirname(__file__) + "/../data/test.json"
    ret = grabber.get_users_followers(outputfile, "patrickbeekman")
    assert len(ret) > 0
