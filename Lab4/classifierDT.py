# read  each  vector  in  input  file
import pickle
import sys

from sklearn.preprocessing import OneHotEncoder

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
encoder = OneHotEncoder()
encoded_df = encoder.fit_transform(data)
X_sentences = encoded_df
predictions = mymodel.predict(X_sentences)
# if the  classifier  predicted a DDI , output  itin the  right  format
with open(file_to_write, 'w') as output:
    for prediction, sid in zip(predictions, SID):
        if prediction != "null":
            print(sid[0] ,sid[1],sid[2],prediction ,sep="|", file=output)