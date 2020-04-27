def dijkstra(self, hexboard, color):
    self.resetHexes(hexboard)
    start = None
    dest = None

    #  Creating outer hexes
    if color == hexboard.RED:
        Rs_neighbors = []
        Re_neighbors = []
        for i in range(hexboard.size):
            Rs_neighbors.append(hexboard.getHex((0, i)).position)
            Re_neighbors.append(hexboard.getHex((hexboard.size - 1, i)).position)
        # Set the distance to zero for our initial node
        Rs = Hex(position=(-1, -1), neighbors=Rs_neighbors, weight=0, distance=0)
        Re = Hex(position=(-2, -2), neighbors=Re_neighbors, weight=0, distance=99999999)

        start = Rs
        dest = Re
    elif color == hexboard.BLUE:
        Bs_neighbors = []
        Be_neighbors = []
        for i in range(hexboard.size):
            Bs_neighbors.append(hexboard.getHex((i, 0)).position)
            Be_neighbors.append(hexboard.getHex((i, hexboard.size - 1)).position)
        # Set the distance to zero for our initial node
        Bs = Hex(position=(-1, -1), neighbors=Bs_neighbors, weight=0, distance=0)
        Be = Hex(position=(-2, -2), neighbors=Be_neighbors, weight=0, distance=99999999)

        start = Bs
        dest = Be

    # Mark all nodes unvisited and store them.
    updatedWeights_nodes = self.updateWeights(color, hexboard)
    unvisited_nodes = self.getLastRow(hexboard, color, updatedWeights_nodes)
    unvisited_nodes.extend([start, dest])

    previous_vertices = {node: None for node in unvisited_nodes}

    while unvisited_nodes:
        # Select the unvisited node with the smallest distance,
        current_node = self.getMin(unvisited_nodes)
        # Stop, if the smallest distance among the unvisited nodes is infinity.
        if current_node.distance == 99999999:
            break

        # Find unvisited neighbors for the current node and calculate their distances through the current node.
        for neighbor_position in current_node.neighbors:
            if neighbor_position == (-2, -2):
                neighbor = dest
            else:
                neighbor = hexboard.getHex(neighbor_position)

            alternative_route = current_node.distance + neighbor.weight

            # Compare the newly calculated distance to the assigned and save the smaller one.

            if alternative_route < neighbor.distance:
                neighbor.distance = alternative_route
                previous_vertices[neighbor] = current_node

        # Mark the current node as visited and remove it from the unvisited set.
        unvisited_nodes.remove(current_node)

    path, current_node = deque(), dest
    while previous_vertices[current_node] is not None:
        path.appendleft(current_node.position)
        current_node = previous_vertices[current_node]
    if path:
        path.appendleft(current_node.position)
    #Remove outer nodes from path returned
    if len(path) > 0:
        path.remove((-1, -1))
        path.remove((-2, -2))
    return path
