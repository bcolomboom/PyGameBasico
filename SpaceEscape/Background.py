import pygame
from PIL import Image
import os


class AnimatedBackground:
    def __init__(self, gif_path, screen_width, screen_height, rotacionar_180=False):
        self.frames, self.durations = self.load_gif_frames(gif_path)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rotacionar_180 = rotacionar_180

        # Pré-redimensiona todos os frames (melhor performance)
        self.scaled_frames = []
        for frame in self.frames:
            scaled = pygame.transform.scale(frame, (screen_width, screen_height))
            if self.rotacionar_180:
                scaled = pygame.transform.rotate(scaled, 180)  # <<< gira 180°
            self.scaled_frames.append(scaled)

        self.current_frame = 0
        self.timer = 0

    def load_gif_frames(self, gif_path):
        frames = []
        durations = []
        with Image.open(gif_path) as img:
            for frame_idx in range(img.n_frames):
                img.seek(frame_idx)
                frame_img = img.convert("RGBA")
                raw_data = frame_img.tobytes()
                size = frame_img.size
                pygame_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
                frames.append(pygame_surface)
                durations.append(img.info.get("duration", 100))
        return frames, durations

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.durations[self.current_frame]:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)


    def draw(self, screen):
        screen.blit(self.scaled_frames[self.current_frame], (0, 0))