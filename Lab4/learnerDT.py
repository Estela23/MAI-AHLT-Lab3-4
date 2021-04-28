import sys
from sklearn import tree
import pickle
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
import pandas as pd


def preprocess(data, model):
    """
    Args:
        data: data.feat read by lines and converted to a list
        model: "DT" or "CRF" depending on the model we want to use

    Returns: X_sentences: list of lists of lists with the sorted features of the tokens in the original file
             Y_sentences: list of lists with the "real" tags of the words of each sentence

    """

    X_tokens = [data[i][4] for i in range(len(data))]
    Y_tokens = [data[j][3] if len(data[j]) > 4 else '' for j in range(len(data))]

    if model == "DT":
        features = ["Feature " + str(i + 1) for i in range(len(X_tokens[0]))]
        df_prov = pd.DataFrame(X_tokens, columns=features)

        blank_indexes = [i for i in range(df_prov.shape[0]) if df_prov.iloc[i][0] is None]

        Y_sentences = [Y_tokens[i] for i in range(len(Y_tokens)) if i not in blank_indexes]

        df = df_prov.copy()
        df = df.drop(df.index[blank_indexes])

        encoder = OneHotEncoder()
        encoded_df = encoder.fit_transform(df)
        X_sentences = encoded_df

        """
        df = df_prov.copy()
        df.drop(df.index[blank_indexes])

        encoder = LabelEncoder()
        encoded_columns = []
        for column in range(df.shape[1]):
            encoded_column = encoder.fit_transform(df[:, column])
            encoded_columns.append(encoded_column)
        encoded_df = pd.DataFrame(encoded_columns)"""

        """aux_x = []
        X_sentences = []
        for row_idx in range(encoded_df.shape[0]):
            if row_idx not in blank_indexes:
                aux_x.append(list(encoded_df[row_idx]))
            elif len(aux_x) > 0:
                X_sentences.append(aux_x)
                aux_x = []"""

    elif model == "CRF":
        aux_y = []
        Y_sentences = []
        for element in Y_tokens:
            if element != '':
                aux_y.append(element)
            elif len(aux_y) > 0:
                Y_sentences.append(aux_y)
                aux_y = []

        aux_x = []
        X_sentences = []
        for element in X_tokens:
            if len(element) > 1:
                aux_x.append(element)
            elif len(aux_x) > 0:
                X_sentences.append(aux_x)
                aux_x = []

    return X_sentences, Y_sentences

training_model = sys.argv[1]      # trainer.dt
training_file = sys.argv[2]   # train.feat

file = open(training_file, "r")
data_init = file.readlines()
data = [x.strip().split("\t") for x in data_init]

X_sentences, Y_sentences = preprocess(data, "DT")

# Creating and training the Decision Tree model
classifier = tree.DecisionTreeClassifier()
classifier.fit(X_sentences, Y_sentences)

features = ["Feature " + str(i + 1) for i in range(X_sentences.shape[1])]

fig = plt.figure(figsize=(25, 20))
_ = tree.plot_tree(classifier, feature_names=features, class_names=classifier.classes_, filled=True)
fig.savefig("decistion_tree.png")


# Save the model to disk
pickle.dump(classifier, open(training_model, 'wb'))