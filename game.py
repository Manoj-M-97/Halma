from copy import deepcopy
import time
import math
import random

class State:
	def __init__(self):
		# Size of the square board
		self.board_size = 16

		# Initially all there are no pawns on the board
		self.board = [['.' for i in range(self.board_size)] for j in range(self.board_size)]

		# Maximum time for playing the move/game.
		self.max_time = None
		self.p_moves = []
		self.white_pawn_list = []
		self.black_pawn_list = []

		self.territory ={ 'W': [(11,15),(11,14),(12,13),(12,14),(12,15),(13,12),(13,13),(13,14),(13,15),(14,11),(14,12),(14,13),(14,14),(14,15),(15,11),(15,12),(15,13),(15,14),(15,15)],
		'B' : [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(4,0),(4,1)]}

	def pawn_locations(self,player):
		# This function returns all the locations of the pawns with a particular player
		search = player
		locs = []
		board = self.board
		for i in range(self.board_size):
			for j in range(self.board_size):
				if board[i][j]:
					if board[i][j].player == search:
						locs.append((i,j))
		return locs

	def terminal_test(self):
		# This function determines the goal state of the game
		opponent = 'B' if self.player == 'W' else 'W'
		plyr_locs = self.pawn_locations(self.player)
		oppn_territory = self.territory[opponent]
		oppn_plyr_locs = self.pawn_locations(opponent)
		check_list = []


		for oppn_plyr in oppn_plyr_locs:
			if oppn_plyr in oppn_territory:
				check_list.append(oppn_plyr)

		#Calculates the empty locations in the opponent territory
		oppn_territory = list(set(oppn_territory) - set(check_list))

		if oppn_territory:
			is_terminal = True
		else:
			return False
		for loc in oppn_territory:
			if loc not in plyr_locs:
				is_terminal = False

		return is_terminal	

	def switch_player(self):
		# This function switches the player 
		player = None
		if self.player == 'W':
			player = 'B'
		elif self.player == 'B':
			player = 'W'

		return player

	def h1(self,plyr_locs):
		# This heuritic function relates the number of pawns in the opponent territory
		opponent = 'B' if self.player == 'W' else 'W'
		plyr_cnt = 0
		for loc in plyr_locs:
			if loc in self.territory[opponent]:
				plyr_cnt += 1
		
		return plyr_cnt

	def get_distance_between_points(self,pnt1,pnt2):
		# Using Eucledian distance to find the distance between two points
		return round(math.sqrt((pnt1[0]-pnt2[0])**2 + (pnt1[1]-pnt2[1])**2))

	def find_min_distance_oppn_terr(self,loc,opponent):
		# Find the minimum distance between the given location and the opponent territory
		minm = 35
		for pos in self.territory[opponent]:
			if loc in self.territory[opponent]:
				dist = 0
				if dist < minm:
					minm = dist
			else:
				if not self.board[pos[0]][pos[1]]:
					dist = self.get_distance_between_points(pos,loc)

					if dist < minm:
						minm = dist

		return minm

	def h2(self,plyr_locs,oppn_plyr_locs):
		# This heuristic using distace measure
		opponent = 'B' if self.player == 'W' else 'W'
		dist = []
		oppn_dist = []

		# Calculate the minimum distance from the pawns to the empty locations in the opponent territory.
		for loc in plyr_locs:
			dist.append(self.find_min_distance_oppn_terr(loc,opponent))

		# Calculate the minimum distance from the oppn pawns to the empty locations in the opponent territory.
		for loc in oppn_plyr_locs:
			oppn_dist.append(self.find_min_distance_oppn_terr(loc,self.player))

		# A function that depicts a better move
		gx = sum(dist) - sum(oppn_dist) if sum(oppn_dist) >=0 else sum(dist) + sum(oppn_dist)

		return gx

	def h3(self):
		# Calculates how many pawns of self are still there in home territory.
		pass

	def utility(self):
		# Outputs a value based on the current board state.
		opponent = 'B' if self.player == 'W' else 'W'
		plyr_locs = self.pawn_locations(self.player)
		oppn_plyr_locs = self.pawn_locations(opponent)
		
		# Formulate an evaluation function.	
		#h1 = self.h1(plyr_locs)
		h2 = self.h2(plyr_locs,oppn_plyr_locs)

		return h2

	def result_state(self,d):
		# For a given state, and an action, return the board.
		new_state= deepcopy(self)
		new_state.move_pawn(d["from"][0],d["from"][1],d["to"][0],d["to"][1])
		new_state.player = new_state.switch_player()

		return new_state

	def move_pawn(self,x,y,new_x,new_y):
		player = self.board[x][y]
		self.board[x][y] = None
		self.board[new_x][new_y] = player

	def valid_moves(self,position):
		# This function returns all the legal moves possible from a location
		i,j = position
		moves = [(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1)]
		legal_moves = []

		for move in moves:
			if move[0] >= 0 and move[0] < self.board_size and move[1] >= 0 and move[1] < self.board_size:
				legal_moves.append(move)

		return legal_moves
	
	def possible_moves(self,loc,moves,is_jump):
		# This checks if the target location is empty or not.

		for move in moves:
			if not self.board[move[0]][move[1]]:
				d = {}
				d["move_type"] = 'E'
				d["move"] = move
				d["parent"] = loc				

				if not is_jump and d not in self.p_moves:
					self.p_moves.append(d)

			else:
				x,y = (move[0] - loc[0]), (move[1] - loc[1])
				
				possible_x,possible_y = (move[0] + x),(move[1] + y)

				if (possible_x >= 0) and (possible_x < self.board_size) and (possible_y >= 0) and (possible_y < self.board_size):
					d = {}
					d["move_type"] = 'J'
					d["move"] = (possible_x,possible_y)
					d["parent"] = loc

					if (d not in self.p_moves) and (not self.board[possible_x][possible_y]):
						self.p_moves = self.p_moves + [d]
						self.get_possible_moves((possible_x,possible_y),1)

	def get_possible_moves(self,loc,is_jump):
		# Get all possible actions
		if loc[0] < 0 or loc[0] >= self.board_size or loc[1] < 0 or loc[1] >= self.board_size:
			return []

		valid_moves = self.valid_moves(loc)

		self.possible_moves(loc,valid_moves,is_jump)

	def is_pawn_in_home_territory(self,player_locs):
		# Returns the pawns that are in its home territory
		inside_territory = []

		for loc in player_locs:
			if loc in self.territory[self.player]:
				inside_territory.append(loc)

		return inside_territory

	def is_pawn_in_oppn_territory(self,player_locs):
		# Returns the pawns that are in the opponent territory		
		inside_territory = []

		oppn = 'B' if self.player == 'W' else 'W'

		for loc in player_locs:
			if loc in self.territory[oppn]:
				inside_territory.append(loc)

		return inside_territory

	def is_not_further_away_move(self,loc,move):
		# Returns true if the move is not going further away
		if self.player == 'B':
			x,y = (move[0] - loc[0]),(move[1] - loc[1])
			if x < 0 or y < 0:
				return True
			else:
				return False
		else:
			x,y = (loc[0] - move[0]),(loc[1] - move[1])

			if x >= 0 and y >= 0:
				return False
			else:
				return True

	def actions(self):
		# Gives all possible actions including the jump sequences
		player_locs = self.pawn_locations(self.player)

		possible_actions = []

		oppn = 'B' if self.player == 'W' else 'W'

		reached_oppn_moves = []
		inside_locs_outside_moves = []
		inside_locs_inside_moves = []
		outside_locs_outside_moves = []
		outside_locs_oppn_moves = []

		acc_player_locs = player_locs

		for loc in acc_player_locs:
			self.p_moves = []
			# These are the moves for this particular location.

			self.get_possible_moves((loc[0],loc[1]),0)

			for p_move in self.p_moves:
				d = self.format_action(p_move,loc)	
				
				if loc in self.territory[self.player] and p_move["move"] in self.territory[self.player] and self.is_not_further_away_move(loc,p_move["move"]):
					continue

				if loc in self.territory[oppn] and p_move["move"] not in self.territory[oppn]:
					continue

				if loc not in self.territory[self.player] and p_move["move"] in self.territory[self.player]:
					continue

				if loc in self.territory[self.player] and p_move["move"] in self.territory[self.player]:
					inside_locs_inside_moves.append(d)
					continue

				if loc in self.territory[self.player] and p_move["move"] not in self.territory[self.player]:
					inside_locs_outside_moves.append(d)
					continue

				if loc not in self.territory[oppn] and loc not in self.territory[self.player] and p_move["move"] not in self.territory[self.player] and p_move["move"] not in self.territory[oppn]:
					outside_locs_outside_moves.append(d)
					continue

				if loc not in self.territory[oppn] and loc not in self.territory[self.player] and p_move["move"] not in self.territory[self.player] and p_move["move"] in self.territory[oppn]:
					outside_locs_oppn_moves.append(d)
					continue

				if loc in self.territory[oppn] and p_move["move"] in self.territory[oppn]:
					reached_oppn_moves.append(d)
					continue
		
		acc_player_moves = []
		if not possible_actions and inside_locs_outside_moves:
			acc_player_moves = inside_locs_outside_moves

		for move in acc_player_moves:
			loc = move["from"]
			if loc in self.territory[self.player] and move["to"] in self.territory[self.player] and self.is_not_further_away_move(loc,move["to"]):
				continue

			if loc in self.territory[oppn] and move["to"] not in self.territory[oppn]:
				continue

			if loc not in self.territory[self.player] and move["to"] in self.territory[self.player]:
				continue

			possible_actions.append(move)

		acc_player_moves = []
		if not possible_actions and inside_locs_inside_moves:
			acc_player_moves = inside_locs_inside_moves

		for move in acc_player_moves:
			loc = move["from"]
			
			if loc in self.territory[self.player] and move["to"] in self.territory[self.player] and self.is_not_further_away_move(loc,move["to"]):
				continue

			if loc in self.territory[oppn] and move["to"] not in self.territory[oppn]:
				continue

			if loc not in self.territory[self.player] and move["to"] in self.territory[self.player]:
				continue
			
			possible_actions.append(move)
	
		acc_player_moves = []
		# The below is to consider cases where there are pawns inside the home territory but are not able to make a move.
		if outside_locs_oppn_moves and not possible_actions:
			acc_player_moves = outside_locs_oppn_moves 

		for move in acc_player_moves:
			loc = move["from"]

			if loc in self.territory[oppn] and move["to"] not in self.territory[oppn]:
				continue

			if loc not in self.territory[self.player] and move["to"] in self.territory[self.player]:
				continue

			possible_actions.append(move)
		acc_player_moves = []

		if not possible_actions:
			acc_player_moves = outside_locs_outside_moves + reached_oppn_moves

		for move in acc_player_moves:
			loc = move["from"]

			if loc in self.territory[oppn] and move["to"] not in self.territory[oppn]:
				continue

			if loc not in self.territory[self.player] and move["to"] in self.territory[self.player]:
				continue

			possible_actions.append(move)

		return possible_actions

	def parent(self,move):
		for m in self.p_moves:
			if m["move"] == move:
				return m["parent"]

	def get_jmp_moves(self,loc,move):
		lst = []
		p = self.parent(move)
		while p != loc:
			lst.append(p)

			p = self.parent(p)
		return lst

	def format_action(self,p_move,loc):
		if p_move["move_type"] == 'J':
			d = {}
			d["from"] = loc
			d["to"] = p_move["move"]
			d["jmp"] = self.get_jmp_moves(loc,p_move["move"])
		else:
			d = {}
			d["from"] = loc
			d["to"] = p_move["move"]
			d["jmp"] = []

		return d

class Pawn:
	def __init__(self,x,y,status,player):
		self.x = x
		self.y = y
		# Status indicates whether it is in the enemy territory or not
		self.enemy_terr = status
		self.player = player

	def move(self,new_x,new_y):
		# The pawn will make this move
		self.x = new_x
		self.y = new_y

class Game:
	def __init__(self):
		# Gets the initial empty board state
		self.state = State()
		self.max_depth = 1

	def read_input(self,filename="input.txt"):
		# Read from file
		file = open(filename,'r')
		
		#Parse the input
		inp = {}
		inp["game_type"] = file.readline().strip()
		inp["pawn_color"] = file.readline().strip()
		inp["max_time"] = float(file.readline().strip())

		matrix = []
		for i in range(self.state.board_size):
			row = file.readline().strip()
			temp = []
			for j in range(self.state.board_size):
				temp.append(row[j])

			matrix.append(temp)

		return inp,matrix

	def initial_state(self):
		# Read the input from file.
		inp,board = self.read_input()

		# Assign territory for each player
		self.black_territory = [(0,4),(1,4),(2,3),(3,2),(4,1),(4,0)]
		self.white_territory = [(11,14),(11,15),(12,13),(13,12),(14,11),(15,11)]

		# Update the board with pawn information
		for i in range(self.state.board_size):
			for j in range(self.state.board_size):
				if board[i][j] == '.':
					board[i][j] = None
				elif board[i][j]=='W' or board[i][j]== 'B':
					board[i][j] = Pawn(i,j,'No',board[i][j])

		# Update the state with the initial setup
		self.state.board = board
		self.state.black_territory = self.black_territory
		self.state.white_territory = self.white_territory

		if inp["pawn_color"] == "WHITE":
			self.state.player = 'W'

		elif inp["pawn_color"] == "BLACK":
			self.state.player = 'B'

		self.state.max_time = inp["max_time"]

		# Assess the depth based on the time taken
		try:
			calibrate_file = open("calibrate.txt","r")

			row = calibrate_file.readline().strip()
			depth1 = row.split(":")
			if len(depth1)>1:
				depth1 = int(depth1[1])
			row = calibrate_file.readline().strip()

			depth3 = row.split(":")
			if len(depth3)>1:
				depth3 = int(depth3[1])

			calibrate_file.close()

		except FileNotFoundError:
			depth1 = 1
			depth3 = 25

		if inp["game_type"] == "SINGLE":
			self.max_depth = 1
		else:		
			self.max_depth = 1

	def play(self):
		# Builds the initial state with all the required information
		self.initial_state()

		# Run adversial search using aplha beta pruning algorithm
		action = self.alpha_beta_search(self.state)
		print(action)

		self.write_output_to_file(action)

	def write_output_to_file(self,action,filename = "output.txt"):
		f = open(filename, "w")

		if "from" in action.keys() and "to" in action.keys():
			if self.check_if_jump(action):
				x,y = action["to"]
				lst = [(x,y)]

				jmp = action["jmp"]

				for i in range(len(jmp)):
					lst.append(jmp[i])

				lst.append(action["from"])
				lst.reverse()
				for i in range(len(lst)-2):
					f.write("J " + str(lst[i][1]) + ',' + str(lst[i][0]) + ' ' + str(lst[i+1][1]) + ',' + str(lst[i+1][0]) + '\n')
				f.write("J " + str(lst[-2][1]) + ',' + str(lst[-2][0]) + ' ' + str(lst[-1][1]) + ',' + str(lst[-1][0]))	
			else:
				f.write("E " + str(action["from"][1]) + ',' + str(action["from"][0]) + ' ' + str(action["to"][1]) + ',' + str(action["to"][0]))
		f.close()

	def check_if_jump(self,move):
		if "from" in move.keys() and "to" in move.keys():
			start = move["from"]
			end = move["to"]

			x,y = start[0] - end[0],start[1] - end[1]
			x,y = abs(x),abs(y)

			if x not in (0,1) or y not in (0,1):
				return True
			else:
				return False

	def alpha_beta_search(self,state):
		# Consider depth and the time as well
		# Figure out how you are returning the results.

		v, action = self.max_value(state,float("-inf"),float("inf"),0)

		return action

	def dummy_print(self,board):
		for i in range(self.state.board_size):
			for j in range(self.state.board_size):
				if board[i][j]:
					print(board[i][j].player,end='')
				else:
					print('.',end='')
			print()

	def max_value(self,state,alpha,beta,depth):

		if depth >= self.max_depth or state.terminal_test():
			return (state.utility(),{})

		v = float("-inf")
		action = None

		for d in state.actions():
			value,act = self.min_value(state.result_state(d),alpha,beta, depth + 1)

			if value > v:
				v = value
				action = d

			if value == v:
				rnd = random.random()
				if rnd<0.5:
					v = value
					action = d

			if v >= beta:
				return (v,action)
			alpha = max(alpha,v)

		return (v,action)

	def min_value(self,state,alpha,beta,depth):

		if depth >= self.max_depth or state.terminal_test():
			return (state.utility(),{})

		v = float("inf")
		action = None
		for d in state.actions():
			value,act =	self.max_value(state.result_state(d),alpha,beta,depth + 1)

			if value < v:
				v = value
				action = d

			if value == v:
				rnd = random.random()
				if rnd<0.5:
					v = value
					action = d

			if v <= alpha:
				return (v,action)
			beta = min(beta,v)

		return (v,action)

	def write_output(self,state):
		# Formulate the output in the required way.
		# Write this into a file 'output.txt'
		for i in range(state.board_size):
			for j in range(state.board_size):
				if state.board[i][j]:
					print(state.board[i][j].player,end='')
				else:
					print(".",end='')
			print()

start_time = time.time()
flag = False

try:
	playdata = open("playdata.txt","r")
except FileNotFoundError:
	flag = True
	playdata = open("playdata.txt","w")
	playdata.write("1:0")

count = 0

if not flag:
	row1 = playdata.readline().strip()
	data = row1.split(":")
	count,time_l = int(data[0]),math.ceil(int(data[1]))

game_obj = Game()
game_obj.play()

playdata = open("playdata.txt","w")
playdata.write(str(count+1) + ':' + str(math.ceil(time.time() - start_time)))
print("Time taken: ",time.time()-start_time)