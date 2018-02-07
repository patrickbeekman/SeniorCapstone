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


def test_authorize_public_key():
    filename = "temp.txt"
    try:
        os.remove(filename)
    except OSError:
        pass
    f = open(filename, "w+")
    f.write("\n")
    f.write("\n")
    f.close()
    assert tg.authorize(filename) == "No public key"
    os.remove(filename)


def test_authorize_private_key():
    filename = "temp.txt"
    try:
        os.remove(filename)
    except OSError:
        pass
    f = open(filename, "w+")
    f.write("hello\n")
    f.write("world\n")
    f.write("\n")
    f.close()
    assert tg.authorize(filename) == "No private key"
    os.remove(filename)

'''
def test_authorize_bearer_tok():
    filename="keys.txt"
    # Checks that authorize correctly returned something other than none
    assert tg.authorize(filename) is not None
    # Checks that the first 10 characters of the bearer token match up
    assert tg.authorize(filename)[0:10] == "AAAAAAAAAA"
'''
