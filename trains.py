# following this tutorial:
# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import pygame

backColor = (0, 127, 0)
gridColor = (0, 111, 0)
railColor = (191, 191, 191)
darkRailColor = (127, 127, 127)
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
	L_SWITCH = 1024
	R_SWITCH = 2048

boardInit = []
with open ("level.txt", encoding='utf-8') as f:
	rows, cols = map (int, f.readline ().split ())
	print (rows, cols)
	boardInit = []
	for row in range (rows):
		boardInit.append (f.readline ().strip ()[:cols])

"""
boardInit = [r"..............",
             r".V--p--q----U.",
             r".../....\.....",
             r".-d-v-u--b-t-.",
             r".............."]
"""

"""
boardInit = [r"..............",
             r".Uzq---t--puZ.",
             r".Vy-bq--pd-vY.",
             r".Wx---bd---wX.",
             r".............."]
"""

rows = len (boardInit)
cols = len (boardInit[0])
print (rows, cols)

boardX = (displayW - cellW * cols) // 2
boardY = (displayH - cellH * rows) // 2

cars = []
rootCar = None
board = [[0 for col in range (cols)] for row in range (rows)]
carLink = [[None for col in range (cols)] for row in range (rows)]
for row in range (rows):
	for col in range (cols):
		cur = boardInit[row][col]

		if cur >= 't' and cur <= 'z':
			car = Car (ord (cur) - ord ('t'), row, col)
			cars.append (car)
			carLink[row][col] = car
			if cur == 't':
				rootCar = car
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
			board[row][col] |= TileKind.L | TileKind.R
			board[row][col] |= TileKind.LD | TileKind.L_SWITCH
		elif cur == 'b':
			board[row][col] |= TileKind.L | TileKind.R
			board[row][col] |= TileKind.LU | TileKind.L_SWITCH
		elif cur == 'q':
			board[row][col] |= TileKind.L | TileKind.R
			board[row][col] |= TileKind.RD | TileKind.R_SWITCH
		elif cur == 'd':
			board[row][col] |= TileKind.L | TileKind.R
			board[row][col] |= TileKind.RU | TileKind.R_SWITCH
		else:
			assert (False)

def dirLeft (row, col):
	cur = board[row][col]
	if (cur & TileKind.L) > 0 and \
	    ((cur & TileKind.SWITCH) == 0 or (cur & TileKind.L_SWITCH == 0)):
		return 0
	if (cur & TileKind.LD) > 0 and \
	    ((cur & TileKind.SWITCH) > 0 or (cur & TileKind.L) == 0):
		return +1
	if (cur & TileKind.LU) > 0 and \
	    ((cur & TileKind.SWITCH) > 0 or (cur & TileKind.L) == 0):
		return -1
	assert (False)

def dirRight (row, col):
	cur = board[row][col]
	if (cur & TileKind.R) > 0 and \
	    ((cur & TileKind.SWITCH) == 0 or (cur & TileKind.R_SWITCH == 0)):
		return 0
	if (cur & TileKind.RD) > 0 and \
	    ((cur & TileKind.SWITCH) > 0 or (cur & TileKind.R) == 0):
		return +1
	if (cur & TileKind.RU) > 0 and \
	    ((cur & TileKind.SWITCH) > 0 or (cur & TileKind.R) == 0):
		return -1
	assert (False)

def coordLeft (row, col):
	return row + dirLeft (row, col), col - 1

def coordRight (row, col):
	return row + dirRight (row, col), col + 1

pygame.init ()

display = pygame.display.set_mode ((displayW, displayH))
layer = []
for i in range (3):
	layer.append (pygame.Surface ((displayW, displayH)))
	layer[-1].set_colorkey ((0, 0, 0))
pygame.display.set_caption ('Trains')

clock = pygame.time.Clock ()

def drawRail0 (x, y, is_active):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * cellW // 6, y + 10,
		    cellW // 9, cellH // 5 * 2))
	for j in range (2):
		pygame.draw.line (layer[0 if is_active else 1],
		    railColor if is_active else darkRailColor,
		    (x, y + 10 + j * 7),
		    (x + cellW // 2 - 1, y + 10 + j * 7), 3)

def drawRail1 (x, y, is_active):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * cellW // 6,
		    y + 9 + (0 - i) * cellH // 6,
		    cellW // 9, cellH // 5 * 2))
	for j in range (2):
		pygame.draw.line (layer[0 if is_active else 1],
		    railColor if is_active else darkRailColor,
		    (x, y + 10 + j * 7 + 0),
		    (x + cellW // 2 - 1, y + 10 + j * 7 - cellH // 2 + 1), 3)

def drawRail2 (x, y, is_active):
	for i in range (3):
		pygame.draw.rect (layer[2], tieColor,
		    (x + 2 + i * cellW // 6,
		    y + 9 + (i - 2) * cellH // 6,
		    cellW // 9, cellH // 5 * 2))
	for j in range (2):
		pygame.draw.line (layer[0 if is_active else 1],
		    railColor if is_active else darkRailColor,
		    (x, y + 10 + j * 7 - cellH // 2 + 1),
		    (x + cellW // 2 - 1, y + 10 + j * 7 + 0), 3)

def drawGoal (x, y, c):
	pygame.draw.rect (layer[2], carColor[c],
	    (x + 5, y + cellH // 5 * 4 - 1, cellW - 10, cellH // 5))

def drawTile (row, col):
	x = boardX + col * cellW
	y = boardY + row * cellH
	kind = board[row][col]
	if kind > 0:
		left = dirLeft (row, col)
		right = dirRight (row, col)
	if kind & TileKind.L:
		drawRail0 (x + 0, y + 0, left == 0)
	if kind & TileKind.R:
		drawRail0 (x + cellW // 2, y + 0, right == 0)
	if kind & TileKind.LD:
		drawRail1 (x + 0, y + cellH // 2, left == +1)
	if kind & TileKind.RU:
		drawRail1 (x + cellW // 2, y + 0, right == -1)
	if kind & TileKind.LU:
		drawRail2 (x + 0, y + 0, left == -1)
	if kind & TileKind.RD:
		drawRail2 (x + cellW // 2, y + cellH // 2, right == +1)
	if kind & (TileKind.GOAL * 7):
		drawGoal (x, y, kind & 7)

def drawCar (car):
	x = boardX + car.col * cellW
	y1 = boardY + car.row * cellH
	y1 += dirLeft (car.row, car.col) * cellH // 4
	y2 = boardY + car.row * cellH
	y2 += dirRight (car.row, car.col) * cellH // 4
	curColor = activeColor if car.active else passiveColor
	pygame.draw.circle (layer[0], curColor,
	    (x + cellW // 4 * 1, (y1 * 2 + y2 * 0) // 2 + 8), 10)
	pygame.draw.circle (layer[0], curColor,
	    (x + cellW // 4 * 3, (y1 * 0 + y2 * 2) // 2 + 8), 10)
	pygame.draw.line (layer[0], curColor,
	    (x + 5, (y1 * 32 + y2 * -9) // 23 + 6),
	    (x + cellW - 6, (y1 * -9 + y2 * 32) // 23 + 6), 4)
	pygame.draw.line (layer[0], carColor[car.kind],
	    (x + 3, (y1 * 32 + y2 * -9) // 23 - 4),
	    (x + cellW - 4, (y1 * -9 + y2 * 32) // 23 - 4), 18)

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
	layer[1].fill ((0, 0, 0))
	layer[0].fill ((0, 0, 0))
#	drawGrid ()
	for row in range (rows):
		for col in range (cols):
			drawTile (row, col)
	for car in cars:
		drawCar (car)
	for i in range (3)[::-1]:
		display.blit (layer[i], (0, 0))

def doMagnet (row, col, level):
	pass

def clearMagnet ():
	for car in cars:
		car.active = False

def updateMagnet (car, magnet_power):
	car.active = True
	row, col = car.row, car.col
	for i in range (magnet_power):
		row, col = coordLeft (row, col)
		if carLink[row][col]:
			carLink[row][col].active = True
		else:
			break
	row, col = car.row, car.col
	for i in range (magnet_power):
		row, col = coordRight (row, col)
		if carLink[row][col]:
			carLink[row][col].active = True
		else:
			break

def moveCar (car, row, col):
	carLink[car.row][car.col] = None
	car.row, car.col = row, col
	carLink[car.row][car.col] = car

def moveLeft (car, magnet_power):
	next_row, next_col = coordLeft (car.row, car.col)
	if board[next_row][next_col] == 0:
		return False
	if next_row + dirRight (next_row, next_col) != car.row:
		return False
	if not carLink[next_row][next_col] or \
	    moveLeft (carLink[next_row][next_col], 0):
		moveCar (car, next_row, next_col)
		if magnet_power > 0:
			prev_row, prev_col = coordRight (car.row, car.col)
			prev_row, prev_col = coordRight (prev_row, prev_col)
			if carLink[prev_row][prev_col]:
				moveLeft (carLink[prev_row][prev_col], \
				    magnet_power - 1)
		return True
	return False

def moveRight (car, magnet_power):
	next_row, next_col = coordRight (car.row, car.col)
	if board[next_row][next_col] == 0:
		return False
	if next_row + dirLeft (next_row, next_col) != car.row:
		return False
	if not carLink[next_row][next_col] or \
	    moveRight (carLink[next_row][next_col], 0):
		moveCar (car, next_row, next_col)
		if magnet_power > 0:
			prev_row, prev_col = coordLeft (car.row, car.col)
			prev_row, prev_col = coordLeft (prev_row, prev_col)
			if carLink[prev_row][prev_col]:
				moveRight (carLink[prev_row][prev_col], \
				    magnet_power - 1)
		return True
	return False

def toggleLeft (car):
	next_row, next_col = coordLeft (car.row, car.col)
	if board[next_row][next_col] == 0:
		return False
	if carLink[next_row][next_col]:
		return toggleLeft (carLink[next_row][next_col])
	elif (board[next_row][next_col] & TileKind.L_SWITCH) > 0 or \
	    (board[next_row][next_col] & TileKind.R_SWITCH) > 0:
		board[next_row][next_col] ^= TileKind.SWITCH
		return True
	return False

def toggleRight (car):
	next_row, next_col = coordRight (car.row, car.col)
	if board[next_row][next_col] == 0:
		return False
	if carLink[next_row][next_col]:
		return toggleRight (carLink[next_row][next_col])
	elif (board[next_row][next_col] & TileKind.L_SWITCH) > 0 or \
	    (board[next_row][next_col] & TileKind.R_SWITCH) > 0:
		board[next_row][next_col] ^= TileKind.SWITCH
		return True
	return False

toExit = False
magnet = 1
while not toExit:
	for event in pygame.event.get ():
		print (event)
		if event.type == pygame.QUIT:
			toExit = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moveLeft (rootCar, magnet)
			elif event.key == pygame.K_RIGHT:
				moveRight (rootCar, magnet)
			elif event.key == pygame.K_UP:
				magnet = min (6, magnet + 1)
			elif event.key == pygame.K_DOWN:
				magnet = max (0, magnet - 1)
			elif event.key == pygame.K_SPACE:
				toggleLeft (rootCar)
				toggleRight (rootCar)

	clearMagnet ()
	updateMagnet (rootCar, magnet)
	draw ()
	pygame.display.update ()
	clock.tick (60)

pygame.quit ()
quit ()
