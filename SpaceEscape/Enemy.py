# Enemy.py - AGORA COM DIFICULDADE PROGRESSIVA!
import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_w, screen_h, speed_multiplier=1.0):
        super().__init__()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.speed_multiplier = speed_multiplier  # NOVO: controla velocidade por level!

        tamanho = random.randint(35, 65)
        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)

        # Inimigo triangular (apontando pra baixo)
        pontos = [(tamanho // 2, tamanho), (0, 0), (tamanho, 0)]
        pygame.draw.polygon(self.image, (200, 30, 30), pontos)
        pygame.draw.polygon(self.image, (255, 120, 120), [(tamanho // 2, tamanho - 8), (8, 8), (tamanho - 8, 8)])

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, screen_w - tamanho - 10)
        self.rect.y = random.randint(-150, -60)

        # Velocidade base + multiplicador do level
        base_speed = random.uniform(2.5, 5.5)
        self.velocidade = base_speed * self.speed_multiplier

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > self.screen_h + 50:
            self.kill()