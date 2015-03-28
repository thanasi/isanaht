from __future__ import division
import cv2
import numpy as np

def loadmov(infile):

    vid = cv2.VideoCapture(infile)
    success, im = vid.read()

    fr = []
    while success:
        fr.append(im)
        success,im = vid.read()

    vid.release()
    fr = np.array(fr)

    return fr