from __future__ import division

def make_subdivided_ims(shape, depth):
    dY = shape[0] // (2**depth)
    dX = shape[1] // (2**depth)
    
    q = []
    
    for i in range(2**depth):
        for j in range(2**depth):
            q.append((slice(i*dY, (i+1)*dY), slice(j*dX, (j+1)*dX)))
            
    return q


def square_window(ws, *center):

    assert ws % 2 == 1, "Need to pick an odd window size"
    r = (ws-1)//2

    return [slice(c-r, c+r+1, 1) for c in center]
