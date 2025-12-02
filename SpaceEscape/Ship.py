# Ship.py - VERSÃO FINAL FUNCIONANDO 100% (com is_dead, som, tudo!)
import pygame
from Laser import Laser

class Ship(pygame.sprite.Sprite):
    def __init__(self, screen_w, screen_h, move_scheme="p1_keyboard", sound_manager=None):
        super().__init__()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sound_manager = sound_manager

        # Imagem da nave
        try:
            self.original_image = pygame.image.load("nave001.png").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (60, 50))
        except:
            self.original_image = pygame.Surface((60, 50), pygame.SRCALPHA)
            points = [(30, 0), (0, 50), (60, 50)]
            pygame.draw.polygon(self.original_image, (255, 80, 80), points)
            pygame.draw.polygon(self.original_image, (255, 200, 100), [(30, 8), (15, 42), (45, 42)])

        self.dead_image = self.original_image.copy()
        self.dead_image.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_w // 2
        self.rect.bottom = screen_h - 50

        self.velocidade = 10
        self.bullets_group = None
        self.last_shot = 0
        self.shoot_delay = 120

        # HP e MORTE
        self.max_hp = 100
        self.hp = self.max_hp
        self.is_dead = False        # ← AQUI ESTAVA FALTANDO!
        self.invencivel = False
        self.invencivel_timer = 0

        # Posição da barra de HP
        self.hp_x = 10

        # Controles
        self.follow_mouse = False
        self.shoot_method = "key"
        self.move_keys = None

        # Configura esquema de controle
        if move_scheme == "p2_keyboard":
            self.move_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                              'up': pygame.K_UP, 'down': pygame.K_DOWN}
            self.shoot_method = "mouse"
            self.hp_x = screen_w - 190
            self.rect.centerx = screen_w * 0.75
        elif move_scheme == "mouse_follow":
            self.follow_mouse = True
            self.shoot_method = "mouse"
        else:  # p1_keyboard
            self.move_keys = {'left': pygame.K_a, 'right': pygame.K_d,
                              'up': pygame.K_w, 'down': pygame.K_s,
                              'shoot': pygame.K_SPACE}

    def atirar(self):
        if self.bullets_group is None or self.is_dead:
            return
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            laser = Laser(self.rect.centerx, self.rect.top)
            self.bullets_group.add(laser)
            self.last_shot = now
            if self.sound_manager:
                self.sound_manager.play_shot()

    def levar_dano(self, dano=25):
        if self.is_dead or self.invencivel:
            return False
        self.hp -= dano
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            self.image = self.dead_image
            return True
        self.invencivel = True
        self.invencivel_timer = pygame.time.get_ticks()
        return False

    def update(self, keys=None, mouse_pos=None, mouse_click=False):
        if self.is_dead:
            return

        if self.invencivel and pygame.time.get_ticks() - self.invencivel_timer > 1200:
            self.invencivel = False

        # Movimento mouse
        if self.follow_mouse and mouse_pos:
            self.rect.centerx += (mouse_pos[0] - self.rect.centerx) * 0.4
            self.rect.centery += (mouse_pos[1] - self.rect.centery) * 0.4

        # Movimento teclado
        if self.move_keys and keys:
            if keys[self.move_keys['left']]:
                self.rect.x -= self.velocidade
            if keys[self.move_keys['right']]:
                self.rect.x += self.velocidade
            if keys[self.move_keys['up']]:
                self.rect.y -= self.velocidade
            if keys[self.move_keys['down']]:
                self.rect.y += self.velocidade

            if self.shoot_method == "key" and self.move_keys.get('shoot') and keys[self.move_keys['shoot']]:
                self.atirar()

        if self.shoot_method == "mouse" and mouse_click:
            self.atirar()

        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_w, self.screen_h))

        # Pisca vermelho quando invencível
        if self.invencivel and (pygame.time.get_ticks() // 120) % 2:
            blink = self.original_image.copy()
            blink.fill((255, 100, 100), special_flags=pygame.BLEND_MULT)
            self.image = blink
        else:
            self.image = self.original_image if not self.is_dead else self.dead_image

    def desenhar_hp(self, tela):
        pygame.draw.rect(tela, (40, 0, 0), (self.hp_x, 10, 180, 28))
        largura = int(176 * (self.hp / self.max_hp))
        cor = (0, 255, 0) if self.hp > 50 else (255, 200, 0) if self.hp > 25 else (255, 0, 0)
        pygame.draw.rect(tela, cor, (self.hp_x + 2, 12, largura, 24))
        pygame.draw.rect(tela, (255, 255, 255), (self.hp_x, 10, 180, 28), 2)
        font = pygame.font.SysFont("arial", 20, bold=True)
        texto = font.render("DEAD" if self.is_dead else f"HP {self.hp}", True, (255, 255, 255))
        tela.blit(texto, (self.hp_x + 10, 14))