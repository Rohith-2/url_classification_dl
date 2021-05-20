#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import pickle
import data_creation_v3 as d
from tensorflow.keras.models import load_model
os.chdir("../")
os.chdir("models/")

order = ['bodyLength', 'bscr', 'dse', 'dsr', 'entropy', 'hasHttp', 'hasHttps',
       'has_ip', 'numDigits', 'numImages', 'numLinks', 'numParams',
       'numTitles', 'num_%20', 'num_@', 'sbr', 'scriptLength', 'specialChars',
       'sscr', 'urlIsLive', 'urlLength']

if __name__ == '__main__':
	a = d.UrlFeaturizer('http://astore.amazon.co.uk/allezvinsfrenchr/detail/1904010202/026-8324244-9330038').run()
	test = []
	for i in order:
	    test.append(a[i])
	encoder = LabelEncoder()
	encoder.classes_ = np.load('lblenc.npy',allow_pickle=True)
	scalerfile = 'scaler.sav'
	scaler = pickle.load(open(scalerfile, 'rb'))
	model = load_model("Model_v1.h5")#, custom_objects={'f1_m':f1_m,"precision_m":precision_m, "recall_m":recall_m})
	test = pd.DataFrame(test).replace(True,1).replace(False,0).to_numpy().reshape(1,-1)
	predicted = np.argmax(model.predict(scaler.transform(test)),axis=1)
	print(encoder.inverse_transform(predicted)[0])
	