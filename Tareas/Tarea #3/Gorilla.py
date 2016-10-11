import math
import random
import time

# Funcion para calcular 
def T(s, lamda):
    return s - ((1/(lamda * 1.0)) * math.log(random.random()))

# Funcion para calcular el tiempo de atencion
def generarY(lamda):
    return -((1/(lamda * 1.0)) * math.log(1 - random.random()))

# Tiempo t.
t = 0
# Numero de llegadas al tiempo t
Na = 0
# Numero de salidas al tiempo t
Nd = 0
# Numero de solicitudes en el sistema al tiempo t
n = 0
# Tiempo extra en el servidor.
tp = 0
# Tiempo en que llega la solicitud
ta = T(0, 40)
# Tiempo en el que sale la solicitud
td = float("inf")
# Tiempo de llegada de la i-esima solicitud
A = []
# Tiempo de salida de la i-esima solicitud
D = []
# Tiempo de cada solicitud en cola
C = []
# Numero de solicitudes atendidas.
numReq = 0
# Tiempo ocupado
tOn = 0
# Tiempo desocupado
tOff = 0
# Tiempo maximo en segundos.
t_max = 3600    # Una hora.
# Lambda
lamda = 40.0;

while (t <= t_max):
    # Caso 1: El siguiente evento es una llegada 
    # de una solicitud al sistema, y aun no es la 
    # hora de cierre.
    if ( (ta <= td) and (ta <= T)):
        t = ta
        A.append(ta)
        Na += 1
        numReq += 1
        ta = T(t, lamda)
        n += 1
        if (n == 1):
            # Medimos el tiempo en que el servidor no hace nada.
            if (len(D) == 0):
                tOff += A[len(A) - 1]
            else:
                tOff += A[len(A) - 1] - D[len(D) - 1]
            td = t + generarY(lamda)
    # Caso 2: El siguiente evento es una salida de 
    # una solicitud del sistema, y aun no es la 
    # hora de cierre.
    elif ( (td < ta) and (td <= T)):
        t = td
        n -= 1
        Nd += 1
        if (n == 0):
            td = float("inf")
        else:
            td = t + generarY(lamda)
        D.append(t)
    # Caso 3: El proximo evento ocurre luego de la 
    # hora de cierre, y aun hay solicitudes en el sistema.
    elif ( (min(ta,td) > T) and (n > 0)):
        t = td
        n -= 1
        Nd += 1
        if (n > 0):
            td = t + generarY(lamda)
        D.append(t)
    # Caso 4: El proximo evento ocurre luego de la 
    # hora de cierre, y ya no hay solicitudes en cola.
    else:
        tp = max(t - T, 0)
        
tOn = t - tOff

print "Tiempo total: ", t
print "Solicitudes atendidas: ", numReq
print "Tiempo de uso: ", tOn
print "Tiempo sin uso: ", tOff
