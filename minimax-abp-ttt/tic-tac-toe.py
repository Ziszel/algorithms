import numpy as np

# Set up the Tic-Tac-Toe board
board = np.array([['-', '-', '-'],
                  ['-', '-', '-'],
                  ['-', '-', '-']])


# Function to check if a player has won
def check_win(player):
    for i in range(3):
        if np.all(board[i, :] == player) or np.all(board[:, i] == player):
            return True
    if np.all(board.diagonal() == player) or np.all(np.fliplr(board).diagonal() == player):
        return True
    return False


# Function to check if the game is over
def game_over():
    if check_win('X') or check_win('O'):
        return True
    if '-' not in board:
        return True
    return False


# Function to get the best move using minimax
def minimax(player, alpha, beta):
    if check_win('X'):
        return -1
    if check_win('O'):
        return 1
    if '-' not in board:
        return 0

    if player == 'O':
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = player
                    score = minimax('X', alpha, beta)
                    board[i][j] = '-'
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = player
                    score = minimax('O', alpha, beta)
                    board[i][j] = '-'
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score


# Function to make a move
def make_move(player):
    if player == 'O':
        best_score = -np.inf
        best_move = None
        alpha = -np.inf
        beta = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = player
                    score = minimax('X', alpha, beta)
                    board[i][j] = '-'
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        board[best_move] = player
    else:
        print(board)
        row = int(input('Enter row: '))
        col = int(input('Enter column: '))
        if board[row][col] == '-':
            board[row][col] = player
        else:
            print('Invalid move!')
            make_move(player)


# Main game loop
while not game_over():
    make_move('X')
    if not game_over():
        make_move('O')

# Print the final board
print(board)

# Print the winner
if check_win('X'):
    print('X wins!')
elif check_win('O'):
    print('O wins!')
else:
    print('It\'s a tie!')