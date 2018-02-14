# similar to the %matplotlib magic, use a magic to initialize a units environment
# template taken from 
# http://ipython.readthedocs.io/en/stable/config/custommagics.html#defining-magics

from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

@register_line_magic
def data(line):
    "initialize an interactive session with data support"

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    plt.ion()

    pi = np.pi

    globals().update(dict(np=np, plt=plt, pd=pd, pi=pi))

    print ("Data Analysis Environment Initialized")

# In an interactive session, we need to delete these to avoid
# name conflicts for automagic to work on line magics.
del data