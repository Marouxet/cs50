from sys import maxsize
from tictactoe import player, initial_state, actions, result, utility, winner, terminal, minValue, maxValue,minimax
import copy
X = "X"
O = "O"
EMPTY = None

a = initial_state()
print(minimax(a))
