import random
import pygame
import numpy as np
import os
import statistics as stats
from keras.models import model_from_json, Sequential
from multiprocessing import Process
import compileModel as CM

class Game():


	def __init__(self):
		self.display_width = 800
		self.display_height = 600
		self.carWidth = 75
		self.carHeight = 157
		self.dx = 10
		
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		self.colors = [self.red, self.green, self.blue]
		
		self.reset()
		
	def __init__(self, seed, limit, chance):
		
		self.limit = limit
		self.chance = chance
		self.seed = str(seed)
		
		self.display_width = 800
		self.display_height = 600
		self.carWidth = 75
		self.carHeight = 157
		self.dx = 10
		
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		self.colors = [self.red, self.green, self.blue]
		
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
		try:
			self.model.load_weights("weights%s.hdf5" % (self.seed))
		except OSError:
			CM.train(self.model, self.seed)
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
		if ((self.x > block[3] and self.x < block[3] + block[1]) or (self.x + self.carWidth > block[3] and self.x + self.carWidth < block[3] + block[1])) and ((block[4] + block[2]) >= self.y and block[4] < (self.y + self.carHeight)):
			print("You ended with a score of %d" % (self.getScore()))
			return True
		elif block[4] < self.display_height + (block[2]/2):
			block[4] += int(block[0])
		elif block[4] >= self.display_height + block[2]/2:
			block[3] = random.randint(0, self.display_width - block[1])
			block[4] = 0
			block[0] += self.speedDelta
			self.currentGameInputs += self.currentString
			self.currentString = ""
		return False

	def cleanup(self):
		pygame.quit()
		quit()
	
	def getScore(self):
		return int((self.blocks[0][0] - self.blockSpeed) * 10)
	
	def gameTestNoVis(self, mod):
		self.reset()
		pygame.quit()
		while not self.quited:
			
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

			if self.limit != -1 and keydir != 0:
				self.currentString += ("%d,%d,%d,%d,%d,%d\n" % (self.x,self.y,self.blocks[0][3],self.blocks[0][4],self.blocks[0][0],keydir) )
			
			for block in self.blocks:
				self.quited = self.updateBlock(block)

		
		score = self.getScore()
		if self.limit != -1 and score > self.limit:
			datafile = open("data%s.csv" % (self.seed), 'a')
			datafile.write(self.currentGameInputs)
			datafile.close()
		return score

	def gameUsrIn(self):
		pygame.quit()
		pygame.init()
		pygame.display.init()
		
		self.reset()
			
		self.clock = pygame.time.Clock()
		self.carImg = pygame.image.load('racecar.png')

		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		pygame.display.set_caption('UsrInput')

		while not self.quited:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quited = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and self.x > 0:
					self.x += -1 * self.dx
				elif event.key == pygame.K_RIGHT and self.x < (self.display_width - self.carWidth):
					self.x += self.dx

			self.gameDisplay.fill(self.black)
			self.car(self.x,self.y)

			for block in self.blocks:
				self.quited = self.updateBlock(block)
				self.drawBlock(block)
			
			pygame.display.update()
			self.clock.tick(60)

	def gameTest(self, mod):
		pygame.quit()
		pygame.init()
		pygame.display.init()
		
		self.reset()
			
		self.clock = pygame.time.Clock()
		self.carImg = pygame.image.load('racecar.png')

		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		pygame.display.set_caption('ID: %s' % (self.seed))
		
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
			if self.limit != -1 and keydir != 0:
				self.currentString += ("%d,%d,%d,%d,%d,%d\n" % (self.x,self.y,self.blocks[0][3],self.blocks[0][4],self.blocks[0][0],keydir) )
			
			for block in self.blocks:
				self.quited = self.updateBlock(block)
				self.drawBlock(block)

			pygame.display.update()
			self.clock.tick(60)
		
		score = self.getScore()
		if self.limit != -1 and score > self.limit:
			datafile = open("data%s.csv" % (self.seed), 'a')
			datafile.write(self.currentGameInputs)
			datafile.close()
		return score

	def gameTests(self, mods):
		scores = []
		for mod in mods:
			scores += self.gameTest(mod)
		
		return scores

	def gameTestsM(self, n):
		file = open("scores%s.csv" % (self.seed), 'a+')
		for i in range(1, n + 1):
			file.write(str(self.gameTestM()) + "\n")
#			if i % (n//4) == 0:
#				print("Games Played in cycle: %d" % (i))
		file.close()
		pygame.quit()
	
	def pureTest(self, n):
		file = open("scores%s.csv" % (self.seed), 'a+')
		self.getModel()
		for i in range(1, n + 1):
			file.write(str(self.gameTest(self.model)) + "\n")
		file.close()
		pygame.quit()

	def gameTestM(self):
		self.getModel()
		return self.gameTestNoVis(self.model)

def getStats(seed):
	scorefile = open("scores%s.csv" % (seed))
	lines = scorefile.readlines()
	scores = []
	for line in lines:
		scores += [int(line[:-1])]
	
	out = { "min" : min(scores), "max" : max(scores), "median" : stats.median(scores), "mean" : stats.mean(scores), "stdev" : stats.stdev(scores) }
	scorefile.close()
	return out

def pureGames(seed, n):
	game = Game(seed, -1, 0)
	game.pureTest(n)
	return True

def playGames(seed, n, limit, chance):
	game = Game(seed, limit, chance)
	game.gameTestsM(n)
	return True

def train(seed):
	try:
		modelFile = open("model.json")
		model = model_from_json(modelFile.read())
		modelFile.close()
	except OSError:
		model = CM.compile()
	
	model.compile(loss='squared_hinge', optimizer='adam', metrics=['accuracy'])
	
	try:
		model.load_weights("weights%s.hdf5" % (seed))
	except OSError:
		CM.train(model, seed)

	dataFile = open("data%s.csv" % (seed))

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

	history = model.fit(x_values, y_values, epochs=5, batch_size=16)
	metrics = history.history
	return metrics
	
def playPure(seed, n, numProcess):
	seed = str(seed)
	newN = n//numProcess
	
	try:
		os.remove("scores%s.csv" % (seed))
	except FileNotFoundError:
		True
	open("scores%s.csv" % (seed), "w").close()
	pureGames(seed, n)
	processes = []
#	for i in range(numProcess):
#		processes += [ Process(target=pureGames, args=(seed, newN)) ]
#		processes[i].start()
#	for process in processes:
#		process.join()
	
	scorefile = open("scores%s.csv" % (seed), "r")
	lines = scorefile.readlines()
	scores = []
	for line in lines:
		scores += [int(line[:-1])]
	
	out = { "min" : min(scores), "max" : max(scores), "median" : stats.median(scores), "mean" : stats.mean(scores), "stdev" : stats.stdev(scores) }
	scorefile.close()
	return out

def playTrain(seed, n, limit, chance, numProcess):
	seed = str(seed)
	try:
		os.remove("data%s.csv" % (seed))
		os.remove("scores%s.csv" % (seed))
	except FileNotFoundError:
		True
	
	newN = n//numProcess
	processes = []
#	for i in range(numProcess):
#		processes += [Process(target=playGames, args=(seed, newN, limit, chance))]
#		processes[i].start()
#	for process in processes:
#		process.join()
	playGames(seed, newN, limit, chance)
	
	train(seed)
	
	scorefile = open("scores%s.csv" % (seed))
	lines = scorefile.readlines()
	scores = []
	for line in lines:
		scores += [int(line[:-1])]
	
	out = { "min" : min(scores), "max" : max(scores), "median" : stats.median(scores), "mean" : stats.mean(scores), "stdev" : stats.stdev(scores) }
	scorefile.close()
	return out
