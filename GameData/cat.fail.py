from typing import Dict
from Tools import counter as c
from enum import Enum
import copy


class GameError(Exception):
    pass


class CatSearchingError(GameError):
    pass


class CatGender(Enum):
    male = 0
    female = 1


class Cat:
    def __init__(self, skills: "Skills", name: "Name", gender: CatGender, clan: "Clan"):
        self.skills: "Skills" = skills
        self.name: Name = name
        self.gender: CatGender = gender
        self.clan: "Clan" = clan
        self.is_frozen: bool = False

    def _check_editing(self):
        if self.is_frozen:
            raise GameError("This cat is frozen")

    def freeze(self):
        self._check_editing()
        self.is_frozen = True

    def join_clan(self, clan: "Clan"):
        self._check_editing()
        self.clan.on_cat_leaving(self)
        self.clan = clan
        clan.on_cat_joining(self)

    def get_name(self) -> str:
        return str(self.name)

    def take_damage(self):
        self._check_editing()
        try:
            self.skills.take_damage()
        except c.CounterOutOfRangeError:
            self.kill()

    def kill(self):
        self.freeze()

    def __hash__(self):
        return super(Cat, self).__hash__()

    def __eq__(self, other):
        return self is other


class Kitten(Cat):
    def __init__(self, name: "Name", gender: CatGender, clan: "Clan"):
        skills = Skills(2, False, False, can_move=False)
        super().__init__(skills, name, gender, clan)


class Paw(Cat):
    def __init__(self, name: "Name", gender: CatGender, clan: "Clan"):
        skills = Skills(3, False, True)
        super().__init__(skills, name, gender, clan)


class MedicPaw(Cat):
    def __init__(self, name: "Name", gender: CatGender, clan: "Clan"):
        skills = Skills(3, False, True, 1, 1, 1, True, False, True)
        super().__init__(skills, name, gender, clan)


class Name:
    def __init__(self, first_name: str, prefix: str = None):
        self.first_name = first_name
        self.prefix = prefix

    def __str__(self):
        return f"{self.first_name} {self.prefix}"

    def __hash__(self):
        return super(Name, self).__hash__()

    def __eq__(self, other):
        return self is other


class Skills:
    def __init__(self, max_health: int = 3, can_learn: bool = False, can_learn_code: bool = False,
                 max_stat_points: int = 4, max_hunting: int = 3, max_fighting: int = 3, can_move: bool = True,
                 can_heal: bool = False, can_learn_healing: bool = False):
        self.can_learn_healing = can_learn_healing
        self.can_heal = can_heal
        self.learned_healing: bool = False
        self.max_stat_points: int = max_stat_points
        self.max_fighting = max_fighting
        self.max_hunting = max_hunting
        self.max_health: int = max_health
        self.can_learn: bool = can_learn
        self.can_learn_code: bool = can_learn_code
        self.learned_code: bool = False
        self.can_move: bool = can_move
        self.health: c.Counter = c.Counter(0, self.max_health)
        self.stats: c.LinkedCounters = c.LinkedCounters(0, self.max_stat_points)
        self.fighting: c.LinkedCounter = self.stats.set_counter("fighting", c.Counter(0, self.max_fighting))
        self.hunting: c.LinkedCounter = self.stats.set_counter("hunting", c.Counter(0, self.max_hunting))

    def update(self):
        self.health = c.Counter(0, self.max_health)
        self.stats = c.LinkedCounters(0, self.max_stat_points)
        self.fighting = self.stats.set_counter("fighting", c.Counter(0, self.max_fighting))
        self.hunting = self.stats.set_counter("hunting", c.Counter(0, self.max_hunting))

    def take_damage(self):
        self.health.back()

    def learn_code(self):
        if self.can_learn_code:
            self.learned_code = True
            self.can_learn = True

    def learn_hunting(self):
        if self.can_learn:
            self.hunting.step()

    def learn_healing(self):
        if self.can_learn_healing:
            self.learned_healing = True

    def clone(self):
        return copy.deepcopy(self)


class Clan:
    def __init__(self, name: str):
        self.name = name
        self.herbs = c.Counter(0, -1)
        self.prey = c.Counter(0, -1)
        self.cats: Dict[Name, Cat] = {}
        self.is_frozen: bool = False

    def _check_editing(self):
        if self.is_frozen:
            raise GameError("This clan is frozen")

    def freeze(self):
        self.is_frozen = True
        for cat_name in self.cats:
            self.cats[cat_name].freeze()

    def add_cat(self, cat: Cat):
        self._check_editing()
        self.cats[cat.name] = cat
        if cat.clan is not self:
            cat.join_clan(self)

    def get_cat(self, cat_name: Name) -> Cat:
        if cat_name in self.cats:
            return self.cats[cat_name]
        raise CatSearchingError("Cat not found")

    def get_cat_by_name(self, cat_str_name: str) -> Cat:
        for e in self.cats:
            if str(e) == cat_str_name:
                return self.cats[e]
        raise CatSearchingError("Cat not found")

    def on_cat_joining(self, cat: Cat):
        self._check_editing()
        self.add_cat(cat)

    def on_cat_leaving(self, cat: Cat):
        self._check_editing()
        if cat.name in self.cats:
            del self.cats[cat.name]

    def register(self):
        Game.instance.add_clan(self)


class Game:
    instance: "Game" = None

    def __init__(self):
        self.instance = self.instance or self
        self.clans: Dict[str, Clan] = {}

    def add_clan(self, clan: Clan):
        self.clans[clan.name] = clan

    def get_clan(self, clan_name: str) -> Clan:
        if clan_name in self.clans:
            return self.clans[clan_name]
        raise GameError("Couldn't find clan.")
