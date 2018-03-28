import pytest
import os
import sys
import json
import numpy as np
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
    try:
        tone = ta.create_connection("0000000", "11111111", now.strftime("%Y-%m-%d %H:%M"))
        assert False
    except Exception as e:
        assert True


def test_bad_json_file():
    with pytest.raises(SystemExit) as e:
        resp = ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/bad_text.json")
        assert e.type == SystemExit


def test_good_json_file():
    resp = ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/good_text.json")
    assert resp is not None


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

def test_write_only_sentence_to_file():
    tone = ta.create_connection(os.environ['TONE_U'], os.environ['TONE_P'], now.strftime("%Y-%m-%d %H:%M"))
    resp = ta.analyze_json_file(analyzer, os.path.dirname(__file__) + "/good_text.json")
    outfile = os.path.dirname(__file__) + "/temp.json"
    ta.write_only_sentence_tone_to_file(resp, outfile)
    data = pd.read_json(outfile)
    os.remove(outfile)
    assert list(data) != 'document_tone'

def test_bad_analyze_all_tweets_text_folder():
    try:
        os.mkdir(ta.path_name("/../tests/test_dir/"))
    except Exception as e:
        print(e)
    with open(ta.path_name("/../tests/test_dir/tweet_text_01.json"), 'w') as file:
        json.dump("{1}", file)
    with open(ta.path_name("/../tests/test_dir/tweet_text_02.json"), 'w') as file:
        json.dump("{2}", file)
    tone_bad = ta.create_connection("0000000", "11111111", now.strftime("%Y-%m-%d %H:%M"))
    with pytest.raises(SystemExit) as e:
        ta.analyze_all_tweets_text_folder(tone_bad, ta.path_name("/../tests/test_dir/"))
        assert e.type == SystemExit

def test_good_analyze_all_tweets_text_folder():
    test_folder = os.path.dirname(__file__) + "/test_dir/"
    try:
        os.mkdir(test_folder)
    except Exception as e:
        print(e)
    d = {'text': ["Happiness comes in a bottle. Hello old friend."]}
    new_df = pd.DataFrame(data=d).to_json(orient='records')[1:-1]
    with open(test_folder + "tweet_text_01.json", 'w') as f:
        f.write(new_df)
    d = {'text': ["Sadness is very sad. This is a second sentence."]}
    new_df = pd.DataFrame(data=d).to_json(orient='records')[1:-1]
    with open(test_folder + "tweet_text_02.json", 'w') as f:
        f.write(new_df)
    tone_good = ta.create_connection(os.environ['TONE_U'], os.environ['TONE_P'], now.strftime("%Y-%m-%d %H:%M"))
    ta.analyze_all_tweets_text_folder(tone_good, test_folder)
    filenames = os.listdir(test_folder + "")
    for f in filenames:
        os.remove(test_folder + f)
    os.rmdir(test_folder)
    assert len(filenames) > 0

