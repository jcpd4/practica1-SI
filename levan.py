import pygame
import time
import random

# Inicializar pygame
pygame.init()

# Definir colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

# Definir dimensiones de la ventana
ancho_ventana = 600
alto_ventana = 400

# Crear la ventana del juego
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption('Snake Game')

# Controlar la velocidad del juego
reloj = pygame.time.Clock()

# Tamaño del bloque de la serpiente
tamano_bloque = 20
velocidad_serpiente = 15

# Fuente del mensaje
fuente = pygame.font.SysFont("bahnschrift", 25)

# Funciones para mostrar mensajes en la pantalla
def mostrar_puntaje(puntaje):
    valor = fuente.render("Puntaje: " + str(puntaje), True, negro)
    ventana.blit(valor, [0, 0])

def nuestro_snake(tamano_bloque, lista_snake):
    for x in lista_snake:
        pygame.draw.rect(ventana, azul, [x[0], x[1], tamano_bloque, tamano_bloque])

# Bucle principal del juego
def juego():
    game_over = False
    game_cerrado = False

    x1 = ancho_ventana / 2
    y1 = alto_ventana / 2

    x1_cambio = 0
    y1_cambio = 0

    lista_snake = []
    largo_snake = 1

    comida_x = round(random.randrange(0, ancho_ventana - tamano_bloque) / 20.0) * 20.0
    comida_y = round(random.randrange(0, alto_ventana - tamano_bloque) / 20.0) * 20.0

    while not game_over:

        while game_cerrado:
            ventana.fill(blanco)
            mensaje = fuente.render("Perdiste! Presiona Q para salir o C para jugar de nuevo", True, rojo)
            ventana.blit(mensaje, [ancho_ventana / 6, alto_ventana / 3])
            mostrar_puntaje(largo_snake - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_cerrado = False
                    if evento.key == pygame.K_c:
                        juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_cambio = -tamano_bloque
                    y1_cambio = 0
                elif evento.key == pygame.K_RIGHT:
                    x1_cambio = tamano_bloque
                    y1_cambio = 0
                elif evento.key == pygame.K_UP:
                    y1_cambio = -tamano_bloque
                    x1_cambio = 0
                elif evento.key == pygame.K_DOWN:
                    y1_cambio = tamano_bloque
                    x1_cambio = 0

        if x1 >= ancho_ventana or x1 < 0 or y1 >= alto_ventana or y1 < 0:
            game_cerrado = True

        x1 += x1_cambio
        y1 += y1_cambio
        ventana.fill(blanco)
        pygame.draw.rect(ventana, verde, [comida_x, comida_y, tamano_bloque, tamano_bloque])
        lista_snake.append([x1, y1])
        if len(lista_snake) > largo_snake:
            del lista_snake[0]

        for segmento in lista_snake[:-1]:
            if segmento == [x1, y1]:
                game_cerrado = True

        nuestro_snake(tamano_bloque, lista_snake)
        mostrar_puntaje(largo_snake - 1)

        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, ancho_ventana - tamano_bloque) / 20.0) * 20.0
            comida_y = round(random.randrange(0, alto_ventana - tamano_bloque) / 20.0) * 20.0
            largo_snake += 1

        reloj.tick(velocidad_serpiente)

    pygame.quit()
    quit()

juego()
