import random
import pygame

class Game():

	

	def mair():	
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

		x = (display_width * 0.45)
		y = (display_height * 0.7)
		
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
		
		currentString = ""
