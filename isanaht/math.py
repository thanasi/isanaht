from __future__ import division

def map_range(x, from_min, from_max, to_min, to_max):
    from_span = from_max - from_min
    to_span = to_max - to_min
    return (x - from_min) * to_span / from_span + to_min

def constrain(x, xmin, xmax):
    x0 = min(x,xmax)
    x1 = max(x0,xmin)
    return x1