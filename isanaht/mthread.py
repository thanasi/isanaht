# Athanasios Athanassiadis
# University of Chicago
# March 2012
#
# code modified from http://www.scipy.org/Cookbook/Multithreading
#
# Updated March 2015
#
######################################
from __future__ import division
import sys
import time
import threading
from itertools import izip, count

def yieldconst(c):
    while True:
        yield c

def foreach(f,l,args,kwargs={},threads=3,return_=False,verb=False, verbmin=False):
    '''
    Apply f to each element of l, in parallel using args and kwargs
    time and supply messages if verb flag is set
    '''

    ll = len(l)
    pbar = ['['] + 20*[' ']+ [']']

    if threads>1:
        iteratorlock = threading.Lock()
        exceptions = []
        if return_:
            n = 0
            d = {}
            i = izip(count(),l.__iter__())
        else:
            i = l.__iter__()

        def runall():
            while True:
                iteratorlock.acquire()
                try:
                    try:
                        if exceptions:
                            return
                        v = i.next()
                    finally:
                        iteratorlock.release()
                except StopIteration:
                    return
                try:
                    t0 = time.time()

                    if return_:
                        n,x = v
                        d[n] = f(x, *args, **kwargs)

                    else:
                        f(v, *args, **kwargs)

                    t = time.time() - t0

                except:
                    e = sys.exc_info()
                    iteratorlock.acquire()
                    try:
                        exceptions.append(e)
                    finally:
                        iteratorlock.release()


        sys.stdout.flush()
        threadlist = [threading.Thread(target=runall) \
                        for j in xrange(threads)]


        for t in threadlist:
            t.start()
        for t in threadlist:
            t.join()
        if exceptions:
            a, b, c = exceptions[0]
            raise a, b, c

        if return_:
            r = d.items()
            r.sort()
            return [v for (n,v) in r]
    else:
        if return_:
            return [f(v, *args, **kwargs) for v in l]
        else:
            for v in l:
                f(v, *args, **kwargs)
            return

def parallel_map(f,l,args=(),threads=3,verb=False,verbmin=False,**kwargs):
    if threads==0:
        return []
    return foreach(f,l,args,kwargs,threads=threads,return_=True,verb=verb, verbmin=verbmin)