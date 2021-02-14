from Tools import counter


class BaseCat:
    def __init__(self, max_health: int):
        pass


class Health:
    def __init__(self, max_h):
        self.max_h = max_h
        self.health = counter.Counter(0, max_h)
        self.alive: bool = True

    def update(self):
        self.alive = self.health.count >= 0

    def damage(self):
        self


class Stats:
    def __init__(self, max_health):
        self.health = Health(max_health)
