import pygame
from pygame.mixer import music

pygame.init()


class Sound:

    def __init__(self, sound_path):
        self.soundPath = sound_path
        self.misc = music.load(self.soundPath)
        self.__stopped = False

    @property
    def stopped(self):
        return self.__stopped

    def play(self):
        self.__stopped = False
        self.misc.play()

    def stop(self):
        self.misc.stop()
        self.__stopped = True
