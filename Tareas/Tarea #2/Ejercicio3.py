# Autor: Alejandro Cortes
# Descripsion: 
#   Este programa simula una inversion,
#   entre 2 proyectos.

import random

# Variables importantes
flujoDeCaja = 0
listaCajasHotel = []
listaCajasCC = []
years = 0
reporteHotel = 0
reporteCC = 0

n = input("Ingrese la cantidad de iteraciones que desea realizar:\n -> ")

print "Calculos hotel..."

for i in range(1, n):
    # Reiniciamos los anios...
    years = 0
    # Iteramos...
    while (years < 8):
		if (years==0):
			flujoDeCaja += -800
		elif (years==1):
			flujoDeCaja += (random.normalvariate(-800, 50) / (1 + 0.1)**years)
		elif (years==2):
			flujoDeCaja += (random.normalvariate(-800, 100) / (1 + 0.1)**years)
		elif (years==3):
			flujoDeCaja += (random.normalvariate(-700, 150) / (1 + 0.1)**years)
		elif (years==4):
			flujoDeCaja += (random.normalvariate(300, 200) / (1 + 0.1)**years)
		elif (years==5):
			flujoDeCaja += (random.normalvariate(400, 200) / (1 + 0.1)**years)
		elif (years==6):
			flujoDeCaja += (random.normalvariate(500, 200) / (1 + 0.1)**years)
		elif (years==7):
			flujoDeCaja += (random.uniform(200, 8440) / (1 + 0.1)**years)
			listaCajasHotel.append(flujoDeCaja)
			flujoDeCaja=0
		years+=1
		
print "Calculos centro comercial...\n\n"

for i in range(1, n):
    # Reiniciamos los anios...
    years = 0
    # Iteramos...
    while (years < 8):
		if (years==0):
			flujoDeCaja += -900
		elif (years==1):
			flujoDeCaja += (random.normalvariate(-600, 50) / (1 + 0.1)**years)
		elif (years==2):
			flujoDeCaja += (random.normalvariate(-200, 50) / (1 + 0.1)**years)
		elif (years==3):
			flujoDeCaja += (random.normalvariate(-600, 100) / (1 + 0.1)**years)
		elif (years==4):
			flujoDeCaja += (random.normalvariate(250, 150) / (1 + 0.1)**years)
		elif (years==5):
			flujoDeCaja += (random.normalvariate(350, 150) / (1 + 0.1)**years)
		elif (years==6):
			flujoDeCaja += (random.normalvariate(400, 150) / (1 + 0.1)**years)
		elif (years==7):
			flujoDeCaja += (random.uniform(1600, 6000) / (1 + 0.1)**years)
			listaCajasCC.append(flujoDeCaja)
			flujoDeCaja=0
		years+=1

# Ahora generamos el reporte de trabajo.
for i in range(1, n):
	reporteHotel += listaCajasHotel[i-1]
	reporteCC    += listaCajasCC[i-1]

reporteHotel /= (n)
reporteCC /= (n)

print "    __ Reporte de simulacion __ "
print " Para: " + str(n) + " iteraciones."
print " Resultados:"
print "  -> Hotel: "+str(reporteHotel)
print "  -> CC: "+str(reporteCC)
