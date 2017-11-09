#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import argparse

import numpy as np

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Plot data in a file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    loggroup = parser.add_mutually_exclusive_group()
    errgroup = parser.add_mutually_exclusive_group()
    parser.add_argument('file', type=str, help='data filename')
    parser.add_argument('--usecols', metavar='N', type=int, nargs='+', 
                        help='columns to load')

    parser.add_argument('--sort', action='store_true', 
                        help='sort loaded data by index')
    parser.add_argument('--polyfit', metavar='M', type=int, 
                help='fit each column of data using a polynomial of order M')

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
    sort_data = args.sort
    polyfit = args.polyfit

    errorbars = args.err
    droperr  = args.droperr
    
    logx = args.logx
    logy = args.logy
    loglog = args.loglog
    
    plt.ioff()
    
    ###################
    # loading block
    ###################
    
    if droperr:
        # assume that error columns are labeled with a _std suffix
        data = pd.read_csv(file, usecols=lambda x: not "_std" in x.lower())

        if usecols is not None:
            data = data.iloc[:,usecols]
        
            
    else:
        if usecols is not None:
            data = pd.read_csv(file,usecols=usecols)
        else:
            data = pd.read_csv(file)
        
    
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
    
    if errorbars:
        # assume that each data column is followed by an errorbar column
        x = data.index.values
        err = data.iloc[:,1::2].values
        dat = data.iloc[:,0::2].values
        la = data.iloc[:,0::2].columns.values
                
        
        for d,e,l in zip(dat.T, err.T, la):
            li, = plt.plot(x, d, '.-', label=l)
            c = li.get_c()
            plt.fill_between(x, d-e, d+e, facecolor=c, alpha=0.5)
            
            if polyfit is not None:
                m = ~np.isnan(d)
                p = np.polyfit(x[m],d[m],polyfit,w=1/e[m])
                print("{:s} polyfit: {}".format(l, p))
                x_ = np.linspace(x[m].min(), x[m].max(), 1000)
                y_ = np.poly1d(p)(x_)
                li.set_ls('')
                plt.plot(x_,y_,'--',c=li.get_c())
                
            
        plt.xlabel(data.index.name)
        plt.legend()
        
    
    else:
        x = data.index.values
        dat = data.values
        la = data.columns.values
                
        
        for d,l in zip(dat.T, la):
            li, = plt.plot(x, d, '.-', label=l)
            
            if polyfit is not None:
                m = ~np.isnan(d)
                p = np.polyfit(x[m],d[m],polyfit)
                print("{} polyfit: {}".format(l, p))
                x_ = np.linspace(x[m].min(), x[m].max(), 1000)
                y_ = np.poly1d(p)(x_)
                li.set_ls('')
                plt.plot(x_,y_,'--',c=li.get_c())
            
            
        plt.xlabel(data.index.name)
        plt.legend()
        
    if logx:
        plt.semilogx()
    elif logy:
        plt.semilogy()
    elif loglog:
        plt.loglog()
        
    plt.show()