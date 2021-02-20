"""
Tic Tac Toe Player
"""

import math
import copy
import time

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Check initial state
    if board == initial_state():
        return X
   #elif terminal(board): ## Falta chequear esto
   #     raise NotImplementedError
    else:
        # Count None: if there are an even number of "nones" -> ist turn of the "O" Player
        nones = [x.count(None) for x in board]
        if ((nones[0]+nones[1]+nones[2]) % 2) == 0:
            return O
        else:
            return X
        #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    opciones = set()
    board2Test = copy.deepcopy(board)
    for x,y in enumerate(board2Test):
        for w,z in enumerate(y):
            if z == None:
                opciones.add((x,w))
    
    return opciones



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Check if action is one posible action
    if action not in actions(board):
        raise NameError('Action not correct')

    # Make deep copy, chek player and replace action by players
    board2 = copy.deepcopy(board)
    board2[action[0]][action[1]] = player(board)
    return board2
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if (board[1][1]==board[0][0]) and (board[1][1]==board[2][2]) or (board[1][1]==board[0][2]) and (board[1][1]==board[2][0]) \
    or (board[1][1]==board[1][0]) and (board[1][1]==board[1][2]) or (board[1][1]==board[0][1]) and (board[1][1]==board[2][1]):
            win = board[1][1]
    elif (board[0][1]==board[0][0]) and (board[0][1]==board[0][2]):
        win = board[0][1]
    elif (board[2][1]==board[2][0]) and (board[2][1]==board[2][2]):
        win = board[2][1]
    elif (board[1][0]==board[0][0]) and (board[1][0]==board[2][0]):
        win = board[1][0]
    elif (board[1][2]==board[0][2]) and (board[1][2]==board[2][2]):
        win = board[1][2]
    else:
        win = None
    return win

def terminal(board):
    """
    Returns True if game is over, False otherwise.

    Game is over if there is a winner or if there are not options
    """
    if (winner(board) != None) or len(actions(board)) == 0:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)== X:
 
        return 1
        
    elif winner(board) == O:
        return -1
        
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    """
    if player(board) == X:
        # MAX PLAYER
        opciones = actions(board)
        opcioneslist= []
        valores = []
        for op in opciones:
            valores.append(minValue(result(board,op)))
            opcioneslist.append(op)
        return opcioneslist[valores.index(max(valores))]
             

    elif player(board) == O:
        # MIN PLAYER
        opciones = actions(board)
        valores = []
        opcioneslist = []
        for op in opciones:
            valores.append(maxValue(result(board,op)))
            opcioneslist.append(op)
        return opcioneslist[valores.index(min(valores))]



def minValue(board):
    if terminal(board):
        a = utility(board)
        return a
    else:
        v = 10
        for action in actions(board):
            v = min(v,maxValue(result(board,action)))
        return  v    


def maxValue(board):
    if terminal(board):
        a = utility(board)
        return a
    else:
        v = -10
        for action in actions(board):
            v = max(v,minValue(result(board,action)))
        return  v 
