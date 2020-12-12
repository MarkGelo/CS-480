from logic import tt_entails, KB, to_cnf, pl_resolution, PropKB, expr, Expr, is_variable
import sys

def parse_file(file):
	# parse file
	# form initial KB
	# add additional rules
	# return KB, and queries
	inp = open(file, "r")
	KB = []
	query = []
	query_start = False
	i = 0
	for line in inp:
		# first not comment is the size of the board
		if not line.startswith("#") and i == 0:
			i += 1
			cur_line = line.replace('\n', '')
			s = cur_line.split('x')
			size = (int(s[0]), int(s[1]))
		elif not line.startswith("#") and not query_start:
			cur_line = line.replace('\n', '')
			KB.append(cur_line)
		elif line.replace('\n', '') == '# Query Sentences' or line.replace('\n', '') == '#Query Sentences':
			query_start = True
		elif query_start and not line.startswith("#"):
			cur_line = line.replace('\n', '')
			query.append(to_cnf(cur_line)) # makes the query into CNF and understandable by the program
	return size, KB, query

class PaKB(PropKB):
	def __init__(self, size, KB):
		# assumes width x height
		self.clauses = []
		# do initial KB first
		initial_KB = []
		# do corners
		initial_KB.append(f"B00 <=> (M01 | M10)")
		initial_KB.append(f"B0{size[0]-1} <=> (M0{size[0]-2} | M1{size[0]-1})")
		initial_KB.append(f"B{size[1]-1}0 <=> (M{size[1]-1}1 | M{size[1]-2}0)")
		initial_KB.append(f"B{size[1]-1}{size[0]-1} <=> (M{size[1]-2}{size[0]-1} | M{size[1]-1}{size[0]-2})")
		# top side
		for i in range(1, size[0] - 1):
			# left right down
			initial_KB.append(f"B0{i} <=> (M0{i-1} | M0{i+1} | M1{i})")
		# bottom side
		for i in range(1, size[0] - 1):
			bot_x = size[1]-1
			# left right up
			initial_KB.append(f"B{bot_x}{i} <=> (M{bot_x}{i-1} | M{bot_x}{i+1} | M{bot_x-1}{i})")
		# left side
		for i in range(1, size[1] - 1):
			# up right down
			initial_KB.append(f"B{i}0 <=> (M{i}1 | M{i+1}0 | M{i-1}0)")
		# right side
		for i in range(1, size[1] - 1):
			right_x = size[0] - 1
			# up left down
			initial_KB.append(f"B{i}{right_x} <=> (M{i}{right_x-1} | M{i-1}{right_x} | M{i+1}{right_x})")
		# middle
		for i in range(1, size[0] - 1):
				for j in range(1, size[1] - 1):
					initial_KB.append(f"B{j}{i} <=> (M{j-1}{i} | M{j+1}{i} | M{j}{i+1} | M{j}{i-1})")
		#print(len(initial_KB), "initial KB")
		#print(initial_KB)
		for sentence in initial_KB:
			self.tell(sentence)
		for sentence in KB:
			self.tell(sentence) # also makes it to CNF

if __name__ == '__main__':
	input_file = sys.argv[1]
	
	size, KB, query = parse_file(input_file)
	pa3KB = PaKB(size, KB)
	for quer in query:
		#print(pa3KB.ask_if_true(quer))
		#result = pl_resolution(pa3KB, quer)
		result = tt_entails(Expr('&', *pa3KB.clauses), expr(quer))
		print('Yes' if result else 'No')