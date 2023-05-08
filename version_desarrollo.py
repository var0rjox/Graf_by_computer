import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import numpy as np

PIXEL_SIZE = 10

def flood_fill_puntos(canvas, x, y, color_reemplazo, color_borde1="#FCFDFF", color_borde2="black"):
    # Implementa el algoritmo de relleno por difusión (flood fill) para pintar un área delimitada por
    # un color de borde en un objeto canvas. La función toma como entrada un objeto canvas, las
    # coordenadas (x, y) del punto de inicio, el color de reemplazo para llenar el área y dos colores
    # de borde.

    # canvas: El objeto canvas en el que se realizará el relleno.
    # x: Coordenada x del punto de inicio.
    # y: Coordenada y del punto de inicio.
    # color_reemplazo: Color con el que se llenará el área.
    # color_borde1: Primer color de borde del área a rellenar.
    # color_borde2: Segundo color de borde del área a rellenar.

    color_inicial = canvas.obtener_color_pixel(x, y)
    if color_inicial == color_reemplazo:
        return

    visitados = set()
    pila = [(x, y)]

    while pila:
        x, y = pila.pop()

        if (x, y) in visitados:
            continue

        visitados.add((x, y))
        # Pinta el rectángulo actual
        canvas.create_rectangle(x-5, y-5, x+5, y+5, outline=color_reemplazo, fill=color_reemplazo)
        # Recorre los vecinos del punto actual
        for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5)]:
            nx, ny = x+dx, y+dy
            # Verifica si el vecino no es un borde y no ha sido visitado ni agregado a la pila
            if (nx, ny) not in visitados and canvas.obtener_color_pixel(nx, ny) not in [color_borde1, color_borde2]:
                pila.append((nx, ny))

    return

def bresenham(x1, y1, x2, y2, line_style='dashed'):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 10 if x1 < x2 else -10
    sy = 10 if y1 < y2 else -10
    err = dx - dy
    x, y = x1, y1
    puntos = []    
    current_length = 0
    current_color = "black"

    while True:
        color = current_color if line_style == 'dashed' else 'black'
        puntos.append((x, y, color))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        # Cambia el color para simular una línea discontinua
        if line_style == 'dashed':
            current_length += 1
            if current_length % 4 in (1, 2, 3):
                current_color = "black"
            else:
                current_color = "#FCFDFF"

    return puntos

def ecuacion_general(x1, y1, x2, y2, line_style='dashed'):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    puntos = []
    current_length = 0
    current_color = "black"

    m = (y2 - y1) / (x2 - x1) if x2 != x1 else None
    b = y1 - m * x1 if m is not None else None

    if dx > dy:
        x = x1
        while x != x2:
            y = round(m * x + b)
            color = current_color if line_style == 'dashed' else 'black'
            puntos.append((x, y, color))
            x += sx
            if line_style == 'dashed':
                current_length += 1
                if current_length % 4 in (1, 2, 3):
                    current_color = "black"
                else:
                    current_color = "#FCFDFF"
    else:
        y = y1
        while y != y2:
            x = round((y - b) / m) if m is not None else x1
            color = current_color if line_style == 'dashed' else 'black'
            puntos.append((x, y, color))
            y += sy
            if line_style == 'dashed':
                current_length += 1
                if current_length % 4 in (1, 2, 3):
                    current_color = "black"
                else:
                    current_color = "#FCFDFF"

    return puntos

def midpoint(x, y, radius):
    radius_in_pixels = math.ceil(radius / PIXEL_SIZE)
    x0 = x * PIXEL_SIZE
    y0 = y * PIXEL_SIZE
    x = 0
    y = radius_in_pixels
    d = 1 - radius_in_pixels
    points = []
    while x <= y:
        points.extend(_get_octant_points(x0, y0, x, y))
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    return points




def _get_octant_points(x0, y0, x, y):
    octant_points = [
        (x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE),
        (x0 + y * PIXEL_SIZE, y0 + x * PIXEL_SIZE),
        (x0 - y * PIXEL_SIZE, y0 + x * PIXEL_SIZE),
        (x0 - x * PIXEL_SIZE, y0 + y * PIXEL_SIZE),
        (x0 - x * PIXEL_SIZE, y0 - y * PIXEL_SIZE),
        (x0 - y * PIXEL_SIZE, y0 - x * PIXEL_SIZE),
        (x0 + y * PIXEL_SIZE, y0 - x * PIXEL_SIZE),
        (x0 + x * PIXEL_SIZE, y0 - y * PIXEL_SIZE),
    ]
    return octant_points

def triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def punto_medio(x0, y0, radio):
    radio_en_pixeles = math.ceil(radio / 10)
    x = 0
    y = radio_en_pixeles
    d = 1 - radio_en_pixeles
    puntos = []
    while x <= y:
        puntos.append((x0 + x * 10, y0 + y * 10))
        puntos.append((x0 + y * 10, y0 + x * 10))
        puntos.append((x0 - y * 10, y0 + x * 10))
        puntos.append((x0 - x * 10, y0 + y * 10))
        puntos.append((x0 - x * 10, y0 - y * 10))
        puntos.append((x0 - y * 10, y0 - x * 10))
        puntos.append((x0 + y * 10, y0 - x * 10))
        puntos.append((x0 + x * 10, y0 - y * 10))
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    return puntos
# def _get_octant_points(x0, y0, x, y):
#     return [
#         (x0 + x, y0 + y),
#         (x0 - x, y0 + y),
#         (x0 + x, y0 - y),
#         (x0 - x, y0 - y),
#         (x0 + y, y0 + x),
#         (x0 - y, y0 + x),
#         (x0 + y, y0 - x),
#         (x0 - y, y0 - x)
#     ]
    
# def interline_points(points, line_style='dashed'):
#     new_points = []
#     current_length = 0
#     current_color = "black"

#     for point in points:
#         if line_style == 'dashed':
#             current_length += 1
#             if current_length % 4 in (1, 2, 3):
#                 current_color = "black"
#             else:
#                 current_color = "#FCFDFF"
#         new_points.append((point[0], point[1], current_color))

#     return new_points

# def punto_medio(x, y, radius, line_style='dashed'):
#     radius_in_pixels = math.ceil(radius / PIXEL_SIZE)
#     x0 = x * PIXEL_SIZE
#     y0 = y * PIXEL_SIZE
#     x = 0
#     y = radius_in_pixels
#     d = 1 - radius_in_pixels
#     points = []

#     while x <= y:
#         octant_points = _get_octant_points(x0, y0, x, y)
#         points.extend(octant_points)
        
#         if d < 0:
#             d += 2 * x + 3
#         else:
#             d += 2 * (x - y) + 5
#             y -= 1
#         x += 1

#     interlined_points = interline_points(points, line_style)
#     return interlined_points  




class Figura:
    def __init__(self, x, y, color='White', grosor=2, tipo_linea='solid'):
        self.x = x
        self.y = y
        self.color = color
        self.grosor = grosor
        self.tipo_linea = tipo_linea
        self.escala = 1
        self.borde_seleccionado = False
        self.rotacion = 0

    def set_rotacion(self, angulo):
        #Establece la rotacion de la figura en grados
        self.rotacion = angulo % 360

    def escalar(self, factor):
        #Establece el factor de escala de la figura
        if factor>0 and factor < 2.5:
            self.escala = factor
        print("LA ESCALA ES DE", self.escala)

    def get_escala(self):
        #Devuelve el factor de escala de la figura
        return self.escala
    
    def get_border_thickness(self):
        # obtiene el grosor actual de los bordes de la figura
        return self.grosor
    
    def set_border_thickness(self , factor):
        self.grosor = factor
    
    def get_rotacion(self):
        return self.rotacion

    def rotar(self, rotacion):
        self.rotacion = rotacion

    def cambiar_color(self, color):
        self.color = color

    def trasladar(self, dx, dy):
        self.x += dx
        self.y += dy

    def imprimir_atributos(self):
        pass

    def colorear(self, canvas):
        pass

class Cuadrado(Figura):
    
    # Clase que representa un cuadrado en un espacio bidimensional. Hereda de la clase Figura.

    # :param color: Color del cuadrado.
    # :param grosor: Grosor del borde del cuadrado.
    # :param tipo_linea: Tipo de línea para el borde del cuadrado ('solid' u otros).
    
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, color='black', grosor=1, tipo_linea='solid'):
        super().__init__(x1, y1, color, grosor, tipo_linea)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.escala = 1
        self.rotacion = 0

    def colisiona_con_punto(self, x, y):
        # """
        # Determina si un punto dado (x, y) colisiona con la figura utilizando el algoritmo de ray casting.
        # Este algoritmo traza un rayo horizontal desde el punto (x, y) hacia la derecha y cuenta cuántas
        # veces cruza los bordes de la figura. Si el número de cruces es impar, el punto está dentro de la
        # figura, de lo contrario, está fuera.

        # :param x: Coordenada x del punto.
        # :param y: Coordenada y del punto.
        # :return: Verdadero (True) si el punto colisiona con la figura, Falso (False) en caso contrario.
        # """
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = self.coordenadas_escaladas()
        x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = self.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

        puntos = [(x1_rotado, y1_rotado), (x2_rotado, y2_rotado), (x3_rotado, y3_rotado), (x4_rotado, y4_rotado)]
        n_puntos = len(puntos)

        intersecciones = 0
        p1_x, p1_y = puntos[0]

        # Recorre los lados de la figura
        for i in range(1, n_puntos + 1):
            p2_x, p2_y = puntos[i % n_puntos]

            # Verifica si el punto está dentro de la región acotada por el par de puntos (lado) actual
            if y > min(p1_y, p2_y) and y <= max(p1_y, p2_y) and x <= max(p1_x, p2_x):
                if p1_y != p2_y:
                    x_intersect = (y - p1_y) * (p2_x - p1_x) / (p2_y - p1_y) + p1_x
                if p1_x == p2_x or x <= x_intersect:
                    intersecciones += 1

            p1_x, p1_y = p2_x, p2_y

        return intersecciones % 2 == 1
    
    def coordenadas_escaladas(self):
        # Identifica el punto superior izquierdo 
        puntos = np.array([[self.x1, self.y1], 
                           [self.x2, self.y2], 
                           [self.x3, self.y3], 
                           [self.x4, self.y4]])
        punto_superior_izquierdo = np.argmin(puntos, axis=0)[0]

        # Calcula la matriz de escalado
        escala_matriz = np.array([[self.escala, 0], 
                                  [0, self.escala]])

        # Resta el punto superior izquierdo
        puntos_escalados = puntos - puntos[punto_superior_izquierdo]  
        # Multiplica por la matriz de escalado
        puntos_escalados = np.dot(puntos_escalados, escala_matriz)    
        # Suma el punto superior izquierdo
        puntos_escalados = puntos_escalados + puntos[punto_superior_izquierdo]  

        # Redondea las coordenadas escaladas
        puntos_escalados = np.round(puntos_escalados / 10) * 10

        # Devuelve las 8 coordenadas escaladas
        x1_escalado, y1_escalado = puntos_escalados[0]
        x2_escalado, y2_escalado = puntos_escalados[1]
        x3_escalado, y3_escalado = puntos_escalados[2]
        x4_escalado, y4_escalado = puntos_escalados[3]
        return (x1_escalado, y1_escalado, x2_escalado, y2_escalado, 
                x3_escalado, y3_escalado, x4_escalado, y4_escalado)
    
    
    
    def puntos_rotados(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # """
        # Calcula y devuelve las coordenadas de los puntos de la figura después de aplicar la rotación.
        # La función rota la figura alrededor de su centro. El centro se calcula como el punto medio
        # entre las coordenadas (x1, y1) y (x3, y3).

        # :return: Las 8 coordenadas de los puntos rotados.
        # """
        puntos = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

        # Calcula el centro de la figura
        centro_x = (x1 + x3) / 2
        centro_y = (y1 + y3) / 2

        # Calcula el ángulo de rotación en radianes
        rad = math.radians(self.rotacion)
        cos_rad = math.cos(rad)
        sin_rad = math.sin(rad)

        # Crea la matriz de rotación
        rotacion_matriz = np.array([[cos_rad, sin_rad], [-sin_rad, cos_rad]])

        # Aplica la rotación a los puntos
        puntos_rotados = puntos - np.array([centro_x, centro_y])  # Resta el centro de la figura
        puntos_rotados = np.dot(puntos_rotados, rotacion_matriz)  # Multiplica por la matriz de rotación
        puntos_rotados = puntos_rotados + np.array([centro_x, centro_y])  # Suma el centro de la figura

        # Redondea las coordenadas de los puntos rotados
        puntos_rotados = np.round(puntos_rotados / 10) * 10

        x1_rotado, y1_rotado = puntos_rotados[0]
        x2_rotado, y2_rotado = puntos_rotados[1]
        x3_rotado, y3_rotado = puntos_rotados[2]
        x4_rotado, y4_rotado = puntos_rotados[3]

        return x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado
   
    def colorear(self, canvas):
        # """
        # Colorea el cuadrado en el objeto canvas proporcionado. Este método escala y rota el cuadrado
        # antes de colorearlo utilizando el algoritmo flood fill, que rellena el área delimitada por los
        # bordes del cuadrado con el color especificado.

        # :param canvas: Objeto canvas donde se dibujará el cuadrado.
        # """
        # Calcula las coordenadas escaladas y rotadas del cuadrado
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = self.coordenadas_escaladas()
        x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = self.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

        # Calcula el centro del cuadrado rotado y escalado
        centro_x = (x1_rotado + x3_rotado) / 2
        centro_y = (y1_rotado + y3_rotado) / 2

        # Redondea las coordenadas del centro a múltiplos de 5
        semilla_x = round(centro_x / 10) * 10
        semilla_y = round(centro_y / 10) * 10

        # Realiza el relleno utilizando las coordenadas de la semilla
        flood_fill_puntos(canvas, semilla_x, semilla_y, self.color)

    def trasladar(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy
        self.x4 += dx
        self.y4 += dy

class Triangulo(Figura):
    # """
    # Clase Triangulo que hereda de Figura. Representa un triángulo en un plano 2D con
    # puntos (x1, y1), (x2, y2) y (x3, y3). Permite cambiar el color, el grosor y
    # el tipo de línea, así como realizar transformaciones de escala y traslación.

    # :param color: Color del triángulo (por defecto 'black').
    # :param grosor: Grosor de la línea del triángulo (por defecto 1).
    # :param tipo_linea: Tipo de línea del triángulo (por defecto 'solid').
    # """
    def __init__(self, x1, y1, x2, y2, x3, y3, color='black', grosor=1, tipo_linea='solid'):
        super().__init__(x1, y1, color, grosor, tipo_linea)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.escala = 1
    
    def coordenadas_escaladas(self):
        # Identifica el punto superior
        puntos = np.array([[self.x1, self.y1], 
                           [self.x2, self.y2], 
                           [self.x3, self.y3]])
        punto_superior = np.argmin(puntos, axis=0)[1]

        # Calcula la matriz de escalado
        escala_matriz = np.array([[self.escala, 0], 
                                  [0, self.escala]])

        # Escala las coordenadas
        puntos_escalados = puntos - puntos[punto_superior]
        puntos_escalados = np.dot(puntos_escalados, escala_matriz)
        puntos_escalados = puntos_escalados + puntos[punto_superior]

        # Redondea las coordenadas escaladas
        puntos_escalados = np.round(puntos_escalados / 10) * 10

        # Devuelve las 6 coordenadas escaladas
        x1_escalado, y1_escalado = puntos_escalados[0]
        x2_escalado, y2_escalado = puntos_escalados[1]
        x3_escalado, y3_escalado = puntos_escalados[2]
        return (x1_escalado, y1_escalado, x2_escalado, 
                y2_escalado, x3_escalado, y3_escalado)

    def puntos_rotados(self, x1, y1, x2, y2, x3, y3):
        # """
        # Rota los puntos del triángulo alrededor de su centroide según el ángulo de rotación.

        # :param x1: Coordenada x del primer vértice del triángulo.
        # :param y1: Coordenada y del primer vértice del triángulo.
        # :param x2: Coordenada x del segundo vértice del triángulo.
        # :param y2: Coordenada y del segundo vértice del triángulo.
        # :param x3: Coordenada x del tercer vértice del triángulo.
        # :param y3: Coordenada y del tercer vértice del triángulo.
        # :return: Coordenadas rotadas de los vértices del triángulo.
        # """
        puntos = [[x1, y1], [x2, y2], [x3, y3]]

        # Calcular el centroide del triángulo
        centro_x, centro_y = Triangulo.punto_medio_triangulo(x1, y1, x2, y2, x3, y3)

        # Convertir el ángulo de rotación en radianes y calcular sus valores de seno y coseno
        rad = math.radians(self.rotacion)
        cos_rad = math.cos(rad)
        sin_rad = math.sin(rad)

        puntos_rotados = []
        for punto in puntos:
            x, y = punto
            # Aplicar la matriz de rotación a las coordenadas
            x_rotado = cos_rad * (x - centro_x) - sin_rad * (y - centro_y) + centro_x
            y_rotado = sin_rad * (x - centro_x) + cos_rad * (y - centro_y) + centro_y
            # Redondear las coordenadas a múltiplos de 10
            x_rounded = round(x_rotado / 10) * 10
            y_rounded = round(y_rotado / 10) * 10
            puntos_rotados.append([x_rounded, y_rounded])

        x1_rotado, y1_rotado = puntos_rotados[0]
        x2_rotado, y2_rotado = puntos_rotados[1]
        x3_rotado, y3_rotado = puntos_rotados[2]

        return x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado

    def punto_medio_triangulo(x1, y1, x2, y2, x3, y3):
        # Calcular el promedio de las coordenadas x de los vértices
        x_medio = (x1 + x2 + x3) / 3

        # Calcular el promedio de las coordenadas y de los vértices
        y_medio = (y1 + y2 + y3) / 3

        return x_medio, y_medio
    
    def colisiona_con_punto(self, x, y):
        # """
        # Determina si un punto (x, y) se encuentra dentro del triángulo escalado y rotado.
        # Utiliza la técnica de áreas de subtriángulos para verificar si el punto está dentro del triángulo.
        
        # :param x: Coordenada x del punto.
        # :param y: Coordenada y del punto.
        # :return: True si el punto está dentro del triángulo, False en caso contrario.
        # """
        # Escalar y rotar los vértices del triángulo
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = self.coordenadas_escaladas()
        x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado = self.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)

        # Calcular el área total del triángulo y las áreas de los subtriángulos
        area_total = triangle_area(x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado)
        area1 = triangle_area(x, y, x2_rotado, y2_rotado, x3_rotado, y3_rotado)
        area2 = triangle_area(x1_rotado, y1_rotado, x, y, x3_rotado, y3_rotado)
        area3 = triangle_area(x1_rotado, y1_rotado, x2_rotado, y2_rotado, x, y)
        return abs(area_total - (area1 + area2 + area3)) < 0.1
    
    def trasladar(self, dx, dy):
        # """
        # Traslada el triángulo en las direcciones x y y.

        # :param dx: Distancia a trasladar en el eje x.
        # :param dy: Distancia a trasladar en el eje y.
        # """
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy
        
    def imprimir_atributos(self):
        # """
        # Imprime los atributos del triángulo. Sobreescribe el método imprimir_atributos de la clase base Figura.
        # """
        super().imprimir_atributos()
        
    def colorear(self, canvas):
        # Calcular el punto medio del triángulo
        semilla_x, semilla_y = Triangulo.punto_medio_triangulo(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
        # Llamar al algoritmo de flood fill
        flood_fill_puntos(canvas, round(semilla_x/10)*10, round(semilla_y/10)*10, self.color)





    
    # def colorear(self, canvas):
    #     # """
    #     # Colorea el interior del triángulo utilizando el algoritmo de flood fill.

    #     # :param canvas: Objeto canvas donde se dibuja el triángulo.
    #     # """
    #     # Escalar los vértices del triángulo
    #     x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = self.coordenadas_escaladas()
    #     # Calcular el punto medio del triángulo
    #     semilla_x, semilla_y = Triangulo.punto_medio_triangulo(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)
    #     # Llamar al algoritmo de flood fill
    #     flood_fill_puntos(canvas, round(semilla_x/10)*10, round(semilla_y/10)*10, self.color)#cambio


class Circunferencia(Figura):
    # """
    # Clase Circunferencia que hereda de Figura. Representa una circunferencia en un plano 2D
    # con centro (x, y) y radio. Permite cambiar el color, el grosor y
    # el tipo de línea, así como realizar transformaciones de escala y traslación.

    # :param x: Coordenada x del centro de la circunferencia.
    # :param y: Coordenada y del centro de la circunferencia.
    # :param radio: Radio de la circunferencia.
    # :param color: Color de la circunferencia (por defecto 'yellow').
    # :param grosor: Grosor de la línea de la circunferencia (por defecto 1).
    # :param tipo_linea: Tipo de línea de la circunferencia (por defecto 'solid').
    # """
    def __init__(self, x, y, radio, color='yellow', grosor=1, tipo_linea='solid'):
        super().__init__(x, y, color, grosor, tipo_linea)
        self.radio = radio

    def colisiona_con_punto(self, x, y):
        # """
        # Determina si un punto (x, y) colisiona con la circunferencia, es decir,
        # si el punto se encuentra dentro de la circunferencia.

        # :param x: Coordenada x del punto.
        # :param y: Coordenada y del punto.
        # :return: True si el punto colisiona, False en caso contrario.
        # """
        distancia_centro = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distancia_centro <= self.radio * self.escala

    def imprimir_atributos(self):
        # """
        # Imprime los atributos de la circunferencia, incluido el radio,
        # llamando al método `imprimir_atributos` de la clase base (Figura).
        # """
        super().imprimir_atributos()
        print(f"Radio: {self.radio}")

    def colorear(self, canvas):
        # """
        # Colorea el interior de la circunferencia utilizando el algoritmo
        # de relleno por inundación (flood_fill_puntos).

        # :param canvas: Objeto canvas donde se dibuja la circunferencia.
        # """
        flood_fill_puntos(canvas, self.x, self.y, self.color)
        
class FigurasCanvas(tk.Canvas):
    # """
    # Clase FigurasCanvas que hereda de tk.Canvas. Permite la interacción con figuras
    # en un lienzo de tkinter, incluyendo la selección y el arrastre de figuras.
    # Además, permite obtener el color de un píxel en el lienzo.

    # :param parent: Widget padre al cual pertenece el lienzo.
    # :param args: Argumentos adicionales para tk.Canvas.
    # :param kwargs: Argumentos de palabras clave adicionales para tk.Canvas.
    # """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.figuras = []
        self.figura_seleccionada = None
        self.bind("<Button-1>", self.on_click_izquierdo)
        self.bind("<B1-Motion>", self.on_arrastre_izquierdo)
        self.bind("<ButtonRelease-1>", self.on_suelta_izquierdo)
        self.estado = ""
        self.figura_actual = ""
        
    def obtener_color_pixel(self, x, y):
        # """
        # Obtiene el color de un píxel en las coordenadas (x, y) en el lienzo.

        # :param x: Coordenada x del píxel.
        # :param y: Coordenada y del píxel.
        # :return: Color del píxel en las coordenadas (x, y), o None si no se encuentra un elemento con color diferente al fondo.
        # """
        # Encuentra los elementos en la coordenada (x, y)
        elementos = self.find_overlapping(x, y, x+1, y+1)

        # Si hay elementos en la coordenada
        if elementos:
            # Obtén el color del fondo del Canvas
            color_fondo = self["bg"]
            
            # Itera sobre los elementos superpuestos
            for elemento in elementos:
                color = self.itemcget(elemento, "fill")
                
                # Si el color del elemento es diferente al fondo, devuélvelo
                if color != color_fondo:
                    return color

        # Si no se encontró un elemento con color diferente al fondo, devuelve None
        return None
          
    def dibujar_figura(self, figura):
        # """
        # Dibuja una figura en el canvas, teniendo en cuenta su escala, rotación, tipo de línea y color.
        # Esta función puede manejar figuras de las clases Cuadrado, Circunferencia y Triangulo.

        # :param figura: Un objeto de la clase Figura (Cuadrado, Circunferencia o Triangulo).
        # """
        escala = figura.escala
        grosor = figura.grosor

        if isinstance(figura, Cuadrado):
            # Calcula las coordenadas escaladas y rotadas del cuadrado
            x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = figura.coordenadas_escaladas()
            x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = figura.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

            # Dibuja las líneas del cuadrado con las coordenadas rotadas
            puntos_linea1 = bresenham(x1_rotado, y1_rotado, x2_rotado, y2_rotado, line_style=figura.tipo_linea)
            puntos_linea2 = bresenham(x2_rotado, y2_rotado, x3_rotado, y3_rotado, line_style=figura.tipo_linea)
            puntos_linea3 = bresenham(x3_rotado, y3_rotado, x4_rotado, y4_rotado, line_style=figura.tipo_linea)
            puntos_linea4 = bresenham(x4_rotado, y4_rotado, x1_rotado, y1_rotado, line_style=figura.tipo_linea)
            
            # Dibuja los rectángulos que componen las líneas del cuadrado
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3 + puntos_linea4:
                x, y, color = punto
                self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)

            figura.colorear(self)

        elif isinstance(figura, Circunferencia):
            # Calcula el radio escalado de la circunferencia
            radio  = (round(figura.radio * escala/10)*10)
            
            # Genera los puntos de la circunferencia utilizando el algoritmo del punto medio
            puntos_circunferencia = punto_medio(figura.x, figura.y, radio)
            
            # Dibuja los rectángulos que componen la circunferencia
            for punto in puntos_circunferencia:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width= grosor, outline="Black", fill="black")
                # x, y, color = punto
                # self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)

            figura.colorear(self)
            
        elif isinstance(figura, Triangulo):
            # Calcula las coordenadas escaladas y rotadas del triángulo
            x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = figura.coordenadas_escaladas()
            x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado = figura.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)

            # Dibuja las líneas del triángulo con las coordenadas rotadas
            puntos_linea1 = bresenham(x1_rotado, y1_rotado, x2_rotado, y2_rotado, line_style=figura.tipo_linea)
            puntos_linea2 = bresenham(x2_rotado, y2_rotado, x3_rotado, y3_rotado, line_style=figura.tipo_linea)
            puntos_linea3 = bresenham(x3_rotado, y3_rotado, x1_rotado, y1_rotado, line_style=figura.tipo_linea)
            
            # Dibuja los rectángulos que componen las líneas del triángulo
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3:
                x, y, color = punto
                self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
            figura.colorear(self)

    def get_pixel_color(self, x, y):
        # """
        # Obtiene el color del píxel en las coordenadas (x, y) del lienzo.
        
        # :param x: Coordenada x del píxel.
        # :param y: Coordenada y del píxel.
        # :return: Color del píxel si existe, None en caso contrario.
        # """
        items = self.find_overlapping(x, y, x, y)
        if items:
            return self.itemcget(items[0], "fill")
        else:
            return None

    def set_pixel_color(self, x, y, color):
        # """
        # Establece el color del píxel en las coordenadas (x, y) del lienzo.
        
        # :param x: Coordenada x del píxel.
        # :param y: Coordenada y del píxel.
        # :param color: Color a asignar al píxel.
        # """
        self.itemconfig(self.find_closest(x, y), fill=color)

    def in_bounds(self, x, y):
        # """
        # Verifica si las coordenadas (x, y) están dentro del área del lienzo.
        
        # :param x: Coordenada x.
        # :param y: Coordenada y.
        # :return: Verdadero si las coordenadas están dentro del área del lienzo, falso en caso contrario.
        # """
        return 0 <= x < self.winfo_width() and 0 <= y < self.winfo_height()
    
    def agregar_cuadrado(self, x, y):
        # """
        # Agrega un cuadrado en la posición (x, y) del lienzo, con lado de 90, color azul, grosor 2 y línea sólida.
        
        # :param x: Coordenada x del vértice superior izquierdo del cuadrado.
        # :param y: Coordenada y del vértice superior izquierdo del cuadrado.
        # """
        lado = 90
        x1, y1 = x, y
        x2, y2 = x + lado, y
        x3, y3 = x + lado, y + lado
        x4, y4 = x, y + lado
        figura = Cuadrado(x1, y1, x2, y2, x3, y3, x4, y4, color="Blue", grosor=2, tipo_linea="solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
             
    def agregar_circulo(self, x, y):
        # """
        # Agrega un círculo a la lista de figuras y lo dibuja en el canvas.

        # :param x: Coordenada x del centro del círculo.
        # :param y: Coordenada y del centro del círculo.
        # """
        figura = Circunferencia(x, y, 45, "Yellow", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
        
    def agregar_triangulo(self, x, y):
        # """
        # Agrega un triángulo a la lista de figuras y lo dibuja en el canvas.

        # :param x: Coordenada x del punto de referencia del triángulo.
        # :param y: Coordenada y del punto de referencia del triángulo.
        # """
        figura = Triangulo(x - 50, y + 80, x, y - 10, x + 50, y + 80, "Green", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
        
    def on_click_izquierdo(self, event):
        # """
        # Maneja el evento de click izquierdo del mouse en el canvas. Dependiendo del estado actual,
        # dibuja una figura, selecciona una figura existente o realiza alguna otra acción.

        # :param event: Objeto de evento que contiene las coordenadas x e y del click.
        # """
        x, y = (round(event.x / 10) * 10), (round(event.y / 10) * 10)

        # Verifica el estado actual para determinar qué acción realizar
        if self.estado == "dibujar":
            if self.figura_actual == "cuadrado":
                self.agregar_cuadrado(x, y)
            elif self.figura_actual == "circulo":
                self.agregar_circulo(x, y)
            elif self.figura_actual == "triangulo":
                self.agregar_triangulo(x, y)
        elif self.estado == "mover":
            self.seleccionar_figura(x, y)
        print("Color del pixel en ({}, {}): {}".format(x, y, self.obtener_color_pixel(x, y)))
        
    def on_arrastre_izquierdo(self, event):
        # """
        # Método que maneja el evento de arrastrar el botón izquierdo del mouse.
        # Mueve la figura seleccionada en el canvas siguiendo el cursor del mouse
        # si el estado es 'mover' y hay una figura seleccionada.

        # :param event: Objeto evento que contiene información sobre la acción del mouse.
        # """
        # Verifica si el estado es "mover" y si hay una figura seleccionada.
        if self.estado == "mover" and self.figura_seleccionada is not None:
            # Guarda las coordenadas previas del mouse si no existen.
            if not hasattr(self, 'prev_x'):
                self.prev_x = event.x
                self.prev_y = event.y

            # Calcula la diferencia entre las coordenadas actuales y previas del mouse.
            dx = round((event.x - self.prev_x) / 10) * 10
            dy = round((event.y - self.prev_y) / 10) * 10

            # Actualiza las coordenadas previas del mouse.
            self.prev_x = event.x
            self.prev_y = event.y

            # Si la figura seleccionada es un Triangulo, actualiza sus vértices.
            if isinstance(self.figura_seleccionada, Triangulo):
                self.figura_seleccionada.x1 += dx
                self.figura_seleccionada.y1 += dy
                self.figura_seleccionada.x2 += dx
                self.figura_seleccionada.y2 += dy
                self.figura_seleccionada.x3 += dx
                self.figura_seleccionada.y3 += dy
            else:
                # Si la figura seleccionada no es un Triangulo, usa el método trasladar().
                self.figura_seleccionada.trasladar(dx, dy)

            # Borra todas las figuras del canvas y las vuelve a dibujar actualizadas.
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
                
    def on_suelta_izquierdo(self, event):
        # """
        # Llamado al soltar el botón izquierdo del ratón. Elimina las coordenadas
        # previas almacenadas (prev_x y prev_y) si existen.

        # :param event: Objeto de evento del ratón.
        # """
        if hasattr(self, 'prev_x'):
            del self.prev_x
            del self.prev_y

    def seleccionar_figura(self, x, y):
        # """
        # Selecciona la figura en la posición (x, y) si colisiona con un punto. Si una
        # figura es seleccionada, su borde se marca como seleccionado y se guarda como
        # figura_seleccionada.

        # :param x: Coordenada x del punto.
        # :param y: Coordenada y del punto.
        # """
        self.figura_seleccionada = None
        for figura in self.figuras:
            if figura.colisiona_con_punto(x, y):
                figura.borde_seleccionado = not figura.borde_seleccionado
                self.figura_seleccionada = figura
                break

    def borrar_figura_seleccionada(self):
        # """
        # Borra la figura seleccionada, elimina todas las figuras del lienzo
        # y vuelve a dibujar las figuras restantes.
        # """
        if self.figura_seleccionada is not None:
            self.figuras.remove(self.figura_seleccionada)
            self.figura_seleccionada = None
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)

    def cambiar_color_figura_seleccionada(self, event):
        # """
        # Cambia el color de la figura seleccionada al color seleccionado en la interfaz
        # de usuario y vuelve a dibujar las figuras en el lienzo.

        # :param event: Objeto de evento del ratón.
        # """
        if self.canvas.figura_seleccionada is not None:
            color_seleccionado = self.color_var.get()
            colores = {'Negro': 'black', 'Rojo': 'red', 'Verde': 'green', 'Azul': 'blue', 'Amarillo': 'yellow', 'Naranja': 'orange', 'Morado': 'purple'}
            self.canvas.figura_seleccionada.cambiar_color(colores[color_seleccionado])
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)
             
    def cambiar_color_seleccionado(self, color):
        # """
        # Cambia el color de la figura seleccionada en el canvas.

        # :param color: Color al que se cambiará la figura seleccionada.
        # """
        if self.figura_seleccionada is not None:
            # Cambie el atributo color de la figura seleccionada
            self.figura_seleccionada.cambiar_color(color)
            self.figura_seleccionada.imprimir_atributos()

            # Redibujar todas las figuras en el canvas
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)

    def mover_figura(self, dx, dy):
        # """
        # Mueve la figura seleccionada en el canvas según las coordenadas (dx, dy).

        # :param dx: Desplazamiento en el eje x.
        # :param dy: Desplazamiento en el eje y.
        # """
        figura = self.figura_seleccionada
        if isinstance(figura, Triangulo):
            # Actualizar las coordenadas del triángulo
            figura.x1 += dx
            figura.y1 += dy
            figura.x2 += dx
            figura.y2 += dy
            figura.x3 += dx
            figura.y3 += dy
        else:
            # Trasladar figura (Cuadrado u otras heredadas de Figura)
            figura.trasladar(dx, dy)

        # Redibujar todas las figuras en el canvas
        self.delete("all")
        for fig in self.figuras:
            self.dibujar_figura(fig)
            
    def escalar_figura(self, factor):
        # """
        # Escala la figura seleccionada en función del factor proporcionado.
        # Luego, borra todas las figuras en el canvas y las vuelve a dibujar con la figura escalada.

        # :param factor: Factor por el cual escalar la figura seleccionada.
        # """
        if self.figura_seleccionada is not None:
            self.figura_seleccionada.escalar(factor)
            self.delete("all")  # Elimina todas las figuras en el canvas.
            for figura in self.figuras:
                self.dibujar_figura(figura)  # Vuelve a dibujar todas las figuras con la figura escalada.

    def rotar_figura(self, rotacion):
        # """
        # Rota la figura seleccionada según el ángulo proporcionado.
        # Luego, borra todas las figuras en el canvas y las vuelve a dibujar con la figura rotada.

        # :param rotacion: Ángulo en grados para rotar la figura seleccionada.
        # """
        if self.figura_seleccionada is not None:
            self.figura_seleccionada.rotar(rotacion)
            self.delete("all")  # Elimina todas las figuras en el canvas.
            for figura in self.figuras:
                self.dibujar_figura(figura)  # Vuelve a dibujar todas las figuras con la figura rotada.     
    
    def modificar_grosor_bordes(self, factor):
        """
        Esta funcion recibe el valor de reemplazo para aumentar o reducir
        el tamaño de los bordes de la figura seleccionada
        que puede ser circulo , cuadrado o triangulo
        """
        if factor >= 0 and factor <=20:
            fig = self.figura_seleccionada    
            if fig is not None:
                fig.set_border_thickness(factor)
                self.delete("all")  # Elimina todas las figuras en el canvas.
                for figura in self.figuras:
                    self.dibujar_figura(figura) #dibuja con la modificacion los bordes de la figuras

class Aplicacion(tk.Tk):
    
    def __init__(self):
        bg1 = "#171c3b"
        col2 = "#787c9f"
        fgc = "#e9eeee"
        
        super().__init__()
        self.title("Dibujo de figuras geométricas")
        self.configure(bg="#d9dee2")
        # Centrar la ventana y hacerla no redimensionable
        # Centrar ventana y hacerla no redimensionable
        w = 1166
        h = 600
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry('{}x{}+{}+{}'.format(w, h, x, y))
        self.resizable(False, False)

        self.canvas = FigurasCanvas(self, width=1000, height=600)
        self.canvas.configure(bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT)

        # Configuración de la sección de controles
        self.frame_controles = tk.Frame(self)
        self.frame_controles.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.frame_controles.configure(bg=bg1)
        
        # Configuración de la sección de selección de figura
        self.frame_figura = tk.Frame(self.frame_controles)
        self.frame_figura.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_figura.configure(bg=bg1)
        
        # Combo box para seleccionar el tipo de figura
        self.figura_var = tk.StringVar()
        self.seleccion_figura = ttk.Combobox(self.frame_figura, textvariable=self.figura_var, state='readonly',width=20)
        self.seleccion_figura['values'] = ('Cuadrado', 'Círculo', 'Triángulo')
        self.seleccion_figura.current(0)
        self.seleccion_figura.grid(row=1, column=0, columnspan=2, padx=0, pady=5, sticky="W")
        self.seleccion_figura.bind("<<ComboboxSelected>>", self.actualizar_figura_actual)

        # Botones para dibujar y seleccionar figuras
        self.boton_dibujar = tk.Button(self.frame_figura, text="Dibujar", font=("Arial", 8, "bold"), command=self.dibujar, width=8)
        self.boton_dibujar.grid(row=2, column=0, padx=0, pady=5, sticky="W")
        self.boton_dibujar.configure(bg=col2)
        self.boton_dibujar.configure(fg="white")
        
        self.boton_mover = tk.Button(self.frame_figura, text="Seleccionar", font=("Arial", 8, "bold"), command=self.mover, width=10)
        self.boton_mover.grid(row=2, column=1, padx=0, pady=5, sticky="W")
        self.boton_mover.configure(bg=col2)
        self.boton_mover.configure(fg="white")
        
        # self.frame_color = tk.Frame(self.frame_controles)
        # self.frame_color.pack(side=tk.LEFT, padx=5, pady=5)
        # self.frame_color.configure(bg=bg1)

        # # Configuración de la sección de selección de color
        # self.label_color = tk.Label(self.frame_color, text="Color de Figura", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        # self.label_color.grid(row=2, column=0, sticky="W", padx=5, pady=7)
        # self.label_color.configure(bg=bg1)
        
        # # Creación del widget de selección de color
        # self.color_var = tk.StringVar()
        # self.seleccion_color = ttk.Combobox(self.frame_color, textvariable=self.color_var, state='readonly', width=14)
        # self.seleccion_color['values'] = ('Black', 'Red', 'Green', 'Blue', 'Yellow', 'Orange')
        # self.seleccion_color.current(0)
        # self.seleccion_color.grid(row=1, column=0, sticky="W", padx=5, pady=0)
        # # Cambio de color de la figura seleccionada al seleccionar un nuevo color en el ComboBox
        # self.seleccion_color.bind("<<ComboboxSelected>>", self.cambiar_color_figura_seleccionada)
        # WILLIAM1
        # Creación del marco separado para la selección de color
        self.frame_color_separado = tk.Frame(self.frame_controles)
        self.frame_color_separado.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_color_separado.configure(bg=bg1)

        self.frame_color = tk.Frame(self.frame_color_separado)
        self.frame_color.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_color.configure(bg=bg1)

        # Configuración de la sección de selección de color
        self.label_color = tk.Label(self.frame_color, text="Color de Figura", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        self.label_color.grid(row=2, column=0, sticky="W", padx=5, pady=7)
        self.label_color.configure(bg=bg1)

        # Creación del widget de selección de color
        self.color_var = tk.StringVar()
        self.seleccion_color = ttk.Combobox(self.frame_color, textvariable=self.color_var, state='readonly', width=14)
        self.seleccion_color['values'] = ('Black', 'Red', 'Green', 'Blue', 'Yellow', 'Orange')
        self.seleccion_color.current(0)
        self.seleccion_color.grid(row=1, column=0, sticky="W", padx=5, pady=0)
        # Cambio de color de la figura seleccionada al seleccionar un nuevo color en el ComboBox
        self.seleccion_color.bind("<<ComboboxSelected>>", self.cambiar_color_figura_seleccionada)


        #####################
        
        
        # Creación del frame para controlar la escala
        self.frame_escala = tk.Frame(self.frame_controles)
        self.frame_escala.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_escala.configure(bg=bg1)
        
        # Etiqueta del control de escala
        self.label_escala = tk.Label(self.frame_escala, text="Tamaño", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2 )
        self.label_escala.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.label_escala.configure(bg=bg1)
        
        # Botón para aumentar la escala
        self.boton_aumentar = tk.Button(self.frame_escala, text="+", command=self.aumentar_escala, width=4, height=1)
        self.boton_aumentar.grid(row=1, column=1, padx=0, pady=2)
        self.boton_aumentar.configure(bg="#d14c69")
        self.boton_aumentar.configure(fg="White")
        
        # Botón para disminuir la escala
        self.boton_disminuir = tk.Button(self.frame_escala, text="-",command=self.disminuir_escala, width=4, height=1)
        self.boton_disminuir.grid(row=1, column=0, padx=0, pady=0)
        self.boton_disminuir.configure(bg="#d14c69")
        self.boton_disminuir.configure(fg="White")

        # Creación del frame para el movimiento
        self.frame_movimiento = tk.Frame(self.frame_controles)
        self.frame_movimiento.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_movimiento.configure(bg=bg1)
        
        # Creación del frame para la rotación
        self.frame_rotacion = tk.Frame(self.frame_controles)
        self.frame_rotacion.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_rotacion.configure(bg=bg1)

        # Configuración del label y botones para la rotación
        self.label_rotacion = tk.Label(self.frame_rotacion, text="Rotación", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        self.label_rotacion.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        self.label_rotacion.configure(bg=bg1)

        self.boton_rotar_horario = tk.Button(self.frame_rotacion, text="⇨", command=self.rotar_horario, width=4, height=1)
        self.boton_rotar_horario.grid(row=3, column=1, padx=0, pady=2)
        self.boton_rotar_horario.configure(bg="#5979f7")
        self.boton_rotar_horario.configure(fg="White")
        self.boton_rotar_antihorario = tk.Button(self.frame_rotacion, text="⇦", command=self.rotar_antihorario, width=4, height=1)
        self.boton_rotar_antihorario.grid(row=3, column=0, padx=0, pady=0)
        self.boton_rotar_antihorario.configure(bg="#5979f7")
        self.boton_rotar_antihorario.configure(fg="White")
        
        # Configuración de botones de movimiento en 4 direcciones
        self.boton_arriba = tk.Button(self.frame_movimiento, text="↑", command=self.mover_arriba, width=4, height=1)
        self.boton_arriba.grid(row=1, column=2)
        self.boton_arriba.configure(bg="#6637ef")
        self.boton_arriba.configure(fg="White")
        
        self.boton_abajo = tk.Button(self.frame_movimiento, text="↓", command=self.mover_abajo, width=4, height=1)
        self.boton_abajo.grid(row=2, column=2)
        self.boton_abajo.configure(bg="#6637ef")
        self.boton_abajo.configure(fg="White")    
            
        self.boton_izquierda = tk.Button(self.frame_movimiento, text="←", command=self.mover_izquierda, width=4, height=1)
        self.boton_izquierda.grid(row=2, column=1)
        self.boton_izquierda.configure(bg="#6637ef")
        self.boton_izquierda.configure(fg="White")
        
        self.boton_derecha = tk.Button(self.frame_movimiento, text="→", command=self.mover_derecha, width=4, height=1)
        self.boton_derecha.grid(row=2, column=3)
        self.boton_derecha.configure(bg="#6637ef")
        self.boton_derecha.configure(fg="White")
        
        # Creación del frame para el control de línea
        self.frame_linea = tk.Frame(self.frame_controles)
        self.frame_linea.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_linea.configure(bg=bg1)
        # WILLIAM2    
        self.boton_solido = tk.Button(self.frame_linea, text="Sólido",font=("Arial", 8, "bold"), command=self.cambiar_a_solido, width=11, height=1)
        self.boton_solido.grid(row=0, column=0, padx=0, pady=2)
        self.boton_solido.configure(bg=col2)
        self.boton_solido.configure(fg="White")
        self.boton_segmentado = tk.Button(self.frame_linea, text="Segmentado",font=("Arial", 8, "bold"), command=self.cambiar_a_segmentado, width=11, height=1)
        self.boton_segmentado.grid(row=1, column=0, padx=0, pady=2)
        self.boton_segmentado.configure(bg=col2)
        self.boton_segmentado.configure(fg="White")
        
        self.boton_borrar = tk.Button(self.frame_controles, text="Borrar",font=("Arial", 8, "bold"), command=self.borrar, width=6, height=2)
        self.boton_borrar.pack(side=tk.TOP, pady=5)
        self.boton_borrar.configure(bg=col2)
        self.boton_borrar.configure(fg="White")

        # Configuración de la sección de selección de acción
        self.botton_mas_ancho_borde = tk.Button(self.frame_controles, text="+ Borde",font=("Arial", 8, "bold"), command=self.aumentar_ancho_bordes, width=8, height=2)
        self.botton_mas_ancho_borde.pack(side=tk.LEFT, padx=5, pady=5)
        self.botton_mas_ancho_borde.configure(bg=bg1)
        self.botton_mas_ancho_borde.configure(fg= "#d7d7d7")

        self.botton_menos_ancho_borde = tk.Button(self.frame_controles, text="- Borde",font=("Arial", 8, "bold"), command=self.disminuir_ancho_bordes, width=8, height=2)
        self.botton_menos_ancho_borde.pack(side=tk.LEFT, padx=5, pady=5)
        self.botton_menos_ancho_borde.configure(bg=bg1)
        self.botton_menos_ancho_borde.configure(fg= "#d7d7d7")
    
    def dibujar(self):
        # """
        # Establece el estado del lienzo en "dibujar" para permitir la creación
        # de nuevas figuras y actualiza los botones correspondientes.
        # """
        self.canvas.estado = "dibujar"
        self.actualizar_botones()

    def aumentar_escala(self):
        # """
        # Aumenta la escala de la figura seleccionada en un 40% si hay una figura seleccionada.
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.escalar_figura(fig.get_escala()+0.4)

    def disminuir_escala(self):
        # """
        # Disminuye la escala de la figura seleccionada en un 40% si hay una figura seleccionada.
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.escalar_figura(fig.get_escala()-0.4)

    def rotar_horario(self):
        # """
        # Rota la figura seleccionada 15 grados en sentido horario si hay una figura seleccionada.
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.rotar_figura(fig.get_rotacion() + 15)

    def rotar_antihorario(self):
        # """
        # Rota la figura seleccionada 15 grados en sentido antihorario si hay una figura seleccionada.
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.rotar_figura(fig.get_rotacion() - 15)            
          

    def cambiar_a_solido(self):
        # """
        # Cambia el tipo de línea de la figura seleccionada a sólido.
        # Borra y vuelve a dibujar todas las figuras en el canvas para reflejar los cambios.
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            fig.tipo_linea = 'solid'
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)

    def cambiar_a_segmentado(self):
        # """
        # Cambia el tipo de línea de la figura seleccionada a segmentado (dashed).
        # Borra y vuelve a dibujar todas las figuras en el canvas para reflejar los cambios.
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            fig.tipo_linea = 'dashed'
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)

    def aumentar_ancho_bordes(self):
        # """
        # Aumenta en un pixel el ancho de los bordes
        # luego lo borra y redibuja con el metodo modificar grosor bordes
        # """
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            ancho_borde = fig.get_border_thickness()
            ancho_borde += 2
            self.canvas.modificar_grosor_bordes(ancho_borde)
    
    # def disminuir_ancho_bordes(self):
        # # """
        # # Decremente en un pixel el ancho de los bordes
        # # luego lo borra y redibuja con el metodo modificar grosor bordes
        # # """
        # fig = self.canvas.figura_seleccionada
        # if fig is not None:
        #     ancho_borde = fig.get_border_thickness()
        #     print(ancho_borde)
        #     ancho_borde -= 2
        #     self.canvas.modificar_grosor_bordes(ancho_borde)
    def disminuir_ancho_bordes(self):
        min_border_thickness = 4
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            ancho_borde = fig.get_border_thickness()
            nuevo_ancho_borde = ancho_borde - 2
            if nuevo_ancho_borde >= min_border_thickness:
                self.canvas.modificar_grosor_bordes(nuevo_ancho_borde)
        
        
    def mover_arriba(self):
        # """
        # Mueve la figura seleccionada en el canvas hacia arriba en 80 unidades.
        # """
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(0, -80)

    def mover_abajo(self):
        # """
        # Mueve la figura seleccionada en el canvas hacia abajo en 80 unidades.
        # """
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(0, 80)

    def mover_izquierda(self):
        # """
        # Mueve la figura seleccionada en el canvas hacia la izquierda en 80 unidades.
        # """
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(-80, 0)

    def mover_derecha(self):
        # """
        # Mueve la figura seleccionada en el canvas hacia la derecha en 80 unidades.
        # """
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(80, 0)

    def mover(self):
        # """
        # Cambia el estado del canvas a 'mover' y actualiza los botones.
        # """
        self.canvas.estado = "mover"
        self.actualizar_botones()

    def actualizar_botones(self):
        # """
        # Actualiza el aspecto visual de los botones 'Dibujar' y 'Mover' según el estado actual del canvas.
        # """
        if self.canvas.estado == "dibujar":
            self.boton_dibujar.config(bg="#3d3f51", relief=tk.SUNKEN)  # Botón presionado
            self.boton_mover.config(bg="#787c9f", relief=tk.RAISED)  # Botón no presionado
        elif self.canvas.estado == "mover":
            self.boton_dibujar.config(bg="#787c9f", relief=tk.RAISED)  # Botón no presionado
            self.boton_mover.config(bg="#3d3f51", relief=tk.SUNKEN)  # Botón presionado

    def borrar(self):
        # """
        # Borra la figura seleccionada en el canvas.
        # """
        self.canvas.borrar_figura_seleccionada()
    
    def actualizar_figura_actual(self, event):
        # """
        # Actualiza la figura actual en función de la opción seleccionada por el usuario.

        # :param event: Evento del ratón o teclado que activa esta función.
        # """
        figura_seleccionada = self.figura_var.get()
        if figura_seleccionada == "Cuadrado":
            self.canvas.figura_actual = "cuadrado"
        elif figura_seleccionada == "Círculo":
            self.canvas.figura_actual = "circulo"
        elif figura_seleccionada == "Triángulo":
            self.canvas.figura_actual = "triangulo"

    def cambiar_color_figura_seleccionada(self, event):
        # """
        # Cambia el color de la figura seleccionada en función de la opción
        # de color seleccionada por el usuario.

        # :param event: Evento del ratón o teclado que activa esta función.
        # """
        color_seleccionado = self.color_var.get()
        self.canvas.cambiar_color_seleccionado(color_seleccionado)

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
    
    
    
    
    

