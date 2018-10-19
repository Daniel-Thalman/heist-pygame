import pygame
import socket

print("Loading...")

# TCP Connoction setup
#addressFile = open("address.txt", 'r')
TCP_IP = "jamulan.com"
TCP_PORT = 5005
# addressFile.close()
sock = socket.socket(socket.AF_INET, # Internet
				 socket.SOCK_STREAM) # TCP
variableName = True
while variableName:
	try:
		sock.bind((TCP_IP, TCP_PORT))
		variableName = False
	except OSError:
		variableName = True
sock.listen(1)
######
input("Press return when your enemy is ready")

conn, addr = sock.accept()

pygame.init()

display_width = 800
display_height = 600
carWidth = 80
dx = 10
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Heist: Car')

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
blockSpeed = 5.0
speedDelta = 0.1
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
		conn.send(str.encode("?"))
		block[3] = float(conn.recv(64).decode())
		block[4] = 0
		block[0] += speedDelta
#		print(int(block[0]))

def crashed():
	conn.send(str.encode("You win.  The car got a score of %d" % ((int((block[0] - blockSpeed) * 100)))))
	
	conn.close()
	pygame.quit()
	quit()
	
while not quited:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quited = True

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT and x > 0:
			x += -1 * dx
		elif event.key == pygame.K_RIGHT and x < (display_width - carWidth):
			x += dx
	dataToSend = str(x) + "," + str(y)
	for block in blocks:
		for atribute in block:
			dataToSend += ("," + str(int(atribute)))
		dataToSend += ","
	conn.send(str.encode(dataToSend))

	gameDisplay.fill(black)
	car(x,y)

	for block in blocks:
		updateBlock(block)
		drawBlock(block)

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
conn.close()
