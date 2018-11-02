import random
import pygame

pygame.init()

display_width = 800
display_height = 600
carWidth = 80
dx = 10
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Heist: SinglePlayer')

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


def thing(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def drawBlock(block):
    thing(block[3], block[4], block[1], block[2], colors[block[5]])

blockStartx = display_width/2
blockStarty = 0
blockWidth = 100
blockHeight = 100
blockSpeed = 7.0
speedDelta = 0.2
blockX = blockStartx
blockY = blockStarty
blockDefault = [blockSpeed, blockWidth, blockHeight, blockX, blockY, 0]
blocks = [blockDefault]

def updateBlock(block, modelInput):
	if ((x > block[3] and x < block[3] + block[1]) or (x + carWidth > block[3] and x + carWidth < block[3] + block[1])) and ((block[4] + block[2]) >= y):
		print("You ended with a score of %d" % ((int((block[0] - blockSpeed) * 100))))
		crashed()
		return True
	elif block[4] < display_height + (block[2]/2):
		block[4] += int(block[0])
		return False
	elif block[4] >= display_height + block[2]/2:
#		print("your score: %d" % ((int((block[0] - blockSpeed) * 100))))
		block[3] = random.randint(0, display_width - block[1])
		block[4] = 0
		file = open("learningData.csv", "a")
		file.write(modelInput)
		file.close()
		block[0] += speedDelta
#		print(int(block[0]))
		return True

def crashed():
	pygame.quit()
	quit()

currentString = ""
while not quited:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quited = True
	
	keyDir = 0
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT and x > 0:
			x += -1 * dx
			keyDir = -1
		elif event.key == pygame.K_RIGHT and x < (display_width - carWidth):
			x += dx
			keyDir = 1

	gameDisplay.fill(black)
	car(x,y)

	if keyDir != 0:
		currentString += ("%d,%d,%d,%d,%d,%d\n" % (x,y,blocks[0][3],blocks[0][4],blocks[0][0],keyDir) )

	for block in blocks:
		if updateBlock(block, currentString):
			currentString = ""
		drawBlock(block)

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
