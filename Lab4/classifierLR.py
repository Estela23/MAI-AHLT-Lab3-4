# read  each  vector  in  input  file
import pickle
import sys

import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
from scipy import sparse
from scipy.sparse import vstack

def find_max_list(list):
    list_len = [len(i) for i in list]
    return max(list_len)

model_to_use = sys.argv[1]
file_to_classify = sys.argv[2]
file_to_write = sys.argv[4]
mymodel = pickle.load(open(model_to_use, 'rb'))
file = open("train.feat", "r")
data_init = file.readlines()
data_train= [x.strip().split("\t") for x in data_init]
X_tokens_train = [{key: 1.0 for key in data_train[i][4:]} for i in range(len(data_train))]
file = open(file_to_classify, "r")
data_init = file.readlines()
data = [x.strip().split("\t") for x in data_init]
X_tokens = [{key: 1.0 for key in data[i][4:]} for i in range(len(data))]
SID = [data[i][:3] for i in range(len(data))]
'''for line in data_init:
        # split  line  into  elements
        fields = line.strip('\n').split("\t")
        # first 4 elements  are sid ,e1 ,e2 , and  groundtruth (ignored  since we are  classifying)
        (sid ,e1,e2,gt) = fields [0:4]
        SID.append(fields[0:4])
        # Rest of  elements  are  features , passed  to theclassifier  of  choice  to get a prediction
        data.append({key: 1.0 for key in fields[4:]})'''
#encoder = joblib.load('vectorizer.pkl')
encoder = DictVectorizer()
encoder.fit(X_tokens_train+X_tokens)
to_predict=encoder.transform(X_tokens)


predictions = mymodel.predict(to_predict)
# if the  classifier  predicted a DDI , output  itin the  right  format
with open(file_to_write, 'w') as output:
    for prediction, sid in zip(predictions, SID):
        if prediction != "null":
            print(sid[0] ,sid[1],sid[2],prediction ,sep="|", file=output)