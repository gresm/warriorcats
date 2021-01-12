from . import cat
from generate_init import generate, insert


__all__, objects, classes = generate(cat)
insert(globals(), __all__, objects)
del generate, insert, objects
