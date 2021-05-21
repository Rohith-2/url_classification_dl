import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import pickle
import data_creation_v3 as d
from tensorflow.keras.models import load_model
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt

order = ['bodyLength', 'bscr', 'dse', 'dsr', 'entropy', 'hasHttp', 'hasHttps',
       'has_ip', 'numDigits', 'numImages', 'numLinks', 'numParams',
       'numTitles', 'num_%20', 'num_@', 'sbr', 'scriptLength', 'specialChars',
       'sscr', 'urlIsLive', 'urlLength']

if __name__ == '__main__':
	st.title("URL Featurizer and Classification")
	st.write("_______________")
	st.sidebar.text("Credits:")
	st.sidebar.text(""" 
            Team - O
            .    Aaditya Jain 
            .    Anirudh Bhaskar
            .    Ankam Srikanth
            .    Rohith Ramakrishnan
        """)

	user_input = st.text_input("Enter URL:")
	a = d.UrlFeaturizer(user_input).run()
	test = []
	for i in order:
	    test.append(a[i])
	encoder = LabelEncoder()
	encoder.classes_ = np.load('lblenc_v1.npy',allow_pickle=True)
	scalerfile = 'scaler.sav'
	scaler = pickle.load(open(scalerfile, 'rb'))
	model = load_model("Model_v2.h5")#, custom_objects={'f1_m':f1_m,"precision_m":precision_m, "recall_m":recall_m})
	test = pd.DataFrame(test).replace(True,1).replace(False,0).to_numpy().reshape(1,-1)
	predicted = np.argmax(model.predict(scaler.transform(test)),axis=1)

	ben = [1.        , 1.        , 1.        , 1.        , 0.56158211,
       0.        , 1.        , 0.        , 0.58866722, 1.        ,
       1.        , 0.16708727, 1.        , 0.16454762, 1.        ,
       1.        , 1.        , 1.        , 1.        , 0.        ,
       0.70961575]

	submit = st.button('Predict')
	if submit:
		st.write(encoder.inverse_transform(predicted)[0])
		plt.figure(figsize=(12,12))
		plt.plot(scaler.transform(test)[0],order,color='red', marker='>',linewidth=0.65,linestyle=":",alpha=0.5)
		plt.plot(ben,order,marker='o',linewidth=0.65,linestyle="--",alpha=0.5)
		plt.legend(["Extracted Features","Avg Safe URL"])
		plt.title("Variation of features for different types of URLs")
		plt.ylabel("Features")
		plt.xlabel("Normalised Mean Values")
		plt.plot()
		st.pyplot()
	