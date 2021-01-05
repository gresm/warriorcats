from Tools import counter


class Skills:
    def __init__(self, max_health: int = 3):
        self.health = counter.Counter(0, max_health)


class Cat:
    def __init__(self):
        self.health = counter.Counter(0, 3)
        #self.
