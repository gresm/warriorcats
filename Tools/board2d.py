from typing import List


class Vector2:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __setattr__(self, key, value):
        raise NotImplemented

    def __add__(self, other: "Vector2"):
        return Vector2(self.x + other.x, self.y + other.y)


class Field2D:
    def __init__(self, x_pos: int, y_pos: int, board: "Board2D"):
        self.board = board
        self.y_pos = y_pos
        self.x_pos = x_pos


class Board2D:
    def __init__(self, size_x: int, size_y: int):
        self.board: List[List] = [[Field2D(x, y, self) for x in range(size_x)] for y in range(size_y)]

    def __getitem__(self, xy):
        return self.board[xy[0]][xy[1]]
