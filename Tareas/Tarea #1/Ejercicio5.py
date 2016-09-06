import random
import math

# Function to evaluate g(x)
def funcH(x, y):
    return ( ((1/x)-1) * math.exp( -(((1/x)-1) * y) - ((1/x)-1) ) ) / (x**2)
    
# Initialize values
iterations = input("Ingrese la cantidad de iteraciones: \n")
theta = 0

# Main loop to 
for i in range(1, iterations):
    theta += funcH(random.random(), random.random()) / iterations
    
# Print results...
print "Resultados: "
print "- Theta real: 0.5"
print "- Theta calculado: ", theta
print "- Error: ", (abs(0.5 - theta) / 0.5)