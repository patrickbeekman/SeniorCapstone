import pandas as pd
import numpy as np
import os


class TweetsDataAnalysis:

    def grab_emotion_per_month(self, data):
        #print(data['created_at'], data['tones'], data['text'])
        print(data['created_at'].values)
        fav_max = np.max(data['favorite_count'])
        fav = data[data.favorite_count == fav_max].index[0]
        # Max FAVs:
        print("The tweet with more likes is: \n{}".format(data['text'][fav]))
        print("Number of likes: {}".format(fav_max))


def main():
    tda = TweetsDataAnalysis()

    merged_analysis = pd.read_json(os.path.dirname(__file__) + "/../data/merged_analysis.json", orient='records')
    tda.grab_emotion_per_month(merged_analysis)

if __name__ == "__main__":
    main()