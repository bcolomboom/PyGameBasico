import pygame
from Background2 import AnimatedBackground
from Ship import Nave
from StartGame import StartScreen

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com GIF de fundo + Nave")
clock = pygame.time.Clock()

# Instancia os módulos
background = AnimatedBackground("spacegif.gif", LARGURA, ALTURA, True)
start_screen = StartScreen(tela, background)
nave = Nave(LARGURA, ALTURA)
todos_sprites = pygame.sprite.Group(nave)

ESTADO_START = 0
ESTADO_JOGANDO = 1
estado = ESTADO_START

rodando = True
while rodando:
    dt = clock.tick(60)
    teclas = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if estado == ESTADO_START and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                estado = ESTADO_JOGANDO

    # Atualiza tudo
    background.update(dt)

    if estado == ESTADO_START:
        # Tela de início
        start_screen.draw()
    elif estado == ESTADO_JOGANDO:
        # Jogo normal
        todos_sprites.update(teclas)

        background.draw(tela)
        todos_sprites.draw(tela)

    pygame.display.flip()

pygame.quit()