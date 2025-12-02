# main.py - VERSÃO FINAL FUNCIONANDO 100% (PAUSE + GAME OVER + HIGHSCORE)
import pygame
from Background import AnimatedBackground
from Ship import Ship
from SpaceEscape.Enemy import Enemy
from StartGame import StartScreen
import json
import os
from SoundManager import *

# ========================================
# INICIALIZAÇÃO
# ========================================
pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("MEU JOGO ESPACIAL - FINAL BOSS!")
clock = pygame.time.Clock()

background = AnimatedBackground("assets/bg/spacegif.gif", LARGURA, ALTURA, True)
menu = StartScreen(tela, background)

# Grupos
players_group = None
lasers_group = None
enemies_group = None

# Variáveis do jogo
controle_escolhido = None
pause_selected = 0
score = 0
level = 1
highscore = 0
sound_manager = SoundManager()
current_music = None

# ESTADOS (TODOS DEFINIDOS ANTES DE USAR!)
ESTADO_MENU = "menu"
ESTADO_JOGANDO = "jogando"
ESTADO_PAUSE = "pause"
ESTADO_GAMEOVER = "gameover"
ESTADO_HIGHSCORES = "highscores"    # ADICIONADO
ESTADO_CREDITS = "credits"          # ADICIONADO

estado = ESTADO_MENU

HIGHSCORE_FILE = "highscore.json"

def carregar_highscore():
    """Lê o highscore do arquivo (se existir)"""
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("highscore", 0)
        except:
            return 0
    return 0

def salvar_highscore(valor):
    """Salva o highscore no arquivo"""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": valor}, f)
    except:
        print("Não foi possível salvar o highscore")

# Fontes
font_score = pygame.font.SysFont("OCR A Extended", 36, bold=True)
font_level = pygame.font.SysFont("OCR A Extended", 32)

# ========================================
# CLASSE LASER
# ========================================
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 24), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 150), (0, 0, 8, 24))
        pygame.draw.rect(self.image, (255, 255, 255), (1, 2, 6, 20), 1)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 15

    def update(self):
        self.rect.y -= self.speed
        if self.rect.top > ALTURA:
            self.kill()

# ========================================
# LOOP PRINCIPAL
# ========================================
rodando = True
while rodando:
    dt = clock.tick(60)
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    background.update(dt)

    # ==============================================================
    # MENU PRINCIPAL
    # ==============================================================
    if estado == ESTADO_MENU:
        if current_music != "menu":
            sound_manager.play_menu_music()
            current_music = "menu"

        comando = menu.handle_events(eventos)
        menu.draw()

        if comando:
            players_group = pygame.sprite.Group()
            lasers_group = pygame.sprite.Group()
            enemies_group = pygame.sprite.Group()

            if comando == "1p_keyboard":
                nave = Ship(LARGURA, ALTURA, move_scheme="p1_keyboard", sound_manager=sound_manager)
                nave.bullets_group = lasers_group
                players_group.add(nave)

            # === 1P MOUSE ===
            elif comando == "1p_mouse":
                nave = Ship(LARGURA, ALTURA, move_scheme="mouse_follow", sound_manager=sound_manager)
                nave.bullets_group = lasers_group
                players_group.add(nave)

            # === 2P ===
            elif comando == "2p":
                ship1 = Ship(LARGURA, ALTURA, move_scheme="p1_keyboard", sound_manager=sound_manager)
                ship2 = Ship(LARGURA, ALTURA, move_scheme="p2_keyboard", sound_manager=sound_manager)
                ship1.bullets_group = ship2.bullets_group = lasers_group
                players_group.add(ship1, ship2)

            elif comando == "highscores":
                estado = ESTADO_HIGHSCORES
            elif comando == "credits":
                estado = ESTADO_CREDITS
            elif comando == "quit":
                rodando = False

            if comando in ("1p_keyboard", "1p_mouse", "2p"):
                score = 0
                level = 1
                game_start_time = pygame.time.get_ticks()
                last_spawn = game_start_time + 1500
                estado = ESTADO_JOGANDO

    # ==============================================================
    # JOGANDO
    # ==============================================================
    elif estado == ESTADO_JOGANDO:
        if current_music != "game":
            sound_manager.play_game_music()
            current_music = "game"

        teclas = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clique = pygame.mouse.get_pressed()[0]
        ticks = pygame.time.get_ticks()

        # PAUSE
        if teclas[pygame.K_ESCAPE]:
            estado = ESTADO_PAUSE
            pause_selected = 0
            pygame.time.wait(150)
            continue

        # Level up
        novo_level = (score // 150) + 1
        if novo_level > level:
            level = novo_level

        # Spawn inimigos
        if last_spawn is None:
            last_spawn = ticks
        base_interval = max(400, 1800 - (level - 1) * 200)
        intervalo_spawn = base_interval / max(1, len(players_group))
        if ticks - last_spawn > intervalo_spawn:
            inimigo = Enemy(LARGURA, ALTURA, speed_multiplier=1 + (level - 1) * 0.15)
            enemies_group.add(inimigo)
            last_spawn = ticks

        # Updates
        players_group.update(keys=teclas, mouse_pos=mouse_pos, mouse_click=mouse_clique)
        lasers_group.update()
        enemies_group.update()

        # Colisões
        hits = pygame.sprite.groupcollide(enemies_group, lasers_group, True, True)
        score += len(hits) * 10

        # SOM DE EXPLOSÃO PRA CADA INIMIGO MORTO!
        for _ in hits:
            sound_manager.play_explosion()

        dano_atual = int(25 * (1 + (level - 1) * 0.2))
        for nave in players_group:
            if not nave.is_dead:
                colidiu = pygame.sprite.spritecollide(nave, enemies_group, True)
                for _ in colidiu:
                    nave.levar_dano(dano_atual)

        # Inimigos que passam (só enquanto vivo)
        if not all(nave.is_dead for nave in players_group):
            for inimigo in enemies_group:
                if inimigo.rect.top > ALTURA:
                    score = max(0, score - 10)
                    inimigo.kill()

        # Desenho
        background.draw(tela)
        enemies_group.draw(tela)
        players_group.draw(tela)
        lasers_group.draw(tela)
        for nave in players_group:
            nave.desenhar_hp(tela)

        # HUD
        score_surf = font_score.render(f"SCORE: {score}", True, (0, 255, 255))
        tela.blit(score_surf, (20, 60))
        level_surf = font_level.render(f"LEVEL {level}", True, (255, 200, 50))
        tela.blit(level_surf, (LARGURA - level_surf.get_width() - 20, 20))

        # Game Over → muda de estado
        if all(nave.is_dead for nave in players_group):
            if score > highscore:
                highscore = score
                salvar_highscore(highscore)
            estado = ESTADO_GAMEOVER

    # ==============================================================
    # GAME OVER (SÓ MENU PRINCIPAL)
    # ==============================================================
    elif estado == ESTADO_GAMEOVER:
        background.draw(tela)
        enemies_group.draw(tela)
        players_group.draw(tela)
        lasers_group.draw(tela)
        for nave in players_group:
            nave.desenhar_hp(tela)

        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(220)
        overlay.fill((30, 0, 0))
        tela.blit(overlay, (0, 0))

        go = font_score.render("GAME OVER", True, (255, 50, 50))
        final = font_score.render(f"SCORE FINAL: {score}", True, (255, 255, 100))
        best = font_score.render(f"HIGHSCORE: {highscore}", True, (100, 255, 100))
        esc = pygame.font.SysFont("OCR A Extended", 36).render("ESC - MENU PRINCIPAL", True, (200, 200, 255))

        tela.blit(go, go.get_rect(center=(LARGURA//2, ALTURA//2 - 80)))
        tela.blit(final, final.get_rect(center=(LARGURA//2, ALTURA//2 - 20)))
        tela.blit(best, best.get_rect(center=(LARGURA//2, ALTURA//2 + 30)))
        tela.blit(esc, esc.get_rect(center=(LARGURA//2, ALTURA//2 + 100)))

        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                players_group = None
                lasers_group = None
                enemies_group = None
                controle_escolhido = None
                menu.state = "main"
                menu.selected_main = 0
                estado = ESTADO_MENU
                pygame.time.wait(150)
                break

    # ==============================================================
    # PAUSE (só enquanto vivo)
    # ==============================================================
    elif estado == ESTADO_PAUSE:
        background.draw(tela)
        enemies_group.draw(tela)
        players_group.draw(tela)
        lasers_group.draw(tela)
        for nave in players_group:
            nave.desenhar_hp(tela)

        score_surf = font_score.render(f"SCORE: {score}", True, (0, 255, 255))
        tela.blit(score_surf, (20, 60))
        level_surf = font_level.render(f"LEVEL {level}", True, (255, 200, 50))
        tela.blit(level_surf, (LARGURA - level_surf.get_width() - 20, 20))

        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill((5, 5, 30))
        tela.blit(overlay, (0, 0))

        paused = font_score.render("PAUSED", True, (255, 100, 100))
        pr = paused.get_rect(center=(LARGURA//2, ALTURA//2 - 120))
        tela.blit(paused, pr)

        options = ["RESUME", "MENU PRINCIPAL"]
        for i, txt in enumerate(options):
            y = ALTURA//2 + 20 + i * 70
            color = (255, 150, 50) if i == pause_selected else (180, 180, 220)
            surf = font_score.render(txt, True, color)
            r = surf.get_rect(center=(LARGURA//2, y))
            tela.blit(surf, r)
            if i == pause_selected:
                t = pygame.time.get_ticks() / 600
                pulse = 6 + int(abs((t % 2) - 1) * 8)
                box = r.inflate(40 + pulse, 20 + pulse)
                pygame.draw.rect(tela, (255, 150, 50), box, width=4, border_radius=12)

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    players_group = None
                    lasers_group = None
                    enemies_group = None
                    controle_escolhido = None
                    menu.state = "main"
                    menu.selected_main = 0
                    estado = ESTADO_MENU
                    pygame.time.wait(150)
                    break
                elif evento.key == pygame.K_UP:
                    pause_selected = (pause_selected - 1) % 2
                elif evento.key == pygame.K_DOWN:
                    pause_selected = (pause_selected + 1) % 2
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if pause_selected == 0:
                        estado = ESTADO_JOGANDO
                    else:
                        players_group = None
                        lasers_group = None
                        enemies_group = None
                        controle_escolhido = None
                        menu.state = "main"
                        menu.selected_main = 0
                        estado = ESTADO_MENU
                    pygame.time.wait(150)
                    break

    # ==============================================================
    # HIGHSCORES / CRÉDITOS
    # ==============================================================
    elif estado == ESTADO_HIGHSCORES:
        background.draw(tela)
        titulo = font_score.render("HIGHSCORES", True, (0, 255, 255))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 180)))
        best = font_score.render(f"BEST: {highscore}", True, (255, 255, 100))
        tela.blit(best, best.get_rect(center=(LARGURA//2, 300)))
        esc = pygame.font.SysFont(None, 32).render("ESC - VOLTAR", True, (150, 150, 200))
        tela.blit(esc, esc.get_rect(center=(LARGURA//2, 500)))
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            estado = ESTADO_MENU

    elif estado == ESTADO_CREDITS:
        background.draw(tela)
        titulo = font_score.render("CRÉDITOS", True, (255, 20, 147))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 140)))
        linhas = ["FEITO COM AMOR", "PYGAME + CAFÉ", "", "OBRIGADO POR JOGAR!"]
        for i, txt in enumerate(linhas):
            cor = (0, 255, 255) if i % 2 == 0 else (255, 100, 200)
            surf = font_score.render(txt, True, cor)
            tela.blit(surf, surf.get_rect(center=(LARGURA//2, 260 + i * 60)))
        esc = pygame.font.SysFont(None, 32).render("ESC - MENU", True, (150, 150, 200))
        tela.blit(esc, esc.get_rect(center=(LARGURA//2, 540)))
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            estado = ESTADO_MENU

    pygame.display.flip()

pygame.quit()