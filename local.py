import fileinput
import re
import time
import random

class CSP:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

class Node:
    def __init__(self, name, possibleColors):
        self.name = name
        self.pColors = possibleColors
        self.neighbors = []


class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

#chooses the value for a node which minimizes conflicts
def pickColor(node, assignment):
    conflicts = {}
    for color in node.pColors:

        #keep count of conflicts for each color
        conflicts[color] = 0

        #count when color matches assigned color of a neighbor
        for neighbor in node.neighbors:
            if assignment[neighbor.name] == color:
                conflicts[color] += 1

    #choose the color that leads to the least conflicts with neighbors
    minConflicts = min(conflicts, key=conflicts.get)
    return minConflicts

#return True if assignment is a valid solution to the csp
def valid(assignment, csp):

    #verify each pair of neighbors are colored differently
    for edge in csp.edges:
        color1 = assignment[edge[0].name]
        color2 = assignment[edge[1].name]
        if color1 == color2:
            return False
    return True

def localSearch(csp):
    #choose starting assignment for csp
    curr = {}
    for node in csp.nodes:
        curr[node.name] = random.choice(node.pColors)

    #set time limit to one minute from now
    limit = time.time() + 60
    loopcount = 0
    #loop up to time limit
    while time.time() < limit:
        
        #if current assignment is a solution, return it
        if valid(curr, csp):
            return curr

        #choose a random node and the value that minimizes conflicts
        node = random.choice(csp.nodes)
        color = pickColor(node, curr)
        curr[node.name] = color
        loopcount += 1
    print("Local Search halted after 1 minute.")
    return None






colors = []
nodes = []
edges = []
nodeSection = False
edgeSection = False

#loop through input file, saving info based on section
for line in fileinput.input():

    if line == '\n':
        if nodeSection:
            edgeSection = True
        else:
            nodeSection = True
        continue

    if not nodeSection:
        colors.append(line.strip())
    elif not edgeSection:
        name = line.strip()
        nodes.append(Node(name,list(colors)))
    else:
        names = line.strip().split()
        node1 = next(node for node in nodes if node.name == names[0])
        node2 = next(node for node in nodes if node.name == names[1])

        node1.neighbors.append(node2)
        node2.neighbors.append(node1)

        edges.append([node1, node2])
        edges.append([node2, node1])


csp = CSP(nodes, edges)
sol = localSearch(csp)
if sol is not None:
    print("Local Search Solution: ")
    for node,color in sol.items():
        print(node + " : " + color)