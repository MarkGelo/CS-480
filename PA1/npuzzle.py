import sys
from utils import memoize
from search import Problem, Graph, breadth_first_tree_search, depth_first_tree_search
from search import depth_first_graph_search, breadth_first_graph_search, greedy_best_first_graph_search
from search import astar_search, uniform_cost_search, depth_first_graph_search
from search import Node, PriorityQueue

def parse(file):
    inp = open(file, 'r')
    pr = []
    for line in inp:
        if line.startswith('#'):
            continue
        line = line.replace('\n', '')
        line = line.split(' ')
        line = [int(x) for x in line]
        pr.extend(line)
    return tuple(pr)

class NPuzzle(Problem):
    
    def __init__(self, initial):
        g = [x for x in range(len(initial))]
        goal = tuple(g)
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)
    
    def actions(self, state):
        possible_actions = ['L', 'R', 'U', 'D']
        index_blank_square = self.find_blank_square(state)
        if index_blank_square % len(state)**(1/2) == 0:
            possible_actions.remove('L')
        if index_blank_square < len(state)**(1/2):
            possible_actions.remove('U')
        if index_blank_square in [*range(int(len(state)**(1/2)) - 1, len(state), int(len(state)**(1/2)))]:
            possible_actions.remove('R')
        if index_blank_square > (len(state)-1) - len(state)**(1/2):
            possible_actions.remove('D')
        return possible_actions
    """
    - 1 3
    - 2 5 8
    - 3 7 11 15
    0 1
    2 3
    """
    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        delta = {'U': -1 * int(len(state)**(1/2)), 'D': int(len(state)**(1/2)), 'L': -1, 'R': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        
        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

def best_first_tree_search(problem, f, display=False):
    # from search -- just modified to make it tree search
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            frontier.append(child)
    return None

def uniform_cost_tree_search(problem, display = False):
    return best_first_tree_search(problem, lambda node: node.path_cost, display)

def greedy_best_first_tree_search(problem, display = False):
    return best_first_tree_search(problem, problem.h, display)

def astar_tree_search(problem, h = None, display = False):
    h = memoize(h or problem.h, 'h')
    return best_first_tree_search(problem, lambda n: n.path_cost + h(n), display)

if __name__ == '__main__':
    input_file = sys.argv[1]
    algo = sys.argv[2]

    pr = parse(input_file)
    problem = NPuzzle(pr)

    if algo == 'BFTS':
        goal_node = breadth_first_tree_search(problem)
    elif algo == 'DFTS': # possible infinite loop
        goal_node = depth_first_tree_search(problem)
    elif algo == 'DFGS': # graph search -- so finite -- but takes so long like impossibly long
        goal_node = depth_first_graph_search(problem)
    elif algo == 'BFGS':
        goal_node = breadth_first_graph_search(problem)
    elif algo == 'UCTS':
        goal_node = uniform_cost_tree_search(problem)
    elif algo == 'UCGS':
        goal_node = uniform_cost_search(problem)
    elif algo == 'GBFTS':
        goal_node = greedy_best_first_tree_search(problem)
    elif algo == 'GBFGS':
        goal_node = greedy_best_first_graph_search(problem, problem.h)
    elif algo == 'ASTS':
        goal_node = astar_tree_search(problem)
    elif algo == 'ASGS':
        goal_node = astar_search(problem, h = problem.h)
    else:
        goal_node = None
    # Do not change the code below.
    if goal_node is not None:
        print("Solution path", goal_node.solution())
        print("Solution cost", goal_node.path_cost)
    else:
        print("No solution was found.")