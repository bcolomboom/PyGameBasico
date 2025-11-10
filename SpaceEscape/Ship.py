import pygame

class Nave(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Carrega a imagem da nave (troque por sua imagem)
        self.image = pygame.image.load("nave001.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 20
        self.velocidade = 8

    def update(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade

        # Limita na tela
        self.rect.x = max(0, min(self.rect.x, pygame.display.get_surface().get_width() - self.rect.width))