import os
import re
import cfsrc
import numpy as np 
from sklearn.neural_network import MLPClassifier

## neural net parameters
def neural_predict(x, y, mode):
	# simple -- predict based on what we already trained
	if mode == 1:
		clf = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(10, 10), random_state=1)
		clf.fit(x, y)
		return np.mean(clf.predict(x) == y)

	# predict the n'th observation based on the first n-1 observations
	if mode == 2: 
		for n in range(len(x)/2 - 1,len(x) - 1):
			# keep track of correct prediction
			correct_count = 0
			clf = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(10, 10), random_state=1)
			clf.fit(x[range(n)], y[range(n)])
			# predict the value, if correct then add 1 to the counter
			prediction = clf.predict(x[n].reshape(1, -1)) == y[n]
			correct_count = correct_count + int(prediction)
		return correct_count/(len(x)/2)

