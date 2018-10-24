from keras.models import Sequential
from keras.layers import Dense
import numpy as np

model = Sequential()

model.add(Dense(units=10, activation='relu', input_dim=5))
model.add(Dense(units=1, activation='softmax'))

model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

dataFile = open("learningData.csv")

x_values = []
y_values = []
for line in dataFile:
	splitline = line[:-1].split(',')
	x_values += [splitline[:-1]]
	y_values += [splitline[-1]]

x_values = np.array(x_values)
y_values = np.array(y_values)
print(x_values)

model.fit(x_values, y_values, epochs=5, batch_size=32)

modelfile = open("model.json", 'w')
modelfile.write(model.to_json())
modelfile.close()

model.save_weights("weights.hdf5")
