import numpy as np
from keras.models import model_from_json, Sequential

modelFile = open("model.json")
model = model_from_json(modelFile.read())
model.load_weights("weights.hdf5")
modelFile.close()

model.compile(loss='squared_hinge', optimizer='adam', metrics=['accuracy'])

dataFile = open("learningData.csv")

x_values = []
y_values = []
for line in dataFile:
	splitline = line[:-1].split(',')
	x_values += [splitline[:-1]]
	y_values += [splitline[-1]]

dataFile.close()

real_y_values = []
for entry in y_values:
	template = [0, 0 ,0]
	template[int(entry) + 1] = 1
	real_y_values += [template]


x_values = np.array(x_values)
y_values = np.array(real_y_values)

model.fit(x_values, y_values, epochs=5, batch_size=16)

modelfile = open("model.json", 'w')
modelfile.write(model.to_json())
modelfile.close()

model.save_weights("weights.hdf5")
