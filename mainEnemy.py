import pygame
import random
import numpy as np
from keras.models import model_from_json, Sequential

modelFile = open("model.json")
model = model_from_json(modelFile.read())
model.load_weights("weights.hdf5")
modelFile.close()

display_width = 800
display_height = 600
carWidth = 80
dx = 10
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Heist: Enemy")

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
blue = (0, 0, 255)
colors = [red, green, blue]

clock = pygame.time.Clock()
quited = False
carImg = pygame.image.load('racecar.png')

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

x = (display_width * 0.65)
y = (display_height * 0.7)

def thing(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


blockStartx = float(display_width/2)
blockStarty = 0
blockWidth = 100
blockHeight = 100
blockSpeed = 7.0
speedDelta = 0.4
blockX = blockStartx
blockY = blockStarty
blockDefault = [blockSpeed, blockWidth, blockHeight, blockX, blockY, 0]
blocks = [ [0, blockWidth, blockHeight, blockStartx, 0, 2], blockDefault]


def updateBlock(block):
	if ((x > block[3] and x < block[3] + block[1]) or (x + carWidth > block[3] and x + carWidth < block[3] + block[1])) and ((block[4] + block[2]) >= y):
		print("You Won.  the car gat a score of %d" % ((int((block[0] - blockSpeed) * 100))))
		pygame.quit()
		quit()
	elif block[4] < display_height + (block[2]/2):
		block[4] += int(block[0])
	elif block[4] >= display_height + block[2]/2:
		block[3] = blocks[0][3]
		block[4] = 0
		block[0] += speedDelta

def drawBlock(block):
	if int(block[0]) == 0:
		c = 2
	else:
		c = 0
	thing(block[3], block[4], block[1], block[2], colors[c] )

while not quited:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quited = True

	if event.type == pygame.KEYDOWN:
		tmpX = int(blocks[0][3])
		if event.key == pygame.K_LEFT and tmpX > 0:
			blocks[0][3] += -1 * dx
		elif event.key == pygame.K_RIGHT and tmpX < (display_width - blocks[0][2]):
			blocks[0][3] += dx
	
	x_values = np.array( [[ x, y, blocks[1][3], blocks[1][4], blocks[1][0] ]] )
	
	prediction = model.predict(x_values).tolist()[0]
	maxVal = max(prediction)
	prediction = prediction.index(maxVal) - 1

	if prediction == -1 and x > 0:
		x += -1 * dx
	elif prediction == 1 and x < (display_width - carWidth):
		x += dx


	gameDisplay.fill(black)
	car(x,y)

	updateBlock(blocks[1])
	for block in blocks:
		drawBlock(block)

	pygame.display.update()
	clock.tick(60)

sock.close()
pygome.quit()
quit()
