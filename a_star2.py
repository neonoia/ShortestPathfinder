import math
import networkx as nx
import matplotlib as plt
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

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

def a_star(adj, coord, start, goal):

    visited = []
    for i in range(0, len(coord)):
        visited.append(False)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for i in range(0, len(adj[current])):
            new_cost = cost_so_far[current] + adj[current][i]
            if (adj[current][i] > 0) and (visited[i] == False) and (new_cost < cost_so_far[i]):
                visited[i] = True
                cost_so_far[i] = new_cost
                priority = i + heuristic(coord[goal], coord[i])
                frontier.put(i, priority)
                came_from[i] = current

    return came_from, cost_so_far
                
"""         for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current """

test,cost = a_star(adj, coord, 0, 8)
print(test)
print(cost)
