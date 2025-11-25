# StartGame.py
import pygame

class StartScreen:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        # Fontes
        self.font_title = pygame.font.SysFont("OCR A Extended", 68, bold=True)
        self.font_big = pygame.font.SysFont("OCR A Extended", 60, bold=True)
        self.font_menu = pygame.font.SysFont("OCR A Extended", 50)
        self.font_small = pygame.font.SysFont("OCR A Extended", 34)

        # Cores neon
        self.cyan = (0, 255, 255)
        self.magenta = (255, 20, 147)
        self.white = (255, 255, 255)
        self.gray = (120, 120, 160)
        self.shadow = (0, 80, 100)

        # Estados do menu
        self.state = "press_enter"          # press_enter → main → play_sub → control_select
        self.selected_main = 0              # 0=PLAY, 1=HIGHSCORES, 2=CREDITS
        self.selected_player = 0            # 0=1P, 1=2P
        self.selected_control = 0           # 0=TECLADO, 1=MOUSE

    def handle_events(self, events):
        if self.state == "press_enter":
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    self.state = "main"
            return None

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.state == "control_select":
                        self.state = "play_sub"
                    elif self.state == "play_sub":
                        self.state = "main"
                    else:
                        return "quit"
                    continue

                if e.key == pygame.K_UP:
                    if self.state == "main":
                        self.selected_main = (self.selected_main - 1) % 3
                    elif self.state == "play_sub":
                        self.selected_player = (self.selected_player - 1) % 2
                    elif self.state == "control_select":
                        self.selected_control = (self.selected_control - 1) % 2

                elif e.key == pygame.K_DOWN:
                    if self.state == "main":
                        self.selected_main = (self.selected_main + 1) % 3
                    elif self.state == "play_sub":
                        self.selected_player = (self.selected_player + 1) % 2
                    elif self.state == "control_select":
                        self.selected_control = (self.selected_control + 1) % 2

                elif e.key == pygame.K_RETURN:
                    return self.select_option()

        return None

    def select_option(self):
        if self.state == "main":
            if self.selected_main == 0:
                self.state = "play_sub"
            elif self.selected_main == 1:
                return "highscores"
            elif self.selected_main == 2:
                return "credits"

        elif self.state == "play_sub":
            if self.selected_player == 0:  # 1P
                self.state = "control_select"
                self.selected_control = 0
            else:  # 2P
                return "2p"  # vai direto pro jogo 2 jogadores

        elif self.state == "control_select":
            control = "keyboard" if self.selected_control == 0 else "mouse"
            return f"1p_{control}"  # retorna "1p_keyboard" ou "1p_mouse"

        return None

    def draw_selector_box(self, rect):
        t = pygame.time.get_ticks() / 800
        pulse = 4 + int(abs((t % 2) - 1) * 6)
        color = self.magenta if (t % 1) < 0.5 else self.cyan
        big = rect.inflate(36 + pulse, 24 + pulse)
        pygame.draw.rect(self.screen, color, big, width=5, border_radius=10)

    def draw(self):
        self.background.draw(self.screen)
        cx = self.WIDTH // 2
        cy = self.HEIGHT // 2

        # === PRESS ENTER ===
        if self.state == "press_enter":
            title = self.font_title.render("MEU JOGO ESPACIAL", True, self.cyan)
            shadow = self.font_title.render("MEU JOGO ESPACIAL", True, self.shadow)
            tr = title.get_rect(center=(cx, 160))
            self.screen.blit(shadow, (tr.x + 6, tr.y + 6))
            self.screen.blit(title, tr)

            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            press = self.font_big.render("PRESS ENTER", True, self.magenta if blink else self.cyan)
            pr = press.get_rect(center=(cx, 360))
            self.screen.blit(press, pr)

        # === MENU PRINCIPAL ===
        elif self.state == "main":
            options = ["PLAY", "HIGHSCORES", "CREDITS"]
            for i, txt in enumerate(options):
                y = 240 + i * 80
                color = self.magenta if i == self.selected_main else self.gray
                surf = self.font_menu.render(txt, True, color)
                r = surf.get_rect(center=(cx, y))
                self.screen.blit(surf, r)
                if i == self.selected_main:
                    self.draw_selector_box(r)

        # === SUBMENU PLAY (1P / 2P) ===
        elif self.state == "play_sub":
            play = self.font_big.render("PLAY", True, self.cyan)
            self.screen.blit(play, play.get_rect(center=(cx, 200)))

            for i, txt in enumerate(["1P", "2P"]):
                y = 300 + i * 80
                color = self.magenta if i == self.selected_player else self.white
                surf = self.font_menu.render(txt, True, color)
                r = surf.get_rect(center=(cx, y))
                self.screen.blit(surf, r)
                if i == self.selected_player:
                    self.draw_selector_box(r)

        # === TELA DE CONTROLE (só 1P) ===
        elif self.state == "control_select":
            title = self.font_big.render("CONTROLES", True, self.cyan)
            self.screen.blit(title, title.get_rect(center=(cx, 180)))

            subtitle = self.font_menu.render("Escolha como jogar:", True, self.gray)
            self.screen.blit(subtitle, subtitle.get_rect(center=(cx, 240)))

            options = ["TECLADO", "MOUSE"]
            for i, txt in enumerate(options):
                y = 340 + i * 80
                color = self.magenta if i == self.selected_control else self.white
                surf = self.font_menu.render(txt, True, color)
                r = surf.get_rect(center=(cx, y))
                self.screen.blit(surf, r)
                if i == self.selected_control:
                    self.draw_selector_box(r)

        # Rodapé
        footer = self.font_small.render("↑↓ NAVEGAR    ENTER SELECIONAR    ESC VOLTAR", True, (70, 70, 120))
        fr = footer.get_rect(center=(cx, self.HEIGHT - 40))
        self.screen.blit(footer, fr)