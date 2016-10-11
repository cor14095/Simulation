from threading import Thread
from multiprocessing import Queue
import numpy as np
import random
from copy import deepcopy
import time
import array

board = np.array([
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
])

p1_token = 1
p2_token = -1
draw_token = 0

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

# Esta funcion me ayuda a saber si el jugador va ganando y si va a ganar, debo detenerlo.
def isPlayerWining(state, x, y, z):
  # Calculos para ver que tan probable es ganar en cada posible forma.
  sum_y = state[x][0][z] + state[x][1][z] + state[x][2][z] + state[x][3][z]
  sum_x = state[0][y][z] + state[1][y][z] + state[2][y][z] + state[3][y][z]
  sum_z = state[x][y][0] + state[x][y][1] + state[x][y][2] + state[x][y][3]
  diag_izq_z = state[0][0][z] + state[1][1][z] + state[2][2][z] + state[3][3][z]
  diag_der_z = state[3][0][z] + state[2][1][z] + state[1][2][z] + state[0][3][z]
  diag_izq_y = state[0][y][0] + state[1][y][1] + state[2][y][2] + state[3][y][3]
  diag_der_y = state[3][y][0] + state[2][y][1] + state[1][y][2] + state[0][y][3]
  diag_izq = state[0][0][0] + state[1][1][1] + state[2][2][2] + state[3][3][3]
  diag_der = state[3][0][0] + state[2][1][1] + state[1][2][2] + state[0][3][3]

  # Ahora tengo que ver cual es mas probable para ganar
  posibles = [sum_x, sum_y, sum_z, diag_izq_z, diag_der_z, diag_izq_y, diag_der_y, diag_izq, diag_der]
  indice = max(sum_x, sum_y, sum_z, diag_izq_z, diag_der_z, diag_izq_y, diag_der_y, diag_izq, diag_der)
  indice = posibles.index(indice)
  
  if (indice == 0):
    return [0, sum_x]
  elif (indice == 1):
    return [1, sum_y]
  elif (indice == 2):
    return [2, sum_z]
  elif (indice == 3):
    return [3, diag_izq_z]
  elif (indice == 4):
    return [4, diag_der_z]
  elif (indice == 5):
    return [5, diag_izq_y]
  elif (indice == 6):
    return [6, diag_der_y]
  elif (indice == 7):
    return [7, diag_izq]
  elif (indice == 8):
    return [8, diag_der]
  else:
    return [-1, -1]

def simGame(state, p1x, p1y, p1z):
    # Le damos a la simulacion el ultimo movimiento del jugador
    x = p1x
    y = p1y
    z = p1z
    player_turn = False   # Falso porque esta simulacion siempre empieza en el turno del jugador 2
    moves = 0
    first_move = [0, 0, 0]
    new_state = deepcopy(state)
    all_moves = []
    win_state = isPlayerWining(new_state, x, y, z)
    
    while (win_state[1] < 4):            # While 1
      # Simulamos...

      # Obtenemos una lista de posibles movimientos
      all_moves = zip(*np.where(new_state == 0))
      size_of_moves = len(all_moves)
      if (size_of_moves == 0):
          # Es un empate y hay que salir del while
          break;
      random_index = random.randint(0, size_of_moves - 1)
      random_move = all_moves[random_index]
      # Asignamos las variables (x, y, z)
      x = random_move[0]
      y = random_move[1]
      z = random_move[2]
      #print (size_of_moves, random_index, winner(new_state), x, y, z, moves, n)
      
      # Necesitamos almacenar el primer movimiento
      if (moves == 0):
        first_move = [x, y, z]
      # END if
      
      # Luego ponemos el token necesario.
      new_state[x][y][z] = (1 if player_turn else -1)
      player_turn =  not player_turn
      moves += 1
      
      # Actualizamos win_state
      win_state = isPlayerWining(new_state, x, y, z)
      
    # END while 1
    return_values = first_move
    # Si se llega a una victoria o un empate
    if (winner(new_state) == 1):
        # Si gana el jugador 1.
        return_values.append(-1)
    elif (winner(new_state) == 1):
        # Gano la maquina.
        return_values.append(1)
    else:
        # Nadie gano.
        return_values.append(5)
    
    # Retornamos un vector con los valores importantes
    return return_values
    # Retorna: [x, y, z, (w/l/t)]

def wrapper(func, qIn, qOut, state):
    for arg in iter(qIn.get, None):
        qOut.put(func(state, arg[0], arg[1], arg[2]))

numThreads = 100  # or N

qIn, qOut = Queue(), Queue()
# Divido la cantidad de iteraciones que quiero hacer en la cantidad de threads que tengo...
t = int(round(100/10))     # Cuantas simulaciones tiene que hacer cada thread
moves = []

for _ in range(t):
  moves.append([random.randint(0,9), random.randint(0,9), random.randint(0,9)])

  
print (moves)
  
# Genero los elementos que estaran en el input.
for _ in xrange(100):
  qIn.put(moves)
  
  
print (moves)
  
print (qIn.qsize())

arg = qIn.get()
  
for test in xrange(len(arg)):
  print arg[test][0], arg[test][1], arg[test][2], qIn.qsize()
  time.sleep(2)
  
# for i in xrange(numThreads):
#     qIn.put(None)
# for i in xrange(numThreads):
#     Thread(target=wrapper, args=(simGame, qIn, qOut, board)).start() 

# for _ in xrange(numThreads):
#     print qOut.get()