import pandas as pd
import os


class TweetsDataAnalysis:

    def attach_analysis_to_tweet(self):
        analysis_path = os.path.dirname(__file__) + "/../data/all_analysis.json"
        tweets_path = os.path.dirname(__file__) + "/../data/tweets.json"

        analysis = pd.read_json(analysis_path)
        tweets = pd.read_json(tweets_path)
        tweets['sentence_id'] = range(0, len(tweets))

        merged = pd.merge(left=tweets, right=analysis, left_on='sentence_id', right_on='sentence_id')
        cols = list(merged.columns)
        print(cols)
        print("text_y: ", cols[-2])
        cols[-2] = 'processed_text'
        print("text_x: ", cols[-9])
        cols[-9] = 'text'
        merged.columns = cols

        output_file_path = os.path.dirname(__file__) + "/../data/merged_analysis.json"
        with open(output_file_path, 'w') as file:
            file.write(merged.to_json(orient='records'))


def main():
    tda = TweetsDataAnalysis()
    tda.attach_analysis_to_tweet()

    data = pd.read_json(os.path.dirname(__file__) + "/../data/merged_analysis.json", orient='records')
    #print(data['tones']['tone_id'])

if __name__ == "__main__":
    main()