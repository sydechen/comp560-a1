import fileinput
import re

#maintaining arc consistency
def ac3(queue, csp):
    inferences = {}
    while queue:
        arc = queue.pop(0)
        removed = []

        for color1 in arc[0].pColors:
            if any(color2 != color1 for color2 in arc[1].pColors):
                #consistent
                continue
            else:
                arc[0].pColors.remove(color1)
                removed.append(color1)
                if not arc[0].pColors:
                    return None
        if removed:
            #keep track of colors removed from node
            inferences[arc[0]] = removed   

            #add to queue: edges leading to current node
            addQueue = [edge for edge in csp.edges if edge[1] == arc[0]]
            queue.extend(edge for edge in addQueue if edge not in queue)
    return inferences

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


#finds most constrained node. If there are multiple, chooses most constraining out of those
def pickNode(nodes, assignment):
    unassigned = [node for node in nodes if node.name not in assignment]
    best = unassigned[0]
    for node in unassigned[1:]:
        if len(node.pColors) < len(best.pColors):
            best = node
        elif len(node.pColors) == len(best.pColors):
            nodeOpenNeighbors = 0
            mostOpenNeighbors = 0
            for neighbor in node.neighbors:
                if neighbor in unassigned:
                    nodeOpenNeighbors += 1
            for neighbor in best.neighbors:
                if neighbor in unassigned:
                    mostOpenNeighbors += 1
            if nodeOpenNeighbors > mostOpenNeighbors:
                best = node

    return best

def pickColor(node):
    #order by color that least constrains adjacent nodes
    candidates = {}
    for color in node.pColors:
        constraints = 0
        for neighbor in node.neighbors:
            if color in neighbor.pColors:
                constraints += 1
        candidates[color] = constraints
    sortCands = sorted(candidates.items(), key=lambda x: x[1])
    return sortCands

def inference(csp, node, assignment):
    #pass ac3 edges (node.neighbor, node)
    queue=[]
    for neighbor in node.neighbors:
        if not neighbor.name in assignment:
            addQueue = next(edge for edge in edges if edge[0] == neighbor and edge[1] == node)
            queue.append(addQueue)
    return ac3(queue, csp)

def consistent(node, color, assignment):
    for neighbor in node.neighbors:
            if neighbor.name in assignment and assignment[neighbor.name] == color:
                return False
    return True

def backtrack(assignment, csp):
    if len(nodes) == len(assignment):
        return assignment
    node = pickNode(csp.nodes, assignment)
    for cand in pickColor(node):
        color = cand[0]
        if consistent(node, color, assignment):
            assignment[node.name] = color
            removed = list(node.pColors)
            removed.remove(color)
            node.pColors = [color]
            inferences = inference(csp, node, assignment)
            if inferences is not None:
                result = backtrack(assignment, csp)
                if result is not None:
                    return result
                #dead tree
                #remove inferences from assignment
                for node, colors in inferences.items():
                    node.pColors += colors
            #remove node = color assignment
            #restore color candidates
            assignment.pop(node.name)
            node.pColors += removed
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
assignment = {}
sol = backtrack(assignment, csp)
print("Backtracking Search Solution: ")
for node,color in sol.items():
    print(node + " : " + color)

