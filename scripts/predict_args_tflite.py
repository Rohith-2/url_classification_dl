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
	interpreter = tf.lite.Interpreter(model_path="tflite_quant_model.tflite")
	interpreter.allocate_tensors()

	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()

	test = pd.DataFrame(test).replace(True,1).replace(False,0).to_numpy().reshape(1,-1)
	interpreter.set_tensor(input_details[0]['index'], test)
	interpreter.invoke()
	output_data = interpreter.get_tensor(output_details[0]['index'])
	predicted = np.argmax(output_data,axis=1)
	print(predicted)

if __name__ == '__main__':
	main(sys.argv[1:])
	