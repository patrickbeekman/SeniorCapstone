import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
import tweet_grabber
import os

tg = tweet_grabber.TweetGrabber()


def test_check_status():
    assert tg.check_status(100) is False
    assert tg.check_status(200) is True
    assert tg.check_status(300) is False


def test_authorize_connection():
    assert tg.authorize() is not None
    assert tg.authorize() == "AAAAAAAAAA"

