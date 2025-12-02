# SoundManager.py - SONS + MÚSICA GERADA AUTOMATICAMENTE (SEM ARQUIVOS!)
import pygame
import math
import array
import random


class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

        self.shot_sound = None
        self.explosion_sound = None
        self.menu_music_data = None
        self.game_music_data = None

        self.load_sounds()

    def load_sounds(self):
        # Sons de efeito (com fallback)
        try:
            self.shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
            self.shot_sound.set_volume(0.2)
        except:
            self.shot_sound = self._generate_pew()

        try:
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
            self.explosion_sound.set_volume(0.3)
        except:
            self.explosion_sound = self._generate_boom()

        # GERA MÚSICA AUTOMATICAMENTE!
        self.menu_music_data = self._generate_menu_music()
        self.game_music_data = self._generate_game_music()

    # === SONS DE EFEITO ===
    def _generate_pew(self):
        sample_rate = 22050
        duration = 0.11
        frames = int(duration * sample_rate)
        arr = array.array('h', [0] * frames)
        for i in range(frames):
            t = i / sample_rate
            env = 1.0 - (t / duration)
            wave = math.sin(2 * math.pi * 1200 * t) * env
            arr[i] = int(32767 * 0.3 * wave)
        return pygame.mixer.Sound(buffer=arr)

    def _generate_boom(self):
        sample_rate = 22050
        duration = 0.35
        frames = int(duration * sample_rate)
        arr = array.array('h', [0] * frames)
        for i in range(frames):
            t = i / sample_rate
            freq = 150 * (1 - t * 2)
            noise = random.randint(-6000, 6000)
            wave = math.sin(2 * math.pi * freq * t) * (1 - t * 2.8)
            val = int(32767 * 0.25 * wave + noise)
            val = max(-32767, min(32767, val))
            arr[i] = val
        return pygame.mixer.Sound(buffer=arr)

    # === MÚSICA DO MENU (calma, misteriosa) ===
    def _generate_menu_music(self):
        sample_rate = 22050
        duration = 60  # 60 segundos (loop)
        frames = int(duration * sample_rate)
        arr = array.array('h', [0] * frames)
        notes = [440, 494, 554, 587, 659]  # A4, B4, C#5, D5, E5
        for i in range(frames):
            t = i / sample_rate
            beat = int(t * 0.5) % len(notes)  # troca nota a cada 2 segundos
            freq = notes[beat]
            wave = math.sin(2 * math.pi * freq * t) * 0.1
            arr[i] = int(32767 * wave)
        return pygame.mixer.Sound(buffer=arr)

    # === MÚSICA DO JOGO (intensa, 8-bit style) ===
    def _generate_game_music(self):
        sample_rate = 22050
        duration = 90  # 90 segundos
        frames = int(duration * sample_rate)
        arr = array.array('h', [0] * frames)
        pattern = [0, 0, 0, 1, 0, 0, 1, 0]  # ritmo simples
        base_freq = 220
        for i in range(frames):
            t = i / sample_rate
            beat = int(t * 4) % 8  # 4 batidas por segundo
            if pattern[beat]:
                freq = base_freq * (2 ** (beat % 4))
            else:
                freq = base_freq * 1.5
            wave = math.sin(2 * math.pi * freq * t) * 0.15
            noise = random.randint(-2000, 2000) if random.random() < 0.1 else 0
            val = int(32767 * wave + noise)
            val = max(-32767, min(32767, val))
            arr[i] = val
        return pygame.mixer.Sound(buffer=arr)

    # === MÉTODOS PÚBLICOS ===
    def play_shot(self):
        if self.shot_sound:
            self.shot_sound.play()

    def play_explosion(self):
        if self.explosion_sound:
            self.explosion_sound.play()

    def play_menu_music(self):
        if self.menu_music_data:
            self.menu_music_data.play(-1)  # loop infinito

    def play_game_music(self):
        if self.game_music_data:
            self.game_music_data.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()