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

import time
from inspect import stack

def timefmt(t):
    ''' format time data to H:M:S '''
    if type(t) is time.struct_time:
        pass
    else:
        t = time.gmtime(t)
    return time.strftime('%H:%M:%S', t)

def msg(m,b=0,override_callername=''):
    ''' return timestamped and function-specific message '''
    b = max(b, len(stack())-2)
    timestamp = timefmt(time.localtime())
    if override_callername:
        callername = override_callername
    else:
        callername = stack()[1][3]+'()'
        if callername == '<module>()':
            callername = stack()[1][1].split('/')[-1]

    return '[%s] %s: %s' % (timestamp, callername, m)

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
                    try:
                        # lock when printing to prevent std out overlaps
                        iteratorlock.acquire()
                        if verbmin:
                            # progress bar display
                            spot = int(20*v[0]/ll)
                            pbar[spot] = '-'
                            pbar[1+spot] = '>'
                            pbar[0] = '['
                            pbar[-1] = ']'
                            m = msg('%s %03d/%03d' %\
                                    (''.join(pbar),v[0]+1,ll),
                                    override_callername=f.__name__)
                            sys.stdout.write(m + '\b'*len(m))
                            sys.stdout.flush()
                        if verb:
                            print(msg('+ starting thread %d' \
                                      % v[0],\
                                      override_callername=f.__name__+'()'))
                    finally:
                        iteratorlock.release()

                    if return_:
                        n,x = v
                        d[n] = f(x, *args, **kwargs)

                    else:
                        f(v, *args, **kwargs)

                    t = time.time() - t0
                    try:
                        iteratorlock.acquire()
                        if verb:
                            print(msg('- finished thread %d in %s' % \
                                      (v[0],\
                                       timefmt(t)),\
                                      override_callername=f.__name__+'()'))
                    finally:
                        iteratorlock.release()
                except:
                    e = sys.exc_info()
                    iteratorlock.acquire()
                    try:
                        exceptions.append(e)
                    finally:
                        t = time.time() - t0
                        sys.stdout.write('\n')
                        print msg('X EXCEPTION CAUGHT:' +\
                                  ' thread %d failed after %s with exception %s\n' %\
                                  (v[0],\
                                   timefmt(t),\
                                   e[0].__name__),\
                                  override_callername=f.__name__+'()')

                        iteratorlock.release()

        if verb: sys.stdout.write('\n')
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

        if verb or verbmin: sys.stdout.write('\n')
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