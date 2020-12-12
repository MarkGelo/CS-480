import sys
from games import TicTacToe, alpha_beta_player, Game, minmax_player, GameState, alpha_beta_search

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

if __name__ == '__main__':
	input_file = sys.argv[1]
	
	turn, board = parse(input_file)
	ttt = TTT(board)
	# dont need to check if terminal state -- prof said
	end = ttt.play_game(alpha_beta_player, alpha_beta_player)
	#end = ttt.play_game(minmax_player, minmax_player)
	if end == -1:
		x_end = 'loss'
	elif end == 1:
		x_end = 'win'
	elif end == 0:
		x_end = 'draw'
	else:
		x_end = "im bad"

	print('Whose turn is it in this state?')
	print(turn) # print either X or O
	print('If both X and O play optimally from this state, does X have a guaranteed win, guaranteed loss, or guaranteed draw')
	print(x_end) #print one of win, loss, draw