import pygame

pygame.init()


class Texture2d:

    def __init__(self, path):
        self.image = pygame.image.load(path)

    def draw(self, screen, position: pygame.Rect):
        screen.blit(self.image, position)
