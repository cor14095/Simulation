# Autor: Alejandro Cortes
# Descripsion: 
#   Este programa simula una distribusion.

import random

# Esta funcion devuelve la suma hasta el subindice 'fin'
def sumaDe(lista, fin):
    suma = 0
    i = 0
    for i in range(0, fin):
        suma += lista[i]
        
    return suma

# Function to make histograms     
def histograma(lst, iterations, n):
    print " Histograma"
    print "  Con: "+str(iterations)+" iteraciones"
    print ""
    for i in range(1,n+1):
        print str(i) +':' + ('*'*((lst[i-1]*100)/iterations)) + '    (' + str(lst[i-1]) + ', ' + str((lst[i-1]*100)/float(iterations)) + "%)"
    print "------------------------------------------------------------"

# Variables importantes
listaIntervalos = []
valoresIntervalos = []
intervalo = 0
flag = True
contIntervalos = 0

n = input("Ingrese su n:\n-> ")

# Pedimos los n valores para el intervalo
while (flag):
    intervalo = raw_input("Ingrese un intervalo o 'fin' si ya no desea ingresar intervalos:\n-> ")
    if (intervalo == "fin"):
        flag = False
    else:
        listaIntervalos.append(float(intervalo))

# Creamos una lista de tamano len(listaIntervalos)
for i in range(0, len(listaIntervalos)):
    valoresIntervalos.append(0)

# Verificamos que el intervalo sea correcto o no
if (( 1.0 - sum(listaIntervalos) ) > 0.00):
    print "Su intervalo es incorrecto."
    # La bandera en True indica un error
    flag = True
else:
    for i in range(1, n):
        # Generamos el valor aleatorio...
        r = random.random()
        # Ponemos en 0 el iterador k de intervalos en la lista...
        k = 1
        # Vemos los intervalos que ingreso el usuario
        while (k <= len(listaIntervalos)):
            # Vemos Si r es menor al intervalo
            if (r < sumaDe(listaIntervalos, k)):
                # Aumentamos el valor en 1
                valoresIntervalos[k-1] += 1
                # Salimos del while
                break;
            # FIN IF
            # Aumentamos k
            k += 1
        # FIN WHILE
    # FIN FOR
# Vemos si fue un intervalo valido para hace run histograma    
if (not(flag)):
    histograma(valoresIntervalos, n, len(valoresIntervalos))
# Sino, es un error.
else: 
    print "Error en sus datos, la suma es: " + str( sum( listaIntervalos ) )