from typing import Union, List, Tuple, Set, Iterable, Optional

_TYPE = Union["Node", type]


class Node:
    def __init__(self, t: _TYPE):
        self.type = t

    def __eq__(self, other):
        return self.check(other)

    @staticmethod
    def _check(obj: object, t: _TYPE) -> bool:
        if isinstance(t, Node):
            return t.check(obj)
        if isinstance(obj, t):
            return True
        else:
            return False

    def check(self, obj: object) -> bool:
        return self._check(obj, self.type)


class AnyNode(Node):
    def __init__(self, t: _TYPE = type(None)):
        super().__init__(t)

    def check(self, obj: object) -> bool:
        return True


class NoneNode(Node):
    def __init__(self, t: _TYPE = type(None)):
        super().__init__(t)

    def check(self, obj: object) -> bool:
        return False


class _IterNode(Node):
    def __init__(self, t: _TYPE, check_type: _TYPE):
        super().__init__(t)
        self.check_type = check_type

    def _check_type(self, obj: object):
        return self._check(obj, self.check_type)

    def check(self, obj: Iterable) -> bool:
        if not self._check_type(obj):
            return False
        for e in obj:
            if not self._check(e, self.type):
                return False
        return True


class DictNode(_IterNode):
    def __init__(self, t: _TYPE, k_t: _TYPE = None):
        super().__init__(t, dict)
        self.key_type = k_t if k_t else AnyNode()

    def check(self, obj: dict) -> bool:
        if not self._check_type(obj):
            return False
        for e in obj:
            if not self._check(e, self.key_type):
                return False
            if not self._check(obj[e], self.type):
                return False
        return True


class StrictDictNode(DictNode):
    def __init__(self, t: _TYPE, elements: Union[List[str], Tuple[str],
                                                 Set[str]], k_t: _TYPE = None):
        super(StrictDictNode, self).__init__(t, k_t)
        assert isinstance(elements, (list, tuple, set))
        self.elements = elements

    def check(self, obj: dict) -> bool:
        if not self._check(obj, dict):
            return False
        if not (set(obj.keys()) == set(self.elements)):
            return False
        return super(StrictDictNode, self).check(obj)


class ListNode(_IterNode):
    def __init__(self, t: _TYPE):
        super().__init__(t, list)

    def check(self, obj: list) -> bool:
        return super(ListNode, self).check(obj)


class TupleNode(_IterNode):
    def __init__(self, t: _TYPE):
        super().__init__(t, tuple)

    def check(self, obj: tuple) -> bool:
        return super(TupleNode, self).check(obj)


class SetNode(_IterNode):
    def __init__(self, t: _TYPE):
        super().__init__(t, set)

    def check(self, obj: set) -> bool:
        return super(SetNode, self).check(obj)


class UnionNode(Node):
    def __init__(self, t: _TYPE, t2: _TYPE, *args: Optional[_TYPE]):
        super(UnionNode, self).__init__(t)
        self.type: _TYPE = t
        self.type2: _TYPE = t2
        self.args: Tuple[Optional[_TYPE]] = args

    def check(self, obj: object) -> bool:
        f = self._check(obj, self.type) or self._check(obj, self.type2)
        if not self.args:
            return f
        else:
            for e in self.args:
                if self._check(obj, e):
                    return True
            return f


class SelectedNode(Node):
    def __init__(self, t: object, t2: object, *args: object):
        super(object, self).__init__()
        self.type = t
        self.type2: object = t2
        self.args: Tuple[object] = args

    def check(self, obj: object) -> bool:
        return obj in (self.type, self.type2, *self.args)


class AllNode(Node):
    def __init__(self, t: _TYPE, *args: _TYPE):
        super().__init__(t)
        self.args: Tuple[_TYPE] = args

    def check(self, obj: object) -> bool:
        f = super(AllNode, self).check(obj)
        if not f:
            return False
        for e in self.args:
            if not self._check(obj, e):
                return False
        return True
