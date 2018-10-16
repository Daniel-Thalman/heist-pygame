import pygame
import socket

# UDP connection setup
UDP_IP_recv = "172.17.59.194"
UDP_IP_send = "jamulan.com"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP_recv, UDP_PORT))
#####

pygame.init()

display_width = 800
display_height = 600
carWidth = 80
dx = 10
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')

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
    thing(block[3], block[4], block[1], block[2], colors[ int(block[5]) ] )

blockStartx = float(display_width/2)
blockStarty = 0
blockWidth = 100
blockHeight = 100
blockSpeed = 3.0
speedDelta = 0.1
blockX = blockStartx
blockY = blockStarty
blockDefault = [blockSpeed, blockWidth, blockHeight, blockX, blockY, 2]
blocks = [blockDefault]

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
	
	dataToSend = str(blocks[0][3])
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	sock.sendto(str.encode(dataToSend), (UDP_IP_send, UDP_PORT))
	dataRecived = data.decode()
	dataOut = dataRecived.split(',')
	x = float(dataOut[0])
	y = float(dataOut[1])
	tmp = []
	for i in range(2,8):
		tmp.append(float(dataOut[i]))

	try:
		blocks[1] = tmp
	except IndexError:
		blocks.append(tmp)

	gameDisplay.fill(black)
	car(x,y)

	for block in blocks:
		drawBlock(block)

	pygame.display.update()
	clock.tick(60)
