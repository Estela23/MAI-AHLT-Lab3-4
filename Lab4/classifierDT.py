# read  each  vector  in  input  file
import pickle
import sys

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import csr_matrix
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
file = open(file_to_classify, "r")
data_init = file.readlines()
data=[]
SID=[]
for line in data_init:
        # split  line  into  elements
        fields = line.strip('\n').split("\t")
        # first 4 elements  are sid ,e1 ,e2 , and  groundtruth (ignored  since we are  classifying)
        (sid ,e1,e2,gt) = fields [0:4]
        SID.append(fields[0:4])
        # Rest of  elements  are  features , passed  to theclassifier  of  choice  to get a prediction
        data.append(fields[4:])
max_value=find_max_list(data)
features = ["Feature " + str(i + 1) for i in range(0, max_value)]
encoder = OneHotEncoder()
df_prov = pd.DataFrame(data, columns=features)
df_prov = pd.DataFrame(data)
encoded_df = encoder.fit_transform(df_prov)
X_sentences = encoded_df
print(mymodel.max_features_)


diff_n_rows = mymodel.max_features_ - X_sentences.shape[1]
tostack=np.zeros((X_sentences.shape[0],diff_n_rows))
X_sentences=hstack([X_sentences, sparse.csr_matrix(tostack)])
predictions = mymodel.predict(X_sentences)
# if the  classifier  predicted a DDI , output  itin the  right  format
with open(file_to_write, 'w') as output:
    for prediction, sid in zip(predictions, SID):
        if prediction != "null":
            print(sid[0] ,sid[1],sid[2],prediction ,sep="|", file=output)