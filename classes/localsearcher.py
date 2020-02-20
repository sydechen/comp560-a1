import time
import random

class LocalSearcher:
        #chooses the value for a node which minimizes conflicts
    def pickColor(self, node, assignment):
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
    def valid(self, assignment, csp):

        #verify each pair of neighbors are colored differently
        for edge in csp.edges:
            color1 = assignment[edge[0].name]
            color2 = assignment[edge[1].name]
            if color1 == color2:
                return False
        return True

    def localSearch(self, csp):
        #choose starting assignment for csp
        curr = {}
        for node in csp.nodes:
            curr[node.name] = random.choice(node.pColors)

        #set time limit to one minute
        limit = time.time() + 60
        changes = 0
        loops = 0

        while time.time() < limit:
            
            #if current assignment is a solution, return it
            if self.valid(curr, csp):
                print("Local Search Steps: ", changes)
                return curr

            #if we loop 50x the number of nodes, reshuffle initial assignment to prevent getting stuck
            if loops == len(csp.nodes) * 50:
                loops = 0
                for node in csp.nodes:
                    curr[node.name] = random.choice(node.pColors)

            #choose a random node and the value that minimizes conflicts
            node = random.choice(csp.nodes)
            color = self.pickColor(node, curr)

            #modify assignment if node wasn't already that color
            if curr[node.name] != color:
                curr[node.name] = color
                changes += 1
            loops += 1
        return None