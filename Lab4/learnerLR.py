import sys

import joblib
import pickle
from matplotlib import pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def find_max_list(list):
    list_len = [len(i) for i in list]
    return max(list_len)

def preprocess(data_train, data_devel):
    vectorizer = DictVectorizer()
    X_tokens = [{key: 1.0 for key in data_train[i][4:]} for i in range(len(data_train))]
    #X_tokens = [data_train[i][4:] for i in range(len(data_train))]
    Y_tokens = [data_train[j][3] if len(data_train[j]) > 4 else '' for j in range(len(data_train))]
    max_value = find_max_list(X_tokens)
    features = ["Feature " + str(i + 1) for i in range(0, max_value)]
    df_prov = pd.DataFrame(X_tokens, columns=features)
    X_tokens_devel = [{key: 1.0 for key in data_devel[i][4:]} for i in range(len(data_devel))]
    max_value = find_max_list(X_tokens_devel)
    features = ["Feature " + str(i + 1) for i in range(0, max_value)]
    df_prov2 = pd.DataFrame(X_tokens_devel, columns=features)

    vectorizer.fit(X_tokens+X_tokens_devel)
    joblib.dump(vectorizer, 'vectorizer.pkl')

    return vectorizer.transform(X_tokens), Y_tokens

training_model = sys.argv[1]      # trainer.dt
training_file = sys.argv[2]   # train.feat

file = open(training_file, "r")
data_init = file.readlines()
data = [x.strip().split("\t") for x in data_init]
file = open("test.feat", "r")
data_init = file.readlines()
data_devel = [x.strip().split("\t") for x in data_init]

X_sentences, Y_sentences = preprocess(data, data_devel)

# Creating and training the Decision Tree model
classifier = LogisticRegression(max_iter=1000000)
classifier.fit(X_sentences, Y_sentences)


# Save the model to disk
pickle.dump(classifier, open(training_model, 'wb'))