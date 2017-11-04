# similar to the %matplotlib magic, use a magic to initialize a units environment
# template taken from 
# http://ipython.readthedocs.io/en/stable/config/custommagics.html#defining-magics

from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

@register_line_magic
def units(line):
    "initialize an interactive session with unit support"
    from math import pi
    from pint import UnitRegistry
    ureg = UnitRegistry()
    Q = ureg.Quantity

    globals().update({'Q':Q, 'ureg':ureg, 'pi':pi})

# In an interactive session, we need to delete these to avoid
# name conflicts for automagic to work on line magics.
del units