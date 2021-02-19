from . import pygame_app as app


class Game(app.App):
    pass


def main():
    game = Game()
    game.run()
