# import copy
from typing import Dict, Union


class CounterOutOfRangeError(Exception):
    pass


class LinkedCountersOutOfTotalRangeError(Exception):
    pass


class Counter:
    def __init__(self, beg: int, end: int):
        self.min = beg
        self.max = end
        self.count = self.min

    def move_by(self, steps: int):
        if (self.min <= self.count + steps or self.min == -1) and (self.count + steps <= self.max or self.max == -1):
            self.count += steps
            return self.count
        raise CounterOutOfRangeError

    def step(self):
        return self.move_by(1)

    def back(self):
        return self.move_by(-1)

    def reset(self):
        self.count = self.min
        return self.count

    def set_pos(self, pos: int):
        if self.min <= pos <= self.max:
            self.count = pos
            return self.count
        raise CounterOutOfRangeError


class LinkedCounters:
    counters: Dict[Union[str, int], Counter]

    def __init__(self, beg, end):
        self.counters = {}
        self.min = beg
        self.max = end

    def get_sum(self):
        s = 0
        for i in self.counters:
            s += self.counters[i].count
        return s

    def validate(self, add_val: int):
        if not ((self.min == -1 or self.min <= self.get_sum() + add_val) and (self.max == -1 or
                                                                              self.get_sum() + add_val <= self.max)):
            raise LinkedCountersOutOfTotalRangeError
        return

    def get_counter(self, counter_id):
        if counter_id in self.counters:
            return LinkedCounter(counter_id, self)
        return None

    def _get_counter(self, counter_id):
        if counter_id in self.counters:
            return self.counters[counter_id]
        return None

    def set_counter(self, counter_id, counter: Counter):
        self.counters[counter_id] = counter
        return LinkedCounter(counter_id, self)

    def remove_counter(self, counter_id):
        del self.counters[counter_id]

    def move_by(self, counter_id, steps: int):
        self.validate(steps)
        return self._get_counter(counter_id).move_by(steps)

    def step(self, counter_id):
        self.validate(1)
        return self._get_counter(counter_id).step()

    def back(self, counter_id):
        self.validate(-1)
        return self._get_counter(counter_id).back()

    def reset(self, counter_id):
        return self._get_counter(counter_id).reset()

    def set_pos(self, counter_id, pos):
        self.validate(pos)
        return self._get_counter(counter_id).set_pos(pos)


class LinkedCounter:
    def __init__(self, counter_id: str, counters: LinkedCounters):
        self.counter_id = counter_id
        self.counters = counters

    def move_by(self, steps: int):
        return self.counters.move_by(self.counter_id, steps)

    def step(self):
        return self.counters.step(self.counter_id)

    def back(self):
        return self.counters.back(self.counter_id)

    def reset(self):
        return self.counters.reset(self.counter_id)

    def set_pos(self, pos: int):
        return self.counters.set_pos(self.counter_id, pos)
