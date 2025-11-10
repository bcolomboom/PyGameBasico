import pygame
import sys
import os

# Inicialização
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Shooter - Menu")

# Cores (RGB)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL_ESCURO = (0, 10, 30)
AZUL_NEON = (0, 200, 255)
VERDE_NEON = (0, 255, 100)
VERMELHO = (255, 50, 50)

# Fonte
# === SUBSTITUA TODAS AS FONTES POR AGENCY FB ===
FONTE_TITULO = pygame.font.SysFont("Agency FB", 78, bold=True)
FONTE_MENU = pygame.font.SysFont("Agency FB", 52, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Agency FB", 32)
FONTE_MINI = pygame.font.SysFont("Agency FB", 24)

# Imagens (opcional - crie pastas ou use retângulos coloridos)
PASTA_IMAGENS = "imagens"
if not os.path.exists(PASTA_IMAGENS):
    os.makedirs(PASTA_IMAGENS)

# Fundo estrelado (simulado com pontos)
def desenhar_estrelas(surface):
    for _ in range(200):
        x = pygame.time.get_ticks() % 3000 // 10 % LARGURA
        y = pygame.time.get_ticks() % 3000 // 15 % ALTURA
        pygame.draw.circle(surface, BRANCO, (x, y), 1)

class TextoBotao:
    def __init__(self, x, y, texto, acao, tamanho_normal=52, cor_normal=BRANCO, cor_hover=AZUL_NEON):
        self.x = x
        self.y = y
        self.texto = texto
        self.acao = acao
        self.tamanho_normal = tamanho_normal
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.fonte_normal = pygame.font.SysFont("Agency FB", tamanho_normal, bold=True)
        self.fonte_hover = pygame.font.SysFont("Agency FB", int(tamanho_normal), bold=False)
        self.clique_ativado = False

    def desenhar(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        texto_surf = self.fonte_normal.render(self.texto, True, self.cor_normal)
        texto_rect = texto_surf.get_rect(center=(self.x, self.y))

        # Hover: muda cor e aumenta fonte
        if texto_rect.collidepoint(mouse_pos):
            texto_surf = self.fonte_hover.render(self.texto, True, self.cor_hover)
            texto_rect = texto_surf.get_rect(center=(self.x, self.y))
            # Opcional: efeito de glow
            self._desenhar_glow(surface, texto_surf, texto_rect)
        else:
            self.clique_ativado = False

        surface.blit(texto_surf, texto_rect)
        return texto_rect  # retorna o retângulo para clique

    def _desenhar_glow(self, surface, texto_surf, rect, intensidade=3):
        """Efeito neon ao redor do texto"""
        for dx in range(-intensidade, intensidade + 1):
            for dy in range(-intensidade, intensidade + 1):
                if dx*dx + dy*dy < intensidade*intensidade:
                    surface.blit(texto_surf, (rect.x + dx, rect.y + dy))

    def clicou(self, rect):
        if rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.clique_ativado:
                self.clique_ativado = True
                return True
        return False

# Telas
def tela_boas_vindas():
    clock = pygame.time.Clock()
    titulo = FONTE_TITULO.render("SPACE WARS", True, AZUL_NEON)
    subtitulo = FONTE_PEQUENA.render("Defenda a galáxia dos invasores!", True, BRANCO)

    # Botões de texto puro
    btn_jogar = TextoBotao(LARGURA//2, 280, "JOGAR", "jogar", 56, BRANCO, VERDE_NEON)
    btn_instrucoes = TextoBotao(LARGURA//2, 360, "INSTRUÇÕES", "instrucoes", 48, BRANCO, AZUL_NEON)
    btn_creditos = TextoBotao(LARGURA//2, 440, "CRÉDITOS", "creditos", 48, BRANCO, AZUL_NEON)
    btn_sair = TextoBotao(LARGURA//2, 520, "SAIR", "sair", 56, BRANCO, VERMELHO)

    botoes = [btn_jogar, btn_instrucoes, btn_creditos, btn_sair]

    while True:
        TELA.fill(PRETO)
        desenhar_estrelas(TELA)

        # Título
        TELA.blit(titulo, titulo.get_rect(center=(LARGURA//2, 100)))
        TELA.blit(subtitulo, subtitulo.get_rect(center=(LARGURA//2, 160)))

        # Desenha e verifica clique
        for btn in botoes:
            rect = btn.desenhar(TELA)
            if btn.clicou(rect):
                pygame.time.delay(200)
                return btn.acao

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def tela_instrucoes():
    clock = pygame.time.Clock()
    linhas = [
        "INSTRUÇÕES",
        "",
        "Use as SETAS ← → para mover a nave",
        "Pressione ESPAÇO para atirar",
        "Evite os inimigos e seus projéteis",
        "Colete power-ups para ficar mais forte!",
        "",
        "Pressione ESC para voltar"
    ]

    while True:
        TELA.fill(PRETO)
        desenhar_estrelas(TELA)

        y = 100
        for i, linha in enumerate(linhas):
            cor = AZUL_NEON if i == 0 else BRANCO
            fonte = FONTE_MENU if i == 0 else FONTE_PEQUENA
            texto = fonte.render(linha, True, cor)
            TELA.blit(texto, texto.get_rect(center=(LARGURA//2, y)))
            y += 50 if i == 0 else 40

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(60)

def tela_creditos():
    clock = pygame.time.Clock()
    creditos = [
        "CRÉDITOS",
        "",
        "Desenvolvedor: [SEU NOME]",
        "Engine: Pygame",
        "Música: OpenGameArt.org",
        "Arte: Kenney.nl",
        "",
        "Obrigado por jogar!",
        "",
        "Pressione ESC para voltar"
    ]

    while True:
        TELA.fill(PRETO)
        desenhar_estrelas(TELA)

        y = 100
        for i, linha in enumerate(creditos):
            cor = VERDE_NEON if i == 0 else BRANCO
            fonte = FONTE_MENU if i == 0 else FONTE_PEQUENA
            texto = fonte.render(linha, True, cor)
            TELA.blit(texto, texto.get_rect(center=(LARGURA//2, y)))
            y += 50 if i == 0 else 40

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(60)

# Loop principal do menu
def main():
    while True:
        acao = tela_boas_vindas()

        if acao == "jogar":
            print("Iniciando o jogo... (aqui você chama sua função de jogo)")
            # Chame aqui: jogar_space_shooter()
            pygame.time.delay(500)
            # Exemplo: break ou chamar função do jogo

        elif acao == "instrucoes":
            tela_instrucoes()

        elif acao == "creditos":
            tela_creditos()

        elif acao == "sair":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()