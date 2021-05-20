import os
import pandas as pd
import tensorflow as ts
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
from sklearn.preprocessing import MinMaxScaler
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras import backend as K
from sklearn.metrics import classification_report


os.chdir("../")
os.chdir("FinalDataset")


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

m = ts.keras.metrics.CategoricalAccuracy()

if __name__ == "__main__":
	data = pd.read_csv("feature.csv")
	data.drop(columns='Unnamed: 0',inplace=True)
	data.replace(True,1,inplace = True)
	data.replace(False,0,inplace = True)
	y = data["File"]
	data = data.drop(columns = "File")
	encoder = LabelEncoder()
	encoder.fit(y)
	Y = encoder.transform(y)
	scaler = MinMaxScaler(feature_range=(0, 1))
	X = scaler.fit_transform(data)
	X = pd.DataFrame(X)

	input_dim = len(data.columns)
	model = Sequential()
	model.add(Dense(128, input_dim = input_dim , activation = 'relu'))
	model.add(Dense(64, activation = 'relu'))
	model.add(Dense(32, activation = 'relu'))
	model.add(Dense(16, activation = 'relu'))
	model.add(Dense(5, activation = 'softmax'))

	model.compile(loss = 'categorical_crossentropy' , optimizer = 'adam' , metrics = ['accuracy',f1_m,precision_m, recall_m] )
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)
	model.fit(X,np_utils.to_categorical(y),epochs = 24,validation_split=0.3, batch_size = 128)
	predicted = model.predict(X_test)
	predicted = np.argmax(y_pred, axis=1)
	print(accuracy_score(y_test,predicted))
	target_names = ['Benign_list_big_final','DefacementSitesURLFiltered','Malware_dataset','phishing_dataset','spam_dataset']
	print(classification_report(y_test, predicted, target_names=target_names))
	#model.save("Model_v1")