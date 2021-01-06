from Tools import counter as c


class Cat:
    def __init__(self, skills: "Skills", name, clan: "Clan" = None):
        self.skills = skills
        self.name = name
        self.clan = clan


class Skills:
    def __init__(self, max_health: int = 3, max_stat_points: int = 4, max_hunting: int = 3, max_fighting: int = 3):
        self.max_stat_points: int = max_stat_points
        self.max_fighting = max_fighting
        self.max_hunting = max_hunting
        self.max_health: int = max_health
        self.health: c.Counter = c.Counter(0, self.max_health)
        self.stats: c.LinkedCounters = c.LinkedCounters(0, self.max_stat_points)
        self.fighting: c.LinkedCounter = self.stats.set_counter("fighting", c.Counter(0, self.max_fighting))
        self.hunting: c.LinkedCounter = self.stats.set_counter("hunting", c.Counter(0, self.max_hunting))

    def update(self):
        self.health = c.Counter(0, self.max_health)
        self.stats = c.LinkedCounters(0, self.max_stat_points)
        self.fighting = self.stats.set_counter("fighting", c.Counter(0, self.max_fighting))
        self.hunting = self.stats.set_counter("hunting", c.Counter(0, self.max_hunting))


class Clan:
    def __init__(self, name: str):
        self.name = name
        self.herbs = c.Counter(0, -1)
        self.prey = c.Counter(0, -1)
        self.cats = {}
