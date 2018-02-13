import pandas as pd
import os
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonException
from watson_developer_cloud import WatsonInvalidArgument
# install with - from watson_developer_cloud import ToneAnalyzerV3

class MyToneAnalyzer():

    #def __init__(self):

    def create_connection(self, version_num):
        try:
            tone_analyzer = ToneAnalyzerV3(
                username=os.environ['TONE_U'],
                password=os.environ['TONE_P'],
                version=version_num)
        except WatsonInvalidArgument as e:
            print(e)
            exit(0)
        return tone_analyzer

    def analyze_json_file(self, analyzer, filename):
        with open(filename) as tone_json:
            try:
                tone_resp = analyzer.tone(tone_json.read())
            except WatsonException as e:
                print("WatsonException", e)
                exit(0)
        return tone_resp



def main():
    ta = MyToneAnalyzer()
    analyzer = ta.create_connection('2018-02-07')

    filename = os.path.dirname(__file__) + "/../test_text.json"
    tone_resp = ta.analyze_json_file(analyzer, filename)
    print(json.dumps(tone_resp, indent=2))

if __name__ == "__main__":
    main()