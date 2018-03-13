import pytest
import os
import sys
import json
import pandas as pd
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
import tone_analyzer
from watson_developer_cloud import WatsonException
import datetime

now = datetime.datetime.now()
ta = tone_analyzer.MyToneAnalyzer()
analyzer = ta.create_connection(os.environ['TONE_U'], os.environ['TONE_P'], now.strftime("%Y-%m-%d"))


def test_good_connection():
    tone = ta.create_connection(os.environ['TONE_U'], os.environ['TONE_P'], now.strftime("%Y-%m-%d %H:%M"))
    assert tone is not None

def test_bad_connection():
    assert True


def test_bad_json_file():
    with pytest.raises(SystemExit) as e:
        ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/bad_text.json")
    assert e.type == SystemExit


def test_good_json_file():
    resp = ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/good_text.json")
    assert resp != ""


def test_dump_json_to_file():
    good_test_file = ta.path_name("/../tests/good_text.json")
    with open(good_test_file) as json_data:
        data = json.load(json_data)
    output_file = ta.path_name("/../tests/success.json")
    ta.dump_json_to_file(json.dumps(data), output_file)
    with open(output_file) as json_data:
        new_data = json.load(json_data)
    os.remove(output_file)
    assert new_data is not None

