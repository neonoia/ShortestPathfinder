import sys

from flask import Flask, render_template, request, redirect, Response, jsonify
import random
import json
from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

@app.route('/')
def output():
    # serve index template
    return render_template('index.html')

@app.route('/receiver', methods=['POST'])
def worker():
    # read json + reply
    data = request.get_json(force = True)
    coord = []

    for i in range(1,len(data) + 1):
        cont = []
        cont.append(data[str(i)]['lat'])
        cont.append(data[str(i)]['lng'])
        coord.append(cont)

    print(data)
    print(coord)

    return jsonify(data)

# function to calculate distance between 2 points
def dist(p1, p2):
    # approximate radius of earth in km
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

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
            pos[i] = coord[i]
            i += 1
    gnx.add_nodes_from(pos.keys())
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

    return g, gnx, pos, coord, cont


# function to draw using networkx and matplotlib

def draw(result, gnx, pos, coord, cont):
    results = []
    other = []

    for i in range(len(coord)):
        for j in range(len(result)):
            if (coord[i] == result[j]):
                results.append(i)
                print(i)
            else:
                other.append(i)

    nx.draw_networkx_nodes(gnx, pos,
                           nodelist=results,
                           node_color='r',
                           node_size=500,
                           alpha=0.8)

    nx.draw_networkx_nodes(gnx, pos,
                           nodelist=other,
                           node_color='b',
                           node_size=500,
                           alpha=0.8)

    resulting_edges = separate_edge(results, cont)

    nx.draw_networkx_edges(gnx, pos,
                           edgelist=resulting_edges,
                           width=5, alpha=0.5, edge_color='r')
    nx.draw_networkx_edges(gnx, pos,
                           edgelist=cont,
                           width=5, alpha=0.5, edge_color='b')

    print(nx.info(gnx))
    plt.show()


def separate_edge(result, cont):
    results = []

    j = 0
    for i in range(len(result)-1):
        found = False
        while (not found) and (j < len(cont)):
            x = cont[j][0], cont[j][1]
            if (cont[j][0] == result[i] and cont[j][1] == result[i+1]) or (cont[j][0] == result[i+1] and cont[j][1] == result[i]):
                found = True
                results.append(x)
            j += 1

    return results

if __name__ == '__main__':
    # run!
    app.debug = True
    app.run()
