# -*- coding: utf-8 -*-
import numpy as np
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.datasets import load_files
nltk.download('stopwords')

reviews = load_files('txt_sentoken/')

X,y = reviews.data,reviews.target

with open('X.pickle','wb') as f:
    pickle.dump(X,f)
    
with open('y.pickle','wb') as f:
    pickle.dump(y,f)
    

with open('X.pickle','rb') as f:
    X = pickle.load(f)
    
with open('y.pickle','rb') as f:
    y = pickle.load(f)
    
#pre processing data
predata = []
for i in range(0,len(X)):
    review = re.sub(r'\W',' ',str(X[i])) #remove all non characters
    review = review.lower() #convert to lower
    review = re.sub(r'\s+[a-z]\s+',' ',review) #remove all single characters like i a etc
    review = re.sub(r'^[a-z]\s+',' ',review) #remove single character from the line beginning
    review = re.sub(r'\s+',' ',review) #remove all spaces
    predata.append(review)

#creating BOW model    
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=2000,min_df=3,max_df=0.6,stop_words = stopwords.words('english'))
X = vectorizer.fit_transform(predata).toarray()
  
#transforming to TF-IDF model
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()
X = transformer.fit_transform(X)

#creating TFIDF vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=2000,min_df=3,max_df=0.6,stop_words = stopwords.words('english'))
X = vectorizer.fit_transform(predata).toarray()

#splitting into test and train
from sklearn.model_selection import train_test_split
text_train,text_test,sent_train,sent_test = train_test_split(X,y,test_size=0.2,random_state =0)

#logistic regression classifier fit training data
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(text_train,sent_train)

#check predicted values using test data
sent_pred = classifier.predict(text_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(sent_test,sent_pred)
#84.75% accuracy

#pickling classifier
with open('classifier.pickle','wb') as f:
    pickle.dump(classifier,f)
    
#pickling vectorizer    
with open('tfidfmodel.pickle','wb') as f:
    pickle.dump(vectorizer,f)
    
#unpickling the classifier and vectorizer
with open('classifier.pickle','rb') as f:
    clf = pickle.load(f)
    
    
with open('tfidfmodel.pickle','rb') as f:
    tfdif = pickle.load(f)
    

file = open("project.txt","r")
sample = (file.read())
print([sample])
sample = tfdif.transform([sample]).toarray()
output = clf.predict(sample)

if output == 0:
    print("It's a negative statement")
else:    
    print("It's a positive statement")    



