import nltk
import re
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



nltk.download('stopwords')
nltk.download('punkt')


#Customizing Stopwords as per data
stopwords = stopwords.words('english')
new_stopwords=["br","movie","one","film","would","shall","could","might","im",'brazil','eightbr','ninebr','sevenbr','tenbr'
               "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
stopwords.extend(new_stopwords)
stopwords.remove("not")


#data cleaning 
def remove_special_characters(content):
    return re.sub(r'[^a-zA-Z\'\s]','',content)

def remove_url(content):
    return re.sub(r'https\S+','',content)

def to_lowercase(content):
    return content.lower()


def remove_stopwords(content):
    words = content.split()        
    # Filter out stopwords
    filtered_words = [word for word in words if word.lower() not in stopwords]
    filtered_text = ' '.join(filtered_words)
    return filtered_text
 
def remove_quotes(content):
    return content.replace('\'','')  
 

def  contraction_expansion(content):
    content = re.sub(r"won\'t","would not",content)
    content = re.sub(r"can\'t","can not",content)
    content = re.sub(r"don\'t","do not",content)
    content = re.sub(r"shouldn\'t","should not",content)
    content = re.sub(r"needn\'t","need not",content)
    content = re.sub(r"hasn\'t","has not",content)
    content = re.sub(r"haven\'t","have not",content)
    content = re.sub(r"weren\'t","were not",content)
    content = re.sub(r"mightn\'t","might not",content)
    content = re.sub(r"didn\'t","did not",content)
    content = re.sub(r"n\'t"," not",content)
    content = re.sub(r"\'re"," are",content)
    content = re.sub(r"\'s"," is",content)
    content = re.sub(r"\'d"," would",content)
    content = re.sub(r"\'ll"," will",content)
    content = re.sub(r"\'ve"," have",content)
    content = re.sub(r"\'m"," am",content)
    content = re.sub(r"Im","I am",content)
    return content

def stemming_content(content):
    # Initialize the Porter Stemmer
    stemmer = PorterStemmer()
    # Tokenize the sentence
    words = word_tokenize(content)
    # Apply stemming to each word
    stemmed_words = [stemmer.stem(word) for word in words]
    # Join the stemmed words back into a sentence
    stemmed_sentence = ' '.join(stemmed_words)
    return stemmed_sentence

def remove_words_with_br(content):
    # Define a regular expression pattern to find words containing 'br'
    pattern = r'\b\w*br\w*\b'
    # Use re.sub() to replace matching words with an empty string
    result = re.sub(pattern, '', content, flags=re.IGNORECASE)
    return result.strip()


def data_cleaning(content):
    content= remove_special_characters(content)
    content = to_lowercase(content)
    content= remove_url(content)
    content = remove_quotes(content)
    content = stemming_content(content)
    content = contraction_expansion(content)
    content = remove_stopwords(content)
    content = remove_words_with_br(content)
    return content

class DataCleaning(BaseEstimator,TransformerMixin):
    
    def __init__(self):
        print("Calling init inside datacleaning")
        
    def fit(self,X,y=None):
        print("Calling fit inside datacleaning")
        return self
            
    def transform(self,X,y=None):
        print("Calling transform")
        X= X.apply(data_cleaning)
        return X
    
    
#lemmatization
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, reviews):
        return [self.wnl.lemmatize(t) for t in word_tokenize(reviews)]