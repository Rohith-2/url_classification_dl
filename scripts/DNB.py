import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from dbn import SupervisedDBNClassification

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

	classifier = SupervisedDBNClassification(hidden_layers_structure=[256, 256],
                                         learning_rate_rbm=0.05,
                                         learning_rate=0.1,
                                         n_epochs_rbm=10,
                                         n_iter_backprop=100,
                                         batch_size=32,
                                         activation_function='relu',
                                         dropout_p=0.2)
	classifier.fit(X_train, Y_train)

	y_pred = classifier.predict(X_test)
	print(accuracy_score(y_test,predicted))
	target_names = ['Benign_list_big_final','DefacementSitesURLFiltered','Malware_dataset','phishing_dataset','spam_dataset']
	print(classification_report(y_test, predicted, target_names=target_names))
	#model.save("Model_v1")