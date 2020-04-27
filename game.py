from hex_skeleton import HexBoard
from util import UTIL
from os import system, name
import uuid
import time
from trueskill import Rating, rate_1vs1

def clearOutput():
    # for windows 
    if name == 'nt':
        system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')
    return


def makeMove(coordinates, game):
    if (game.turn % 2) == 0:
        color = game.minimizer
    else:
        color = game.maximizer
    try:
        game.place(coordinates, color)
        game.turn = game.turn + 1
    except:
        print('An error occured while making move!')
    return game


def getReady(game):
    if (game.turn % 2) == 0:
        player = game.minimizer
    else:
        player = game.maximizer
    if player == 1:
        playerName = '(Blue Player)'
    elif player == 2:
        playerName = '(Red Player)'
    else:
        print("PlayerName Error!!!!")
    while True:
        print(playerName + " Choose the coordinate to place your color: ")
        ans = input("Example: 2 c : ")
        move = getCoords(ans)
        if move[0] >= game.size or move[1] >= game.size:
            print('The coordinates you entered are out of bounds. Try again.')
        elif not game.isEmpty(move):
            print('Please select an empty cordinate. Try again.')
        else:
            break
    return move


def getCoords(answer):
    coords = answer.split()
    coordinates = list()
    for coord in coords:
        coord = coord.strip()
    if len(coords) == 2:
        coordinates.append(int(coords[0]))
        coordinates.append(ord(coords[1]) - ord('a'))
    elif len(coords) == 1 and len(coords[0]) == 2:
        coordinates.append(int(coords[0][0]))
        coordinates.append(ord(coords[0][1]) - ord('a'))
    return tuple(coordinates)


# def initGame(b_size):
#     h = HexBoard(b_size)
#     h.maximizer = h.RED
#     h.minimizer = h.BLUE
#     return h
def initGame():
    clearOutput()
    b_size = int(input("Enter the board size you want to play: "))
    h = HexBoard(b_size)
    ans = str(input("In order to start the game, please choose a side 'R' or 'B': ")).lower()
    if ans == 'b':
        h.maximizer = h.RED
        h.minimizer = h.BLUE
    elif ans == 'r':
        h.maximizer = h.BLUE
        h.minimizer = h.RED
    else:
        print("You pressed a wrong key. Please type 'R' or 'B'.")
        print("Game is restarting!!!")
        time.sleep(2)
        h = initGame()
    return h

if __name__ == '__main__':
    t0 = time.time()
    r1 = Rating()
    r2 = Rating()

    # bord_size = int(input("Enter the board size for experiment: "))
    FirstTable = {}
    SecondTable = {}
    game = initGame()

    util = UTIL(infinity=99, maximizer=game.maximizer, minimizer=game.minimizer)
    node_id = str(uuid.uuid4())
    node = {'id': node_id, 'type': 'MIN', 'children': [], 'searched': False, 'value':None, 'parent_type':'MAX', 'board': game.board, 'name': node_id[-3:]}
    while True:
        game.print()
        if (game.turn % 2) == 0:
            # Computer 1's turn
            best_value = util.alphaBetaSearch(node, 4, -9999999, 9999999, isMaximizer=False)
            move = getReady(game)
            game = makeMove(move, game)
            node = util.updateNode(node, game)
        else:
            # Computer 2's turn
            boardState = node['board'].copy()
            try:
                move = FirstTable[boardState.tobytes()]
            except KeyError:
                best_value = util.iterativeDeepening(node, True)
                move = util.getBestMove(node, best_value)
                FirstTable[boardState.tobytes()] = move
            game = makeMove(move, game)
            node = util.updateNode(node, game)

        if game.isGameOver():
            if game.checkWin(game.BLUE):
                print("!!! Blue Player Won !!!")
            elif game.checkWin(game.RED):
                print("!!! Red Player Won !!!")
            else:
                print("!!! DRAW nobody could win !!!")
            ans = str(input("In order to restart the game press 'A'\nTo exit the game press something else: ")).lower()
            if ans == 'a':
                game = initGame()
                game.print()
                node_id = str(uuid.uuid4())
                node = {'id': node_id, 'type': 'MAX', 'children': [], 'searched': False, 'board': game.board,
                        'name': node_id[-3:]}
            else:
                print("Thank you for your playing. We hoped you enjoyed the game.")
                time.sleep(2)  # 2 sec waiting to show previous closing sentence.
                break

