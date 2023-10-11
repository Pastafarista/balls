import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import multiprocessing as mpp
from multiprocessing import Pool
import tqdm
import gc

def f(x):
     return x**4 - 3*x**2 
 
def derivada(x):
     return 4*x**3 - 6*x

def color(numero):
     if numero >= 0 and numero < 40:
          return (0,255,0)
     elif numero >= 40 and numero < 81:
          return (0,0,255)
     elif numero >= 81 :
          return (255,0,0)
     else:
          print(numero)
 
# Constantes
funcion = [1, 0, -3, 0, 0]
G = 9.81

# Configuracion
MIN_X = -1.95
MAX_X = 1.95

MIN_Y = -2.5
MAX_Y = 4

LARGO_PANTALLA = 1000
ALTO_PANTALLA = 2000

X = np.linspace(MIN_X, MAX_X, LARGO_PANTALLA)
Y = np.linspace(MIN_Y, MAX_Y, ALTO_PANTALLA)

def numero_botes(x_0, y_0):

     x = x_0
     y = y_0

     # Calculamos la primera intersección con la curva (intersección con una recta vertical)
     y_i = f(x_0)
     
     # Calculamos la distancia que ha caido la pelota
     distancia_caida = y_0 - y_i
     
     # Si no está por encima de la curva no hay botes
     if(y_0 < y_i):
          return 0
     
     # Calculamos la velocidad inicial de la pelota
     v = np.sqrt(2*G*distancia_caida) 
     
     y = y_i

     numero_botes = 0
     
     derecha = True
     
     if(x_0 < 0):
          derecha = False
     else:
          derecha = True

     while( ((x < 0 and derecha == False) or (x > 0 and derecha == True)) and numero_botes < 1000):
          m = -derivada(x)
          c = G*(m**2 + 1) / (2*v**2)

          trayectoria = [0, 0, -c, m + 2*x*c, -m*x -c*x**2 + y]

          resta = np.subtract(trayectoria, funcion)

          r = np.roots(resta)
          r = r[np.isreal(r)].real # Seleccionar solo las raices reales
          
          # Seleccionar la raiz correcta (puede haber muchas intersecciones en la parábola pero solo una es correcta)
          mayor = 0
          menor = 0
          
          if m > 0:
               menor = 9000
               
               for raiz in r: 
                    raiz_final = round(raiz, 7)
                    if(raiz_final != round(x,7)):
                         if(raiz_final < menor):
                              menor = round(raiz, 7)
               x_i = menor
          else:
               mayor = -9000
               
               for raiz in r: 
                    raiz_final = round(raiz, 7)
                    if(raiz_final != round(x,7)):
                         if(raiz_final > mayor):
                              mayor = round(raiz, 7)
               x_i = mayor
                    
          y_i = f(x_i)
          
          # Actualizar la velocidad
          distancia_caida = y - y_i
          
          if(distancia_caida < 0):
               distancia_caida = -distancia_caida
               velocidad_ganada = -np.sqrt(2*G*distancia_caida)
          else:
               velocidad_ganada = np.sqrt(2*G*distancia_caida)
          
          # Actualizar parámetros
          v += velocidad_ganada
          
          x = x_i
          y = y_i
          
          numero_botes += 1
          
     # limpiar memoria
     try:
          del trayectoria, resta, r, x_i, y_i, x_0, y_0, x, y, v, distancia_caida, velocidad_ganada, m, c, mayor, menor, raiz_final
     except:
          pass     
     
     return numero_botes

#Generar el colormap de colores
colores = []

STEP = 32

for r in range(0, 256, STEP):
     for g in range(0, 256, STEP):
          for b in range(0, 256, STEP):
               colores.append((r,g,b))
                        
# Funcion que mapea un numero a un color rgb  
def map_to_color(numero):
     if( numero == 0):
          return (255, 255, 255)
     if(numero > len(colores)):
          return (0,0,0)
     else:
          return colores[numero]


def procesar(pos):
     # limpiar memoria cada 100 iteraciones
     if(pos[0] % 100 == 0 and pos[1] % 100 == 0):
          gc.collect()
     
     n_botes = numero_botes(X[pos[0]], Y[pos[1]])
     return map_to_color(n_botes)

if __name__ == '__main__':
     
     pixeles = np.zeros((ALTO_PANTALLA, LARGO_PANTALLA, 3), dtype=np.uint8)
     
     fila = 0
     columna = 0
     
     
     iterable =  [(x,y) for y in range(ALTO_PANTALLA - 1, -1, -1) for x in range(0, LARGO_PANTALLA, 1)]
     
     with Pool(mpp.cpu_count() - 1) as pool:
          for pixel in tqdm.tqdm(pool.imap(procesar, iterable),
                           total=len(iterable)):
               
               pixeles[fila][columna] = pixel
            
               columna += 1
               if columna == LARGO_PANTALLA:
                    columna = 0
                    fila += 1
          
          pool.close()
          pool.join()
     
     new_image = Image.fromarray(pixeles)
     new_image.save('fractal.png')
     