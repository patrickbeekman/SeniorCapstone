import pandas as pd
import os
import json
from watson_developer_cloud import ToneAnalyzerV3
# install with - from watson_developer_cloud import ToneAnalyzerV3

class MyToneAnalyzer():

    #def __init__(self):

    def create_connection(self, cred_filename):
        #credentials_df = pd.read_json(cred_filename)
        with open(cred_filename) as credentials:
            username = json.load(credentials)['username']
            print(username)
            password = json.load(credentials)['password']
            print(password)
        tone_analyzer = ToneAnalyzerV3(
            username=username,
            password=password,
            version='2018-02-07')
        return tone_analyzer


def main():
    ta = MyToneAnalyzer()
    analyzer = ta.create_connection(os.path.dirname(__file__) + "/../credentials.json")

    filename = os.path.dirname(__file__) + "/../test_text.json"
    with open(filename) as tone_json:
        tone = analyzer.tone(tone_json.read())

    print(json.dumps(tone, indent=2))

if __name__ == "__main__":
    main()