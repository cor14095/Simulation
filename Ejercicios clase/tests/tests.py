import random
import numpy as np

board = np.array([
  [
    [10, 0, 0, 0],
    [0, 20, 0, 0],
    [0, 0, 30, 0],
    [0, 0, 0, 40]
  ],
  [
    [11, 0, 0, 0],
    [0, 21, 0, 0],
    [0, 0, 31, 0],
    [0, 0, 0, 41]
  ],
  [
    [12, 0, 0, 0],
    [0, 22, 0, 0],
    [0, 0, 32, 0],
    [0, 0, 0, 42]
  ],
  [
    [13, 0, 0, 0],
    [0, 23, 0, 0],
    [0, 0, 33, 0],
    [0, 0, 0, 43]
  ]
])

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

for i in range(10):
    print random.randint(0, 3)
    
vector = []

for i in range(10):
    vector.append([random.randint(0, 4), random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)])

vector[2] = [1, 2, 3, 0]

if (isInVector(vector, 1, 2, 3)):
    print "EUREKAAA!"
else:
    print "You fail "
    
lista = zip(*np.where(board == 0))
r = random.randint(0, len(lista))

lista2 = lista[r]

print lista[r]
print lista2[0], lista2[1], lista2[2]