"""
    tool for fast generate __init__.py file for any package
"""


import inspect
# to inspect module/file


def generate(*args):
    """
    generate names, objects, classes for list of modules/files
    :param args: imported files
    :return: list of names, list of objects, list of classes
    """
    names = []
    classes = []
    objects = []
    for e in args:
        n, o, c = _generate(e)
        names += n
        classes += c
        objects += o
    return names, objects, classes


def _generate(module):
    """
    generates names, objects, classes for selected module/file
    :param module: module/file
    :return: names, objects, classes
    """
    n = []
    c = []
    o = []
    for name, obj in inspect.getmembers(module):
        if not name[0] == "_":
            if inspect.isclass(obj):
                c.append(obj)
            n.append(name)
            o.append(obj)
    return n, o, c


def insert(g, names, objects):
    """
    inserts to globals elements
    :param g: globals()
    :param names: list of generated names
    :param objects: list of objects
    :return: None
    """
    for n in range(len(names)):
        g[names[n]] = objects[n]
