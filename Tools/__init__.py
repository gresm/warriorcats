from . import counter
from . import serializing
from . import board2d
from . import types_protocol

from generate_init import generate, insert


# generate __all__ and classes
__all__, objects,  classes = generate(counter, serializing, board2d, types_protocol)
insert(globals(), __all__, objects)

# cleanup
del generate, insert, objects
