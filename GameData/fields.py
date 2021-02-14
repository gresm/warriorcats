from typing import Any, Dict, Tuple
from Tools.board2d import *
from enum import Enum


class GameFieldTypes(Enum):
    medic_den = 0
    den = 1
    hunting = 2
    unpassable = 3
    normal = 4


class GameFieldTexture:
    def __init__(self, board: "GameBoard", texture_id: int):
        self.board: board = board
        self.texture_id: int = texture_id


class Textures:
    def __init__(self, textures: Dict[Any, Any]):
        self.textures = textures

    def get_texture(self, texture_id):
        return self.textures[texture_id]

    def has_texture(self, texture_id) -> bool:
        return texture_id in self.textures


class TexturesQueue:
    def __init__(self, texture: Textures, *args: Textures):
        self.texture: Textures = texture
        self.args: Tuple[Textures] = args

    def get_texture(self, texture_id):
        if not self.has_texture(texture_id):
            raise KeyError(str(texture_id))
        if self.texture.has_texture(texture_id):
            return self.texture.get_texture(texture_id)
        else:
            for e in self.args:
                if e.has_texture(texture_id):
                    return e.get_texture(texture_id)

    def has_texture(self, texture_id) -> bool:
        if self.has_texture(texture_id):
            return True
        for e in self.args:
            if e.has_texture(texture_id):
                return True
        return False


class TexturesRule:
    def __init__(self, left_id: int, up_id: int, right_id: int, down_id: int, texture_id: int):
        self.texture_id = texture_id
        self.down_id = down_id
        self.right_id = right_id
        self.up_id = up_id
        self.left_id = left_id


class GameField(Field2d):
    def __init__(self, x_pos: int, y_pos, obj: object, board: Board2d,
                 field_type: GameFieldTypes = GameFieldTypes.normal):
        super().__init__(x_pos, y_pos, obj, board)
        self.field_type: GameFieldTypes = field_type


class GameBoard(Board2d):
    def __init__(self, x_size: int, y_size: int, board_type: Board2dType = Board2dType.square,
                 field_class: Optional[Type[Field2d]] = None, default_args: Optional[tuple] = None,
                 default_kwargs: Optional[dict] = None):
        super().__init__(x_size, y_size, board_type, field_class, default_args, default_kwargs)
