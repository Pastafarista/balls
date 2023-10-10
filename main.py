import numpy as np
from matplotlib import pyplot as plt

def f(x):
     return x**4 - 3*x**2 
 
def derivada(x):
     return 4*x**3 - 6*x
 
def PolyCoefficients(x, coeffs):
    """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

    The coefficients must be in ascending order (``x**0`` to ``x**o``).
    """
    o = len(coeffs)
    print(f'# This is a polynomial of order {o}.')
    y = 0
    for i in range(o):
        y += coeffs[i]*x**i
    return y
 
def poly_plot(polinomio, x):
     y = [np.polyval(polinomio, i) for i in x]
     plt.plot(x,y)
 
# Constantes
funcion = [1, 0, -3, 0, 0]

# Configuracion de la grafica
plt.xlim(xmax=2, xmin=-2)
plt.ylim(ymin=-3, ymax=5)

x_0 = 1.5
y_0 = 1

distancia_caida = y_0 - f(x_0)

G = 9.81

v = np.sqrt(2*G*distancia_caida)
inter = [x_0, f(x_0)]
x = np.linspace(-2, 2, 100)

plt.plot(x_0, y_0, 'ro')
plt.plot(x_0, f(x_0), 'ro')

y_0 = f(x_0)

for i in range(1):
     m = -derivada(x_0)
     print(G)
     c = G*(m**2 + 1) / (2*v**2)

     trayectoria = [0, 0, -c, m + 2*x_0*c, -m*x_0 -c*x_0**2 + y_0]

     resta = np.subtract(trayectoria, funcion)

     print(v)

     r = np.roots(resta)

     r = r[np.isreal(r)].real
     
     # Seleccionar la raiz correcta
     for raiz in r: 
          raiz_final = round(raiz, 7)
          
          if(raiz_final != round(x_0,7)):
               if(m > 0):
                    if(raiz > x_0):
                         x_i = raiz_final
               else:
                    if(raiz < x_0):
                         x_i = raiz_final

     y_i = f(x_i)
     
     # Actualizar la velocidad
     distancia_caida = y_0 - y_i
     
     if(distancia_caida < 0):
          distancia_caida = -distancia_caida
          velocidad_ganada = -np.sqrt(2*G*distancia_caida)
     else:
          velocidad_ganada = np.sqrt(2*G*distancia_caida)
     
     # Actualizar parámetros
     v += velocidad_ganada
     
     print("Velocidad: " + str(v))
     
     x_0 = x_i
     y_0 = y_i

     poly_plot(trayectoria, x)
     print(v)
     
     plt.plot(x_i, y_i, 'ro')
     plt.plot(inter[0], inter[1], 'ro')

poly_plot(funcion, x)
plt.show()