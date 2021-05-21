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
import time
from PIL import Image
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
l = os.getcwd()
st.write(l)

order = ['bodyLength', 'bscr', 'dse', 'dsr', 'entropy', 'hasHttp', 'hasHttps',
       'has_ip', 'numDigits', 'numImages', 'numLinks', 'numParams',
       'numTitles', 'num_%20', 'num_@', 'sbr', 'scriptLength', 'specialChars',
       'sscr', 'urlIsLive', 'urlLength']

class TimerError(Exception):
     """A custom exception used to report errors in use of Timer class"""
 
class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return (f"Elapsed time: {elapsed_time:0.4f} seconds")

if __name__ == '__main__':
	st.title("URL Featurizer and Classification")
	
	st.text("A Neural Network based trained model for extracting features and predicting the type of URL.")
	st.write("_______________")
	st.text(""" 
            Different Types of URL's
            .    Benign 
            .    Defacement
            .    Malware
            .    Phishing
            .    Spam
        """)
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
	encoder.classes_ = np.load(l+'/GUI/lblenc_v1.npy',allow_pickle=True)
	scalerfile = l+'/GUI/scaler.sav'
	scaler = pickle.load(open(scalerfile, 'rb'))
	model = load_model(l+'/GUI/Model_v2.h5')#, custom_objects={'f1_m':f1_m,"precision_m":precision_m, "recall_m":recall_m})
	test = pd.DataFrame(test).replace(True,1).replace(False,0).to_numpy().reshape(1,-1)
	t = Timer()
	t.start()
	predicted = np.argmax(model.predict(scaler.transform(test)),axis=1)
	s = t.stop()
	st.sidebar.text("Prediction :")
	st.sidebar.text(str(s))

	ben = [1.        , 1.        , 1.        , 1.        , 0.56158211,
       0.        , 1.        , 0.        , 0.58866722, 1.        ,
       1.        , 0.16708727, 1.        , 0.16454762, 1.        ,
       1.        , 1.        , 0.95        , 1.        , 0.        ,
       0.70961575]

	submit = st.button('Predict')
	if (user_input==""):
		st.write("Enter Valid URL")

	if submit and user_input!="":
		pred = encoder.inverse_transform(predicted)[0]
		st.header("Type of URL : "+pred)
		st.subheader("What is a "+pred+" URL?")
		if (pred!="Benign"):
			image = Image.open(l+'/GUI/danger.jpeg')
			st.sidebar.image(image)
		else:
			image = Image.open(l+'/GUI/safe.png')
			st.sidebar.image(image)

		if (pred=="Benign"):
			st.text("These URLs are generally harmless and non-malicious.")
		elif(pred=="Spam"):
			st.write("Spam refers to a broad range of unwanted pop-ups, links, data and emails that we face in our daily interactions on the web. Spam’s namesake is, (now unpopular) luncheon meat that was often unwanted but ever present. Spam can be simply unwanted, but it can also be harmful, misleading and problematic for your website in a number of ways.")
			st.write("Read More: [https://www.goup.co.uk/guides/spam/](https://www.goup.co.uk/guides/spam/)")
		elif(pred=="Defacement"):
			st.write("Web defacement is an attack in which malicious parties penetrate a website and replace content on the site with their own messages. The messages can convey a political or religious message, profanity or other inappropriate content that would embarrass website owners, or a notice that the website has been hacked by a specific hacker group.")
			st.write("Read More: [https://www.imperva.com/learn/application-security/website-defacement-attack/](https://www.imperva.com/learn/application-security/website-defacement-attack/)")	
		elif(pred=="Malware"):
			st.write("The majority of website malware contains features which allow attackers to evade detection or gain and maintain unauthorized access to a compromised environment. Some common types of website malware include credit card stealers, injected spam content, malicious redirects, or even website defacements.")
			st.write("Read More: [https://sucuri.net/guides/website-malware/](https://sucuri.net/guides/website-malware/)")	
		else:
			st.write("A phishing website (sometimes called a 'spoofed' site) tries to steal your account password or other confidential information by tricking you into believing you're on a legitimate website. You could even land on a phishing site by mistyping a URL (web address).")
			st.write("Read More: [https://safety.yahoo.com/Security/PHISHING-SITE.html#:~:text=A%20phishing%20website%20(sometimes%20called,a%20URL%20(web%20address).](https://safety.yahoo.com/Security/PHISHING-SITE.html#:~:text=A%20phishing%20website%20(sometimes%20called,a%20URL%20(web%20address).)")	


		st.header("Basis for this prediction")
		st.text("Any URL can be decomposed into the following subsections:")
		st.image(Image.open(l+'/GUI/url.png'))

		st.text("""
		.	URL String Characteristics: Features derived from the URL string itself.
		.	URL Domain Characteristics: Domain characteristics of the URLs domain. These include whois information and shodan information.
		.	Page Content Characteristics: Features extracted from the URL’s page (if any)
			""")

		st.write("For more information regarding the features extracted, please visit [github](https://github.com/Rohith-2/url_classification_dl)")
		st.header("Extracted Features vs Safe URL")
		st.text("Given below are the features extracted from the URL and the values of these features are plotted along x-axis with the features on the y-axis.")
		plt.figure(figsize=(12,12))
		plt.plot(scaler.transform(test)[0],order,color='red', marker='>',linewidth=0.65,linestyle=":",alpha=0.5)
		plt.plot(ben,order,marker='o',linewidth=0.65,linestyle="--",alpha=0.5)
		plt.legend(["Extracted Features","Avg Safe URL"])
		plt.title("Variation of features for different types of URLs")
		plt.ylabel("Features")
		plt.xlabel("Normalised Mean Values")
		plt.plot()
		st.pyplot()
	
