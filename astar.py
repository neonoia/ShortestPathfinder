import math
import csv
import networkx as nx
import matplotlib.pyplot as plt


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
        # Check all nodes for the lowest f_score node (best path)
        for node in nodes:
            if current is None:
                current = node  # first iteration through this loop will set current to the first node
            # We compare previous node to the next node and current becomes the smaller of the two
            elif f_score[node] < f_score[current]:
                current = node

        # At this point we have the smallest f_score node (best combined choice of h_score and g_score) in current
        # Remove node current from the open_set of unvisited nodes
        nodes.remove(current)
        if current == goal_node:  # if current is our goal node we return the set of visited nodes, we are done!
            return visited, tentative_g_score

        closed_set.add(current)  # Add current to the set of closed nodes
        # Now we check all neighbors of current
        for neighbor in graph.edges[current]:
            # if neighbor is visited (in closed set) we ignore it and continue
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + \
                graph.distances[(current, neighbor)]
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
    # Returns route taken from astar algorithm
    paths, cost = astar(graph, initial_node, goal_node, h)
    route = [goal_node]

    while goal_node != initial_node:  # Route becomes an array of all Nodes used in the path
        route.append(paths[goal_node])  # Reverse iterate from goal to start
        goal_node = paths[goal_node]

    route.reverse()  # reverse this list so that we are going from start to goal
    return route, cost


def read_adj(file, fp, start, goal):

    g = Graph()
    gnx = nx.Graph()
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

    # open coordinate file
    pos = {}    # create map of positions of each nodes
    i = 0
    with open(fp) as f:
        reader = csv.reader(f)
        for col in reader:
            pt = float(col[0]), float(col[1])
            coord.append(pt)
            gnx.add_node(i, pos=coord[i])
            i += 1
    # print(coord)

    cont = []   # graph number container
    # initialize graph nodes and edges
    for i in range(0, len(data)):
        g.add_node(coord[i])
        for j in range(0, i):
            if (data[i][j] == 1):
                g.add_edge(coord[i], coord[j], distance(coord[i], coord[j]))
                gnx.add_edge(i, j, weight=round(
                    distance(coord[i], coord[j]), 2))
                x = i, j
                cont.append(x)

    return g, gnx, coord, cont

# function to calculate distance


def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# function to draw using networkx and matplotlib


def draw(result, gnx, coord, cont, cost):
    other = set(coord) - set(result)
    other = list(other)
    result = convert_list(result, coord)
    other = convert_list(other, coord)

    pos = nx.get_node_attributes(gnx, 'pos')
    labels = nx.get_edge_attributes(gnx, 'weight')

    nx.draw_networkx_nodes(gnx, pos,
                           nodelist=result,
                           node_color='r',
                           node_size=150,
                           alpha=0.8)

    nx.draw_networkx_nodes(gnx, pos,
                           nodelist=other,
                           node_color='y',
                           node_size=150,
                           alpha=0.8)

    new_result = []
    for i in range(len(result)-1):
        temp = result[i], result[i+1]
        new_result.append(temp)

    nx.draw_networkx_edges(gnx, pos,
                           edgelist=new_result,
                           width=1, alpha=1, edge_color='b', label=labels)

    nx.draw_networkx_edges(gnx, pos,
                           edgelist=cont,
                           width=1, alpha=0.5, edge_color='y', label=labels)

    nx.draw_networkx_labels(gnx, pos, font_size=8, font_family='sans-serif')

    plt.axis('off')
    dist = "Total Distance = " + str(cost)
    plt.title("Path Result" + "\n" + dist)
    plt.show()

def convert_list(conv, coord):
    result = []
    for i in range(len(conv)):
        for j in range(len(coord)):
            if ((conv[i])[0] == (coord[j])[0]) and ((conv[i])[1] == (coord[j])[1]):
                result.append(j)

    return result


if __name__ == '__main__':
    # Used Euclidean distance heuristic, slower but a bit more accurate
    def sldist(c1, c2): return math.sqrt(
        (c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)

    adj = input("Enter adjacency matrix file name (.csv) : ")
    coord = input("Enter nodes coordinate file name (.csv) : ")
    start = int(input("Enter desired start node : "))
    goal = int(input("Enter desired destination node : "))
    g, gnx, coordinate, cont = read_adj(adj, coord, start, goal)

    result, cost = shortest_path(
        g, coordinate[start], coordinate[goal], sldist)

    newrest = convert_list(result, coordinate)
    print("RESULT = ")
    print("Step by step to reach goal node from start node")
    res_str = ""
    for i in range(len(newrest)):
        res_str = res_str + "-->" + str(newrest[i])
    print(res_str)

    print("\nTotal Distance = " + str(cost))

    # here we set up the graph we are using for testing purposes
    draw(result, gnx, coordinate, cont, cost)
