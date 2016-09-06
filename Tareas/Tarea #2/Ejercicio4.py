# Autor: Alejandro Cortes
# Descripsion: 
#   Este programa simula una venta 
#   de periodicos, para ayudar a un
#   vocero.

import random

# Variables importantes
ventas = 0
saldoFinal = 0
numPeriodicos = input("Cuantos periodicos desea comprar al dia?\n -> ")

# Se calcula el dinero que se ha gastado...
saldo = numPeriodicos * -1.50
print "Usted tiene un saldo de: \n -> " + str(saldo) + " al inicio del dia."

print "\nPara la simulacion es necesario que ingrese el tiempo que desea simular."
dia = input("- Ingrese los dias:\n --> ")
mes = input("- Ingrese los meses:\n --> ")
year = input("- Ingrese los anios:\n --> ")

# Calculamos el tiempo maximo en dias...
time = dia + (mes * 30.4375) + (year * 12 * 30.4375)

for i in range(1, int(round(time,0))):
    r = random.random()
    if (r < 0.30):      # Se venden 9 el 30% de los dias.
        ventas = 9
    elif ( r < 0.70):   # Se venden 10 el 40% de los dias.
        ventas = 10
    else:               # Se venden 11 el 30% de los dias.
        ventas = 11
    # Se calcula el saldo final...
    if (ventas > numPeriodicos):
        ventas = numPeriodicos
    
    saldoFinal += (ventas * 2.50) + ((numPeriodicos-ventas) * 0.50) + saldo

# Generamos el reporte... 
print "\n    __ Reporte de ventas: __"
print " Se simularon " + str(time) + " dias de ventas."
print " Su saldo final luego de la simulacion es de:\n  -> $" + str(saldoFinal)