import pygame
from PIL import Image  # pip install pillow
import io
import os


# =============================================
# Função para carregar todos os frames de um GIF
# =============================================
def load_gif_frames(gif_path):
    frames = []
    durations = []  # tempo em ms que cada frame deve ficar na tela

    with Image.open(gif_path) as img:
        for frame in range(img.n_frames):
            img.seek(frame)
            # Converte para RGBA se tiver transparência
            frame_img = img.convert("RGBA")

            # Pega o raw data do frame
            raw_data = frame_img.tobytes()
            size = frame_img.size

            # Cria uma surface do pygame a partir do frame
            pygame_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
            frames.append(pygame_surface)

            # Pega a duração do frame (em milissegundos)
            duration = img.info.get("duration", 100)  # padrão 100ms se não tiver
            durations.append(duration)

    return frames, durations


# =============================================
# Código principal
# =============================================
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("GIF como Background no Pygame")
clock = pygame.time.Clock()

# Carrega o GIF (coloque seu GIF na mesma pasta ou coloque o caminho completo)
gif_path = "spacegif.gif"  # <-- MUDE AQUI PARA O NOME DO SEU GIF

if not os.path.exists(gif_path):
    print(f"Arquivo {gif_path} não encontrado!")
    pygame.quit()
    exit()

frames, durations = load_gif_frames(gif_path)

# Controle da animação
frame_atual = 0
tempo_acumulado = 0

rodando = True
while rodando:
    dt = clock.tick(60)  # delta time em milissegundos
    tempo_acumulado += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Troca de frame quando o tempo do frame atual acabar
    if tempo_acumulado >= durations[frame_atual]:
        tempo_acumulado = 0
        frame_atual = (frame_atual + 1) % len(frames)

    # Desenha o frame atual como background (redimensiona para caber na tela)
    frame_redimensionado = pygame.transform.scale(
        frames[frame_atual], (LARGURA, ALTURA)
    )
    tela.blit(frame_redimensionado, (0, 0))

    # Aqui você desenha o resto do seu jogo por cima...
    # Exemplo: um texto simples
    font = pygame.font.SysFont(None, 55)
    texto = font.render("", True, (255, 255, 255))
    tela.blit(texto, (100, 100))

    pygame.display.flip()

pygame.quit()