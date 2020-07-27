# following this tutorial:
# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import pygame

backColor = (0, 127, 0)
gridColor = (0, 111, 0)
railColor = (191, 191, 191)
tieColor = (180, 112, 85)
passiveColor = (191, 191, 255)
activeColor = (255, 255, 159)
carColor = [(191, 105, 238), (191, 63, 63), (63, 191, 63), (63, 63, 191),
    (127, 127, 63), (127, 63, 127), (63, 127, 127)]

displayW = 1100
displayH = 450
cellW = 90
cellH = 30

class Car:
	def __init__ (self, kind, row, col):
		self.kind = kind
		self.active = False
		self.row = row
		self.col = col

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
		    (x + 2 + i * cellW // 6, y + 10,
		    cellW // 9, cellH // 5 * 2))
	for j in range (2):
		pygame.draw.line (layer[1], railColor,
		    (x, y + 10 + j * 7),
		    (x + cellW // 2 - 1, y + 10 + j * 7), 3)

def drawRail1 (x, y):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * cellW // 6,
		    y + 9 + (0 - i) * cellH // 6,
		    cellW // 9, cellH // 5 * 2))
	for j in range (2):
		pygame.draw.line (layer[1], railColor,
		    (x, y + 10 + j * 7 + 0),
		    (x + cellW // 2 - 1, y + 10 + j * 7 - cellH // 2 + 1), 3)

def drawRail2 (x, y):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * cellW // 6,
		    y + 9 + (i - 2) * cellH // 6,
		    cellW // 9, cellH // 5 * 2))
	for j in range (2):
		pygame.draw.line (layer[1], railColor,
		    (x, y + 10 + j * 7 - cellH // 2 + 1),
		    (x + cellW // 2 - 1, y + 10 + j * 7 + 0), 3)

def drawGoal (x, y, c):
	pygame.draw.rect (layer[2], carColor[c],
	    (x + 5, y + cellH // 5 * 4 - 1, cellW - 10, cellH // 5))

def drawTile (x, y, kind):
	if kind & TileKind.L:
		drawRail0 (x + 0, y + 0)
	if kind & TileKind.R:
		drawRail0 (x + cellW // 2, y + 0)
	if kind & TileKind.LD:
		drawRail1 (x + 0, y + cellH // 2)
	if kind & TileKind.RU:
		drawRail1 (x + cellW // 2, y + 0)
	if kind & TileKind.LU:
		drawRail2 (x + 0, y + 0)
	if kind & TileKind.RD:
		drawRail2 (x + cellW // 2, y + cellH // 2)
	if kind & (TileKind.GOAL * 7):
		drawGoal (x, y, kind & 7)

def drawCar (car):
	x = boardX + car.col * cellW
	y1 = boardY + car.row * cellH
	y2 = boardY + car.row * cellH
	curColor = activeColor if car.active else passiveColor
	pygame.draw.circle (layer[0], curColor,
	    (x + cellW // 4 * 1, (y1 * 3 + y2 * 1) // 4 + 8), 10)
	pygame.draw.circle (layer[0], curColor,
	    (x + cellW // 4 * 3, (y1 * 1 + y2 * 3) // 4 + 8), 10)
	pygame.draw.line (layer[0], curColor,
	    (x + 5, y1 + 6), (x + cellW - 6, y2 + 6), 4)
	pygame.draw.line (layer[0], carColor[car.kind],
	    (x + 3, y1 - 4), (x + cellW - 4, y2 - 4), 18)

def drawGrid ():
	for row in range (rows):
		for col in range (cols):
			if board[row][col] > 0:
				pygame.draw.rect (layer[2], gridColor,
				    (boardX + col * cellW + 1,
				    boardY + row * cellH + 1,
				    cellW - 2, cellH - 2), 3)

def draw ():
	layer[2].fill (backColor)
#	drawGrid ()
	for row in range (rows):
		for col in range (cols):
			drawTile (boardX + col * cellW, boardY + row * cellH,
			    board[row][col])
	for car in cars:
		drawCar (car)
	for i in range (3)[::-1]:
		display.blit (layer[i], (0, 0))

def doMagnet (row, col, level):
	pass

def updateMagnet ():
	for car in cars:
		car.active = False

	for car0 in cars:
		if car0.kind == 0:
			car0.active = True
			doMagnet (car0.row, car0.col, magnet)

toExit = False
magnet = 1
while not toExit:
	for event in pygame.event.get ():
		print (event)
		if event.type == pygame.QUIT:
			toExit = True

	updateMagnet ()
	draw ()
	pygame.display.update ()
	clock.tick (60)

pygame.quit ()
quit ()
