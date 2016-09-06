import random
import math

# Function to evaluate g(x)
def funcG(x):
    return math.exp(-(x**2))
    
# Function to evaluate h(y)
def funcH(y):
    return funcG((1/y) - 1) / (y**2)
    
# Initialize values
iterations = input("Ingrese la cantidad de iteraciones: \n")
theta = 0

# Main loop to 
for i in range(1, iterations):
    theta += (funcH(random.random())) / iterations
    
# Since we know the integral was simetric.
theta *= 2
    
# Print results...
print "Resultados: "
print "- Theta real: 1.77245385090551602"
print "- Theta calculado: ", theta
print "- Error: ", (abs(1.77245385090551602 - theta) / 1.77245385090551602)