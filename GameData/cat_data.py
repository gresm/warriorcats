from Tools import counter
from typing import Dict
from fields import HuntingField


class Health:
    def __init__(self, max_h):
        self.max_h = max_h
        self.health = counter.Counter(0, max_h)
        self._alive: bool = True

    @property
    def alive(self):
        if self.health.count == 0:
            self._alive = False
        else:
            self._alive = True
        return self._alive

    @alive.setter
    def alive(self, v):
        self._alive = v

    def update(self):
        self.alive = self.health.count >= 0

    def damage(self):
        self.update()
        if self.alive:
            self.health.back()


class Stats:
    def __init__(self, max_health: int, stat_points: int):
        self.max_health = max_health
        self.stat_points = stat_points
        self.health = Health(max_health)
        self.connected_stats = counter.LinkedCounters(0, stat_points)
        self.fighting = self.connected_stats.set_counter("Hunting", counter.Counter(0, stat_points))
        self.hunting = self.connected_stats.set_counter("Fighting", counter.Counter(0, stat_points))
        self.can_heal = False


class Name:
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        object.__hash__(self)

    def __eq__(self, other):
        return self is other


class Clan:
    def __init__(self):
        self.cats: Dict[Name, "Cat"] = {}
        self.herbs = counter.Counter(0, -1)
        self.prey = counter.Counter(0, -1)

    def add_cat(self, cat: "Cat"):
        self.cats[cat.name] = cat
        cat.clan._del_cat(cat)
        cat.clan = self

    def _del_cat(self, cat):
        del self.cats[cat.name]


class Cat:
    def __init__(self, name: Name, stats: Stats, clan: Clan):
        self.name = name
        self.stats = stats
        self.clan = clan
        clan.add_cat(self)

    def hunt(self, filed: HuntingField):
        filed.hunt(self)
