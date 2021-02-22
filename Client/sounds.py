from pygame.mixer import music


class Sound:

    def __init__(self, sound_path):
        self.__stopped = False
        self.soundPath = sound_path
        music.load(self.soundPath)
        self._stopped = False

    @property
    def stopped(self):
        return self._stopped

    @stopped.setter
    def stopped(self, val):
        self._stopped = val

    def play(self):
        self.__stopped = False
        music.play()

    def stop(self):
        music.stop()
        self._stopped = True
