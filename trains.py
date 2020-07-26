# following this tutorial:
# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import pygame

backColor = (0, 127, 0)
railColor = (191, 191, 191)
tieColor = (160, 82, 45)
carColor = [(175, 105, 238), (191, 63, 63), (63, 191, 63), (63, 63, 191),
    (127, 127, 63), (127, 63, 127), (63, 127, 127)]

displayW = 800
displayH = 300
cellW = 60
cellH = 24

class Car:
	def __init__ (self, kind, row, col):
		self.kind = kind
		self.row = row
		self.row = col

class TileKind:
	GOAL = 1
	L = 8
	R = 16
	LD = 32
	LU = 64
	RD = 128
	RU = 256
	SWITCH = 512

boardInit = [r"..............",
             r".V--p--q----U.",
             r".../....\.....",
             r".-d-v-u--b-t-.",
             r".............."]

rows = len (boardInit)
cols = len (boardInit[0])

boardX = (displayW - cellW * cols) // 2
boardY = (displayH - cellH * rows) // 2

cars = []
board = [[0 for col in range (cols)] for row in range (rows)]
for row in range (rows):
	for col in range (cols):
		cur = boardInit[row][col]

		if cur >= 't' and cur <= 'z':
			cars.append (Car (ord (cur) - ord ('t'), row, col))
			cur = '-'

		if cur >= 'U' and cur <= 'Z':
			board[row][col] |= TileKind.GOAL * \
			    (ord (cur) - ord ('U') + 1)
			cur = '-'

		if cur == '.':
			pass
		elif cur == '-':
			board[row][col] |= TileKind.L | TileKind.R
		elif cur == '/':
			board[row][col] |= TileKind.LD | TileKind.RU
		elif cur == '\\':
			board[row][col] |= TileKind.LU | TileKind.RD
		elif cur == 'p':
			board[row][col] |= TileKind.L | TileKind.R | TileKind.LD
		elif cur == 'b':
			board[row][col] |= TileKind.L | TileKind.R | TileKind.LU
		elif cur == 'q':
			board[row][col] |= TileKind.L | TileKind.R | TileKind.RD
		elif cur == 'd':
			board[row][col] |= TileKind.L | TileKind.R | TileKind.RU
		else:
			assert (False)

pygame.init ()

display = pygame.display.set_mode ((displayW, displayH))
layer = []
for i in range (3):
	layer.append (pygame.Surface ((displayW, displayH)))
	layer[-1].set_colorkey ((0, 0, 0))
pygame.display.set_caption ('Trains')

clock = pygame.time.Clock ()

def drawRail0 (x, y):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * 10, y + 10, 6, 9), 0)
	pygame.draw.lines (layer[1], railColor, False,
	    [(x, y + 10), (x + 29, y + 10)], 2)
	pygame.draw.lines (layer[1], railColor, False,
	    [(x, y + 15), (x + 29, y + 15)], 2)

def drawRail1 (x, y):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * 10, y + 10 - 1 - i * 4, 6, 9), 0)
	pygame.draw.lines (layer[1], railColor, False,
	    [(x, y + 10 + 0), (x + 29, y + 10 - 11)], 2)
	pygame.draw.lines (layer[1], railColor, False,
	    [(x, y + 15 + 0), (x + 29, y + 15 - 11)], 2)

def drawRail2 (x, y):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * 10, y + 10 - 9 + i * 4, 6, 9), 0)
	pygame.draw.lines (layer[1], railColor, False,
	    [(x, y + 10 - 11), (x + 29, y + 10 + 0)], 2)
	pygame.draw.lines (layer[1], railColor, False,
	    [(x, y + 15 - 11), (x + 29, y + 15 + 0)], 2)

def drawGoal (x, y, c):
	pygame.draw.rect (layer[2], carColor[c],
	    (x + 5, y + 19, 49, 4))

def drawTile (x, y, kind):
	if kind & TileKind.L:
		drawRail0 (x + 0, y + 0)
	if kind & TileKind.R:
		drawRail0 (x + 30, y + 0)
	if kind & TileKind.LD:
		drawRail1 (x + 0, y + 12)
	if kind & TileKind.RU:
		drawRail1 (x + 30, y + 0)
	if kind & TileKind.LU:
		drawRail2 (x + 0, y + 0)
	if kind & TileKind.RD:
		drawRail2 (x + 30, y + 12)
	if kind & (TileKind.GOAL * 7):
		drawGoal (x, y, kind & 7)

def draw ():
	layer[2].fill (backColor)
	for row in range (rows):
		for col in range (cols):
			drawTile (boardX + col * cellW, boardY + row * cellH,
			    board[row][col])
	for i in range (3)[::-1]:
		display.blit (layer[i], (0, 0))

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
