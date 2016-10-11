from __future__ import print_function
import random
from copy import deepcopy
import time
import numpy as np
from threading import Thread
from multiprocessing import Queue


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
num_threads = 1

# Funcion para juntar los outputs
# Credit: http://stackoverflow.com/a/22429572/4808919
def wrapper(func, qIn, qOut, state):
    for arg in iter(qIn.get, None):
        qOut.put(func(state, arg[0], arg[1], arg[2]))

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
  
# Esta funcion me ayuda a ver si el valor x, y, z ya esta en el vector de movimientos o no
def isInVector(vector, x, y, z):
  # Variables utiles
  n = 0
  while (n < len(vector)):
    if (vector[n][0] == x and vector[n][1] == y and vector[n][2] == z):
      # Si las coordenadas x, y, z que se dan estan en el vector 'vector'
      # entonces retornamos True.
      return True
    n += 1
  # Si acaba el ciclo y las coordenadas no se encontraron, retornamos False.
  return False
  
# Esta funcion me ayuda a buscar en un vector
def getInVector(vector, x, y, z):
  # Variables utiles
  n = 0
  while (n < len(vector)):
    if (vector[n][0] == x and vector[n][1] == y and vector[n][2] == z):
      # Si las coordenadas x, y, z que se dan estan en el vector 'vector'
      # entonces retornamos True.
      return n
    n += 1
  # Si acaba el ciclo y las coordenadas no se encontraron, retornamos False.
  return -1
  
# Esta funcion me ayuda a saber que movimiento tuvo la mayor cantidad de victorias.
def getBestPlay(vector):
  # Variables utiles
  max_value = -100000
  index_of_max = -1
  # Tenemos que iterar por el vector y buscar en todas las posibles
  for i in range(len(vector)):
    # Verificamos si i es un valor maximo
    if (vector[i][3] > max_value):
      # Si lo es, cambiamos nuestros valores
      max_value = vector[i][3]
      index_of_max = i
  # Al final retornamos el vector de valores maximos
  return [vector[index_of_max][0], vector[index_of_max][1], vector[index_of_max][2]]

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
    
# Esta funcion es para imprimir un mensaje de load
def loadMsg(dots):
    if (dots > 5):
        dots = 0
        
    print ("Thiking" + ("."*(dots)), end="\r")
    return dots + 1

# Esta funcion simula el turno del jugador 2
def AISim(state, x, y, z, maxIt):
  # Variables utiles
  n = 0                 # Numero de simulaciones
  p2_moves = []         # Un vector para saber que jugadas me causaron mayor cantidad de visctorias
  temp_result = []      # Un Array para el rusltado temporal.
  game_result = 0       # Un temporal para recibir el resultado del juego
  temp_pos = 0          # Un temporal para la posicion de la jugada
  qIn, qOut = Queue(), Queue()  # Uso colas porque se pueden mover entre Threads
  num_dots = 0
  
  while (n < maxIt):
      num_dots = loadMsg(num_dots)
      # Genero los elementos que estaran en el input.
      for i in xrange(num_threads):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        z = random.randint(0, 3)
        qIn.put([x, y, z])
      # Creo los threads y los corro.
      for i in xrange(num_threads):
        Thread(target=wrapper, args=(simGame, qIn, qOut, board)).start() 
      # Proceso los resultados.
      for i in xrange(num_threads):
        temp_result = qOut.get()
        x = temp_result[0]
        y = temp_result[1]
        z = temp_result[2]
        game_result = temp_result[3]
        # Reviso si el movimiento no esta en los movimientos anteriores
        if (not isInVector(p2_moves, x, y, z)):
            # Si no esta, entonces lo agrego
            p2_moves.append(temp_result)
        else:
            # Si esta, entonces agrego el resultado a su score.
            temp_pos = getInVector(p2_moves, x, y, z)
            p2_moves[temp_pos][3] += game_result
      # Al finalizar todo, aumento n  
      n += num_threads
  print("")
  # Terminan las maxIt simulaciones entonces tenemos que buscar el movimiento que nos dio mas victorias.
  return getBestPlay(p2_moves)


# --------------------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN PROGRAM -------------------------------------------------
# --------------------------------------------------------------------------------------------------------

# Variables para el AI
AIMove = []

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
    AIMove = AISim(board, x, y, z, 6000)
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
