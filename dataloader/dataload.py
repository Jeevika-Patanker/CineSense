import pandas as pd

def load_dataset(path):
    dataframe = pd.read_csv(path,encoding='latin-1')
    dataframe['sentiment']= dataframe['sentiment'].apply(Changing_sentiment_to_labels) 
    data = dataframe[['review','sentiment']]
    return data
 
 
def Changing_sentiment_to_labels(sentence):
    if sentence=='positive':
        return 1
    else:
        return 0     