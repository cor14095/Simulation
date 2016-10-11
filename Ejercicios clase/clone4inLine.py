from __future__ import print_function
import random
from copy import deepcopy
import time
from multiprocessing.pool import ThreadPool


board = [
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ]
]

p1_token = 1
p2_token = -1
draw_token = 0
pool = ThreadPool(processes=1)


def slice_winner(state_slice):
  slice_size = len(state_slice)
  sums = [sum(row) for row in state_slice]
  sums.extend([sum([row[i] for row in state_slice]) for i in range(slice_size)])

  if (p1_token * slice_size) in sums:
    return p1_token
  elif (p2_token * slice_size) in sums:
    return p2_token

  return 0

def winner(state):
  for state_slice in state:
    winner_in_slice = slice_winner(state_slice)
    if winner_in_slice != draw_token:
      return winner_in_slice

  state_size = len(state)

  for i in range(state_size):
    state_slice = []
    for j in range(state_size):
      state_slice.append([state[j][i][k] for k in range(state_size)])

    winner_in_slice = slice_winner(state_slice)

    if winner_in_slice != draw_token:
      return winner_in_slice

  diagonals = [0, 0, 0, 0]
  for i in range(state_size):
    diagonals[0] += state[i][i][i]
    diagonals[1] += state[state_size - 1 - i][i][i]
    diagonals[2] += state[i][state_size - 1 - i][i]
    diagonals[3] += state[state_size - 1 - i][state_size - 1 - i][i]

  if (p1_token * state_size) in diagonals:
    return p1_token

  elif (p2_token * state_size) in diagonals:
    return p2_token

  return draw_token

def str_token(cell):
  if cell == p1_token:
    return "X"
  elif cell == p2_token:
    return "O"

  return "."

def draw_board(state):
  result = ""
  state_size = len(state)
  for y in range(state_size):
    for z in range(state_size):
      for x in range(state_size):
        result += str_token(state[x][y][z]) + " "
      result += "\t"
    result += "\n"
  return result
  
def isInVector(vector, x, y, z):
  n = 0
  while (n < len(vector)):
    if (vector[n][0] == x and vector[n][1] == y and vector[n][2] == z):
      return True
    n += 1
  return False
  
def getInVector(vector, x, y, z):
  n = 0
  while (n < len(vector)):
    if (vector[n][0] == x and vector[n][1] == y and vector[n][2] == z):
      return n
    n += 1
  return -1
  
def getBestPlay(vector):
  max_value = -100000
  index_of_max = -1
  for i in range(len(vector)):
    if (vector[i][3] > max_value):
      max_value = vector[i][3]
      index_of_max = i
  return [vector[index_of_max][0], vector[index_of_max][1], vector[index_of_max][2]]

def AISim(main_state, p1x, p1y, p1z, maxIt):
  n = 0                 # Number of simulations
  p2Moves = []          # A vector to hold player 2 moves.
  while (n < maxIt):    # While 1
    x = p1x
    y = p1y
    z = p1z
    player_turn = False   # False because simulation will always start with player 2 turn
    moves = 0
    first_move = [0, 0, 0]
    new_state = deepcopy(main_state)
    while winner(new_state) == draw_token:            # While 2
      
      temp = new_state[x][y][z]
      while temp != draw_token:         # While 3
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        z = random.randint(0, 3)
        
        temp = new_state[x][y][z]
        
        # THIS IS THE PROBLEEEEEM!!!!
        time.sleep(0.01)
        
      # END while 3
      
      if (moves == 0):
        first_move = [x, y, z]
        if (not isInVector(p2Moves, x, y, z)):
          p2Moves.append([x, y, z, 0])
        # END if
      # END if
      
      new_state[x][y][z] = (1 if player_turn else -1)
      player_turn =  not player_turn
      moves += 1
    # END while 2
    
    if (winner(new_state) == 1):
      temPos = getInVector(p2Moves, first_move[0], first_move[1], first_move[2])
      p2Moves[temPos][3] -= 1
    else:
      temPos = getInVector(p2Moves, first_move[0], first_move[1], first_move[2])
      p2Moves[temPos][3] += 1
    # END if-else
    
    n += 1
  # END while 1
  
  return getBestPlay(p2Moves)


# --------------------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN PROGRAM -------------------------------------------------
# --------------------------------------------------------------------------------------------------------

AIMove = [0, 0, 0]

player_1_turn = True
while winner(board) == draw_token:

  # Print board state
  print ("")
  print ("Board:")
  print (draw_board(board))
  print ("")

  # Print 
  print ("Player %s turn:" % (1 if player_1_turn else 2))
  
  if (player_1_turn):

    # Get input
    x = int(raw_input("x: "))
    y = int(raw_input("y: "))
    z = int(raw_input("z: "))
  else:
    # Player 2 turn
    start = time.time()
    new_board = deepcopy(board)
    async_result = pool.apply_async(AISim, (new_board, x, y, z, 100))
    AIMove = async_result.get()
    end = time.time()
    print ("Thinking time: %0.4f seconds" % (end - start))
    x = AIMove[0]
    print ("x:",x)
    y = AIMove[1]
    print ("y:",y)
    z = AIMove[2]
    print ("z:",z)
    
  
  if board[x][y][z] == draw_token:
    board[x][y][z] = 1 if player_1_turn else -1
    player_1_turn = not player_1_turn
  
  else:
    print ("")
    print ("ERROR: occupied position, please retry in a new position")
    print ("")

print ("Player %s is the winner!" % (1 if winner(board) == 1 else 2))
