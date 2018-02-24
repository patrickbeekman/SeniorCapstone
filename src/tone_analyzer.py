import pandas as pd
import os
import json
from io import StringIO
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonException
from watson_developer_cloud import WatsonInvalidArgument
# install with - from watson_developer_cloud import ToneAnalyzerV3


class MyToneAnalyzer:

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

    def write_only_sentence_tone_to_file(self, resp, output_file):
        # Load the data and create a new string with only the sentence_tones not the document_tone
        data = json.loads(json.dumps(resp))
        try:
            io = StringIO()
            str = "["
            for i in data["sentences_tone"]:
                json.dump(i, io)
            str += io.getvalue()
            new = str.replace("}{", "},{")
            new += "]"
            self.dump_json_to_file(json.loads(new), output_file)
        except Exception as e:
            print(e)


    # analyzes all the tweet_text files in /data/tweets_text/ and saves the
    # analysis files to /data/analysis/
    def analyze_all_tweets_text_folder(self, analyzer):
        tweets_path = os.path.dirname(__file__) + "/../data/tweets_text/"
        for filename in os.listdir(tweets_path):
            num = filename.split('tweet_text_')[1].split('.')[0]
            print("analyzing : " + num.zfill(4))
            tone_resp = self.analyze_json_file(analyzer, tweets_path + filename)
            output_file = tweets_path + "/../analysis/tone_tweet_" + str(num).zfill(4) + ".json"
            self.write_only_sentence_tone_to_file(tone_resp, output_file)


    # Tone analyzer only reads first 100 sentences for tone analysis and only first
    # 1000 sentences for document level analysis. Max filesize = 128KB
    def clean_text_write_to_json(self, tweet_text, newfilename):
        ninety_tweets = ""
        for tweet in tweet_text:
            s_tweet = tweet.strip().replace('\n', ' ').replace('\r', ' ').replace('.', ' ') + ".\\n"
            ninety_tweets += " " + s_tweet
        d = {'text': [ninety_tweets]}
        new_df = pd.DataFrame(data=d).to_json(orient='records')[1:-1]
        with open(newfilename, 'w') as f:
            f.write(new_df)

    # Creates a new tone analysis ready json file of 90 tweets per file
    # Saves it in /data/tweets_text
    def send_all_tweets_to_text_json(self, input_filename):
        num = 0
        start = 0
        stop = 90
        increment = 90
        df = pd.read_json(input_filename)
        while start < (len(df)-increment):
            newfilename = self.path_name("/../data/tweets_text/tweet_text" + "_" + str(num).zfill(4) + ".json")
            subset = df[start:stop]['text']
            self.clean_text_write_to_json(subset, newfilename)
            start += 90
            stop += 90
            num += 1
        newfilename = self.path_name("/../data/tweets_text/tweet_text" + "_" + str(num).zfill(4) + ".json")
        start -= 90
        stop = len(df)
        subset = df[start:stop]['text']
        self.clean_text_write_to_json(subset, newfilename)

    def dump_json_to_file(self, data, filename):
        with open(filename, 'w') as out:
            json.dump(data, out)

    def path_name(self, filename):
        return os.path.dirname(__file__) + filename

def main():
    ta = MyToneAnalyzer()
    analyzer = ta.create_connection('2018-02-07')

    ta.send_all_tweets_to_text_json(ta.path_name("/../data/tweets.json"))

    #ta.analyze_all_tweets_text_folder(analyzer)

    '''
    resp = ta.analyze_json_file(analyzer, ta.path_name("/../data/tweets_text/tweet_text_0000.json"))
    ta.write_only_sentence_tone_to_file(resp, ta.path_name("/../data/hi.json"))
    '''

    #tone_resp = ta.analyze_json_file(analyzer, ta.path_name("/../test_text.json"))
    #print(json.dumps(tone_resp, indent=2, separators=(',', ': ')))

    #ta.strip_text_from_json(ta.path_name("/../small_tweets.json"), "hundred_tweets.json")

    '''
    ta.send_all_tweets_to_text_json(ta.path_name("/../tweets.json"), ta)
    ta.analyze_all_data_folder(ta, analyzer)
    '''
    #tweet_resp = ta.analyze_json_file(analyzer, ta.path_name("/../data/tweet_text_0.json"))
    #ta.dump_json_to_file(json.dumps(tweet_resp, indent=4, separators=(',', ': ')), "/tweets_tone.json")


if __name__ == "__main__":
    main()