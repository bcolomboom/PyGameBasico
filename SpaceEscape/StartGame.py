# start_screen.py
import pygame

class StartScreen:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background  # recebe o fundo animado
        self.font_grande = pygame.font.SysFont("OCR A Extended", 68, bold=True)
        self.font_pequena = pygame.font.SysFont("OCR A Extended", 40)
        self.cor_texto = (0, 255, 255)
        self.cor_sombra = (0, 100, 100)
        self.cor_pisca = (255, 0, 0)

    def draw(self):
        # Desenha o fundo animado normalmente
        self.background.draw(self.screen)

        # Título com sombra
        titulo = self.font_grande.render("MEU JOGO ESPACIAL", True, self.cor_texto)
        sombra_titulo = self.font_grande.render("MEU JOGO ESPACIAL", True, self.cor_sombra)
        rect_titulo = titulo.get_rect(center=(400, 200))

        self.screen.blit(sombra_titulo, (rect_titulo.x + 5, rect_titulo.y + 5))
        self.screen.blit(titulo, rect_titulo)

        # Instrução
        instrucao = self.font_pequena.render("Pressione ENTER para começar", True, self.cor_texto)
        rect_inst = instrucao.get_rect(center=(400, 400))
        self.screen.blit(instrucao, rect_inst)

        # Pisca o texto (efeito bonito)
        if pygame.time.get_ticks() % 1000 < 500:
            pisca = self.font_pequena.render("Pressione ENTER para começar", True, (255, 0, 100))
            self.screen.blit(pisca, rect_inst)