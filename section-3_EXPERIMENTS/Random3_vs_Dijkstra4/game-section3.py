from hex_skeleton import HexBoard
from util import UTIL
from os import system, name
import uuid
import time
from trueskill import Rating, rate_1vs1
import pickle
import matplotlib.pyplot as plt

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
    #clearOutput()
    #game.print()
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


def initGame(b_size, starter):
    #clearOutput()
    h = HexBoard(b_size)
    if starter == h.RED:
        h.maximizer = h.BLUE
        h.minimizer = h.RED
    else:
        h.maximizer = h.RED
        h.minimizer = h.BLUE
    return h

def saveRatings(object, name):
    with open('ratings'+ str(name), 'wb') as f:
        pickle.dump(object, f)

def plotElo(*argv):
    y1, y2 = argv
    x = [x for x in range(len(y1))]
    fig, ax = plt.subplots()
    ax.plot(x, y1, color='blue')
    ax.plot(x, y2, color='red')
    ax.set(xlabel='game (n)', ylabel='Elo (mu)')
    ax.legend(['BLUE', 'RED'])
    ax.grid()
    fig.savefig('fig.png')
    plt.show()

if __name__ == '__main__':
    t0 = time.time()
    r1 = Rating()
    r2 = Rating()
    experiment_number = 100
    countblue = 0
    countred = 0
    countdraw = 0
    #BLUE = 1
    #RED = 2
    starter = 2
    bord_size = int(input("Enter the board size for experiment: "))
    ratings1 = []
    ratings2 = []
    while experiment_number > 0:
        #if experiment_number < 50:
        #    starter = 2
        game = initGame(bord_size, starter)
        #game.print()
        
        util = UTIL(infinity=99, maximizer=game.maximizer, minimizer=game.minimizer)
        
        node_id = str(uuid.uuid4())
        node = {'id': node_id, 'type': 'MIN', 'children': [], 'searched': False, 'value':None, 'parent_type':'MAX', 'board': game.board, 'name': node_id[-3:]}
        print(f'Experiments left: {experiment_number} ')
        while True:
            if (game.turn % 2) == 0:
                # Computer 1's turn (Random)
                best_value = util.alphaBetaSearchRandom(node, 3, -9999999, 9999999, isMaximizer=False)
                move = util.getBestMove(node, best_value)
                game = makeMove(move, game)
                node = util.updateNode(node, game)
            else:
                # Computer 2's turn (Dijkstra)
                best_value = util.alphaBetaSearchDijkstra(node, 4, -9999999, 9999999, isMaximizer=True)
                move = util.getBestMove(node, best_value)
                game = makeMove(move, game)
                node = util.updateNode(node, game)
                
            if game.isGameOver():
                if game.checkWin(game.BLUE):
                    countblue = countblue + 1
                    r1, r2 = rate_1vs1(r1, r2)
                    # print("!!! Blue Player Won !!!")
                elif game.checkWin(game.RED):
                    countred = countred + 1
                    r2, r1 = rate_1vs1(r2, r1)

                    # print("!!! Red Player Won !!!")
                else:
                    countdraw = countdraw + 1
                    # print("!!! DRAW nobody could win !!!")

                ratings1.append(r1)
                ratings2.append(r2)
                experiment_number = experiment_number-1
                break

        saveRatings(ratings1, 1)
        saveRatings(ratings2, 2)

    plotElo(ratings1, ratings2)
    t1 = time.time()
    
    with open("output.txt", "w") as f: 
        f.write("------- Result of experiment -------\n")
        f.write("Number of experiment: 100\n")
        f.write(f"Win count of Red: {countred}\n")
        f.write(f"Win count of Blue: {countblue}\n")
        f.write(f'Rating of player 1 (RED): {r2}\n')
        f.write(f'Rating of player 2 (BLUE): {r1}\n')
        f.write(f"Total time: {t1 - t0}\n")

    print("------- Result of experiment -------")
    print("Number of experiment:", 100)
    print("Win count of Red:", countred)
    print("Win count of Blue:", countblue)
    # print("Total draw count:", countdraw)
    print(f'Rating of player 1 (RED): {r2}, Rating of player 2 (BLUE): {r1}')
    print(f"Total time: {t1 - t0}")
