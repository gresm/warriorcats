from typing import Union, List, Tuple, Set, Iterable, Optional

_TYPE = Union["Node", type]
_OBJECT_TYPE = Union["ObjectTypeNode", object]


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


class SubClassNode(Node):
    def __init__(self, t: type, *args: type):
        super(Node, self).__init__()
        self.type: type = t
        self.args = args

    @staticmethod
    def _check(t: type, t2: Union[type, Tuple[type]]) -> bool:
        if isinstance(t, type):
            return issubclass(t, t2)
        return False

    def check(self, t: type) -> bool:
        a = list(self.args)
        a.append(self.type)
        a = tuple(a)
        return self._check(t, a)


class ObjectTypeNode(Node):
    def __init__(self, o: _OBJECT_TYPE):
        super(Node, self).__init__()
        self.object: _OBJECT_TYPE = o

    @staticmethod
    def _check(obj: object, node: Union[_OBJECT_TYPE, Node]) -> bool:
        if isinstance(node, ObjectTypeNode):
            return node.check(obj)
        elif isinstance(node, Node):
            return node.check(obj)
        else:
            return obj is node

    def check(self, obj: object) -> bool:
        return self._check(obj, self.object)


class UnionObjectNode(ObjectTypeNode):
    def __init__(self, o: _OBJECT_TYPE, o2: _OBJECT_TYPE, *args: _OBJECT_TYPE):
        super().__init__(o)
        self.object2: _OBJECT_TYPE = o2
        self.args: Tuple[_OBJECT_TYPE] = args

    def check(self, obj: object) -> bool:
        f = self._check(obj, self.object) or self._check(obj, self.object2)
        if not self.args:
            return f
        else:
            for e in self.args:
                if self._check(obj, e):
                    return True
            return f


class SelectedNode(ObjectTypeNode):
    def __init__(self, t: _OBJECT_TYPE, t2: _OBJECT_TYPE, *args: _OBJECT_TYPE):
        super(SelectedNode, self).__init__(t)
        self.type = t
        self.type2: _OBJECT_TYPE = t2
        self.args: Tuple[_OBJECT_TYPE] = args

    def check(self, obj: object) -> bool:
        return obj in (self.type, self.type2, *self.args)


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


class ObjectNode(ObjectTypeNode):
    def __init__(self, t: _OBJECT_TYPE):
        super().__init__(t)
