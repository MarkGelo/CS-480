from search import Problem, Graph, breadth_first_tree_search, depth_first_tree_search
from search import depth_first_graph_search, breadth_first_graph_search, greedy_best_first_graph_search
from search import astar_search, uniform_cost_search, Node, PriorityQueue
import sys
from utils import memoize

def parse(file):
    inp = open(file, 'r')
    map_dict = {}
    heuristic = {}
    for line in inp:
        line = line.replace('\n', '')
        if line.startswith('#') or line == '':
            continue
        node = line.split(' ')
        if len(node) == 4: # form of A B <> 5
            if node[2] == '<>': # bidirectional
                if node[0] in map_dict: # first dir
                    map_dict[node[0]][node[1]] = int(node[3])
                else:
                    map_dict[node[0]] = {node[1]: int(node[3])}
                if node[1] in map_dict: # second dir
                    map_dict[node[1]][node[0]] = int(node[3])
                else:
                    map_dict[node[1]] = {node[0]: int(node[3])}
            elif node[2] == '>':
                if node[0] in map_dict:
                    map_dict[node[0]][node[1]] = int(node[3])
                else:
                    map_dict[node[0]] = {node[1]: int(node[3])}
        elif len(node) == 2: # form of S G -- initial to goal or D 5 -- heuristic
            # check if node[1] is str or int
            try:
                heu = int(node[1]) # heuristic
                heuristic[node[0]] = heu
            except: # start and goal
                start = node[0]
                goal = node[1]
    #print(map_dict)
    return map_dict, heuristic, start, goal

class MapProblem(Problem):
    def __init__(self, initial, goal, graph, heuristics):
        Problem.__init__(self, initial, goal)
        self.graph = graph
        self.heuristics = heuristics
    
    def actions(self, A):
        return list(self.graph.get(A).keys())
    
    def result(self, state, action):
        return action
    
    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A)[B] or infinity)

    def find_min_edge(self):
        m = infinity
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)
        return m

    def h(self, node):
        # user determined heuristic functions -- from the fiule
        return self.heuristics[node.state]

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

if __name__ == "__main__":

    input_file = sys.argv[1]
    algo = sys.argv[2]

    map_dict, heuristic, start, goal = parse(input_file)
    problem = MapProblem(start, goal, map_dict, heuristic)
    if algo == 'BFTS':
        goal_node = breadth_first_tree_search(problem)
    elif algo == 'DFTS':
        goal_node = depth_first_tree_search(problem)
    elif algo == 'DFGS':
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
        goal_node = astar_tree_search(problem, h = problem.h)
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