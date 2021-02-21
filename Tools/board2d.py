from typing import List


class Vector2:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __setattr__(self, key, value):
        raise AttributeError

    def __add__(self, other: "Vector2"):
        return Vector2(self.x + other.x, self.y + other.y)

    def __iter__(self) -> "Vector2Iterator":
        return Vector2Iterator(self)


class Vector2Iterator:
    def __init__(self, vector: Vector2):
        self.vector = vector
        self._x = 0
        self._y = 0

    def __iter__(self) -> "Vector2Iterator":
        self._x = 0
        self._y = 0
        return self

    def __next__(self) -> Vector2:
        if self._x + 1 > self.vector.x:
            self._y += 1
            self._x = 0
        if self._y + 1 > self.vector.y:
            raise StopIteration
        self._x += 1
        return Vector2(self._x, self._y)


class FieldData:
    def __init__(self):
        self.field: Optional["Field2D"] = None
        self.connected = False

    def connect(self, field: "Field2D"):
        self.field = field
        self.connected = True


class Field2D:
    __slots__ = ("board", "pos", "_field_data")
    board: "Board2D"
    pos: Vector2
    _field_data: FieldData

    def __init__(self, pos: Vector2, board: "Board2D", field_data: FieldData):
        object.__setattr__(self, "board", board)
        object.__setattr__(self, "pos", pos)
        object.__setattr__(self, "_field_data", field_data)

    def __setattr__(self, key, value):
        raise AttributeError

    @property
    def field_data(self):
        return self._field_data

    @field_data.setter
    def field_data(self, value: FieldData):
        object.__setattr__(self, "_field_data", value)
        self._field_data.connect(self)


class Board2D:
    def __init__(self, size: Vector2):
        self.board: Dict[int, Dict[int, Field2D]] = {}
        for pos in size:
            if pos.x not in self.board:
                self.board[pos.x] = {}
            self.board[pos.x][pos.y] = Field2D(pos, self, FieldData())

    def __getitem__(self, pos: Vector2):
        return self.board[pos.x][pos.y]

    def __setitem__(self, pos: Vector2, value: FieldData):
        self.board[pos.x][pos.y].field_data = value
