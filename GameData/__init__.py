from . import cat_data
from generate_init import generate, insert


__all__, objects, __classes__ = generate(cat_data)
insert(globals(), __all__, objects)
del generate, insert, objects
