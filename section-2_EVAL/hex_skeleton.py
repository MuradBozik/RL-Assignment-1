import numpy as np

class HexBoard:
    BLUE = 1
    RED = 2
    EMPTY = 0

    def __init__(self, board_size):
        self.board = np.zeros(shape=(board_size, board_size), dtype=int)
        self.size = board_size
        self.game_over = False
        self.turn = 0
        self.hexes = self.createHexes()

    def createHexes(self):
        hexes = []
        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                neighbors = self.getNeighbors(position)
                hexes.append(Hex(position, neighbors))
        return hexes

    def getHex(self, position):
        x = None
        hexes = self.hexes.copy()
        for hx in hexes:
            if hx.position == position:
                x = hx
                return x
        if x is None:
            print("Error! Counldn't be found.")

    def isGameOver(self):
        return self.game_over

    def isEmpty(self, coordinates):
        return self.board[coordinates] == HexBoard.EMPTY

    def isColor(self, coordinates, color):
        return self.board[coordinates] == color

    def getColor(self, coordinates):
        if coordinates == (-1, -1):
            return HexBoard.EMPTY
        return self.board[coordinates]

    def place(self, coordinates, color):
        if not self.game_over and self.board[coordinates] == HexBoard.EMPTY:
            self.board[coordinates] = color
            if self.checkWin(HexBoard.RED) or self.checkWin(HexBoard.BLUE):
                self.game_over = True

    def getOppositeColor(self, current_color):
        if current_color == HexBoard.BLUE:
            return HexBoard.RED
        return HexBoard.BLUE

    def getNeighbors(self, coordinates):
        (cx, cy) = coordinates
        neighbors = []
        if cx - 1 >= 0:   neighbors.append((cx - 1, cy))
        if cx + 1 < self.size: neighbors.append((cx + 1, cy))
        if cx - 1 >= 0 and cy + 1 <= self.size - 1: neighbors.append((cx - 1, cy + 1))
        if cx + 1 < self.size and cy - 1 >= 0: neighbors.append((cx + 1, cy - 1))
        if cy + 1 < self.size: neighbors.append((cx, cy + 1))
        if cy - 1 >= 0:   neighbors.append((cx, cy - 1))
        return neighbors

    def border(self, color, move):
        (nx, ny) = move
        return (color == HexBoard.RED and nx == self.size - 1) or (color == HexBoard.BLUE and ny == self.size - 1)

    def traverse(self, color, move, visited):
        if not self.isColor(move, color) or (move in visited and visited[move]): return False
        if self.border(color, move): return True
        visited[move] = True
        for n in self.getNeighbors(move):
            if self.traverse(color, n, visited): return True
        return False

    def checkWin(self, color):
        for i in range(self.size):
            if color == HexBoard.RED:
                move = (0, i)
            else:
                move = (i, 0)
            if self.traverse(color, move, {}):
                return True
        return False

    def print(self):
        print("   ", end="")
        for y in range(self.size):
            print(chr(y + ord('a')), "", end="")
        print("")
        print(" -----------------------")
        for x in range(self.size):
            print(x, "|", end="")
            for z in range(x):
                print(" ", end="")
            for y in range(self.size):
                piece = self.board[x, y]
                if piece == HexBoard.BLUE:
                    print("b ", end="")
                elif piece == HexBoard.RED:
                    print("r ", end="")
                else:
                    if y == self.size:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")
        print("   -----------------------")

    def getMoveList(node):
        """
        Returns freeCoordinates that we can move as a list of tuples
        """
        boardState = node['board']  # it is ndarray
        freeCoordinates = []
        fcoords = np.where(boardState == 0)
        for (x, y) in zip(fcoords[0], fcoords[1]):
            freeCoordinates.append((x, y))
        return freeCoordinates

    def unMakeMove(game, coordinates):
        game.place(coordinates, game.EMPTY)


class Hex:
    def __init__(self, position, neighbors, weight=1, distance=99999999):
        self.position = position
        self.neighbors = neighbors
        self.weight = weight
        self.distance = distance
