import math
import networkx as nx
import matplotlib as plt

adj = [ [0, 10, 0, 15, 0, 0, 0, 0, 0, 0, 0],
        [10, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 10, 0, 10, 0, 15, 0, 0, 0, 0, 0],
        [15, 0, 10, 0, 0, 25, 10, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 0],
        [0, 0, 15, 25, 10, 0, 50, 0, 50, 0, 5],
        [0, 0, 0, 10, 0, 50, 0, 0, 0, 0, 25],
        [0, 0, 0, 0, 10, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 50, 0, 5, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 20],
        [0, 0, 0, 0, 0, 5, 25, 0, 0, 20, 0] ]

coord = [ [0, 0],
          [5, 0],
          [5, 5],
          [0, 5],
          [7.5, 7.5],
          [5, 10],
          [0, 10],
          [10, 10],
          [7.5, 12.5],
          [7.5, 15],
          [0, 15], ]

def heuristic(point1, point2):
    return math.sqrt(math.pow(point2[0] - point1[0],2) + math.pow(point2[1] - point1[1],2))

def a_star(adj, coord, start, dest):

    visited = []
    for i in range(0,len(coord)):
        visited.append(False)

    result = []
    result.append(start)
    current_node = start
    total_weight = 0

    counter = 0
    while (current_node != dest):
        found = False
        comp_weight = float('Inf')
        visited[current_node] = True
        
        for i in range(0,len(adj[current_node])):
            if (adj[current_node][i] > 0) and (visited[i] == False):
                length = heuristic(coord[i], coord[dest])
                if (adj[current_node][i] + length <= comp_weight):
                    found = True
                    min = i
                    comp_weight = adj[current_node][min] + length

        if found:
            total_weight += adj[current_node][min]
            current_node = min
            result.append(min)
            counter+=1
        else:
            print("Unable to find shortest path.")
            return -1

        if (counter > len(coord)):
            print("Unable to find shortest path.")
            return -1

    return result

test = a_star(adj, coord, 0, 8)
print(test)
