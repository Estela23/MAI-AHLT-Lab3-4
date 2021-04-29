# read  each  vector  in  input  file
import pickle
import sys

model_to_use = sys.argv[1]
file_to_classify = sys.argv[2]
file_to_write = sys.argv[4]
mymodel = pickle.load(open(model_to_use, 'rb'))
file = open(file_to_classify, "r")
data_init = file.readlines()
for line in data_init:
        # split  line  into  elements
        fields = line.strip('\n').split("\t")
        # first 4 elements  are sid ,e1 ,e2 , and  groundtruth (ignored  since we are  classifying)
        (sid ,e1,e2,gt) = fields [0:4]
        # Rest of  elements  are  features , passed  to theclassifier  of  choice  to get a prediction
        prediction = mymodel.predict(fields[4])
        # if the  classifier  predicted a DDI , output  itin the  right  format
        if prediction  != "null" :
            print(sid ,e1,e2,prediction ,sep="|")