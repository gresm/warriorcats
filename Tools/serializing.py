from typing import Union, Optional, Dict, List, Set, Tuple, Type


class ItemNotConnectedError(Exception):
    pass


class NonExistingObjectInMemoryError(Exception):
    pass


class UnknownItemTypeError(Exception):
    pass


class SerializeSpaceError(Exception):
    pass


class DeserializeError(Exception):
    pass


class SerializeSpace:
    def __init__(self):
        self.des_dict: dict = {}
        self.type_list: Dict[str, Type[type]] = {}
        self.ref: list = []
        self.memory: List["Item"] = []
        self.main: Set[int] = set()
        self.is_serializing = True
        self.des_mem: Dict[int, object] = {}

    def add_element(self, element: "Item") -> int:
        if not self.is_serializing:
            raise SerializeSpaceError("This SerializeSpace is setup to deserialize no serialize")
        r = self.add_attribute(element)
        self.main.add(len(self.memory) - 1)
        element.connect(self)
        return r

    def add_attribute(self, atr: "Item") -> int:
        if not self.is_serializing:
            raise SerializeSpaceError("This SerializeSpace is setup to deserialize no serialize")
        for i in range(len(self.memory)):
            if self.memory[i].obj is atr.obj:
                return i
        self.memory.append(atr)
        return len(self.memory) - 1

    def get_attribute(self, i: int) -> "Item":
        if not self.is_serializing:
            raise SerializeSpaceError("This SerializeSpace is setup to deserialize no serialize")
        if i not in self.memory:
            raise NonExistingObjectInMemoryError()
        return self.memory[i]

    def get_classes(self) -> Set[Type[type]]:
        if not self.is_serializing:
            raise SerializeSpaceError("This function is working only for serialize state.")
        ret: set = set()
        for e in self.memory:
            ret.add(e.type)
        return ret

    def serialize(self):
        if not self.is_serializing:
            raise SerializeSpaceError("This SerializeSpace is setup to deserializing not serializing")
        ref = []
        for i in range(len(self.memory)):
            ref.append(self.memory[i].serialize())
        return {"main": list(self.main), "references": ref}

    def deserialize(self, dct: dict, type_list: Dict[str, type]) -> List[object]:
        self.is_serializing = False
        self.des_dict = dct
        self.type_list = type_list
        if "main" not in dct or not isinstance(dct["main"], list):
            raise DeserializeError("Invalid deserialize protocol: invalid 'main' data.")
        self.main = self.des_dict["main"]
        if "references" not in dct or not isinstance(dct["references"], list):
            raise DeserializeError("Invalid deserialize protocol: invalid 'references' data.")
        self.ref = dct["references"]
        for i in range(len(self.ref)):
            self.convert_item(self.ref[i], i)
        ret = []
        for i in self.main:
            ret.append(self.des_mem[i])
        return ret

    def convert_item(self, item: dict, des_index: int):
        if self.is_serializing:
            raise SerializeSpaceError("This SerializeSpace is setup to serializing not deserializing")
        if "class-type" not in item or not isinstance(item["class-type"], str) or \
                item["class-type"] not in Item.class_types:
            raise DeserializeError("Invalid deserialize protocol: invalid 'class-type' data.")
        if "class" not in item or (item["class-type"] == "handmade" and item["class"] not in self.type_list):
            raise DeserializeError("Invalid deserialize protocol: invalid 'class' data.")
        if "const" not in item or not isinstance(item["const"], bool):
            raise DeserializeError("Invalid deserialize protocol: invalid 'const' data.")
        if "memory" not in item:
            raise DeserializeError("Invalid deserialize protocol: missing 'memory' field")
        obj_type: Optional[Type[type]] = self.type_list[item["class"]] if item["class-type"] == "handmade" else None
        obj_save_protocol: str = item["class-type"]
        obj_is_const = item["const"]
        obj_memory = item["memory"]
        if des_index in self.des_mem:
            return self.des_mem[des_index]
        if obj_save_protocol == "simple":
            self.des_mem[des_index] = obj_memory
            return obj_memory
        if obj_save_protocol == "iterable" or obj_save_protocol == "set":
            ret: list = []
            for e in obj_memory:
                if e in self.des_mem:
                    ret.append(self.des_mem[e])
                else:
                    ret.append(self.convert_item(self.ref[e], e))
            ret = ret if not obj_is_const else tuple(ret) if obj_save_protocol != "set" else set(ret)
            self.des_mem[des_index] = ret
            return ret
        if obj_save_protocol == "dict":
            ret: dict = {}
            for i, v in obj_memory.items():
                if v in self.des_mem:
                    ret[i] = self.des_mem[v]
                else:
                    ret[i] = self.convert_item(self.ref[v], v)
            self.des_mem[des_index] = ret
            return ret
        if obj_save_protocol == "handmade":
            ret: object = object.__new__(obj_type)
            for i, v in obj_memory.items():
                if v in self.des_mem:
                    ret.__dict__[i] = self.des_mem[v]
                else:
                    ret.__dict__[i] = self.convert_item(self.ref[v], v)
            self.des_mem[des_index] = ret
            return ret
        raise DeserializeError("How?")


class Item:
    class_types: Tuple[str] = ("handmade", "simple", "iterable", "set", "dict")

    def __init__(self, obj: Union[str, int, float, bool, type(None), list, tuple, dict, set, object]):
        self.obj: Union[str, int, float, bool, type(None), list, tuple, dict, set, object] = obj
        self.type: type = type(obj)
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
            raise ItemNotConnectedError()
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
            raise UnknownItemTypeError()

    def add_attribute(self, atr: "Item"):
        if not self.connected:
            raise ItemNotConnectedError()
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


def serialize(obj: object, *args: object):
    space = SerializeSpace()
    space.add_element(Item(obj))
    for e in args:
        space.add_element(Item(e))
    return space.serialize()


def _convert_to_correct(type_list: Union[Dict[str, Type[type]], List[Type[type]], Tuple[Type[type]],
                                         Set[Type[type]]]):
    if isinstance(type_list, (list, tuple, set)):
        ret = {}
        for e in type_list:
            e: type
            ret[e.__class__.__name__] = e
        return ret
    elif isinstance(type_list, dict):
        return type_list
    else:
        raise DeserializeError("Incorrect types list.")


def deserialize(dct: dict, type_list: Union[type, Dict[str, Type[type]], List[Type[type]], Tuple[Type[type]],
                                            Set[Type[type]]], *args: Type[type]) -> List[object]:
    if isinstance(type_list, type):
        types = {type_list.__name__: type_list}
        types.update(_convert_to_correct(args))
        space = SerializeSpace()
        return space.deserialize(dct, types)
    else:
        types = _convert_to_correct(type_list)
        space = SerializeSpace()
        return space.deserialize(dct, types)


def get_classes(obj, *args: object) -> Set[Type[type]]:
    space = SerializeSpace()
    space.add_element(obj)
    for e in args:
        space.add_element(Item(e))
    return space.get_classes()


def copy(obj: object, *args: object) -> List[object]:
    return deserialize(serialize(obj, *args), get_classes(obj, *args))
