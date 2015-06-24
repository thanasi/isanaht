from __future__ import division
import os
import sys
import cv2
import numpy as np

from isanaht.math import map_range

from progress.bar import Bar
from progress.spinner import MoonSpinner

def check_filepath(path):
    if os.path.exists(path):
        pass
    else:
        sys.stdout.write("Creating directory structure for path: %s\n" % path)
        sys.stdout.flush()

        os.makedirs(path)

def write_output_ims(outfile, data, timeinfo=None):
    if outfile is not None:
        check_filepath(os.path.split(outfile)[0])

        ext = os.path.splitext(outfile)[-1]

        if ext == '.mp4':
            savemov(outfile,data, verb=True, timeinfo=timeinfo)

        elif ext == '.npy':
            print "saving %s" % outfile
            np.save(outfile, data)

        elif ext == '.png':
            saveimstack(outfile, data, timeinfo=timeinfo, verb=True)

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

def saveimstack(filename, data, timeinfo=None, verb=False):

    if data.ndim ==4:
        d_nfr, d_h, d_w, d_nch = data.shape

    elif data.ndim==3:
        d_nfr, d_h, d_w = data.shape
        d_nch = 1

    elif data.ndim==2:
        d_nfr = 1
        d_nch = 1
        d_h, d_w = data.shape
        data = [data]

    else:
        raise AttributeError("Need either a 3D or 4D array to save as movie.")

    outfile0, ext = os.path.splitext(filename)

    outfile = outfile0 + "-%04d" + ext

    if verb:
        pbar = Bar("Saving %s/*" % outfile0, max=d_nfr)
        pbar.start()

    for i in range(d_nfr):

        outim = data[i].copy()

        if d_nch == 1:
            outim = cv2.cvtColor(outim, cv2.COLOR_GRAY2RGB)

        if timeinfo is not None:
            t = timeinfo[i]
            cv2.putText(outim, "t=%2.4f" % t, (20, d_h-20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255))

        cv2.imwrite(outfile % i, outim)

        if verb:

            pbar.next()

    if verb:
        pbar.finish()





def savemov(filename, data, fourcc = cv2.cv.FOURCC(*'mp4v'), timeinfo=None, verb=False):

    if data.ndim ==4:
        d_nfr, d_h, d_w, d_nch = data.shape

    elif data.ndim==3:
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

        if timeinfo is not None:
            t = timeinfo[ii]
            cv2.putText(outframe, "t=%2.4fs" % t, org=(20, d_h-20),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=.5, color=(255,255,255))

        vid_writer.write(outframe)
        if verb:
            pbar.next()

    if verb:
        pbar.finish()

    vid_writer.release()