from __future__ import division
import numpy as np

def maptouint8(im):
    return map_range(im, im.min(), im.max(), 0, 255).astype(np.uint8)

def map_range(x, from_min, from_max, to_min, to_max):
    from_span = from_max - from_min
    to_span = to_max - to_min
    return 1.0 * (x - from_min) * to_span / from_span + to_min

def constrain(x, xmin, xmax):
    x0 = min(x,xmax)
    x1 = max(x0,xmin)
    return x1