import random
import pygame
import numpy as np
from keras.models import model_from_json, Sequential

modelFile = open("model.json")
model = model_from_json(modelFile.read())
model.load_weights("weights.hdf5")
modelFile.close()

pygame.init()

display_width = 800
display_height = 600
carWidth = 80
dx = 10
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Heist: Model')

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

x = (display_width * 0.45)
y = (display_height * 0.7)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('font.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def scoreDisplay(text):
    largeText = pygame.font.Font('font.ttf', 30)
    TextSurf, TextRect = text_objects(str(text), largeText)
    TextRect.center = (display_width/2, 30)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def thing(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def drawBlock(block):
    thing(block[3], block[4], block[1], block[2], colors[block[5]])

blockStartx = display_width/2
blockStarty = 0
blockWidth = 100
blockHeight = 100
blockSpeed = 7.0
speedDelta = 0.4
blockX = blockStartx
blockY = blockStarty
blockDefault = [blockSpeed, blockWidth, blockHeight, blockX, blockY, 0]
blocks = [blockDefault]

def updateBlock(block):
	if ((x > block[3] and x < block[3] + block[1]) or (x + carWidth > block[3] and x + carWidth < block[3] + block[1])) and ((block[4] + block[2]) >= y):
		print("You ended with a score of %d" % ((int((block[0] - blockSpeed) * 100))))
		crashed()
	elif block[4] < display_height + (block[2]/2):
		block[4] += int(block[0])
	elif block[4] >= display_height + block[2]/2:
#		print("your score: %d" % ((int((block[0] - blockSpeed) * 100))))
		block[3] = random.randint(0, display_width - block[1])
		block[4] = 0
		block[0] += speedDelta
#		print(int(block[0]))

def crashed():
	pygame.quit()
	quit()

	
while not quited:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quited = True
	
	x_values = np.array( [[ x, y, blocks[0][3], blocks[0][4], blocks[0][0] ]] )
	
	prediction = model.predict(x_values).tolist()[0]
	maxVal = max(prediction)
	prediction = prediction.index(maxVal) - 1

	if prediction == -1 and x > 0:
		x += -1 * dx
	elif prediction == 1 and x < (display_width - carWidth):
		x += dx
	
	gameDisplay.fill(black)
	car(x,y)

	for block in blocks:
		updateBlock(block)
		drawBlock(block)

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
