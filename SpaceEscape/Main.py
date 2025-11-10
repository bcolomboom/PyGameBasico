import pygame
from Background2 import AnimatedBackground
from Ship import Nave

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com GIF de fundo + Nave")
clock = pygame.time.Clock()

# Instancia os módulos
background = AnimatedBackground("spacegif.gif", LARGURA, ALTURA, True)
nave = Nave(LARGURA, ALTURA)
todos_sprites = pygame.sprite.Group(nave)

rodando = True
while rodando:
    dt = clock.tick(60)
    teclas = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Atualiza tudo
    background.update(dt)
    todos_sprites.update(teclas)

    # Desenha tudo
    background.draw(tela)
    todos_sprites.draw(tela)

    pygame.display.flip()

pygame.quit()