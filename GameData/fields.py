import random
from typing import Dict, Optional, List
from Tools import board2d as b2
from . import cat_data as cd
from enum import Enum


class EnteringDirection(Enum):
    left = 0
    right = 1
    up = 2
    down = 3


class GameFieldData(b2.FieldData):
    def __init__(self):
        super().__init__()
        self.cats: Dict[cd.Name, cd.Cat] = {}
        self.clan_bel: Optional[cd.Clan] = None
        self.protected_by: Optional[cd.Cat] = None

    def _enter(self, cat: cd.Cat):
        self.cats[cat.name] = cat
        self.clan_bel = cat.clan

    def _exit(self, cat):
        del self.cats[cat.name]

    def enter(self, cat: cd.Cat, enter_dir: EnteringDirection) -> bool:
        if self.can_enter(cat, enter_dir):
            self._enter(cat)
            return True
        return False

    def can_enter(self, cat: cd.Cat, enter_dir: EnteringDirection) -> bool:
        if self.clan_bel and self.clan_bel is cat.clan:
            return True
        elif not self.protected_by and len(self.cats) == 0:
            return True
        return False

    def exit(self, cat):
        self._exit(cat)


# types of Fields:
# Camp, Hunting, Den, Medic Den

class CampField(GameFieldData):

    def __init__(self, walls):
        super(CampField, self).__init__()
        self.walls: List[bool] = walls

    def can_enter(self, cat: cd.Cat, enter_dir: EnteringDirection) -> bool:
        if self.clan_bel and self.clan_bel is cat.clan and self.walls[enter_dir.value]:
            return True
        elif not self.protected_by:
            return True
        return False


class HuntingField(GameFieldData):

    @staticmethod
    def hunt(cat: cd.Cat):
        cat.stats.hunting.move_by(random.randint(1, 3))

    def can_enter(self, cat: cd.Cat, enter_dir: EnteringDirection) -> bool:
        return True


# TODO
class DenField(GameFieldData):
    pass


# TODO
class MedicDenField(DenField):
    pass
