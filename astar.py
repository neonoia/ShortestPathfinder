import math
import csv
import networkx as nx

class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self._add_edge(from_node, to_node, distance)
        self._add_edge(to_node, from_node, distance)

    def _add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, [])
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def astar(graph, initial_node, goal_node, h):
    closed_set = set()  # set of nodes already evaluated
    nodes = set()  # set of tentative nodes to be evaluated
    nodes.add(initial_node)

    visited = {}  # map of navigated nodes
    g_score = {initial_node: 0}  # distance from start along optimal path
    h_score = {initial_node: h(initial_node, goal_node)}  # heuristic estimate
    f_score = {initial_node: h_score[initial_node]}  # estimated distance

    while nodes:  # We pull all nodes in the 'Open Set', nodes that have not been visited
        current = None
        for node in nodes:  # Check all nodes for the lowest f_score node (best path)
            if current is None:
                current = node  # first iteration through this loop will set current to the first node
            elif f_score[node] < f_score[current]:  # We compare previous node to the next node and current becomes the smaller of the two
                current = node

        # At this point we have the smallest f_score node (best combined choice of h_score and g_score) in current
        nodes.remove(current)  # Remove node current from the open_set of unvisited nodes
        if current == goal_node:  # if current is our goal node we return the set of visited nodes, we are done!
            return visited

        closed_set.add(current)  # Add current to the set of closed nodes
        for neighbor in graph.edges[current]:  # Now we check all neighbors of current
            if neighbor in closed_set:  # if neighbor is visited (in closed set) we ignore it and continue
                continue
            tentative_g_score = g_score[current] + graph.distances[(current, neighbor)]
            # Calculate g_score (distance known from start to current to this neighbor
            # If neighbor isn't in the set of Nodes to be evaluated or if it is and this path is lower we add
            # this neighbor to be evaluated
            if neighbor not in nodes or tentative_g_score < g_score[neighbor]:
                nodes.add(neighbor)
                # add all scoring information about this neighbor so we can determine whether it is optimal
                # later on
                visited[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score[neighbor] = h(neighbor, goal_node)
                f_score[neighbor] = g_score[neighbor] + h_score[neighbor]
    return False  # Cannot move from start to goal if we return False


def shortest_path(graph, initial_node, goal_node, h):
    paths = astar(graph, initial_node, goal_node, h)  # Returns route taken from astar algorithm
    route = [goal_node]

    while goal_node != initial_node:  # Route becomes an array of all Nodes used in the path
        route.append(paths[goal_node])  # Reverse iterate from goal to start
        goal_node = paths[goal_node]

    route.reverse()  # reverse this list so that we are going from start to goal
    return route

def read_adj(file, fp):

    g = Graph()
    data = []   # Array container of adjacency matrix
    coord = []  # Array of coordinates 

    # open adjacency file
    with open(file) as fl:
        read = csv.reader(fl)
        for col in read:
            row = []
            i = 0
            for i in range(len(col)):
                row.append(float(col[i]))
                i += 1
            data.append(row)
    
    for i in range(0,len(data)):
        # print(data[i][0] + data[i][1] + data[i][2] + data[i][3] + data[i][4])

    # open coordinate file
    with open(fp) as f:
        reader = csv.reader(f)
        for col in reader:
            pt = float(col[0]),float(col[1])
            coord.append(pt)
    # print(coord)

    # initialize graph nodes and edges
    for i in range(0,len(data)):
        g.add_node(coord[i])
        # print("added boi")
        for j in range(0,i):
            if (data[i][j] == 1):
                g.add_edge(coord[i], coord[j], distance(coord[i], coord[j]))

    return g

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

"""     for i in range(1,len(data)-1):
        for j in range(0,len(data[i])):
            if (data[i][j] == 1):
                graph.add_node(coord[i])
                graph.add_node(coord[j]) """

if __name__ == '__main__':
    # Used Euclidean distance heuristic, slower but a bit more accurate
    sldist = lambda c1, c2: math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)
    
    file = input("Enter adjacency matrix file (.csv) : ")
    coord = input("Enter nodes coordinate file (.csv) : ")
    g = read_adj(file, coord)

    # here we set up the graph we are using for testing purposes

    assert shortest_path(g, (0, 0), (2, 2), sldist) == [(0, 0), (1, 1), (2, 2)]
