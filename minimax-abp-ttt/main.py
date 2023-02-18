import numpy as np
import matplotlib.pyplot as plt


def move_still_possible(S):
    # return false if the game state (S for state) contains no cells with '0'. 0 representing an empty cell.
    return not (S[S == 0].size == 0)


# Use Minimax with alpha beta pruning to return the best move
# https://www.youtube.com/watch?v=zp3VMe0Jpf8
def move_by_minimax(S, p, alpha, beta):
    # 'X' return 1 and None as move_by_minimax requires 2 return values.
    # None will represent the best_move which is set at another return point below
    if move_was_winning_move(S, 1):
        return 1, None
    # 'O'
    if move_was_winning_move(S, -1):
        return -1, None
    # if there are no more moves to be made, then return a 0 to represent a draw
    if not move_still_possible(S):
        return 0, None

    # if it is 'X' turn, run max
    if p == 1:
        best_score = -np.inf # set the best_score to -infinity and loop through the entire grid
        for i in range(3):
            for j in range(3):
                if S[i][j] == 0:  # if an empty space is found (0), set it to the current player (1)
                    S[i][j] = p
                    score, _ = move_by_minimax(S, -1, alpha, beta)  # move has been made, call min
                    # after reaching this point, set the board space back to 0 and check if new score is better than
                    # previous best
                    S[i][j] = 0
                    if score > best_score:
                        best_score = score  # set the highest value to best score, and get the move that was made
                        best_move = (i, j)
                    # use alpha / beta to see if we can return early
                    # alpha will equal -infinity or the best score, and then it will compare itself to beta
                    # if beta is less than alpha we can break out of the loop prematurely
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        # return the best_score and best_move to be actioned in the game loop
        return best_score, best_move
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if S[i][j] == 0:
                    S[i][j] = p
                    score, _ = move_by_minimax(S, 1, alpha, beta)  # move has been made, call max
                    S[i][j] = 0
                    if score < best_score:
                        best_score = score  # set the lowest value to best score, and get the move that was made
                        best_move = (i, j)
                    # alpha beta pruning can return earlier using min as well.
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move


# Probability values worked out via 10000 runs where the best move was evaluated from winning games
# this can be seen in the normalised_data.npy file
def move_by_probability(S, p):
    global prob_table  # pass in a global value so that changes made to the probability table persist
    for n in range(len(prob_table)):  # go through every element of the probability table
        max_value = np.max(prob_table)  # get the max value still in the table
        index = np.where(prob_table == max_value)  # get the index of the max value (may return more than one)
        prob_table[index[0][0]][index[1][0]] = 0.01  # set first element of the index to 0.01; it cannot be reused
        if S[index[0][0]][index[1][0]] == 0:  # if that index is 0
            S[index[0][0]][index[1][0]] = p  # set the gameState table to the player value
            break

    return S  # return, and update the game state


def move_at_random(S, p):
    # Get all grid spaces not yet used
    xs, ys = np.where(S == 0)

    # np.arrange returns an array the size of (with upper and lower bounds) the array passed in
    # np.random.permutation returns the array but in a new order
    # [0] returns the first element of the array
    i = np.random.permutation(np.arange(xs.size))[0]

    # set the random grid space to the player whose turn it is
    S[xs[i], ys[i]] = p

    return S


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    # rotate entire matrix such that the first row becomes the first column (anti-clockwise)
    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


# used to convert numbers to symbols when drawing out the grid for easier recognition
symbols = {1: 'x',
           -1: 'o',
            0: ' '}


# print game state matrix using characters
def print_game_state(S):
    board = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        board[board == n] = symbols[n]
    print(board)


def initialise_game():
    # use of global recommended here: https://www.w3schools.com/python/python_variables_global.asp
    # initialize an empty tic tac toe board
    global gameState
    gameState = np.zeros((3, 3), dtype=int)

    # initialize the player who moves first (either +1 or -1)
    global player
    player = 1

    # initialize a move counter
    global mvcntr
    mvcntr = 1

    # initialize a flag that indicates whether the game has ended
    global noWinnerYet

    global prob_table
    global loaded_prob_table
    prob_table = np.copy(loaded_prob_table)

    noWinnerYet = True


def normalise_count_data(T):
    # https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
    x = np.reshape(T, T.size)
    s = sum(x)
    norm = [float(i)/s for i in x]  # divide each value of list 'x' by the total sum of all elements
    for i in range(len(norm)):
        norm[i] = round(norm[i], 3)
    # https://geekflare.com/numpy-reshape-arrays-in-python/
    # line norm = [float... returns a standard list which means I must convert back to an np.array to reshape
    norm_array = np.asarray(norm)
    norm_array = norm_array.reshape(3,3)
    return norm_array


def save_data_to_disk(data):
    np.save('normalised_data', data)


def get_occupied_fields(S, p, T):
    if symbols[p] == 'x':
        # returns a tuple, first item is a row and second is the column
        #i.e (array([0, 0, 0, 1, 1]), array([0, 2, 3, 1, 3])) = (0,0),(0,2),(0,3),(1,1),(1,3) co-ords where it was true
        # https://numpy.org/doc/stable/reference/generated/numpy.where.html
        # condition (1), array_like (shape?), value to broadcast
        allX = np.where(S == 1, S, 0) # 0 means set to 0 a value which is false
        T += allX
    elif symbols[p] == 'o':
        allX = np.where(S == -1, S, 0)
        T += allX


if __name__ == '__main__':
    gameState = np.zeros((3, 3), dtype=int)
    player = 1  # the player that will go first (1 = 'X', -1 = 'O')
    mvcntr = 1  # move counter
    noWinnerYet = True
    gamesPlayed = 0
    loaded_prob_table = np.load('normalised_data.npy')  # Load in the normalised data for move_by_probability()
    prob_table = np.copy(loaded_prob_table)
    winTable = []
    winTally = np.zeros((3, 3), dtype=int)

    # the number of games value here can be updated for more or less games depending on what is desired
    while gamesPlayed < 100:
        while move_still_possible(gameState) and noWinnerYet:
            # turn current player number into player symbol
            name = symbols[player]
            #print ('%s moves' % name)

            # move current player by probability / random
            if player == 1:
                # gameState = move_by_probability(gameState, player)
                # gameState = move_by_heuristic(gameState, player)
                best_score_p, best_move_p = move_by_minimax(gameState, player, -np.inf, np.inf)
                gameState[best_move_p] = player
            elif player == -1:
                gameState = move_at_random(gameState, player)

            # print current game state
            # print_game_state(gameState)

            # evaluate current game state
            if move_was_winning_move(gameState, player):
                print ('player %s wins after %d moves' % (name, mvcntr))
                noWinnerYet = False
                winTable.append(player)
                get_occupied_fields(gameState, player, winTally)  # Find out the winning positions, for probability data

            # switch current player and increase move counter
            player *= -1
            mvcntr += 1

        if noWinnerYet:
            print ('game ended in a draw' )
            winTable.append(0)

        gamesPlayed += 1
        initialise_game()

    # normalise the winTally data and save it to a new file called 'normalised_data.txt'
    #save_data_to_disk(normalise_count_data(winTally)) # returns (row1), (row2), (row3) contiguously in a single array form
    # plot histogram of wins and draws
    # this plot can be outputted to file. I have used PyCharm for ease of doing this.
    # I am unsure what this would look like if ran through a terminal, the file may not be savable.
    plt.hist(winTable)
    plt.xticks(range(-1, 2))
    plt.xlabel('game outcome')
    plt.ylabel('outcome count')
    plt.title('Games won and drawn after 100 plays')
    plt.show()
