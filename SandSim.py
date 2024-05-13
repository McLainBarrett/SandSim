import math, operator, pygame, random
pygame.init()

class coord(object):
	x = 0
	y = 0
	def magnitude(self):
		return math.sqrt(self.x**2 + self.y**2)
	def normalized(self):
		mag = self.magnitude()
		return coord(self.x/mag, self.y/mag)
	def floored(self):
		return coord(math.floor(self.x), math.floor(self.y))
	def __init__(self,x=None,y=None):
		if x == None and y == None:
			self.x = x
			self.y = y
		elif y == None:
			self.x = x[0]
			self.y = x[1]
		else:
			self.x = x
			self.y = y        
	def __add__(self, c):
		return coord(self.x + c.x, self.y + c.y)
	def __sub__(self, c):
		return coord(self.x - c.x, self.y - c.y)
	def __mul__(self, c):
		return coord(self.x * c, self.y * c)
	def __truediv__(self, c):
		return coord(self.x / c.x, self.y / c.y)
	#def __truediv__(self, c):
		#return coord(self.x / c, self.y / c)
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
	def tuple(self):
		return (self.x, self.y)


running = True
size = coord(50, 50)
res = size * 10
screen = pygame.display.set_mode((res.x, res.y))
pygame.display.set_caption("Sand Simulator")
clock = pygame.time.Clock()
board = []
physboard = []

class Cell:
	Position = coord()
	Color = pygame.Color(0, 0, 0)
	ID = 0
	def __init__(self, pos, col):
		self.Position = pos
		self.Color = col;
		self.ID = random.randrange(0, 99999)
	def GetNs(self):
		Ns = []
		oS = [0, 1, 1, 1, 0, -1, -1, -1]
		for i in range(8):
			c = self.Position + coord(oS[i], oS[(i+2)%8])
			if 0 <= c.x < size.x and 0 <= c.y < size.y:
				Ns.append("V" if board[c.x][c.y] == None else board[c.x][c.y])
			else:
				Ns.append(None)
		return Ns
	def Move(self, move):
		global physboard
		pos = self.Position + move
		if (not (0 <= pos.y < size.y and 0 <= pos.x < size.x)):
			return False
		if (board[pos.x][pos.y] or physboard[pos.x][pos.y]):
			return False
		physboard[pos.x][pos.y] = self
		self.Position += move
		return True

def ClearBoard(board):
	board.clear()
	for x in range(size.x):
		board.append([])
		for y in range(size.y):
			board[x].append(None)

def InsertCell(offset = (0,0)):
	pos = (coord(pygame.mouse.get_pos()) / (res / size)).floored()
	pos += coord(offset)
	if (0 <= pos.y < size.y and 0 <= pos.x < size.x):
		board[pos.x][pos.y] = Cell(coord(pos.x, pos.y), pygame.Color(random.randrange(50,256), random.randrange(50,256), random.randrange(50,256)))	

def RemoveCell(offset = (0,0)):
	pos = (coord(pygame.mouse.get_pos()) / (res / size)).floored()
	pos += coord(offset)
	if (0 <= pos.y < size.y and 0 <= pos.x < size.x):
		board[pos.x][pos.y] = None

def Input():
	global running
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				ClearBoard(board)
				ClearBoard(physboard)
	if pygame.mouse.get_pressed()[0]:
		if pygame.key.get_mods() & pygame.KMOD_SHIFT:
			for pos in [(0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
				InsertCell(pos)
		else:
			InsertCell()
	if pygame.mouse.get_pressed()[2]:
		if pygame.key.get_mods() & pygame.KMOD_SHIFT:
			for pos in [(0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
				RemoveCell(pos)
		else:
			RemoveCell()
	if pygame.mouse.get_pressed()[1]:
		Phys()


def Phys():
	global board, physboard
	for x in range(size.x):
		for y in range(size.y):
			cell = board[x][y]
			if cell:
				Ns = cell.GetNs()
				
				if (Ns[0] == "V"):
					if (not cell.Move(coord(0, 1))):
						physboard[x][y] = cell
				elif(Ns[4] and Ns[4] != "V"):
					if (cell.Move(coord(-1, 0))): pass
					elif (cell.Move(coord(1, 0))): pass
					else: physboard[x][y] = cell
				else:
					physboard[x][y] = cell
			
				
	board = physboard
	physboard = []
	ClearBoard(physboard)    

def Render():
	ratio = res / size
	ratio = coord(math.floor(ratio.x), math.floor(ratio.y))
	for x in range(size.x):
		for y in range(size.y):
			cell = board[x][y]
			rect = pygame.Rect(x * ratio.x, y * ratio.y, ratio.x, ratio.y)
			if (cell == None):
				pygame.draw.rect(screen, pygame.Color(0,0,0), rect)
			else:
				pygame.draw.rect(screen, cell.Color, rect)
	pygame.display.flip()

#---

for b in [board, physboard]:
	ClearBoard(b)

def Count():
	i = 0
	for x in range(size.x):
		for y in range(size.y):
			cell = board[x][y]
			if (cell):
				i += 1
	print(i)

while(running):
	Input()
	Phys()
	Render()
	#Count()
	clock.tick(0)
pygame.quit()
