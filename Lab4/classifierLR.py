import pickle
import sys
import joblib


model_to_use = sys.argv[1]
file_to_classify = sys.argv[2]
file_to_write = sys.argv[4]
mymodel = pickle.load(open(model_to_use, 'rb'))

file = open(file_to_classify, "r")
data_init = file.readlines()
data = [x.strip().split("\t") for x in data_init]
X_tokens = [{key: 1.0 for key in data[i][4:]} for i in range(len(data))]
SID = [data[i][:3] for i in range(len(data))]

encoder = joblib.load('vectorizer.pkl')

to_predict = encoder.transform(X_tokens)

predictions = mymodel.predict(to_predict)
# if the classifier predicted a DDI, output it in the right format
with open(file_to_write, 'w') as output:
    for prediction, sid in zip(predictions, SID):
        if prediction != "null":
            print(sid[0], sid[1], sid[2], prediction, sep="|", file=output)
