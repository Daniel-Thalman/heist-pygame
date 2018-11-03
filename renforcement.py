import random
import pygame
import numpy as np
import os
import statistics as stats
from keras.models import model_from_json, Sequential

class Game():

	def __init__(self, seed, limit, chance):
		self.limit = limit
		self.chance = chance
		self.seed = str(seed)

		pygame.init()
		
		self.display_width = 800
		self.display_height = 600
		self.carWidth = 80
		self.dx = 10
		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		pygame.display.set_caption('ID: %s' % (self.seed))
		
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		self.colors = [self.red, self.green, self.blue]
		
		self.clock = pygame.time.Clock()
		self.carImg = pygame.image.load('racecar.png')

		self.reset()

		self.model = Sequential()
	
	def reset(self):
		self.currentString = ""
		self.currentGameInputs = ""
		self.quited = False

		self.x = (self.display_width * 0.45)
		self.y = (self.display_height * 0.7)
		
		self.blockStartx = self.display_width/2
		self.blockStarty = 0
		self.blockWidth = 100
		self.blockHeight = 100
		self.blockSpeed = 7.0
		self.speedDelta = 0.2
		self.blockX = self.blockStartx
		self.blockY = self.blockStarty
		self.blockDefault = [self.blockSpeed, self.blockWidth, self.blockHeight, self.blockX, self.blockY, 0]
		self.blocks = [self.blockDefault]
	
	def getModel(self):
		modelFile = open("model.json")
		self.model = model_from_json(modelFile.read())
		self.model.load_weights("weights%s.hdf5" % (self.seed))
		modelFile.close()
		self.model.compile(loss='squared_hinge', optimizer='adam', metrics=['accuracy'])
		

	def setModel(self):
		modelfile = open("model.json", 'w')
		modelfile.write(self.model.to_json())
		modelfile.close()

		self.model.save_weights("weights%s.hdf5" % (self.seed))
		
	def trainModel(self, datafileName):
		dataFile = open(datafileName)

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

		history = self.model.fit(x_values, y_values, epochs=5, batch_size=16)
		metrics = history.history
		return metrics
		
	def car(self, x,y):
		self.gameDisplay.blit(self.carImg, (x,y))
	
	
	def thing(self, thingx, thingy, thingw, thingh, color):
	    pygame.draw.rect(self.gameDisplay, color, [thingx, thingy, thingw, thingh])

	def drawBlock(self, block):
		self.thing(block[3], block[4], block[1], block[2], self.colors[block[5]])
	
	def updateBlock(self, block):
		if ((self.x > block[3] and self.x < block[3] + block[1]) or (self.x + self.carWidth > block[3] and self.x + self.carWidth < block[3] + block[1])) and ((block[4] + block[2]) >= self.y):
#			print("You ended with a score of %d" % (self.getScore()))
#			crashed()
			return True
		elif block[4] < self.display_height + (block[2]/2):
			block[4] += int(block[0])
		elif block[4] >= self.display_height + block[2]/2:
	#		print("your score: %d" % ((int((block[0] - blockSpeed) * 100))))
			block[3] = random.randint(0, self.display_width - block[1])
			block[4] = 0
			block[0] += self.speedDelta
	#		print(int(block[0]))
			self.currentGameInputs += self.currentString
			self.currentString = ""
		return False

	def crashed(self):
		pygame.quit()
		quit()
	
	def getScore(self):
		return int((self.blocks[0][0] - self.blockSpeed) * 100)
	
	def gameTest(self, mod):
		self.reset()
		while not self.quited:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quited = True
			
			x_values = np.array( [[ self.x, self.y, self.blocks[0][3], self.blocks[0][4], self.blocks[0][0] ]] )
			
			prediction = mod.predict(x_values).tolist()[0]
			maxVal = max(prediction)
			prediction = prediction.index(maxVal) - 1

			if random.random() < self.chance:
				rand = random.random()
				if rand < 0.33:
					prediction = -1
				if rand >= 0.33 and rand < 0.66:
					prediction = 1
				else:
					prediction = 0

			keydir = 0
			if prediction == -1 and self.x > 0:
				self.x += -1 * self.dx
				keydir = -1
			elif prediction == 1 and self.x < (self.display_width - self.carWidth):
				self.x += self.dx
				keydir = 1
			
			self.gameDisplay.fill(self.black)
			self.car(self.x,self.y)
			if keydir != 0:
				self.currentString += ("%d,%d,%d,%d,%d,%d\n" % (self.x,self.y,self.blocks[0][3],self.blocks[0][4],self.blocks[0][0],keydir) )
			
			for block in self.blocks:
				self.quited = self.updateBlock(block)
				self.drawBlock(block)

			pygame.display.update()
			self.clock.tick(60)
		
		score = self.getScore()
		if score > self.limit:
			datafile = open("data%s.csv" % (self.seed), 'a')
			datafile.write(self.currentGameInputs)
			datafile.close()
		return self.getScore()

	def gameTests(self, mods):
		scores = []
		for mod in mods:
			scores += self.gameTest(mod)
			pygame.display.set_caption('ID: %s, Games Played: %d' % (self.seed, len(scores)))
		
		return scores

	def gameTestsM(self, n):
		file = open("scores%s.csv" % (self.seed), 'a+')
		for i in range(1, n + 1):
			file.write(str(self.gameTestM()) + "\n")
			if i % 8 == 0:
				print("Games Played in cycle: %d" % (i))
		file.close()

	def gameTestM(self):
		self.getModel()
		return self.gameTest(self.model)

def playTrain(seed, n, limit, chance):
	seed = str(seed)
	try:
		os.remove("data%s.csv" % (seed))
		os.remove("scores%s.csv" % (seed))
	except FileNotFoundError:
		True

	game = Game(seed, limit, chance)
	game.gameTestsM(n)
	game.trainModel("data%s.csv" % (seed))
	game.setModel()
	
	scorefile = open("scores%s.csv" % (seed))
	lines = scorefile.readlines()
	scores = []
	for line in lines:
		scores += [int(line[:-1])]
	
	out = { "min" : min(scores), "max" : max(scores), "median" : stats.median(scores), "mean" : stats.mean(scores), "stdev" : stats.stdev(scores) }
	scorefile.close()
	return out
