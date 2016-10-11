# Autor: Alejandro Cortes
# Carne: 14095
# Mini proyecto #4
# Modelacion y simulacion.

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
num_threads = 50

# Funcion para juntar los outputs
# Credit: http://stackoverflow.com/a/22429572/4808919
def wrapper(func, qIn, qOut, state):
    arg = qIn.get()
    for i in arg:
        qOut.put(func(state, i[0], i[1], i[2]))

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
  sum_x         = state[0][y][z] + state[1][y][z] + state[2][y][z] + state[3][y][z]
  sum_y         = state[x][0][z] + state[x][1][z] + state[x][2][z] + state[x][3][z]
  sum_z         = state[x][y][0] + state[x][y][1] + state[x][y][2] + state[x][y][3]
  
  diag_izq_x    = state[x][0][0] + state[x][1][1] + state[x][2][2] + state[x][3][3]
  diag_der_x    = state[x][3][0] + state[x][2][1] + state[x][1][2] + state[x][0][3]
  diag_izq_y    = state[0][y][0] + state[1][y][1] + state[2][y][2] + state[3][y][3]
  diag_der_y    = state[3][y][0] + state[2][y][1] + state[1][y][2] + state[0][y][3]
  diag_izq_z    = state[0][0][z] + state[1][1][z] + state[2][2][z] + state[3][3][z]
  diag_der_z    = state[3][0][z] + state[2][1][z] + state[1][2][z] + state[0][3][z]
  
  diag_izq      = state[0][0][0] + state[1][1][1] + state[2][2][2] + state[3][3][3]
  diag_der      = state[3][0][0] + state[2][1][1] + state[1][2][2] + state[0][3][3]

  # Ahora tengo que ver cual es mas probable para ganar
#  posibles = [sum_x, sum_y, sum_z, diag_izq_x, diag_der_x, diag_izq_y, diag_der_y, diag_izq_z, diag_der_z, diag_izq, diag_der]
#  print(posibles, x, y, z, state[x][y][z])
  indice = max(abs(sum_x), abs(sum_y), abs(sum_z), 
               abs(diag_izq_x), abs(diag_der_x), 
                abs(diag_izq_y), abs(diag_der_y), 
                abs(diag_izq_z), abs(diag_der_z), 
                abs(diag_izq), abs(diag_der))
  
  return indice
    
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
    
    while (win_state < 4):            # While 1
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
      
      # Necesitamos almacenar el primer movimiento
      if (moves == 0):
        first_move = [x, y, z]
      # END if
      
      # Luego ponemos el token necesario.
      new_state[x][y][z] = (1 if player_turn else -1)
      player_turn =  not player_turn
      moves += 1
      
      # Actualizamos win_state
      win_state = abs(isPlayerWining(new_state, x, y, z))
      
    # END while 1
    return_values = first_move
    # Si se llega a una victoria o un empate
    if (not player_turn):
        # Si gana el jugador 1.
        return_values.append(-1)
    elif (player_turn):
        # Gano la maquina.
        return_values.append(2)
    else:
        # Nadie gano.
        return_values.append(4)
    
    # Retornamos un vector con los valores importantes
    return return_values
    # Retorna: [x, y, z, (w/l/t)]

# Esta funcion simula el turno del jugador 2
def AISim(state, x, y, z, maxIt):
  # Variables utiles
  p2_moves = []                 # Un vector para saber que jugadas me causaron mayor cantidad de visctorias
  temp_state = deepcopy(state)  # un estado temporal
  temp_result = []              # Un Array para el rusltado temporal.
  moves = []                    # Array para almacenar los inputs que se van a dar.
  threads = []                  # Array para manejar todos mis threads
  game_result = 0               # Un temporal para recibir el resultado del juego
  temp_pos = 0                  # Un temporal para la posicion de la jugada
  qIn, qOut = Queue(), Queue()  # Uso colas porque se pueden mover entre Threads
  
  # Divido la cantidad de iteraciones que quiero hacer en la cantidad de threads que tengo...
  t = int(round(maxIt/num_threads))     # Cuantas simulaciones tiene que hacer cada thread
  for _ in range(t):
      moves.append([x, y, z])
  
#  start = time.time()
  for i in xrange(num_threads):
      # Genero los elementos que estaran en el input.
      qIn.put(moves)
      # Creo mis threads
      threads.append(Thread(target=wrapper, args=(simGame, qIn, qOut, temp_state)))
#  for i in xrange(num_threads):
      # Luego los ejecuto 1 a 1
      threads[i].start()
      # Esperamos que cada thread se una al principal
      threads[i].join()
#      stop1 = time.time()
#      print ("Thread numero:", i + 1, "con tiempo: %0.4f" % (stop1 - start) ) 
#  for t in xrange(num_threads):
#      # Unimos todos los threads...    
#      print ("Thread  #", t + 1)
#      threads[num_threads - t - 1].join()
#      print (time.time() - start)
#  # Luego espero a que el ultimo termine.
#  threads[num_threads - 1].join()
#  stop2 = time.time()
#  print (stop2 - start, qOut.qsize())

  # Proceso los resultados.
  while ( qOut.qsize() > 0 ):
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
      
#  end = time.time()
#  print ("Processing time: %0.4f seconds" % (end - start))
      # Al finalizar todo, aumento n  
#  print("")
  # Terminan las maxIt simulaciones entonces tenemos que buscar el movimiento que nos dio mas victorias.
  return getBestPlay(p2_moves)

def AIgame(state, x, y, z, maxIt):
    move = []
    start = time.time()
    move =  AISim(state, x, y, z, maxIt)    
    end = time.time()
    print ("Thinking time: %0.4f seconds" % (end - start))
    
    return move
    
def playPvP(state):
    # Variables utiles    
    match_state = deepcopy(state)
    x = 0
    y = 0
    z = 0
    player_turn = True      # True = p1, False = p2
    
    while (not(abs(isPlayerWining(match_state, x, y, z)) == 4)):
        
        # Print 
        print ("Player %s turn:" % (1 if player_turn else 2))
        x = int(raw_input("x: "))
        y = int(raw_input("y: "))
        z = int(raw_input("z: "))
        
        if match_state[x][y][z] == draw_token:
            match_state[x][y][z] = 1 if player_turn else -1
            player_turn = not player_turn
        else:
            print ("")
            print ("ERROR: occupied position, please retry in a new position")
            print ("")
            
        # Print board state
        print ("")
        print ("Board:")
        print (draw_board(match_state))
        print ("")
        
    print ("Player %s is the winner!" % (1 if not player_turn else 2))
    
def playPvE(state):
    # Variables utiles    
    match_state = deepcopy(state)
    x = 0
    y = 0
    z = 0
    player_turn = True      # True = p1, False = p2
    AIMove = []
    
    while (not(abs(isPlayerWining(match_state, x, y, z)) == 4)):
        
        # Print 
        print ("Player %s turn:" % (1 if player_turn else 2))
        
        if (player_turn):
            # Turno del jugador
            x = int(raw_input("x: "))
            y = int(raw_input("y: "))
            z = int(raw_input("z: "))
        else:
            # Turno de la maquina
            AIMove = AIgame(match_state, x, y ,z, 20000)
            x = AIMove[0]
            y = AIMove[1]
            z = AIMove[2]
            print ("x:",x)
            print ("y:",y)
            print ("z:",z)
            
        if match_state[x][y][z] == draw_token:
            match_state[x][y][z] = 1 if player_turn else -1
            player_turn = not player_turn
        else:
            print ("")
            print ("ERROR: occupied position, please retry in a new position")
            print ("")
            
        # Print board state
        print ("")
        print ("Board:")
        print (draw_board(match_state))
        print ("")
        
            
    print ("Player %s is the winner!" % (1 if not player_turn else 2))
    
def playEvE(state):
    # Variables utiles    
    match_state = deepcopy(state)
    x = random.randint(0, 3)    # El primer movimiento es random
    y = random.randint(0, 3)    # El primer movimiento es random
    z = random.randint(0, 3)    # El primer movimiento es random
    player_turn = True      # True = p1, False = p2
    AIMove = []
    
    while (not(abs(isPlayerWining(match_state, x, y, z)) == 4)):
        
        # Print 
        print ("Player %s turn:" % (1 if player_turn else 2))
        
        # Turno de la maquina
        AIMove = AIgame(match_state, x, y ,z, 20000)
        
        x = AIMove[0]
        y = AIMove[1]
        z = AIMove[2]
        
        print ("x:",x)
        print ("y:",y)
        print ("z:",z)
        
        if match_state[x][y][z] == draw_token:
            match_state[x][y][z] = 1 if player_turn else -1
            player_turn = not player_turn
        else:
            print ("")
            print ("ERROR: occupied position, please retry in a new position")
            print ("")
            
        # Print board state
        print ("")
        print ("Board:")
        print (draw_board(match_state))
        print ("")
        
    print ("Player %s is the winner!" % (1 if not player_turn else 2))
# --------------------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN PROGRAM -------------------------------------------------
# --------------------------------------------------------------------------------------------------------

while True:
    # Imprimimos un menu simple
    print ( "Hola! Que modalidad de juego desea?\n1) Jugador vrs Jugador\n2) Jugador vrs AI\n3) AI vrs AI\n4) Salir" )
    game_type = int(raw_input("Seleccion: "))
    
    if (game_type == 1):
        # Se desea jugar una partida de jugador vrs jugador
        playPvP(board)
    elif (game_type == 2):
        # Se desea jugar Jugador vrs AI
        playPvE(board)
    elif (game_type == 3):
        playEvE(board)
    elif (game_type == 4):
        print ("Gracias por jugar!")
        break
    else:
        print ("Comando incorrecto!")
