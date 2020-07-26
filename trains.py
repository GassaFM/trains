# following this tutorial:
# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import pygame

backColor = (0, 127, 0)

displayW = 800
displayH = 600
cellW = 50
cellH = 10

class Car:
	def __init__ (self, nx, ny):
		self.x = nx
		self.y = ny

board = [r"..............",
         r".V--p--q----U.",
         r".../....\.....",
         r".-d-v-u--b-t-.",
         r".............."]

pygame.init ()

display = pygame.display.set_mode ((displayW, displayH))
pygame.display.set_caption ('Trains')

clock = pygame.time.Clock ()

def draw ():
	display.fill (backColor)

toExit = False
while not toExit:
	for event in pygame.event.get ():
		print (event)
		if event.type == pygame.QUIT:
			toExit = True

	draw ()
	pygame.display.update ()
	clock.tick (60)

pygame.quit ()
quit ()
