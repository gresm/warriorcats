from Tools import counter as c


class Cat:
    def __init__(self, skills: "Skills", name: "Name", clan: "Clan" = None):
        self.skills: "Skills" = skills
        self.name: Name = name
        self.clan: "Clan" = clan

    def join_clan(self, clan: "Clan"):
        self.clan = clan

    def get_name(self) -> str:
        return str(self.name)

    def __hash__(self):
        return super(Cat, self).__hash__()

    def __eq__(self, other):
        return self is other


class Name:
    def __init__(self, first_name: str, prefix: str):
        self.first_name = first_name
        self.prefix = prefix

    def __str__(self):
        return f"{self.first_name} {self.prefix}"


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

    def add_cat(self, cat: Cat):
        self.cats[cat.get_name()] = cat
