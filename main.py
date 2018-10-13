#!/bin/py
import random
import pygame

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

clock = pygame.time.Clock()
quited = False
crashed = False
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
    thing(block[3], block[4], block[1], block[2], block[5])

blockStartx = display_width/2
blockStarty = 0
blockWidth = 100
blockHeight = 100
blockSpeed = 3.0
speedDelta = 0.1
blockX = blockStartx
blockY = blockStarty
blockDefault = [blockSpeed, blockWidth, blockHeight, blockX, blockY, red, 0.0]
blocks = [blockDefault]

def updateBlock(block):
    if ((block[3] > x and block[3] < x + carWidth) or (block[3] + blockWidth > x and block[3] + block[1] < x + carWidth)) and ((block[4] + block[2]) >= y):
        crashed = True
    elif block[4] < display_height + (block[2]/2):
        block[4] += block[0]
    elif block[4] >= display_height + block[2]/2:
        block[3] = random.randint(0, display_width - block[1])
        block[4] = 0
        block[0] += speedDelta
        block[6] += 1

while not quited:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quited = True
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and x > 0:
            x += -1 * dx
        elif event.key == pygame.K_RIGHT and x < (display_width - carWidth):
            x += dx

    gameDisplay.fill(black)
    car(x,y)
    
    score = 0.0
    for block in blocks:
        updateBlock(block)
        score += block[6]
        scoreDisplay(score)
        drawBlock(block)

    if crashed == True:
        message_display("GAME OVER")
        break
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
