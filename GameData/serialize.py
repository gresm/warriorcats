from typing import Dict, Type


def _func():
    pass


def _g(cls: type):
    return cls.__name__


def _d(obj: object):
    return obj.__class__.__name__


_default = {_d(_func): type(_func), _g(bytes): bytes, _g(bytearray): bytearray,
            _d(_func.__code__): type(_func.__code__)}


def is_primitive(obj):
    return type(obj) in {int, str, float, bool, None}


def is_list(obj):
    return type(obj) in {list, tuple}


def is_dict(obj):
    return type(obj) == dict


def is_set(obj):
    return type(obj) == set


def is_deserializable(dct: dict) -> bool:
    return is_dict(dct) and "__class__" in dct


def set_to_dict(st: set):
    d = {"__class__": "set"}
    for v in st:
        d[v] = v
    return d


def serialize(obj):
    if is_primitive(obj):
        return obj
    elif is_list(obj):
        n = []
        for e in obj:
            n.append(serialize(e))
        return n
    elif is_dict(obj):
        d = {}
        for i, v in obj.items():
            v = serialize(v)
            d[i] = v
        return d
    elif is_set(obj):
        return set_to_dict(obj)
    else:
        if "__on_serialize__" in dir(obj):
            obj.__on_serialize__()
        n = obj.__class__.__name__
        d = obj.__dict__.copy()
        r = {}
        ig = "__serialize_ignore__" in d
        ig_lst = {}
        if ig:
            ig_lst = d["__serialize_ignore__"]

        for i, v in d.items():
            if not ig or i not in ig_lst:
                new = serialize(v)
                r[i] = new
            r.update({"__class__": n})
            return r


def deserialize(dct: dict, classes: Dict[str, Type[object]]):
    if is_deserializable(dct) and dct["__class__"] in classes:
        new_m = {}
        for i, v in dct.items():
            new_m[i] = deserialize(v, classes)
        new_ob = classes[dct["__class__"]].__new__(classes[dct["__class__"]])
        new_ob.__dict__.update(new_m)
        if "__serialize_setup__" in dir(new_ob):
            getattr(new_ob, "__serialize_setup__")()
        return new_ob
    else:
        if is_dict(dct) and "__class__" in dct and dct["__class__"] == "set":
            return set(dct)
        return dct
