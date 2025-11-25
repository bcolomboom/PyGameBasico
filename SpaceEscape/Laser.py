# Laser.py - COM ROTACIONAÇÃO PERFEITA PARA CIMA! 🚀
import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Carrega sprite PNG (se existir)
        try:
            self.original_image = pygame.image.load("assets/laser/39.png").convert_alpha()
            # ROTACIONA 90° ANTI-HORÁRIO (pra cima se estava pra direita!)
            self.image = pygame.transform.rotate(self.original_image, -90)
            self.image = pygame.transform.scale(self.image, (12, 32))  # ajusta tamanho pós-rotação
        except:
            # Fallback: laser vertical neon (já pronto pra cima)
            self.image = pygame.Surface((16, 40), pygame.SRCALPHA)
            # Corpo principal vertical
            pygame.draw.rect(self.image, (0, 255, 150), (0, 0, 12, 32))
            # Brilho interno
            pygame.draw.rect(self.image, (255, 255, 255), (2, 4, 8, 24))
            # Contorno glow
            pygame.draw.rect(self.image, (100, 255, 200), (0, 0, 12, 32), 2)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y+20  # sai perfeitamente do topo da nave

        self.velocidade = 10

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.bottom < 0:
            self.kill()