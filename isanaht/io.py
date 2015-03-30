from __future__ import division
import cv2
import numpy as np

from isanaht.math import map_range

def loadmov(filename):

    vid = cv2.VideoCapture(filename)
    success, im = vid.read()

    fr = []
    while success:
        fr.append(im)
        success,im = vid.read()

    vid.release()
    fr = np.array(fr)

    return fr

def savemov(filename, data, fourcc):



    if len(data.shape)==4:
        d_nfr, d_h, d_w, d_nch = data.shape

    elif len(data.shape)==3:
        d_nfr, d_h, d_w = data.shape
        d_nch = 1

    else:
        raise AttributeError("Need either a 3D or 4D array to save as movie.")



    vid_writer =  cv2.VideoWriter(filename, fourcc, 8, (d_w, d_h))


    for ii in range(1, d_nfr):

        outframe = map_range(data[ii,...], data.min(), data.max(), 0, 255).astype(np.uint8)

        if d_nch == 1:
            outframe = cv2.cvtColor(outframe, cv2.COLOR_GRAY2BGR)

        vid_writer.write(outframe)

    vid_writer.release()