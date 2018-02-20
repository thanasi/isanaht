#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import string

import numpy as np

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Plot data in a file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    loggroup = parser.add_mutually_exclusive_group()
    errgroup = parser.add_mutually_exclusive_group()
    linegroup = parser.add_mutually_exclusive_group()
    
    parser.add_argument('file', type=str, help='data filename')
    parser.add_argument('--usecols', metavar='N', type=int, nargs='+', 
                        help='columns to load')
    parser.add_argument('--skiprows', metavar='N', type=int, nargs='+',
                        help='rows to skip')
    parser.add_argument('--sort', action='store_true', 
                        help='sort loaded data by index')
    parser.add_argument('--grid', action='store_true', 
                        help='show plot grid')
    parser.add_argument('--axeq', action='store_true', 
                        help='plot with equal axes')
    
    parser.add_argument('--polyfit', metavar='M', type=int, 
                help='fit each column of data using a polynomial of order M')
    
    linegroup.add_argument('--lineplot', action='store_true',
                           help='only plot lines, not markers')
#    linegroup.add_argument('--nolines', action='store_true',
#                           help="don't plot lines, only markers")

    errgroup.add_argument('--droperr', action='store_true',
                        help='drop error columns during import')
    errgroup.add_argument('--err', action='store_true', 
                        help='read and plot errorbars')

    loggroup.add_argument('--logx', action='store_true', help='log x-axis')
    loggroup.add_argument('--logy', action='store_true', help='log y-axis')
    loggroup.add_argument('--loglog', action='store_true', help='log-log plot')
        
    
    args = parser.parse_args()
    file = args.file
    usecols = args.usecols
    skiprows = args.skiprows
    sort_data = args.sort
    grid_on = args.grid
    equal_axis = args.axeq
    
    polyfit = args.polyfit
    
    lineplot = args.lineplot

    errorbars = args.err
    droperr  = args.droperr
    
    logx = args.logx
    logy = args.logy
    loglog = args.loglog
    
    plt.ioff()
    
    
    ###################
    # loading block
    ###################
    
    data = pd.read_csv(file,skiprows=skiprows,comment='#')
                       
    if usecols is not None:
        data = data.iloc[:,usecols]
    
    if droperr:
        # assume that error columns are labeled with a _std suffix
        is_errcol = lambda x: "_std" in x.lower()
        errcols = np.asarray(list(map(is_errcol, data.columns)), 
                             dtype=bool)
        
        data = data.iloc[:,~errcols]
        
    # get rid of any rows where the index is NaN
    data.dropna(axis=0, how='all', subset=[data.columns[0]], inplace=True)
    
    # get rid of any rows that have no values among the data
    data.dropna(axis=0, how='all', inplace=True)

    # set the first column as the x (index) column
    data.set_index(keys=data.columns[0], drop=True, inplace=True)
    
    if sort_data:
        data = data.sort_index()
       
    
    ###################
    # plotting block
    ###################
    
    fmt = '.-'
    if lineplot:
        fmt = '-'
    
    if errorbars:
        # assume that each data column is followed by an errorbar column
        x = data.index.values
        err = data.iloc[:,1::2].values
        dat = data.iloc[:,0::2].values
        la = data.iloc[:,0::2].columns.values
                
        
        for d,e,l in zip(dat.T, err.T, la):
            li, = plt.plot(x, d, fmt, label=l)
            c = li.get_c()
            plt.fill_between(x, d-e, d+e, facecolor=c, alpha=0.5)
            
            if polyfit is not None:
                m = ~np.isnan(d)
                x_ = x[m]
                d_ = d[m]
                e_ = e[m]

                w_ = 1/e
                
                if logx or loglog:
                    x_ = np.log10(x_)
                if logy or loglog:
                    w = None
                    d_ = np.log10(d_)

                if logx:
                    print("  Y vs log(X) polyfit")
                elif logy: 
                    print("  log(Y) vs X polyfit")
                elif loglog:
                    print("  log(Y) vs log(X) polyfit")
                else:
                    print("  Y vs X polyfit")
                
#                p,v = np.polyfit(x_,d_,polyfit,w=w_, cov=True)
#                p_std = np.sqrt(np.diag(v))
#                print("{:s} polyfit: {} +/- {}".format(l, p, p_std))\
                p = np.polyfit(x_,d_,polyfit,w=w_, cov=False)
                print("{:s} polyfit: {}".format(l, p))
                
                xx = np.linspace(x_.min(), x_.max(), 1000)
                yy = np.poly1d(p)(xx)
                li.set_ls('')

                if logx or loglog:
                    xx = 10**xx
                if logy or loglog:
                    yy = 10**yy

                plt.plot(xx,yy,'--',c=li.get_c())
                
        
        plt.xlabel(data.index.name)
        plt.legend()
        
    
    else:
        x = data.index.values
        dat = data.values
        la = data.columns.values
                
        
        for d,l in zip(dat.T, la):
            li, = plt.plot(x, d, fmt, label=l)
            
            if polyfit is not None:
                m = ~np.isnan(d)
                x_ = x[m]
                d_ = d[m]
                
                if logx or loglog:
                    x_ = np.log10(x_)
                if logy or loglog:
                    d_ = np.log10(d_)

                if logx:
                    print("  Y vs log(X) polyfit")
                elif logy: 
                    print("  log(Y) vs X polyfit")
                elif loglog:
                    print("  log(Y) vs log(X) polyfit")
                else:
                    print("  Y vs X polyfit")
                                   
#                p,v = np.polyfit(x_,d_,polyfit,w=w_, cov=True)
#                p_std = np.sqrt(np.diag(v))
#                print("{:s} polyfit: {} +/- {}".format(l, p, p_std))\
                p = np.polyfit(x_,d_,polyfit,w=w_, cov=False)
                print("{:s} polyfit: {}".format(l, p))

                xx = np.linspace(x_.min(), x_.max(), 1000)
                yy = np.poly1d(p)(xx)
                li.set_ls('')

                if logx or loglog:
                    xx = 10**xx
                if logy or loglog:
                    yy = 10**yy

                plt.plot(xx,yy,'--',c=li.get_c())
            
            
        plt.xlabel(data.index.name)
        plt.legend()
        
    if logx:
        plt.semilogx()
    elif logy:
        plt.semilogy()
    elif loglog:
        plt.loglog()
        
    plt.grid(b=grid_on, color='#666666', which='both')
        
    if equal_axis:
        plt.axis('equal')
             
    plt.show()