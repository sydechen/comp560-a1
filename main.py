import fileinput
import re
import copy
from classes.node import Node
from classes.edge import Edge
from classes.csp import CSP
from classes.backtracker import Backtracker
from classes.localsearcher import LocalSearcher

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
csp2 = copy.deepcopy(csp)
assignment = {}
search = Backtracker()
bSol = search.backtrack(assignment, csp, 0)
print("Solution: ")
for node,color in bSol.items():
    print(node + " : " + color)

print("\nLocal Search Start...")
search = LocalSearcher()
lSol = search.localSearch(csp2)
if lSol is not None:
    print("Solution: ")
    for node,color in lSol.items():
        print(node + " : " + color)
else:
    print("Local Search halted after 1 minute.")
