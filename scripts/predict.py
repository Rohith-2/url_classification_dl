import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from keras import backend as K
import pickle
import data_creation_v3 as d
import keras
os.chdir("../")
os.chdir("models/")

order = ['bodyLength', 'bscr', 'dse', 'dsr', 'entropy', 'hasHttp', 'hasHttps',
       'has_ip', 'numDigits', 'numImages', 'numLinks', 'numParams',
       'numTitles', 'num_%20', 'num_@', 'sbr', 'scriptLength', 'specialChars',
       'sscr', 'urlIsLive', 'urlLength']

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

if __name__ == '__main__':
	a = d.UrlFeaturizer('http://astore.amazon.co.uk/allezvinsfrenchr/detail/1904010202/026-8324244-9330038').run()
	test = []
	for i in order:
	    test.append(a[i])
	encoder = LabelEncoder()
	encoder.classes_ = np.load('lblenc.npy',allow_pickle=True)
	scalerfile = 'scaler.sav'
	scaler = pickle.load(open(scalerfile, 'rb'))
	model = keras.models.load_model("Model_v1", custom_objects={'f1_m':f1_m,"precision_m":precision_m, "recall_m":recall_m})
	predicted = np.argmax(model.predict(scaler.transform(np.array(test).reshape(1,-1))),axis=1)
	print(encoder.inverse_transform(predicted)[0])
	