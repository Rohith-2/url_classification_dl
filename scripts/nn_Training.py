#!/usr/bin/env python
import os
os.environ['KERAS_BACKEND']='tensorflow'
import pandas as pd
import tensorflow as ts
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import backend as K
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
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

if __name__ == '__main__':

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
    model.add(Dense(256, input_dim = input_dim , activation = 'relu'))
    model.add(Dense(128, activation = 'relu'))
    model.add(Dense(64, activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(16, activation = 'relu'))
    model.add(Dense(5, activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy' , optimizer = 'adam' , metrics = ['accuracy'] )

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model.fit(X_train,to_categorical(y_train),epochs = 50,validation_split=0.3, batch_size = 128)
    y_pred = model.predict(X_test)
    predicted = np.argmax(y_pred, axis=1)
    target_names = ['Benign','Defacement','Malware','Phishing','Spam']
    print(classification_report(y_test, predicted, target_names=target_names))

    os.chdir("../")
    os.chdir("models")
    model.save("Model_v1.h5")
    np.save('lblenc.npy', encoder.classes_)
    scalerfile = 'scaler.sav'
    pickle.dump(scaler, open(scalerfile, 'wb'))

