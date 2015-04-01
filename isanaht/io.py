from __future__ import division
import cv2
import numpy as np

from isanaht.math import map_range

from progress.bar import Bar
from progress.spinner import MoonSpinner

def loadmov(filename, verb=False):

    vid = cv2.VideoCapture(filename)
    success, im = vid.read()

    fr = []

    if verb:
        pspin = MoonSpinner("Loading %s " % filename)
        pspin.start()
        i=0

    while success:

        fr.append(im)
        success,im = vid.read()
        if verb:
            i +=1
            if (i%10)==0:
                pspin.next()

    if verb: pspin.finish()
    vid.release()
    fr = np.array(fr)

    return fr

def savemov(filename, data, fourcc = cv2.cv.FOURCC(*'mp4v'), verb=False):



    if len(data.shape)==4:
        d_nfr, d_h, d_w, d_nch = data.shape

    elif len(data.shape)==3:
        d_nfr, d_h, d_w = data.shape
        d_nch = 1

    else:
        raise AttributeError("Need either a 3D or 4D array to save as movie.")



    vid_writer =  cv2.VideoWriter(filename, fourcc, 8, (d_w, d_h))

    if verb:
        pbar = Bar("Saving %s" % filename, max=d_nfr)
        pbar.start()
        pbar.next()
    for ii in range(1, d_nfr):

        outframe = map_range(data[ii,...], data.min(), data.max(), 0, 255).astype(np.uint8)

        if d_nch == 1:
            outframe = cv2.cvtColor(outframe, cv2.COLOR_GRAY2BGR)

        vid_writer.write(outframe)
        if verb:
            pbar.next()

    if verb:
        pbar.finish()

    vid_writer.release()