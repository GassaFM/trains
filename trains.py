# following this tutorial:
# https://pythonprogramming.net/pygame-python-3-part-1-intro/
import enum
import pygame

backColor = (0, 127, 0)
railColor = (191, 191, 191)
tieColor = (160, 82, 45)

displayW = 800
displayH = 600
cellW = 50
cellH = 20

class CarKind (enum.Enum):
	CAR_0 = 0
	CAR_1 = 1
	CAR_2 = 2
	CAR_3 = 3
	CAR_4 = 4
	CAR_5 = 5
	LOCOMOTIVE = 6

class Car:
	def __init__ (self, kind, row, col):
		self.kind = kind
		self.row = row
		self.row = col

class TileKind (enum.Enum):
	EMPTY = 0
	L_R = 1
	LD_RU = 2
	LU_RD = 3
	SWITCH_LD_0 = 4
	SWITCH_LD_1 = 5
	SWITCH_LU_0 = 6
	SWITCH_LU_1 = 7
	SWITCH_RD_0 = 8
	SWITCH_RD_1 = 9
	SWITCH_RU_0 = 10
	SWITCH_RU_1 = 11
	GOAL_0 = 12
	GOAL_1 = 13
	GOAL_2 = 14
	GOAL_3 = 15
	GOAL_4 = 16
	GOAL_5 = 17

boardInit = [r"..............",
             r".V--p--q----U.",
             r".../....\.....",
             r".-d-v-u--b-t-.",
             r".............."]

rows = len (boardInit)
cols = len (boardInit[0])

boardX = (displayW - cellW * cols) // 2
boardY = (displayH - cellH * cols) // 2

cars = []
board = [[TileKind.EMPTY for col in range (cols)] for row in range (rows)]
for row in range (rows):
	for col in range (cols):
		print (row, col)
		cur = boardInit[row][col]
		if cur == 't':
			cars.append (Car (CarKind.LOCOMOTIVE, row, col))
			cur = '.'
		elif cur == 'u':
			cars.append (Car (CarKind.CAR_0, row, col))
			cur = '.'
		elif cur == 'v':
			cars.append (Car (CarKind.CAR_1, row, col))
			cur = '.'
		elif cur == 'w':
			cars.append (Car (CarKind.CAR_2, row, col))
			cur = '.'
		elif cur == 'x':
			cars.append (Car (CarKind.CAR_3, row, col))
			cur = '.'
		elif cur == 'y':
			cars.append (Car (CarKind.CAR_4, row, col))
			cur = '.'
		elif cur == 'z':
			cars.append (Car (CarKind.CAR_5, row, col))
			cur = '.'
		if cur == '.':
			board[row][col] = TileKind.EMPTY
		elif cur == '-':
			board[row][col] = TileKind.L_R
		elif cur == '/':
			board[row][col] = TileKind.LD_RU
		elif cur == '\\':
			board[row][col] = TileKind.LU_RD
		elif cur == 'p':
			board[row][col] = TileKind.SWITCH_LD_0
		elif cur == 'b':
			board[row][col] = TileKind.SWITCH_LU_0
		elif cur == 'q':
			board[row][col] = TileKind.SWITCH_RD_0
		elif cur == 'd':
			board[row][col] = TileKind.SWITCH_RU_0
		elif cur == 'U':
			board[row][col] = TileKind.GOAL_0
		elif cur == 'V':
			board[row][col] = TileKind.GOAL_1
		elif cur == 'W':
			board[row][col] = TileKind.GOAL_2
		elif cur == 'X':
			board[row][col] = TileKind.GOAL_3
		elif cur == 'Y':
			board[row][col] = TileKind.GOAL_4
		elif cur == 'Z':
			board[row][col] = TileKind.GOAL_5
		else:
			assert (False)

pygame.init ()

display = pygame.display.set_mode ((displayW, displayH))
pygame.display.set_caption ('Trains')

clock = pygame.time.Clock ()

def drawTile (x, y, kind):
	if kind == TileKind.EMPTY:
		pass
	elif kind == TileKind.L_R:
		for i in range (5):
			pygame.draw.rect (display, tieColor,
			    (x + 3 + i * 10, y + 10, 4, 9), 0)
		pygame.draw.lines (display, railColor, False,
		    [(x, y + 10), (x + 49, y + 10)], 2)
		pygame.draw.lines (display, railColor, False,
		    [(x, y + 15), (x + 49, y + 15)], 2)
	elif kind == TileKind.LD_RU:
		for i in range (5):
			pygame.draw.rect (display, tieColor,
			    (x + 3 + i * 10, y + 10 + 8 - i * 4, 4, 9), 0)
		pygame.draw.lines (display, railColor, False,
		    [(x, y + 10 + 10), (x + 49, y + 10 - 10)], 2)
		pygame.draw.lines (display, railColor, False,
		    [(x, y + 15 + 10), (x + 49, y + 15 - 10)], 2)
	elif kind == TileKind.LU_RD:
		for i in range (5):
			pygame.draw.rect (display, tieColor,
			    (x + 3 + i * 10, y + 10 - 8 + i * 4, 4, 9), 0)
		pygame.draw.lines (display, railColor, False,
		    [(x, y + 10 - 10), (x + 49, y + 10 + 10)], 2)
		pygame.draw.lines (display, railColor, False,
		    [(x, y + 15 - 10), (x + 49, y + 15 + 10)], 2)
	else:
		pass

def draw ():
	display.fill (backColor)
	for row in range (rows):
		for col in range (cols):
			drawTile (boardX + col * cellW, boardY + row * cellH,
			    board[row][col])

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
