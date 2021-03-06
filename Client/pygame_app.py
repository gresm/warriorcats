from typing import Tuple
import pygame

pygame.init()


class BaseApp:
    def __init__(self, title="my game", icon_path: str = "./images/icon.png", height: int = 300, width: int = 300,
                 bg_color: Tuple[int, int, int] = (0, 0, 0)):
        self.screen = pygame.display.set_mode((height, width))
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.max_tps = 20
        self.running = True
        self.bg_color = bg_color
        pygame.display.set_icon(pygame.image.load(icon_path))
        pygame.display.set_caption(title)
        self.draw_background()

    def run(self):
        """
        Function to run game\n
        Handles KeyboardInterrupt as exit command, but re-raises it after.
        """
        try:
            pygame.init()
            while self.running:
                # checking events
                self.check_events()

                # ticking
                self.delta += self.clock.tick() / 1000
                while self.delta > 1 / self.max_tps:
                    self.delta -= 1 / self.max_tps
                    # running loop
                    self.loop()
        except KeyboardInterrupt:
            self.on_exit()
            raise KeyboardInterrupt

        self.on_exit()
        return

    def loop(self):
        # checking events
        self.check_events()

        # drawing
        self.draw_background()
        self.draw()

        # checking input
        self.handle_input()

    def handle_input(self):
        keys_pressed = pygame.key.get_pressed()
        for i in range(len(keys_pressed)):
            if keys_pressed[i]:
                self.on_key_pressed(i)
        return

    def on_key_pressed(self, key_code: int):
        pass

    # noinspection PyMethodMayBeStatic
    def key_pressed(self, key_code: int) -> bool:
        return pygame.key.get_pressed()[key_code]

    def draw_background(self):
        self.screen.fill(self.bg_color)

        pygame.display.flip()
        return

    def on_exit(self):
        self.running = False
        pygame.quit()

    def draw(self):
        # To override
        pass

    def check_events(self):
        for event in pygame.event.get():
            # checking events
            self.handle_event(event)
        return

    def handle_event(self, event: pygame.event.Event):
        e = event.type
        if e == pygame.QUIT:
            self.on_exit()
        elif e == pygame.KEYDOWN:
            self.on_key_down(event.key)
        elif e == pygame.KEYUP:
            self.on_key_up(event.key)
        else:
            self.on_event(event)

    def on_event(self, event: pygame.event.Event):
        """
        To override.
        :param event: event
        :return: None
        """
        pass

    def on_key_down(self, key_code: int):
        """
        To override.
        :param key_code: int
        :return: None
        """
        pass

    def on_key_up(self, key_code: int):
        """
        To override.
        :param key_code: int
        :return: None
        """
        pass
