import pytest
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
import tone_analyzer
from watson_developer_cloud import WatsonException
import datetime

now = datetime.datetime.now()
ta = tone_analyzer.MyToneAnalyzer()


def test_good_login():
    tone = ta.create_connection(now.strftime("%Y-%m-%d %H:%M"))
    assert tone is not None


def test_bad_json_file():
    analyzer = ta.create_connection(now.strftime("%Y-%m-%d"))
    with pytest.raises(SystemExit) as e:
        ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/bad_text.json")
    assert e.type == SystemExit


def test_good_json_file():
    analyzer = ta.create_connection(now.strftime("%Y-%m-%d"))
    resp = ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/good_text.json")
    assert resp != ""

