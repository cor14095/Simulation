import random

g1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14, 30, 31, 32]
g2 = [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29, 33, 34, 35]
parejas = []

i = 0
# len = lenght = largo()
while (i < len(g1)):
    r = random.randint(0,len(g1))
    if (g2[r] != -1):
        parejas.append("("+str(g1[i])+", "+str(g2[r])+")")
        g2[r] = -1
        i += 1
    
print parejas