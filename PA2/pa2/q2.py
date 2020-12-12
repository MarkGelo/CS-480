import sys
from games import TicTacToe, Game, GameState
import numpy as np

# from test_games.py
def gen_state(to_move='X', x_positions=[], o_positions=[], h=3, v=3):
    """Given whose turn it is to move, the positions of X's on the board, the
    positions of O's on the board, and, (optionally) number of rows, columns
    and how many consecutive X's or O's required to win, return the corresponding
    game state"""

    moves = set([(x, y) for x in range(1, h + 1) for y in range(1, v + 1)]) - set(x_positions) - set(o_positions)
    moves = list(moves)
    board = {}
    for pos in x_positions:
        board[pos] = 'X'
    for pos in o_positions:
        board[pos] = 'O'
    return GameState(to_move=to_move, utility=0, board=board, moves=moves)

def parse(file):
	inp = open(file, 'r')
	X = []
	O = []
	turn = None
	board_state = {}
	row = 1
	for line in inp:
		square = line.replace('\n', '').split(' ')
		idx = 1
		for a in square:
			if a == 'X':
				X.append((row, idx))
			elif a == 'O':
				O.append((row, idx))
			idx += 1
		row += 1
	if len(X) == len(O): # X goes next because X starts first
		turn = 'X'
	if len(X) > len(O):
		turn = 'O'
	if len(O) > len(X):
		turn = 'X'
	if len(O) == 0 and len(X) == 0: # X starts first
		turn = 'X'
	return turn, gen_state(to_move = turn, x_positions = X, o_positions = O)

class TTT(TicTacToe):
	def __init__(self, board_state):
		super().__init__()
		self.initial = board_state
	
	def play_game(self, *players):
		state = self.initial
		while True:
			for player in players:
				move = player(self, state)
				state = self.result(state, move)
				if self.terminal_test(state):
					#self.display(state)
					return self.utility(state, 'X') # X is what matters

states = []
def alpha_beta_search(state, game):
	states.append(state) # initial state
	player = game.to_move(state)
	def max_value(state, alpha, beta):
		states.append(state)
		if game.terminal_test(state):
			return game.utility(state, player)
		v = -np.inf
		temp = 'temp'
		for a in game.actions(state):
			v = max(v, min_value(game.result(state, a), alpha, beta))
			if v >= beta and temp == 'temp':
				temp = v
				#return v # dont return to populate whole tree?
			alpha = max(alpha, v)
		if temp != 'temp':
			return temp
		return v
	
	def min_value(state, alpha, beta):
		states.append(state)
		if game.terminal_test(state):
			return game.utility(state, player)
		v = np.inf
		temp = 'temp'
		for a in game.actions(state):
			v = min(v, max_value(game.result(state, a), alpha, beta))
			if v <= alpha and temp == 'temp':
				temp = v
				#return v # dont return to populate whole tree?
			beta = min(beta, v)
		if temp != 'temp':
			return temp
		return v

	best_score = -np.inf
	beta = np.inf
	best_action = None
	for a in game.actions(state):
		v = min_value(game.result(state, a), best_score, beta)
		if v > best_score:
			best_score = v
			best_action = a
	return best_action

def alpha_beta_player(game, state):
	return alpha_beta_search(state, game)

if __name__ == '__main__':
	
	input_file = sys.argv[1]
	
	turn, board = parse(input_file)
	ttt = TTT(board)
	# dont need to check if initially terminal state
	end = ttt.play_game(alpha_beta_player, alpha_beta_player)

	terminal = [x for x in states if ttt.terminal_test(x)]
	terminal_win = [x for x in terminal if x.utility == 1]
	terminal_lose = [x for x in terminal if x.utility == -1]
	terminal_draw = [x for x in terminal if x.utility == 0]
	non_terminal = [x for x in states if not ttt.terminal_test(x)]
	non_terminal_gw = []
	non_terminal_gl = []
	non_terminal_gd = []
	for state in non_terminal:
		temp = TTT(state)
		end = temp.play_game(alpha_beta_player, alpha_beta_player)
		if end == 1:
			non_terminal_gw.append(state)
		elif end == -1:
			non_terminal_gl.append(state)
		else: # 0
			non_terminal_gd.append(state)
	# Starting from this state, populate the full game tree.
	# The leaf nodes are the terminal states.
	# The terminal state is terminal if a player wins or there are no empty squares.
	# If a player wins, the state is considered terminal, even if there are still empty squares.
	# Answer the following questions for this game tree.
	print('How many terminal states are there?')
	print(len(terminal))
	print('In how many of those terminal states does X win?')
	print(len(terminal_win))
	print('In how many of those terminal states does X lose?')
	print(len(terminal_lose))
	print('In how many of those terminal states does X draw?')
	print(len(terminal_draw))
	print('How many non-terminal states are there?')
	print(len(non_terminal))
	print('In how many of those non-terminal states does X have a guranteed win?')
	print(len(non_terminal_gw))
	print('In how many of those non-terminal states does X have a guranteed loss?')
	print(len(non_terminal_gl))
	print('In how many of those non-terminal states does X have a guranteed draw?')
	print(len(non_terminal_gd))
	