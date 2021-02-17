from typing import Optional, Type, List
from enum import Enum
from image import Texture2d



class Vector2:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __setattr__(self, key, value):
        raise NotImplemented

    def __add__(self, other: "Vector2"):
        return Vector2(self.x + other.x, self.y + other.y)


class Field2d:
    def __init__(self, x_pos: int, y_pos, obj: object, board: "Board2d"):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.obj = obj
        self.board = board

    def set_obj(self, new_obj: object):
        self.obj = new_obj


class InvulnerableField2D(Field2d):
    def __setattr__(self, key, value):
        pass


class Board2dType(Enum):
    square = 0
    fake_inf = 1
    torus = 2


class Board2dOverRangeError(Exception):
    pass


class Board2d:
    def __init__(self, x_size: int, y_size: int, board_type: Board2dType = Board2dType.square,
                 field_class: Optional[Type[Field2d]] = None, default_args: Optional[tuple] = None,
                 default_kwargs: Optional[dict] = None):
        self.x_size = x_size
        self.y_size = y_size
        self.board_type: Board2dType = board_type
        self.default_field_class: Type[Field2d]
        if not field_class:
            self.default_field_class = Field2d
        elif issubclass(field_class, Field2d):
            self.default_field_class = field_class
        else:
            raise ValueError("field_class must be")
        self.default_args: tuple
        if default_args:
            self.default_args = default_args
        else:
            self.default_args = ()
        self.default_kwargs: dict
        if default_kwargs:
            self.default_kwargs = default_kwargs
        else:
            self.default_kwargs = {}
        self.board = self.generate_board()

    def generate_board(self) -> List[List[Field2d]]:
        new_board: List[List[Field2d]] = []
        for x in range(self.x_size):
            new_line = []
            for y in range(self.y_size):
                obj = self.default_field_class.__new__(self.default_field_class)
                obj.__init__(x, y, None, self)
                new_line.append(obj)
            new_board.append(new_line)
        return new_board

    def is_in_range(self, x_pos: int, y_pos: int) -> bool:
        return self.x_size >= x_pos > 0 and self.y_size >= y_pos > 0

    def get_field(self, x_pos: int, y_pos: int) -> Field2d:
        if self.is_in_range(x_pos, y_pos):
            return self.board[x_pos - 1][y_pos - 1]
        elif self.board_type == Board2dType.square:
            raise Board2dOverRangeError()
        elif self.board_type == Board2dType.torus:
            return self.get_field((x_pos % self.x_size) + 1, (y_pos % self.y_size) + 1)
        elif self.board_type == Board2dType.fake_inf:
            obj = self.default_field_class.__new__(self.default_field_class)
            obj.__init__(x_pos, y_pos, None, self)
            return obj
        else:
            raise ValueError("Invalid board_type")

    def set_field(self, x_pos: int, y_pos: int, obj: object):
        if self.is_in_range(x_pos, y_pos):
            self.board[x_pos][y_pos].set_obj(obj)
        elif self.board_type == Board2dType.square:
            raise Board2dOverRangeError()
        elif self.board_type == Board2dType.torus:
            self.set_field((x_pos % self.x_size) + 1, (y_pos % self.y_size) + 1, obj)
        elif self.board_type == Board2dType.fake_inf:
            pass
        else:
            raise ValueError("Invalid board_type")


class FiledObj:

    def __init__(self):
        self.can_walk_into = False


class Wall(FiledObj):

    def __init__(self, texture: Texture2d):
        super(Wall, self).__init__()
        self.can_walk_into = True
        self.texture = texture
