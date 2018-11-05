from keras.models import Sequential
from keras.layers import Dense
import numpy as np

def compile():
	model = Sequential()

	model.add(Dense(units=8, activation='relu', input_dim=5))
	model.add(Dense(units=16, activation='softmax'))
	model.add(Dense(units=8, activation='softmax'))
	model.add(Dense(units=3, activation='softmax'))

	model.compile(loss='squared_hinge', optimizer='adam', metrics=['accuracy'])
	
	modelfile = open("model.json", 'w')
	modelfile.write(model.to_json())
	modelfile.close()
	return model

def train(model, seed):
	model.compile(loss='squared_hinge', optimizer='adam', metrics=['accuracy'])
	dataFile = open("learningData.csv")

	x_values = []
	y_values = []
	for line in dataFile:
		splitline = line[:-1].split(',')
		x_values += [splitline[:-1]]
		y_values += [splitline[-1]]

	real_y_values = []
	for entry in y_values:
		template = [0, 0 ,0]
		template[int(entry) + 1] = 1
		real_y_values += [template]


	x_values = np.array(x_values)
	y_values = np.array(real_y_values)

	model.fit(x_values, y_values, epochs=5, batch_size=16)


	model.save_weights("weights%s.hdf5" % (seed))
