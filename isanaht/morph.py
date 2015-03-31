from __future__ import division

import numpy as np
import scipy.ndimage as ndi

from skimage.morphology import disk

from mahotas.labeled import label, labeled_size

def disk_grid(d0, h, w):
    '''
    Create a grid of nearly touching disks (separated by two pix each) to fill the window

    Parameters
    ----------
    d0 : int
        disk diameter

    h : int
        height of grid

    w : int
        width of grid

    Returns
    -------
    arr : ndarray
        2d grid of nearly touching disks

    '''

    d = disk(d0)
    d = np.pad(d, 1, mode='constant', constant_values=0)

    Nx = (w // (d.shape[1])) + 1
    Ny = (h // (d.shape[0])) + 1

    arr = np.tile(d, (Ny,Nx))
    y0 = arr.shape[0]//2
    x0 = arr.shape[1]//2

    return arr[y0-h//2:y0+h//2+h%2, x0-w//2:x0+w//2+w%2]

