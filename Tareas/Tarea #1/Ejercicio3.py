import random
import time

# Function to test generator #1
def generador1(seed):
    return ((5**5)*seed)%((2**35)-1)
    
# Function to test generator #2
def generador2(seed):
    return ((7**5)*seed)%((2**31)-1)

# Function to test generator #3
def generador3():
    return random.random()

# Function to make histograms     
def histograma(lst, iterations, number):
    print " Histograma para el generador #", number
    print "  Con: "+str(iterations)+" iteraciones"
    print ""
    for i in range(1,11):
        print str((i)/10.0) +':' + ('*'*((lst[i-1]*100)/iterations)) + '    (' + str(lst[i-1]) + ', ' + str((lst[i-1]*100)/float(iterations)) + "%)"
    print "------------------------------------------------------------"
        
# First we're gonna generate our lists
lstGen1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lstGen2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lstGen3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# GENERADOR #1
# This variable will carry the random number generated
randValue = [generador1(time.clock()) ]
maxValue = 0
iterations = input('Ingrese la cantidad de iteraciones que desea realizar: \n')

# Loops to fill the lists
for i in range(1, iterations):
    # cal our respective genereting function
    randValue.append( generador1(randValue[i-1]) ) # We give a random seed and fill the list
    
for i in range(0, len(randValue)-1):
    randValue[i] /= ((2**35)-2)
    
for i in range(1, iterations):
    if (randValue[i-1] >= 0) & (randValue[i-1] < 0.1):       # for 0.0 to 0.1
        lstGen1[0] += 1
    elif (randValue[i-1] >= 0.1) & (randValue[i-1] < 0.2):   # for 0.1 to 0.2
        lstGen1[1] += 1
    elif (randValue[i-1] >= 0.2) & (randValue[i-1] < 0.3):   # for 0.2 to 0.3
        lstGen1[2] += 1
    elif (randValue[i-1] >= 0.3) & (randValue[i-1] < 0.4):   # for 0.3 to 0.4
        lstGen1[3] += 1
    elif (randValue[i-1] >= 0.4) & (randValue[i-1] < 0.5):   # for 0.4 to 0.5
        lstGen1[4] += 1
    elif (randValue[i-1] >= 0.5) & (randValue[i-1] < 0.6):   # for 0.5 to 0.6
        lstGen1[5] += 1
    elif (randValue[i-1] >= 0.6) & (randValue[i-1] < 0.7):   # for 0.2 to 0.3
        lstGen1[6] += 1
    elif (randValue[i-1] >= 0.7) & (randValue[i-1] < 0.8):   # for 0.2 to 0.3
        lstGen1[7] += 1
    elif (randValue[i-1] >= 0.8) & (randValue[i-1] < 0.9):   # for 0.2 to 0.3
        lstGen1[8] += 1
    else:
        lstGen1[9] += 1
        
# GENERADOR #2
# This variable will carry the random number generated
randValue = [generador2(time.clock()) ]
maxValue = 0

# Loops to fill the lists
for i in range(1, iterations):
    # cal our respective genereting function
    randValue.append( generador2(randValue[i-1]) ) # We give a random seed and fill the list
    
for i in range(0, len(randValue)-1):
    randValue[i] /= ((2**31)-2)

for i in range(1, iterations):
    if (randValue[i-1] >= 0) & (randValue[i-1] < 0.1):       # for 0.0 to 0.1
        lstGen2[0] += 1
    elif (randValue[i-1] >= 0.1) & (randValue[i-1] < 0.2):   # for 0.1 to 0.2
        lstGen2[1] += 1
    elif (randValue[i-1] >= 0.2) & (randValue[i-1] < 0.3):   # for 0.2 to 0.3
        lstGen2[2] += 1
    elif (randValue[i-1] >= 0.3) & (randValue[i-1] < 0.4):   # for 0.3 to 0.4
        lstGen2[3] += 1
    elif (randValue[i-1] >= 0.4) & (randValue[i-1] < 0.5):   # for 0.4 to 0.5
        lstGen2[4] += 1
    elif (randValue[i-1] >= 0.5) & (randValue[i-1] < 0.6):   # for 0.5 to 0.6
        lstGen2[5] += 1
    elif (randValue[i-1] >= 0.6) & (randValue[i-1] < 0.7):   # for 0.2 to 0.3
        lstGen2[6] += 1
    elif (randValue[i-1] >= 0.7) & (randValue[i-1] < 0.8):   # for 0.2 to 0.3
        lstGen2[7] += 1
    elif (randValue[i-1] >= 0.8) & (randValue[i-1] < 0.9):   # for 0.2 to 0.3
        lstGen2[8] += 1
    else:
        lstGen2[9] += 1

# GENERADOR #3
# This variable will carry the random number generated
randValue = []
maxValue = 0

# Loops to fill the lists
for i in range(1, iterations):
    # cal our respective genereting function
    randValue.append( generador3() ) # We give a random seed and fill the list
    
for i in range(1, iterations):
    if (randValue[i-1] >= 0) & (randValue[i-1] < 0.1):       # for 0.0 to 0.1
        lstGen3[0] += 1
    elif (randValue[i-1] >= 0.1) & (randValue[i-1] < 0.2):   # for 0.1 to 0.2
        lstGen3[1] += 1
    elif (randValue[i-1] >= 0.2) & (randValue[i-1] < 0.3):   # for 0.2 to 0.3
        lstGen3[2] += 1
    elif (randValue[i-1] >= 0.3) & (randValue[i-1] < 0.4):   # for 0.3 to 0.4
        lstGen3[3] += 1
    elif (randValue[i-1] >= 0.4) & (randValue[i-1] < 0.5):   # for 0.4 to 0.5
        lstGen3[4] += 1
    elif (randValue[i-1] >= 0.5) & (randValue[i-1] < 0.6):   # for 0.5 to 0.6
        lstGen3[5] += 1
    elif (randValue[i-1] >= 0.6) & (randValue[i-1] < 0.7):   # for 0.2 to 0.3
        lstGen3[6] += 1
    elif (randValue[i-1] >= 0.7) & (randValue[i-1] < 0.8):   # for 0.2 to 0.3
        lstGen3[7] += 1
    elif (randValue[i-1] >= 0.8) & (randValue[i-1] < 0.9):   # for 0.2 to 0.3
        lstGen3[8] += 1
    else:
        lstGen3[9] += 1


# Graph all functions in order
# Graph 1, gen 1
histograma(lstGen1, iterations, 1)
# Graph 2, gen 2
histograma(lstGen2, iterations, 2)
# Graph 3, gen 3
histograma(lstGen3, iterations, 3)