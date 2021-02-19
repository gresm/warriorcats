from . import counter
from . import serializing
from . import board2d
from . import types_checker
from . import virtual_object

from generate_init import generate, insert


# generate __all__ and classes
__all__, objects,  __classes__ = generate(counter, serializing, board2d, types_checker, virtual_object)
insert(globals(), __all__, objects)

# cleanup
del generate, insert, objects
