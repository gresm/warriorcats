import pygame


class Texture2d:

    def __init__(self, path):
        self.image = pygame.image.load(path)
