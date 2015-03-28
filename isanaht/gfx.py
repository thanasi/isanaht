from __future__ import division
import pylab as pl

def overlay_withcolor(base, overlay, overlaycm=pl.cm.jet, overlayalpha=.8):
    '''
    overlay_withcolor(base, overlay, overlaycm, overlayalpha)
        take a base grayscale image and overlay the overlay image
        with colormap overlaycm and alpha level overlayalpha

    '''
    gr = pl.cm.gray(1.0 * base / base.max())
    col = overlaycm(1.0 * overlay / overlay.max(),alpha=overlayalpha)
    for j in range(4):
        col[:,:,j][overlay==0] = 0

    return gr + col * overlayalpha - gr * col * overlayalpha