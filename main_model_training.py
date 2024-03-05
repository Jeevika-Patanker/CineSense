import os
from dataloader.dataload import load_dataset
from datapreprocessing.preprocessing import DataCleaning
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score,roc_auc_score,f1_score,recall_score
import pandas as pd
import joblib


#loading dataset
path=os.getcwd()+r'\data'
data=  load_dataset(path + r'\IMDB-Dataset.csv') 

print(type(data))

#split data
x_train,x_test,y_train,y_test = train_test_split(data['review'],data['sentiment'],test_size=0.3,random_state=42,shuffle=True)

#Text_classifier Pipeline
# txt_clf = Pipeline(
#     steps=[
#         ("cleaning",DataCleaning()),
#         ("vect",TfidfVectorizer(),
#         ("classifier",LogisticRegression())
#     ]
# )

cleaner = DataCleaning()
x_train_clean_data =  cleaner.transform(x_train)
x_test_clean_data =  cleaner.transform(x_test)
print(x_train_clean_data)
print(type(x_train_clean_data))
x_train_clean_data = pd.Series(x_train_clean_data)
x_test_clean_data = pd.Series(x_test_clean_data)

# Tfidf_Vector = TfidfVectorizer(use_idf=True ,norm='l2',tokenizer= LemmaTokenizer(),smooth_idf=True, ngram_range=(1,3),min_df=1,max_features=5000)
Tfidf_Vector = TfidfVectorizer()

x_train_tfidf=Tfidf_Vector.fit_transform(x_train_clean_data)
x_test_tfidf=Tfidf_Vector.transform(x_test_clean_data)

classifier=LogisticRegression()




#model training
classifier.fit(x_train_tfidf,y_train)




#generate prediction on test data
y_predict = classifier.predict(x_test_tfidf)
print(y_predict)
y_score = classifier.predict_proba(x_test_tfidf)[:1]
print(y_score)


#evaluation of the base model
print("Precision score on test data for Logistic Regression = %s"% precision_score(y_test,y_predict))
print("Roc Auc score on test data for Logistic Regression = %s"% roc_auc_score(y_test,y_predict))
print("f1 score on test data for Logistic Regression = %s"% f1_score(y_test,y_predict))
print("recall score on test data for Logistic Regression = %s"% recall_score(y_test,y_predict))

model_path=os.getcwd()+r'\models\model'
joblib.dump(cleaner,model_path+r'\data_cleaner.pkl',compress=True)
joblib.dump(Tfidf_Vector,model_path+r'\tfidf_vector.pkl',compress=True)
joblib.dump(classifier,model_path+r'\classifier.pkl',compress=True)
print('model successfully extracted')