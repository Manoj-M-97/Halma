import play_game
import time
from play_game import Game
from play_game import Pawn
from pathlib import Path

def read_input(filename="input.txt"):
	# Read from file
	file = open(filename,'r')
	
	#Parse the input
	inp = {}
	inp["game_type"] = file.readline().strip()
	inp["pawn_color"] = file.readline().strip()
	inp["max_time"] = float(file.readline().strip())

	matrix = []
	for i in range(16):
		row = file.readline().strip()
		temp = []
		for j in range(16):
			temp.append(row[j])

		matrix.append(temp)

	return inp,matrix

def dummy_print(board):
	for i in range(16):
		for j in range(16):
			if board[i][j]:
				print(board[i][j].player,end='')
			else:
				print('.',end='')
		print()

start_time = time.time()
count = 0

board = None
new_board = None
player = None

while 1:
	#inp_file = open("input.txt","a")
	#out_file = open("output.txt","a")
	if count == 0:
		inp,board = read_input()
		player = 'W' if inp["pawn_color"] == "WHITE" else 'B'

		for i in range(16):
			for j in range(16):
				if board[i][j] == '.':
					board[i][j] = None
				elif board[i][j]=='W' or board[i][j]== 'B':
					board[i][j] = Pawn(i,j,'No',board[i][j])
	#print(board)
	dummy_print(board)
	game_obj_1 = Game()
	new_board = game_obj_1.play(player,board)
	if not new_board:
		break
	#print(player,frm,to)
	#print(new_board)
	print("Player : ", player," played",count)
	dummy_print(new_board)
	player = 'W' if player == 'B' else 'B'

	game_obj_2 = Game()
	board = game_obj_2.play(player,new_board)

	if not board:
		break	
	#print(player,frm,to)
	print("Player : ", player," played",count)

	player = 'W' if player == 'B' else 'B'

	
	count += 1


	
print("Game Done. Moves by one player :",count)
#game_obj_2.play()
print("Time taken: ",time.time()-start_time)


	# print("Player 1 played")
	# contents = Path("output.txt").read_text()
	# print(contents.split('\n'))
	# contents = contents.split('\n')

	# start_move = contents[0]
	# end_move = None
	# if len(contents) > 1:
	# 	end_move = contents[-1]

	# start_move = start_move.split(' ')

	# frm = start_move[1]
	# frm = frm.split(',')
	# to = None
	# if end_move:
	# 	end_move = end_move.split(' ')
	# 	to = to.split(',')
	# 	to = end_move[2]
	# 	to = (int(to[2]),int(to[0]))
	# else:
	# 	to = start_move[2]
	# 	to = to.split(',')
	# 	print(to)
	# 	to = (int(to[1]),int(to[0]))

	# frm = (int(frm[1]),int(frm[0]))