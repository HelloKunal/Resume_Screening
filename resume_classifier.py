from resume_rating import textract_processing as txt
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def clean_text(text):
    nltk.download('stopwords')
    special_character_remover = re.compile('[/(){}\[\]\|@,;]')
    extra_symbol_remover = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))
    text = text.lower()
    text = special_character_remover.sub(' ', text)
    text = extra_symbol_remover.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def logistic_regression(resume_docs):
    df = pd.read_csv('UpdatedResumeDataset.csv')
    df['Resume'] = df['Resume'].apply(clean_text)

    X = df.Resume
    y = df.Category
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)
    lr = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', LogisticRegression()),
                   ])
    lr.fit(X_train, y_train)

    resume_docs = list(map(clean_text, resume_docs))
    result=[]

    for resume in resume_docs:
        res=[]
        # print(resume)
        temp_resume = resume.split(' ')[0]
        res.append(temp_resume)
        res.append(lr.predict([resume]))
        result.append(res)

    return result


def process_files(resume_docs):

    resume_doc_text = []
    for doct in resume_docs:
        resume_doc_text.append(txt.get_content_as_string(doct))

    result = logistic_regression(resume_doc_text)
    return result