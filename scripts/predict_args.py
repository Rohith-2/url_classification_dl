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
import sys, getopt
from tensorflow.keras.models import load_model
os.chdir("../")
os.chdir("models/")

order = ['bodyLength', 'bscr', 'dse', 'dsr', 'entropy', 'hasHttp', 'hasHttps',
       'has_ip', 'numDigits', 'numImages', 'numLinks', 'numParams',
       'numTitles', 'num_%20', 'num_@', 'sbr', 'scriptLength', 'specialChars',
       'sscr', 'urlIsLive', 'urlLength']
def main(argv):
	url = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile="])

	except getopt.GetoptError:
		print('predict_args.py -i <url>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('predict_args.py -i <url>')
			sys.exit()
		elif opt in ("-i","--ifile"):
			url = arg

	a = d.UrlFeaturizer(url).run()
	test = []
	for i in order:
		test.append(a[i])

	encoder = LabelEncoder()
	encoder.classes_ = np.load('lblenc_v1.npy',allow_pickle=True)
	scalerfile = 'scaler.sav'
	scaler = pickle.load(open(scalerfile, 'rb'))
	model = load_model("Model_v1.h5")#, custom_objects={'f1_m':f1_m,"precision_m":precision_m, "recall_m":recall_m})
	test = pd.DataFrame(test).replace(True,1).replace(False,0).to_numpy().reshape(1,-1)
	predicted = np.argmax(model.predict(scaler.transform(test)),axis=1)
	print(encoder.inverse_transform(predicted)[0])

if __name__ == '__main__':
	main(sys.argv[1:])
	