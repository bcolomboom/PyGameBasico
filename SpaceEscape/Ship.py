# Ship.py
import pygame
from Laser import Laser  # ← Importa a classe Laser corretamente


class Ship(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, controle="keyboard"):
        super().__init__()

        # Tenta carregar imagem, se não tiver usa nave desenhada
        try:
            self.original_image = pygame.image.load("nave001.png").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (70, 60))
        except:
            # Nave triangular clássica (vermelha com detalhes)
            self.original_image = pygame.Surface((70, 60), pygame.SRCALPHA)
            points = [(35, 0), (0, 60), (70, 60)]
            pygame.draw.polygon(self.original_image, (255, 80, 80), points)
            pygame.draw.polygon(self.original_image, (255, 200, 100), [(35, 10), (20, 50), (50, 50)])

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 40

        self.velocidade = 8
        self.controle = controle
        self.bullets_group = None  # será definido no main.py
        self.last_shot = 0
        self.shoot_delay = 150  # ms entre tiros

    def atirar(self):
        if self.bullets_group is None:
            return

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            laser = Laser(self.rect.centerx, self.rect.top)
            self.bullets_group.add(laser)
            self.last_shot = now

    def update(self, keys=None, mouse_pos=None, mouse_click=False):
        # === MOVIMENTO ===
        if self.controle == "keyboard" and keys:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= self.velocidade
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.velocidade
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= self.velocidade
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += self.velocidade

            # Limita na tela
            self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

            # Tiro com ESPAÇO
            if keys[pygame.K_SPACE]:
                self.atirar()

        elif self.controle == "mouse" and mouse_pos:
            # Segue o mouse suavemente
            self.rect.centerx += (mouse_pos[0] - self.rect.centerx) * 0.3
            self.rect.centery += (mouse_pos[1] - self.rect.centery) * 0.3
            self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

            # Tiro com clique esquerdo
            if mouse_click:
                self.atirar()