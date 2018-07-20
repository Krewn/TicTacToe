Com = """
     _/\/\/\/\/\/\__/\/\____________________/\/\/\/\/\/\______________________________/\/\/\/\/\/\_________________________
    _____/\/\________________/\/\/\/\__________/\/\______/\/\/\________/\/\/\/\__________/\/\________/\/\/\______/\/\/\___ 
   _____/\/\______/\/\____/\/\________________/\/\__________/\/\____/\/\________________/\/\______/\/\__/\/\__/\/\/\/\/\_  
  _____/\/\______/\/\____/\/\________________/\/\______/\/\/\/\____/\/\________________/\/\______/\/\__/\/\__/\/\_______   
 _____/\/\______/\/\/\____/\/\/\/\__________/\/\______/\/\/\/\/\____/\/\/\/\__________/\/\________/\/\/\______/\/\/\/\_    
______________________________________________________________________________________________________________________     
"""

# deps for `def img` for text to image.
from PIL import Image
from PIL import ImageDraw


# Map numerical to chars so "1" is  and -1 is "O", anthing else (0) is blank.
xo = lambda x: "X" if x == 1 else "O" if x == -1 else " "

# Reflection maps for detecting redundancies in board state. See `def boardDataRotations`
rmap =  {(0,0):(0,2),(0,1):(1,2),(0,2):(2,2),(1,0):(0,1),(1,1):(1,1),(1,2):(2,1),(2,0):(0,0),(2,1):(1,0),(2,2):(2,0)}  # @
rmaph = {(0,0):(2,0),(0,1):(2,1),(0,2):(2,2),(1,0):(1,0),(1,1):(1,1),(1,2):(1,2),(2,0):(0,0),(2,1):(0,1),(2,2):(0,2)}  # -
#rmapv = {(0,0):(0,2),(0,1):(0,1),(0,2):(0,0),(1,0):(1,2),(1,1):(1,1),(1,2):(1,0),(2,0):(2,2),(2,1):(2,1),(2,2):(2,0)} # |
#rmapd = {(0,0):(0,0),(0,1):(1,0),(0,2):(2,0),(1,0):(0,1),(1,1):(1,1),(1,2):(2,1),(2,0):(0,2),(2,1):(1,2),(2,2):(2,2)} # \
#https://math.stackexchange.com/questions/2476469/taking-into-account-symmetry-how-many-possible-games-of-tic-tac-toe-are-there
rmapP = {(0,0):(2,2),(0,1):(1,2),(0,2):(0,2),(1,0):(2,1),(1,1):(1,1),(1,2):(0,1),(2,0):(2,0),(2,1):(1,0),(2,2):(0,0)}  # /

# `def transforWrotations` takes a map of `(x,y) : enum(-1,0,1)` and applys the specified transformation (reflections above)
# in addition to creating data for the 4 posibile rotated postion of each reflected board state.
def transforWrotations(data,transform = None):
		r0 = {}									#empty dictionary
		r1 = {}									#...
		r2 = {}
		r3 = {}
		if(transform == None):					# set r0 to data without changing anything.
			r0 = data
		else:									# or apply trasformation
			for k in data:						# k is the (row, column) and r0[k] is the value indicating x 0 or blank.
				r0[transform[k]] = data[k]		
# by accesing transform[index] as the index on r0 for the value data[k] for each index, we rotate or reflect the board.
		for k in r0:
			r1[rmap[k]]=r0[k]
			r2[rmap[rmap[k]]]=r0[k]
			r3[rmap[rmap[rmap[k]]]]=r0[k]		# by repeating the process multiple times to apply multiple 90 degre rotations.
		return([r0,r1,r2,r3])

		
# The `class board` is a node containing data for a specific tic-tac-toe board state, and edges to voiable plays.
class board:
#	Variables declaried here are shared between all instances of the class.
	IMGS = ""                  # This text will be inserted to the template to apply a css image property to each of the nodes.
	NODES =""                  # This text will be inserted to the template to specify the unique nodes and their id.
	EDGES =""                  # This text will be inserted to the template to specify the edges i.e. viable plays connecting board states
	edgelist = []              # This list of tuples will be kept to kepp from adding redundant edges.
	nNODES = 0                 # nNODES is a cound of unique board states.
	countWins = {1:0,0:0,-1:0} # countWins is a map of the end game state when a game state has no viable plays.
#	The `__init__()` function is called when a new instance of the class is created.
	def __init__(self):
		#Variables appended with `self.` are local to each instance of the class.
		self.b = [[0,0,0],[0,0,0],[0,0,0]]  # Each instance of a board has a 3x3 array that is the board.
		self.plays = []                     # This is effectivly the edge list in implementation it is an array of boards.
		self.turn = 1                       # This value indicates the value to be placed on the board in for each play from this board.
		self.turnsPlayed = 0			    # I try to pick reasonable variable names...
		self.winner = 0					    # Feel me?
		self.label = str(board.nNODES)      # This value is updated when a board is confirmed to be new. see: `isNew` in `play()`
		self.parent = None				    # This variable makes our nodes traversable back up edges. // eww bug maybe? could be []
#	The `copy` function is used to load provided `boarddata()` from the Board `cp` into `self.b` i.e. the board data for that game state.
	def copy(self,cp):
		bd = cp.boardData()
		for k in bd:
			self.b[k[0]][k[1]] = bd[k]
#	The `boardData` function returns a dictionary of (board positions) : 1 0 or -1
#	This is usfull for relfection and rotation of the board... `r3[rmap[rmap[rmap[k]]]]=r0[k]`
	def boardData(self):
		ret = {}							# Create an empty dictionary of key value pairs
		for n,k in enumerate(self.b):		# for each nth row k
			for n2,k2 in enumerate(k):		# for each n2th column k2
				ret[(n,n2)] = self.b[n][n2]	# (rowIndex,columnIndex) : value
		return(ret)							# Don't return None...
#	This function applys necessary reflections and rotations to obtain all possible representaitons of a given board in a list.
	def boardDataRotations(self):
		bd = self.boardData()				# Start with the flat list fro mthe above method.
		ret = []							# and an empty list
		ret = transforWrotations(bd,transform = None) # set the 4 rotated versions of the original ro the return list.
		ret += transforWrotations(bd,rmaph) # add the 4 possible rotations of the horizontal reflection of the board to the list.
#		ret += transforWrotations(bd,rmapv) # horizontal reflection + 2 rotations == vertical reflection ?
#		ret += transforWrotations(bd,rmapd) # similar story with the second diagonal refection axis.
# https://math.stackexchange.com/questions/2476469/taking-into-account-symmetry-how-many-possible-games-of-tic-tac-toe-are-there/2854110?noredirect=1#comment5886893_2854110
# I still feel like this part is overkill but I don't really care? //Todo better
		ret += transforWrotations(bd,rmapP) # add the 4 possible rotations of the diagonal reflection of the board to the list.
		return(ret)
# `playsWsiblings` gets all the board states that have been discovered with the same number of xs and os.
	def playsWsiblings(self):
		if(self.parent == None):			# The first generation of plays has no cousins.
			return(self.plays)
		genX = self.parent.plays
		genY = []
		for k in genX:						# For each of the parents generation (siblings including parents).
			genY += k.plays					# Add the children to the list.
		return(genY)
# Given a row and a colum `play(self,r,c)` uses `self.turn` to generate the board state by playing at (r,c)
	def play(self,r,c):
		b = board()							# b starts as an empty baord.
		b.copy(self)						# b copyies the instance calling play.
		b.b[r][c] = self.turn				# update the board data at secified row and colum from 0 to self.turn
		b.turn = -1 if self.turn == 1 else 1# set the turn to be played to the oposite of the parent generating board.
		b.checkWinner()						# check if the play made won.
		rotations = b.boardDataRotations()	# get the alternative representations of the board.
		isNew = True						# assume that the baord is new
		playings = self.playsWsiblings()	# get all the know plays with the same number of x's and o's
		for k in playings:					# check against each...
			check = k.boardData()			# baord representations are flat listed so we need to get flat lists from each board object in our list playings
			for k2 in rotations:			# for each representation of the board we just made a play on
				if(k2 == check):			# if that representation is known
					isNew = False			# it's not new.
					if not((self.label,k.label) in board.edgelist):	# Draw a line from this board to the play if one isn't there already.
						board.EDGES+="""{ data: { source: '"""+self.label+"""', target: '"""+k.label+"""' } },"""# This is a js object member as python text
						board.edgelist.append((self.label,k.label))#the tuple of node ids is added to the edge list so that we avoid adding edges redundantly.
		if(isNew):							# now that we have varified our assumption that the play is new we can us this value in controlling logic.
			board.nNODES += 1				# increment the number of board states global to all board instances.
			b.label = str(board.nNODES)		# convert the number to a string for use in js object members
			b.turnsPlayed = self.turnsPlayed + 1# update the turns played variable for the new board as this variable will be referenced down the line.
			b.parent = self					# set the parent of the new board to this instance of baord which called play to generate it.
			self.plays.append(b)			# add the new board to the list of viable plays for the board calling 'play'.
			if not((self.label,b.label) in board.edgelist):			# Draw a line from this board to the play if one isn't there already.
				board.EDGES+="""{ data: { source: '"""+self.label+"""', target: '"""+b.label+"""' } },"""# This is a js object member as python text
				board.edgelist.append((self.label,b.label))# do you see where this happended already? ... it's about 10 lines ago.
			b.img()							# we need to create a png for the board so that our final product doesn't look half baked.
# to reduce the decision tree we assume that wining plays are played. So a board needs to know what plays win.
	def winningPlays(self):
		ret = []							# start with an empty list. each member of the list will be a tuple with a row and a column.
		bd = self.boardData()				# get the flat list of board data (row, column): enum(-1,w/e,1)
		for k in bd:						# for each spot (row column pair in the flat list)
				if(bd[k] != 0 and bd[k] != 1):# if the spot is not x or o 
					b = board()				# make a new board
					b.copy(self)			# copy the parent
					b.b[k[0]][k[1]] = self.turn# update the empty sopt to x or o
					b.checkWinner()			# check if the board won.
					if(b.winner == self.turn):# if it won
						ret.append(k)		# add the spot `(row,column)` tuple to the list that gets returned
		return(ret)
# now that we can find winning plays we can revent them.
	def defensivePlays(self):
		ret = []							# once again we start with an empty list.
		opponent =  self.turn*-1			# given that we can make play self.turn, we need to anticipate wins for the opposite.
		bd = self.boardData()				# and we will need our friend the flat board data to get there.
		for k in bd:						# for each spot on the board.
				if(bd[k] == 0):				# if it's open
					b = board()				# make an empty board
					b.copy(self)			# copy this board to the empty one so it's not empty anymore.
					b.b[k[0]][k[1]] = opponent # make the openents play in the empty spot.
					b.checkWinner()			# see if that play won.
					if(b.winner == opponent):# if it won
						ret.append(k)		# add that spot to the list of defensive plays.
		return(ret)
# to check if a board has a winner we have a conditional for each combinations of spots that can win.
	def checkWinner(self):
		if(self.b[1][1]!=0):# if the spot is not empty it might be part of a winning combo.
			if(self.b[1][1] == self.b[0][1] and self.b[1][1] == self.b[2][1]):# if all the winning spots match the winner is the thing in the spots.
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
				self.winner = self.b[2][2] # If there were multiple winning combos on the board this logic would be preferential to what comes last.
# 'playAll' applys the current turn to each of the th open spaces
	def playAll(self):
		self.img()							# This method is our edge discovery and child generation, so it's a good time to make an image to display.
		if(self.winner != 1 and self.winner != -1):# we don't want to play boards that have a winner already so this is an important control statement.
			wp = self.winningPlays()		# knowing that there isn't a winner yet we check if we can win wirst.
			dp = self.defensivePlays()		# similarly we don't want to be won on so we have to make defensive plays second.
			if(len(wp)>0):					# check for oportunities to win
				for k in wp:
					self.play(k[0],k[1])
			elif(len(dp)>0):				# before checking if we have to defend
				for k in dp:
					self.play(k[0],k[1])
			else:							# before doing everything else.
				bd = self.boardData()
				for k in bd:
					if(bd[k] == 0):			# if the board is open.
						self.play(k[0],k[1])
			for k in self.plays:			# now that we have discovered our new children we play them.
				k.playAll()					# discover new plays for each play discovered.
			if(len(self.plays) == 0):		# If you cannot win, can't defend and can't play an empty spot this is end game, so we will count this posibility accordingly.
				board.countWins[self.winner]+=1 # as such, a draw.
		else:								# If we attempt to discover plays on a board that has a winner,
			board.countWins[self.winner]+=1	# we count that winner.
# It may be desired to play only a small number of turns off of a given board, as such the `playN` method is provided.
	def playN(self,n):
		self.img()	#we must create an image for the root node.
		if(self.winner != 1 and self.winner != -1 and self.turnsPlayed < n): # This control logic is one of 2 differences from playAll
			wp = self.winningPlays()
			dp = self.defensivePlays()
			if(len(wp)>0):
				for k in wp:
					self.play(k[0],k[1])
			elif(len(dp)>0):
				for k in dp:
					self.play(k[0],k[1])
			else:
				bd = self.boardData()
				for k in bd:
					if(bd[k] == 0):
						self.play(k[0],k[1])
			for k in self.plays:
				k.playN(n)					# Calling 'playN(n)' instead of `playAll()` is the other difference.
		else:
			print(self.report())
# reort provides a text representation that we can see as a tic tac toe baord.
	def report(self):
		ret = "\n"# starts with an empty line for vertical padding.
		ret+=" "+xo(self.b[0][0])+"|"+xo(self.b[0][1])+"|"+xo(self.b[0][2])	# converts 1 and -1 to x and o with lamda function from the global scope.
		ret+="\n -+-+-\n"													# adds the line break and board break and line break.
		ret+=" "+xo(self.b[1][0])+"|"+xo(self.b[1][1])+"|"+xo(self.b[1][2])	# "
		ret+="\n -+-+-\n"													# "
		ret+=" "+xo(self.b[2][0])+"|"+xo(self.b[2][1])+"|"+xo(self.b[2][2])+"\n"	# " with vertical padding.
		return(ret)
# for purposes of cytoscape output, because html canvas doesn't support multiline text (wtf?) we need pngs.
	def img(self):
		if(True):# we don't always want to write these images so this control statment is provided for that...
			txt = self.report()
			img = Image.new('RGB', (85, 135), (255, 255, 255))
			d = ImageDraw.Draw(img)
			d.multiline_text((20, 20), txt, fill=(0, 0, 0))
			img.save(self.label+".png", 'png') # Pretty much took that straight from stack overflow... I don't have the link rn.
		board.IMGS+="""
		.selector('#"""+self.label+"""')
		  .css({
			'background-image': '"""+self.label+".png"+"""'
		  })"""# This pythonic text is a js object member containing embedded css... yeah I'm sorry. That comment makes this way worse.
		board.NODES+="""{ data: { id: '"""+self.label+"""' } },"""
# The output method takes the board instances shared varibales containing js obj memeber text and puts that text into the template.
	def outPut(self):
		fh = open("template.js","r")	# `template.js` and an index should be provided with this code.
		code = fh.read()
		fh.close()
		code = code.replace("__IMGS__",self.IMGS)
		code = code.replace("__NODES__",self.NODES)
		code = code.replace("__EDGES__",self.EDGES)
		fh = open("code.js","w") # The output is called code.js and is referenced in index.html
		fh.write(code)
		fh.close()
		print(board.nNODES)
		print(board.countWins)
Com = """
     _/\/\/\/\/\/\__/\/\____________________/\/\/\/\/\/\______________________________/\/\/\/\/\/\_________________________
    _____/\/\________________/\/\/\/\__________/\/\______/\/\/\________/\/\/\/\__________/\/\________/\/\/\______/\/\/\___ 
   _____/\/\______/\/\____/\/\________________/\/\__________/\/\____/\/\________________/\/\______/\/\__/\/\__/\/\/\/\/\_  
  _____/\/\______/\/\____/\/\________________/\/\______/\/\/\/\____/\/\________________/\/\______/\/\__/\/\__/\/\_______   
 _____/\/\______/\/\/\____/\/\/\/\__________/\/\______/\/\/\/\/\____/\/\/\/\__________/\/\________/\/\/\______/\/\/\/\_    
______________________________________________________________________________________________________________________     
"""
# Given the above class generating decision trees for a given board is as follows.
b = board()			# get a board.
# edit b.b ???
print(b.report())	# print it to the console for fun.
b.playN(4)			# play a finite number of turns	
#b.playAll()		# or until endgame.
b.outPut()			# write the output.

# Don't forget to delete the images from previous runs or move the code.js and a copy of the index to a new folder after each run...
# I guess I could do that in here but we will leave this for now.








