import math
import random

# Funcion para simular tiempos de entrada tipo Poisson homogeneo.
def solicitudesP(lamda):
    return - ((1 / (lamda * 1.0)) * math.log(random.random()))

# Funcion para simular una variable de tipo exponencial.
def expV(lamda):
    return - float((1 / (lamda * 1.0)) * math.log(random.random()))

# Creamos unos contenedores para almacenar datos para imprimir al final...
ArriveTimes = []
exitTimes = []
servicesTime = []

# Imprimir cosas para el usuario...
num = input("Ingrese la cantidad de servidores:\n -> ")

# Inicializamos unas variables utiles...
t_0 = 0                         # Tiempo sub 0
Na = Nd = tp = n = 0            # Variables en 0.
ta = expV(10)                   # 2400 solicitudes por minuto = 40 por segundo.
td = [float("inf")] * num       # Vector de tiempo de salida
procesVector = [0] * num        # Vector procesos servidores
procesTimeVector = [0] * num    # Tiempo en cada servidor.
requestVector = [0]*(1+num)     # Vector de Solicitudes
serversInUse = -1
minimo = -1
    
while (t_0 < 3600) or (requestVector[0] > 0):
    m = min(td)
    minimo = td.index(m)
    
    if (ta < td[minimo]) and (ta < 3600):   # Aun hay un servidor libre...
        t_0 = ta
        Na += 10
        ta += expV(6)      # Nuevo tiempo de llegada. 
        ArriveTimes.append(t_0)
            
        if requestVector[0] == 0:              # Caso 1
            servicesTime.append(t_0)             
            requestVector[0] += 1
            requestVector[1] = Na
            td[0] = t_0 + expV(10)
            
        elif requestVector[0] < num:            # Caso 2
            notBusy = requestVector.index(0) - 1
            servicesTime.append(t_0)
            requestVector[0] += 1
            requestVector[notBusy+1] = Na
            td[notBusy] = t_0 + expV(10)
        
        else:                       # Caso 3
            requestVector[0] += 1
        
    else:                               # Salida o cierre
        t_0 = td[minimo]                # tiempo actual es el minimo tiempo de salida
        procesTimeVector[minimo] = abs(t_0 - 3600)  # Veo cuanto tiempo estuvo ocupado ese servidor.
        procesVector[minimo] += 10      # se agrega el proceso al contador de procs. del servidor
        exitTimes.append(t_0)           # se agrega el tiempo actual a las salidas
        
        if requestVector[0] <= num:     # Caso 1
            requestVector[0] -= 10
            td[minimo] = float("inf")
            requestVector[minimo + 1] = 0
        
        else:                           # Caso 2
            requestVector[0] *= -1
            siguiente = max(requestVector)+1
            requestVector[0] *= -1
            servicesTime.append(t_0)                
            requestVector[0] -= 1
            td[minimo] = t_0 + expV(10)
            requestVector[minimo + 1] = siguiente
        
print "Servidores: "
for i in range (len(procesVector)):
    print "-> "+str(i+1)+": \nSolicitudes:\t", procesVector[i], "solicitudes.\nTiempo libre:\t", abs(procesTimeVector[i] - 3600), "segundos.\nTiempo ocupado:\t", procesTimeVector[i], "segundos."
    if (procesVector[i] > 0 ):
        serversInUse += 1
print ""
print "Solicitudes atendidas: ", Na
tiempoTotal = 0
for k in range(len(ArriveTimes)):
    resta=servicesTime[k] - ArriveTimes[k]
    tiempoTotal += resta
tiempoTotal /= (len(ArriveTimes) * 1.0)
print "Ultima llegada:", ArriveTimes[serversInUse], "s."
print "Ultima salida:", exitTimes[serversInUse], "s."
print "Promedio de tiempo en cola: ", tiempoTotal, "segundos."
