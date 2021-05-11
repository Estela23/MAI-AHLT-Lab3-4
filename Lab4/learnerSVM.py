import sys
import joblib
import pickle
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer


def preprocess(data_train, data_devel):
    vectorizer = DictVectorizer()
    X_tokens = [{key: 1.0 for key in data_train[i][4:]} for i in range(len(data_train))]
    Y_tokens = [data_train[j][3] if len(data_train[j]) > 4 else '' for j in range(len(data_train))]

    X_tokens_devel = [{key: 1.0 for key in data_devel[i][4:]} for i in range(len(data_devel))]

    vectorizer.fit(X_tokens+X_tokens_devel)
    joblib.dump(vectorizer, 'vectorizer.pkl')

    return vectorizer.transform(X_tokens), Y_tokens


training_model = sys.argv[1]  # trainer.dt
training_file = sys.argv[2]   # train.feat

file = open(training_file, "r")
data_init = file.readlines()
data = [x.strip().split("\t") for x in data_init]
file = open("test_casi_todo.feat", "r")
data_init = file.readlines()
data_test = [x.strip().split("\t") for x in data_init]

X_sentences, Y_sentences = preprocess(data, data_test)

# Creating and training the Decision Tree model
classifier = svm.SVC(kernel="linear")
classifier.fit(X_sentences, Y_sentences)

# Save the model to disk
pickle.dump(classifier, open(training_model, 'wb'))
