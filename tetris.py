import pygame
import random
import time

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ancho_ventana = 400
alto_ventana = 800
tamaño_celda = 40
filas = alto_ventana // tamaño_celda
columnas = ancho_ventana // tamaño_celda

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
CYA = (0, 255, 255)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)
COLOR_PIEZAS = [ROJO, AZUL, VERDE, CYA, NARANJA, MORADO]

# Configuración de la ventana
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption('Tetris')

# Definir las piezas
piezas = [
    [[1, 1, 1, 1]],  # Línea
    [[1, 1], [1, 1]],  # Cuadrado
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 0], [0, 1, 1]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

def rotar_pieza(pieza):
    return [list(fila) for fila in zip(*pieza[::-1])]

def dibujar_tablero(tablero):
    for y, fila in enumerate(tablero):
        for x, celda in enumerate(fila):
            if celda:
                pygame.draw.rect(pantalla, celda,
                                 pygame.Rect(x * tamaño_celda, y * tamaño_celda, tamaño_celda, tamaño_celda))

def dibujar_pieza(pieza, offset):
    for y, fila in enumerate(pieza):
        for x, celda in enumerate(fila):
            if celda:
                pygame.draw.rect(pantalla, celda,
                                 pygame.Rect((offset[0] + x) * tamaño_celda, (offset[1] + y) * tamaño_celda,
                                             tamaño_celda, tamaño_celda))

def colision(tablero, pieza, offset):
    for y, fila in enumerate(pieza):
        for x, celda in enumerate(fila):
            if celda:
                if (x + offset[0] < 0 or x + offset[0] >= columnas or
                    y + offset[1] >= filas or
                    tablero[y + offset[1]][x + offset[0]]):
                    return True
    return False

def combinar_pieza(tablero, pieza, offset):
    for y, fila in enumerate(pieza):
        for x, celda in enumerate(fila):
            if celda:
                tablero[y + offset[1]][x + offset[0]] = celda

def eliminar_lineas(tablero):
    lineas_eliminadas = 0
    y = filas - 1
    while y >= 0:
        if all(tablero[y]):
            del tablero[y]
            tablero.insert(0, [0] * columnas)
            lineas_eliminadas += 1
        else:
            y -= 1
    return lineas_eliminadas

def generar_pieza():
    pieza = random.choice(piezas)
    color = random.choice(COLOR_PIEZAS)
    return [[color if celda else 0 for celda in fila] for fila in pieza]

# Variables del juego
tablero = [[0] * columnas for _ in range(filas)]
pieza = generar_pieza()
offset_pieza = [columnas // 2 - len(pieza[0]) // 2, 0]
clock = pygame.time.Clock()
corriendo = True

# Configuración del temporizador
tiempo_inicio_juego = time.time()  # Momento en que comienza el juego
tiempo_inicio_caida = tiempo_inicio_juego  # Momento en que comienza la caída de la pieza
intervalo_caida = 1.0  # Tiempo inicial para la caída de las piezas (en segundos)
velocidad_incremento = 0.01  # Incremento de la velocidad cada cierto tiempo

# Puntuación
puntaje = 0
puntos_por_pieza = 10
puntos_por_linea = 100
racha = 0

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Movimiento de la pieza
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        offset_pieza[0] -= 1
        if colision(tablero, pieza, offset_pieza):
            offset_pieza[0] += 1
    if keys[pygame.K_RIGHT]:
        offset_pieza[0] += 1
        if colision(tablero, pieza, offset_pieza):
            offset_pieza[0] -= 1
    if keys[pygame.K_DOWN]:
        offset_pieza[1] += 1
        if colision(tablero, pieza, offset_pieza):
            offset_pieza[1] -= 1
            combinar_pieza(tablero, pieza, offset_pieza)
            puntaje += puntos_por_pieza  # Sumar puntos por colocar la pieza
            pieza = generar_pieza()
            offset_pieza = [columnas // 2 - len(pieza[0]) // 2, 0]
            if colision(tablero, pieza, offset_pieza):
                print("Game Over")
                corriendo = False

    if keys[pygame.K_UP]:
        pieza = rotar_pieza(pieza)
        if colision(tablero, pieza, offset_pieza):
            pieza = rotar_pieza(rotar_pieza(rotar_pieza(pieza)))  # Rotar hacia atrás

    # Caída automática de las piezas
    tiempo_actual = time.time()
    tiempo_transcurrido_caida = tiempo_actual - tiempo_inicio_caida
    tiempo_transcurrido_juego = tiempo_actual - tiempo_inicio_juego

    if tiempo_transcurrido_caida > intervalo_caida:
        offset_pieza[1] += 1
        if colision(tablero, pieza, offset_pieza):
            offset_pieza[1] -= 1
            combinar_pieza(tablero, pieza, offset_pieza)
            puntaje += puntos_por_pieza  # Sumar puntos por colocar la pieza
            pieza = generar_pieza()
            offset_pieza = [columnas // 2 - len(pieza[0]) // 2, 0]
            if colision(tablero, pieza, offset_pieza):
                print("Game Over")
                corriendo = False
        tiempo_inicio_caida = tiempo_actual

        # Aumentar la velocidad con el tiempo
        intervalo_caida = max(0.2, intervalo_caida - velocidad_incremento)  # Asegurarse de que no sea menor a 0.2

    # Limpiar pantalla y dibujar
    pantalla.fill(NEGRO)
    dibujar_tablero(tablero)
    dibujar_pieza(pieza, offset_pieza)
    
    # Mostrar el contador de tiempo
    fuente = pygame.font.SysFont(None, 36)
    texto_tiempo = fuente.render(f'Tiempo: {int(tiempo_transcurrido_juego)} s', True, BLANCO)
    pantalla.blit(texto_tiempo, (10, 10))
    
    # Mostrar el puntaje
    texto_puntaje = fuente.render(f'Puntaje: {puntaje}', True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 50))
    
    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(10)

    # Eliminar líneas completas
    lineas_eliminadas = eliminar_lineas(tablero)
    if lineas_eliminadas > 0:
        racha += 1
        puntaje += puntos_por_linea * lineas_eliminadas * racha  # Sumar puntos con multiplicador por racha
    else:
        racha = 0  # Resetear la racha si no se eliminaron líneas

pygame.quit()
