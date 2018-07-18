from PIL import Image
from PIL import ImageDraw

xo = lambda x: "X" if x == 1 else "O" if x == -1 else " "

rmap =  {(0,0):(0,2),(0,1):(1,2),(0,2):(2,2),(1,0):(0,1),(1,1):(1,1),(1,2):(2,1),(2,0):(0,0),(2,1):(1,0),(2,2):(2,0)} # @
rmaph = {(0,0):(2,0),(0,1):(2,1),(0,2):(2,2),(1,0):(1,0),(1,1):(1,1),(1,2):(1,2),(2,0):(0,0),(2,1):(0,1),(2,2):(0,2)} # -
rmapv = {(0,0):(0,2),(0,1):(0,1),(0,2):(0,0),(1,0):(1,2),(1,1):(1,1),(1,2):(1,0),(2,0):(2,2),(2,1):(2,1),(2,2):(2,0)} # |
rmapd = {(0,0):(0,0),(0,1):(1,0),(0,2):(2,0),(1,0):(0,1),(1,1):(1,1),(1,2):(2,1),(2,0):(0,2),(2,1):(1,2),(2,2):(2,2)} # \
rmapP = {(0,0):(2,2),(0,1):(1,2),(0,2):(0,2),(1,0):(2,1),(1,1):(1,1),(1,2):(0,1),(2,0):(2,0),(2,1):(1,0),(2,2):(0,0)} # /

def transforWrotations(data,transform = None):
		r0 = {}
		r1 = {}
		r2 = {}
		r3 = {}
		if(transform == None):
			r0 = data
		else:
			for k in data:
				r0[transform[k]] = data[k]
		for k in r0:
			r1[rmap[k]]=r0[k]
			r2[rmap[rmap[k]]]=r0[k]
			r3[rmap[rmap[rmap[k]]]]=r0[k]
		return([r0,r1,r2,r3])

class board:
	IMGS = ""
	NODES ="" 
	EDGES =""
	edgelist = []
	nNODES = 0
	countWins = {1:0,0:0,-1:0}
	def __init__(self):
		self.b = [[0,0,0],[0,0,0],[0,0,0]]
		self.plays = []
		self.turn = 1
		self.turnsPlayed = 0
		self.winner = 0
		self.label = str(board.nNODES)
		self.parent = None
	def copy(self,cp):
		bd = cp.boardData()
		for k in bd:
			self.b[k[0]][k[1]] = bd[k]
	def boardData(self):
		ret = {}
		for n,k in enumerate(self.b):
			for n2,k2 in enumerate(k):
				ret[(n,n2)] = self.b[n][n2]
		return(ret)
	def boardDataRotations(self):
		bd = self.boardData()
		ret = []
		ret = transforWrotations(bd,transform = None)
		ret += transforWrotations(bd,rmaph)
		ret += transforWrotations(bd,rmapv)
		ret += transforWrotations(bd,rmapd)
		ret += transforWrotations(bd,rmapP)
		return(ret)
	def playsWsiblings(self):
		if(self.parent == None):
			return(self.plays)
		genX = self.parent.plays
		genY = []
		for k in genX:
			genY += k.plays
		return(genY)
	def play(self,r,c,xo):
		b = board()
		b.copy(self)
		b.b[r][c] = self.turn
		b.turn = -1 if self.turn == 1 else 1
		b.checkWinner()
		rotations = b.boardDataRotations()
		isNew = True
		playings = self.playsWsiblings()
		for k in playings:
			check = k.boardData()
			for k2 in rotations:
				if(k2 == check):
					isNew = False
					if not((self.label,k.label) in board.edgelist):
						board.EDGES+="""{ data: { source: '"""+self.label+"""', target: '"""+k.label+"""' } },"""
						board.edgelist.append((self.label,k.label))
		if(isNew):
			board.nNODES += 1
			b.label = str(board.nNODES)
			b.turnsPlayed = self.turnsPlayed + 1
			b.parent = self
			self.plays.append(b)
			if not((self.label,b.label) in board.edgelist):
				board.EDGES+="""{ data: { source: '"""+self.label+"""', target: '"""+b.label+"""' } },"""
				board.edgelist.append((self.label,b.label))
			b.img()
	def winningPlays(self):
		ret = []
		bd = self.boardData()
		for k in bd:
				if(bd[k] == 0):
					b = board()
					b.copy(self)
					b.b[k[0]][k[1]] = self.turn
					b.checkWinner()
					if(b.winner == self.turn):
						ret.append(k)
		return(ret)
	def defensivePlays(self):
		ret = []
		opponent =  self.turn*-1
		bd = self.boardData()
		for k in bd:
				if(bd[k] == 0):
					b = board()
					b.copy(self)
					b.b[k[0]][k[1]] = opponent 
					b.checkWinner()
					if(b.winner == opponent):
						ret.append(k)
		return(ret)
	def checkWinner(self):
		if(self.b[1][1]!=0):
			if(self.b[1][1] == self.b[0][1] and self.b[1][1] == self.b[2][1]):
				self.winner = self.b[1][1]
			if(self.b[1][1] == self.b[0][0] and self.b[1][1] == self.b[2][2]):
				self.winner = self.b[1][1]
			if(self.b[1][1] == self.b[1][0] and self.b[1][1] == self.b[1][2]):
				self.winner = self.b[1][1]
			if(self.b[1][1] == self.b[2][0] and self.b[1][1] == self.b[0][2]):
				self.winner = self.b[1][1]
		if(self.b[0][0]!=0):
			if(self.b[0][0] == self.b[0][1] and self.b[0][0] == self.b[0][2]):
				self.winner = self.b[0][0]
			if(self.b[0][0] == self.b[1][0] and self.b[0][0] == self.b[2][0]):
				self.winner = self.b[0][0]
		if(self.b[2][2]!=0):
			if(self.b[2][2] == self.b[2][1] and self.b[2][2] == self.b[2][0]):
				self.winner = self.b[2][2]
			if(self.b[2][2] == self.b[1][2] and self.b[2][2] == self.b[0][2]):
				self.winner = self.b[2][2]
	def playAll(self):
		self.img()
		if(self.winner == 0):
			wp = self.winningPlays()
			dp = self.defensivePlays()
			if(len(wp)>0):
				for k in wp:
					self.play(k[0],k[1],self.turn)
			elif(len(dp)>0):
				for k in dp:
					self.play(k[0],k[1],self.turn)
			else:
				bd = self.boardData()
				for k in bd:
					if(bd[k] == 0):
						self.play(k[0],k[1],self.turn)
			for k in self.plays:
				k.playAll()
			if(len(self.plays) == 0):
				board.countWins[self.winner]+=1
		else:
			board.countWins[self.winner]+=1
		
	def playN(self,n):
		self.img()
		if(self.winner == 0 and self.turnsPlayed < n):
			wp = self.winningPlays()
			dp = self.defensivePlays()
			if(len(wp)>0):
				for k in wp:
					self.play(k[0],k[1],self.turn)
			elif(len(dp)>0):
				for k in dp:
					self.play(k[0],k[1],self.turn)
			else:
				bd = self.boardData()
				for k in bd:
					if(bd[k] == 0):
						self.play(k[0],k[1],self.turn)
			for k in self.plays:
				k.playN(n)
		else:
			print(self.report())
	def report(self):
		ret = "\n"
		ret+=" "+xo(self.b[0][0])+"|"+xo(self.b[0][1])+"|"+xo(self.b[0][2])
		ret+="\n -+-+-\n"
		ret+=" "+xo(self.b[1][0])+"|"+xo(self.b[1][1])+"|"+xo(self.b[1][2])
		ret+="\n -+-+-\n"
		ret+=" "+xo(self.b[2][0])+"|"+xo(self.b[2][1])+"|"+xo(self.b[2][2])+"\n"
		return(ret)
	def img(self):
		if(False):
			txt = self.report()
			img = Image.new('RGB', (75, 130), (255, 255, 255))
			d = ImageDraw.Draw(img)
			d.multiline_text((20, 20), txt, fill=(0, 0, 0))
			img.save(self.label+".png", 'png')
		board.IMGS+="""
		.selector('#"""+self.label+"""')
		  .css({
			'background-image': '"""+self.label+".png"+"""'
		  })"""
		board.NODES+="""{ data: { id: '"""+self.label+"""' } },"""
	def outPut(self):
		fh = open("template.js","r")
		code = fh.read()
		fh.close()
		code = code.replace("__IMGS__",self.IMGS)
		code = code.replace("__NODES__",self.NODES)
		code = code.replace("__EDGES__",self.EDGES)
		fh = open("code.js","w")
		fh.write(code)
		fh.close()
		print(board.nNODES)
		print(board.countWins)
		

b = board()
#b.playN(2)
b.playAll()
b.outPut()








