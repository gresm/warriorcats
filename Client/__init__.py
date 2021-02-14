import pygame

pygame.init()


class App:

    def __init__(self, title="my game", icon_path="./images/icon.png", height=300, width=300):
        self.screen = pygame.display.set_mode((height, width))
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.max_tps = 20
        self.running = True
        self.bg_color = (0, 0, 0)
        pygame.display.set_icon(pygame.image.load(icon_path))
        pygame.display.set_caption(title)
        self.draw()

    def run(self):
        while self.running:
            # checking events
            self.check_events()

            # ticking
            self.delta += self.clock.tick() / 1000
            while self.delta > 1 / self.max_tps:
                self.delta -= 1 / self.max_tps

                # drawing
                self.draw()

                # checking input
                self.check_input()

        return 0

    def check_input(self):
        keys_pressed = pygame.key.get_pressed()
        self._pass()
        return

    def _pass(self):
        return

    def draw(self):
        self.screen.fill(self.bg_color)

        pygame.display.flip()
        return

    def check_events(self):
        for event in pygame.event.get():
            # checking events
            if event.type == pygame.QUIT:
                self.running = False
        return


def main():
    app = App()
    return app.run()
