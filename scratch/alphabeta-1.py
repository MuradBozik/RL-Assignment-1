def alphaBetaSearch(self, node, depth, alpha, beta, isMaximizer):
    node['searched'] = True

    if depth == 0 or node['type'] == 'LEAF':
        # if depth == 0, then it is already a leaf node
        node['type'] = 'LEAF'
        # node['value'] = self.dummyEval()
        # calculate the value
        if isMaximizer:
            node['value'] = self.dijkstraEval(node['board'], 1)
        else:
            node['value'] = self.dijkstraEval(node['board'], 2)
        return node['value']

    # If we already get this nodes children then this section we be skipped
    if len(node['children']) <= 0:
        # get children of this node
        children = []
        moves = HexBoard.getMoveList(node)

        # If there is no possible move then this is a leaf node
        if len(moves) == 0:
            # Node type is changing!!!!
            node['type'] = 'LEAF'
            if isMaximizer:
                node['value'] = self.dijkstraEval(node['board'], 1)
            else:
                node['value'] = self.dijkstraEval(node['board'], 2)
            return node['value']
        else:
            for move in moves:
                b = node['board'].copy()
                if isMaximizer:
                    b[move] = self.MAXIMIZER
                else:
                    b[move] = self.MINIMIZER
                child_id = str(uuid.uuid4())
                node_type = 'MIN'
                if node['type'] == 'MIN':
                    node_type = 'MAX'

                child = {'id': child_id, 'type': node_type, 'children': [], 'parent_type': node['type'],
                         'searched': False, 'board': b, 'value': None, 'name': child_id[-3:]}
                children.append(child)
        node['children'] = children

    if isMaximizer:
        bestVal = -self.INF
        for n in node['children']:
            bestVal = max(bestVal, self.alphaBetaSearch(n, depth - 1, alpha, beta, False))
            alpha = max(alpha, bestVal)  # Updating alpha
            if bestVal >= beta:
                break  # beta cutoff, a>=b
    else:
        bestVal = self.INF
        for n in node['children']:
            bestVal = min(bestVal, self.alphaBetaSearch(n, depth - 1, alpha, beta, True))
            beta = min(beta, bestVal)  # Updating beta
            if alpha >= bestVal:
                break  # alpha cutoff, a>=b

    node['value'] = bestVal

    return bestVal
