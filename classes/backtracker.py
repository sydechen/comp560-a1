class Backtracker:

    #maintains arc consistency
    def ac3(self, queue, csp):
        inferences = {}

        while queue:
            arc = queue.pop(0)
            removed = []

            for color1 in arc[0].pColors:

                #remove color from node if it leads to inconsistency with any neighbors
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

                #add to queue: any edges in csp leading to current node
                addQueue = [edge for edge in csp.edges if edge[1] == arc[0]]
                queue.extend(edge for edge in addQueue if edge not in queue)
        return inferences


    #MRV followed by degree heuristic
    #returns most constrained node. If there are multiple, chooses most constraining out of those
    def pickNode(self, nodes, assignment):

        #get unassigned nodes
        unassigned = [node for node in nodes if node.name not in assignment]
        best = unassigned[0]
        for node in unassigned[1:]:

            #choose node with less remaining values
            if len(node.pColors) < len(best.pColors):
                best = node
            elif len(node.pColors) == len(best.pColors):
                nodeOpenNeighbors = 0
                mostOpenNeighbors = 0

                #count unassigned neighbors to find most constraining node
                for neighbor in node.neighbors:
                    if neighbor in unassigned:
                        nodeOpenNeighbors += 1
                for neighbor in best.neighbors:
                    if neighbor in unassigned:
                        mostOpenNeighbors += 1
                if nodeOpenNeighbors > mostOpenNeighbors:
                    best = node

        return best

    #Least constraining value heuristic
    #returns list of possible colors for node ordered by least constraining
    def pickColor(self, node):
        candidates = {}
        for color in node.pColors:
            constraints = 0

            #count how many neighbors have this color in their domain
            for neighbor in node.neighbors:
                if color in neighbor.pColors:
                    constraints += 1
            candidates[color] = constraints
        
        #list colors sorted by least to most constraints
        sortCands = sorted(candidates.items(), key=lambda x: x[1])
        return sortCands

    #calls ac3 with edge queue
    def inference(self, csp, node, assignment):
        queue=[]

        #create queue of edges from node's unassigned neighbors --> node
        for neighbor in node.neighbors:
            if not neighbor.name in assignment:
                addQueue = next(edge for edge in csp.edges if edge[0] == neighbor and edge[1] == node)
                queue.append(addQueue)

        return self.ac3(queue, csp)

    #returns True if none of node's neighbors are already assigned to the given color
    def consistent(self, node, color, assignment):
        for neighbor in node.neighbors:
                if neighbor.name in assignment and assignment[neighbor.name] == color:
                    return False
        return True

    def backtrack(self, assignment, csp, count):

        #if assignment is finished, return assignment
        if len(csp.nodes) == len(assignment):
            print("Backtracking Search Steps: ", count)
            return assignment
        
        #choose node
        node = self.pickNode(csp.nodes, assignment)

        #update step counter
        count += 1

        #loop through colors starting with least constraining
        for cand in self.pickColor(node):
            color = cand[0]

            if self.consistent(node, color, assignment):
                #add node = color to assignment
                assignment[node.name] = color

                removed = list(node.pColors)
                removed.remove(color)
                node.pColors = [color]

                #do arc consistency
                inferences = self.inference(csp, node, assignment)
                if inferences is not None:
                    #continue search tree
                    result = self.backtrack(assignment, csp, count)
                    if result is not None:
                        return result

                    #dead tree
                    #put back colors removed from node domains during ac3
                    for node, colors in inferences.items():
                        node.pColors += colors

                #remove node = color assignment and restore node domain
                assignment.pop(node.name)
                node.pColors += removed
        return None