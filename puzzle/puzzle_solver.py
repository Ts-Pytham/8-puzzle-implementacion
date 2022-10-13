from utils.distance_metrics import manhattan_distance, eculidean_distance
from utils.search_algorithms import BFS, DFS, A_STAR, First_Best_Search
from puzzle.puzzle_state import PuzzleState
import math
import time

class PuzzleSolver(object):

    def __init__(self, initial_state, goal, algorithm='bfs', heuristic= None):

        self.initial_state = initial_state

        # Assign the search algorithm that will be used in the solver.
        if(algorithm == 'bfs'): 
            self.search_alg = BFS
        elif(algorithm == 'dfs'):
            self.search_alg = DFS
        elif(algorithm == 'ast'):
            self.search_alg = A_STAR
        elif(algorithm == 'best'):
            self.search_alg = First_Best_Search
        else:
            raise NotImplementedError("No such algorithm is supported.")

        # Assign the heuristic algorithm that will be used in the solver.
        if(heuristic == None and algorithm == 'ast'):
            raise AttributeError("Required Attribute `heuristic` in case of useing A* Search.")
        elif(heuristic == 'manhattan'):
            self.dist_metric = manhattan_distance
        elif(heuristic == 'euclidean'):
            self.dist_metric = eculidean_distance
        elif(heuristic == None and algorithm != 'ast'):
            pass
        else:
            raise NotImplementedError("No such Heuristic is supported.")

        print(f"distribution metric: {self.calculate_total_cost}")
        # Create a Puzzle State Object with the inputs for Solver.
        initial_state = tuple(map(int, initial_state))
        size = int(math.sqrt(len(initial_state)))
        self.puzzle_state = PuzzleState(initial_state, size, goal, self.calculate_total_cost)

        # Start off by checking the solvability of the state and raise error in case of false.
        if(not self.puzzle_state.is_solvable()):
            raise Exception("The initial state enetred is not solvable !")

    def calculate_total_cost(self, state):
        """calculate the total estimated cost of a state"""
        sum_heuristic = 0
        for i, item in enumerate(state.config):
            current_row = i // state.n
            current_col = i % state.n
            goal_idx = state.goal.index(item)
            goal_row = goal_idx // state.n
            goal_col = goal_idx % state.n  
            sum_heuristic += self.dist_metric(current_row,current_col,goal_row,goal_col)
        
        if self.search_alg == A_STAR:
            return sum_heuristic + state.cost
        else:
            return sum_heuristic    

    def writeOutput(self, result, running_time):
        final_state, nodes_expanded, max_search_depth, explored_nodes = result
        path_to_goal = [final_state.action]
        cost_of_path = final_state.cost
        parent_state = final_state.parent

        while parent_state:
            if parent_state.parent:
                path_to_goal.append(parent_state.action)
            parent_state = parent_state.parent
        path_to_goal.reverse()
        search_depth = len(path_to_goal)

        print("******* Results *******")
        print("Camino a la solución: " + str(path_to_goal) + "\n")
        print("Número de pasos del camino solución: " + str(len(path_to_goal)) + "\n")
        print("Costo del camino: " + str(cost_of_path) +  "\n")
        print("Nodos expandidos: " + str(nodes_expanded) + "\n")
        print("Nodos explorados: " + str(explored_nodes) + "\n")
        print("Profundidad de búsqueda: " + str(search_depth) + "\n")
        print("Máxima profundidas de búsqueda: " + str(max_search_depth) +  "\n")
        print("Tiempo de ejecución: " + str(running_time) + " segundos. \n")

    def solve(self):
        start_time = time.time()
        if(self.search_alg == A_STAR):
            results = A_STAR(self.puzzle_state, self.calculate_total_cost)

        elif(self.search_alg == First_Best_Search):
            results = First_Best_Search(self.puzzle_state, self.calculate_total_cost)
        else:
            results = self.search_alg(self.puzzle_state)
        running_time = time.time() - start_time
        self.writeOutput(results, running_time)
 