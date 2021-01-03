from typing import Union, Optional, Dict, List, Set


class ItemNotConnectedError(Exception):
    pass


class NonExistingObjectInMemoryError(Exception):
    pass


class UnknownItemTypeError(Exception):
    pass


class SerializeSpace:
    def __init__(self):
        self.memory: List["Item"] = []
        self.main: Set[int] = set()

    def add_element(self, element: "Item") -> int:
        r = self.add_attribute(element)
        self.main.add(len(self.memory)-1)
        element.connect(self)
        return r

    def add_attribute(self, atr: "Item") -> int:
        for i in range(len(self.memory)):
            if self.memory[i].obj is atr.obj:
                return i
        self.memory.append(atr)
        return len(self.memory) - 1

    def get_attribute(self, i: int) -> "Item":
        if i not in self.memory:
            raise NonExistingObjectInMemoryError
        return self.memory[i]

    def serialize(self):
        ref = []
        for i in range(len(self.memory)):
            ref.append(self.memory[i].serialize())
        return {"main": self.main, "references": ref}


class Item:
    def __init__(self, obj: Union[str, int, float, bool, type(None), list, tuple, dict, set, object]):
        self.obj: Union[str, int, float, bool, type(None), list, tuple, dict, set, object] = obj
        self.type = type(obj)
        self.type_name = self.type.__name__
        self.memory: Optional[Union[List[int], Dict[str, int], str, int, float, bool, type(None)]] = {}
        self.space: Optional[SerializeSpace] = None
        self.class_type = self.get_class_type(self.obj)
        self.const: bool = self.is_const(self.obj)
        self.connected: bool = False
        self.finished_setup: bool = False

    def connect(self, space: SerializeSpace):
        self.space = space
        self.connected = True
        self.setup()
        self.finished_setup = True

    def setup(self):
        if not self.connected:
            raise ItemNotConnectedError
        if self.class_type == "simple":
            self.memory = self.obj
        elif self.class_type == "iterable" or self.class_type == "set":
            new_m = []
            for v in self.obj:
                it = Item(v)
                it.connect(self.space)
                new_m.append(self.space.add_attribute(it))
            self.memory = new_m
        elif self.class_type == "dict":
            new_m = {}
            for i, v in self.obj.items():
                it = Item(v)
                it.connect(self.space)
                new_m[i] = self.space.add_attribute(it)
            self.memory = new_m
        elif self.class_type == "handmade":
            new_m = {}
            for i, v in self.obj.__dict__.items():
                it = Item(v)
                it.connect(self.space)
                new_m[i] = self.space.add_attribute(it)
            self.memory = new_m
        else:
            raise UnknownItemTypeError

    def add_attribute(self, atr: "Item"):
        if not self.connected:
            raise ItemNotConnectedError
        return self.space.add_attribute(atr)

    def serialize(self):
        if not self.finished_setup:
            raise ItemNotConnectedError("Didn't finish setup object.")
        return {"class-type": self.class_type, "class": self.type_name, "memory": self.memory, "const": self.const}

    @classmethod
    def get_class_type(cls, obj: object) -> str:
        if isinstance(obj, (str, int, float, bool, type(None))):
            return "simple"
        elif isinstance(obj, (list, tuple)):
            return "iterable"
        elif isinstance(obj, dict):
            return "dict"
        elif isinstance(obj, set):
            return "set"
        return "handmade"

    @classmethod
    def is_const(cls, obj: object) -> bool:
        return isinstance(obj, tuple)

# class SerializeSpace:
#     def __init__(self):
#         self.references: List["Item"] = []
#         self.n_index: int = 0
#         self.items: Dict[str, "Item"] = {}
#
#     def connect_item(self, item: "Item", name: str):
#         item.connect(self)
#         self.items[name] = item
#
#     def add_reference(self, dct: dict):
#         self.references[self.n_index] = dct
#         self.n_index += 1
#         return self.n_index - 1
#
#     def serialize(self) -> Dict[str, dict]:
#         ret: Dict[str, dict] = {}
#         for i, v in self.items.items():
#             ret[i] = v.serialize()
#         return ret
#
#
# class Item:
#     def __init__(self, obj: object = None):
#         self.obj = obj
#         self.type: type = type(obj)
#         self.type_name: str = self.type.__name__
#         self.memory: Dict[str, int] = {}
#         self.references: List["Item"] = []
#         self.parent: Optional[Union[SerializeSpace, "Item"]] = None
#         self.connected: bool = False
#
#     @class method
#     def is_primitive(cls, obj: object):
#         return isinstance(obj, (int, str, type(None), bool))
#
#     @class method
#     def is_list(cls, obj: object):
#         return isinstance(obj, (list, tuple))
#
#     def connect(self, obj: Union[SerializeSpace, "Item"]):
#         self.connected = True
#         self.parent = obj
#         self.references = obj.references
#         self.setup()
#
#     def add_reference(self, dct: dict):
#         return self.parent.add_reference(dct)
#
#     def serialize(self) -> Dict[str, dict]:
#         if not self.connected:
#             raise ItemOperationWithoutConnectionError
#         ret: Dict[str, dict] = {}
#         for i, v in self.memory.items():
#             ret[i] = self.get_object(v).serialize()
#         return ret
#
#     def get_object(self, i: int) -> "Item":
#         if not self.connected:
#             raise ItemOperationWithoutConnectionError
#         if i in self.memory:
#             return self.references[i]
#         else:
#             raise NonExistingObjectInMemoryError
#
#     def setup(self):
#         if not self.connected:
#             raise ItemOperationWithoutConnectionError
#         pass
