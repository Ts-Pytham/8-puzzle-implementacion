from puzzle.puzzle_solver import PuzzleSolver
import sys
import os
if __name__ == '__main__':

    path = r'/Datos/puzzle.txt'
    separador = os.path.sep
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    dir = separador.join(dir_actual.split(separador)[:-1])
    newPath = dir + path
    list = []
    with open(newPath, 'r') as f:       
        for line in f.readlines(): 
            for x in line.split(","):
                list.append(int(x))

    lista = ['Arriba', 'Izquierda', 'Arriba', 'Derecha', 'Abajo', 'Abajo', 'Izquierda', 'Arriba', 'Izquierda','Arriba', 'Arriba', 'Derecha', 'Abajo', 'Izquierda', 'Arriba']
    print(len(lista))
    chosen_heuristic = None
    chosen_algorithm = 'ast'
    begin_state = list
    if(chosen_algorithm == 'ast' or chosen_algorithm == 'best'):
        value = input("Please choose a heuristic fucntion:\n[1] Manhattan Distance  [2] Euclidean Distance  ")
        if(value == str(1)):
            chosen_heuristic = "manhattan"
        elif(value == str(2)):
            chosen_heuristic = "euclidean"
        else: 
            raise Exception("Wrong input heuristic function !") 
        
    solver = PuzzleSolver(begin_state,[0,1,2,3,4,5,6,7,8], chosen_algorithm, heuristic=chosen_heuristic)
    solver.solve()