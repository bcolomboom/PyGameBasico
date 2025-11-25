# main.py - VERSÃO COMPLETA COM TIROS PEW PEW! 🚀💥
import pygame
from Background import AnimatedBackground
from Ship import Ship
from StartGame import StartScreen

# ========================================
# INICIALIZAÇÃO
# ========================================
pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("MEU JOGO ESPACIAL - ARCADE PEW PEW EDITION")
clock = pygame.time.Clock()

# Instâncias principais
background = AnimatedBackground("assets/bg/spacegif.gif", LARGURA, ALTURA, True)
menu = StartScreen(tela, background)

# Grupos de sprites
players_group = None
lasers_group = None



# Controle escolhido
controle_escolhido = None

# Estados
ESTADO_MENU = "menu"
ESTADO_JOGANDO = "jogando"
ESTADO_HIGHSCORES = "highscores"
ESTADO_CREDITS = "credits"

estado = ESTADO_MENU

# ========================================
# CLASSE LASER (PEW PEW VERDE NEON!)
# ========================================
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Laser simples verde neon (sem precisar de imagem!)
        self.image = pygame.Surface((8, 24), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 150), (0, 0, 8, 24))
        pygame.draw.rect(self.image, (255, 255, 255), (1, 2, 6, 20), 1)  # glow interno
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 15  # velocidade do tiro

    def update(self):
        self.rect.y -= self.speed
        # Remove se sair da tela
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

    # Atualiza fundo SEMPRE
    background.update(dt)

    # ==============================================================
    # MENU (StartScreen gerencia seu próprio fundo)
    # ==============================================================
    if estado == ESTADO_MENU:
        comando = menu.handle_events(eventos)
        menu.draw()

        if comando:
            # Só cria a nave SE for começar o jogo (1p ou 2p)
            if comando in ("1p_keyboard", "1p_mouse", "2p"):
                players_group = pygame.sprite.Group()
                lasers_group = pygame.sprite.Group()

                # Cria a nave com o controle correto
                if comando == "1p_keyboard":
                    nave = Ship(LARGURA, ALTURA, controle="keyboard")
                    controle_escolhido = "keyboard"
                    print("Iniciando 1P com TECLADO + SPACE para PEW PEW!")
                elif comando == "1p_mouse":
                    nave = Ship(LARGURA, ALTURA, controle="mouse")
                    controle_escolhido = "mouse"
                    print("Iniciando 1P com MOUSE + CLICK para PEW PEW!")
                elif comando == "2p":
                    nave = Ship(LARGURA, ALTURA, controle="keyboard")
                    controle_escolhido = "keyboard"
                    print("Iniciando 2P (em breve!)")

                # Agora sim, conecta os lasers e adiciona ao grupo
                nave.bullets_group = lasers_group
                players_group.add(nave)
                estado = ESTADO_JOGANDO

            # Telas que NÃO precisam da nave
            elif comando == "highscores":
                estado = ESTADO_HIGHSCORES
            elif comando == "credits":
                estado = ESTADO_CREDITS
            elif comando == "quit":
                rodando = False

    # ==============================================================
    # JOGANDO COM TIROS!
    # ==============================================================
    elif estado == ESTADO_JOGANDO:
        teclas = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clique = pygame.mouse.get_pressed()[0]

        # ESC volta pro menu
        if teclas[pygame.K_ESCAPE]:
            estado = ESTADO_MENU
            players_group = None
            lasers_group = None
            controle_escolhido = None
            pygame.time.wait(150)
            continue

        # Atualiza jogadores (movimento + tiros)
        if controle_escolhido == "keyboard":
            players_group.update(keys=teclas)
        else:
            players_group.update(mouse_pos=mouse_pos, mouse_click=mouse_clique)

        # Atualiza lasers (PEW PEW voando!)
        lasers_group.update()

        # Desenha TUDO
        background.draw(tela)
        players_group.draw(tela)
        lasers_group.draw(tela)

    # ==============================================================
    # HIGHSCORES
    # ==============================================================
    elif estado == ESTADO_HIGHSCORES:
        background.draw(tela)
        font_big = pygame.font.SysFont("OCR A Extended", 70, bold=True)
        titulo = font_big.render("HIGHSCORES", True, (0, 255, 255))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 180)))

        font_med = pygame.font.SysFont("OCR A Extended", 42)
        info = font_med.render("EM BREVE... PEW PEW SCORES!", True, (200, 200, 255))
        tela.blit(info, info.get_rect(center=(LARGURA//2, 320)))

        font_small = pygame.font.SysFont(None, 32)
        esc_txt = font_small.render("ESC para voltar", True, (120, 120, 180))
        tela.blit(esc_txt, esc_txt.get_rect(center=(LARGURA//2, 500)))

        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            estado = ESTADO_MENU

    # ==============================================================
    # CRÉDITOS
    # ==============================================================
    elif estado == ESTADO_CREDITS:
        background.draw(tela)
        font_big = pygame.font.SysFont("OCR A Extended", 70, bold=True)
        titulo = font_big.render("CRÉDITOS", True, (255, 20, 147))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 140)))

        creditos = [
            "💻 DESENVOLVIDO POR VOCÊ",
            "🎨 ARTE: GIF ESPACIAL ÉPICO",
            "🔫 TIROS: PEW PEW NEON",
            "🚀 ENGINE: PYGAME PURO",
            "",
            "OBRIGADO POR JOGAR! ✨"
        ]
        font_cred = pygame.font.SysFont("OCR A Extended", 38)
        for i, linha in enumerate(creditos):
            cor = (0, 255, 255) if i % 2 == 0 else (255, 100, 200)
            texto = font_cred.render(linha, True, cor)
            tela.blit(texto, texto.get_rect(center=(LARGURA//2, 260 + i * 45)))

        esc_txt = pygame.font.SysFont(None, 32).render("ESC - VOLTAR AO MENU", True, (120, 120, 180))
        tela.blit(esc_txt, esc_txt.get_rect(center=(LARGURA//2, 540)))

        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in eventos):
            estado = ESTADO_MENU

    pygame.display.flip()

pygame.quit()