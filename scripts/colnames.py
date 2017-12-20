#!/usr/bin/env python

import argparse


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Print column names for a csv file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', type=str, help='filename')
    args = parser.parse_args()
    file = args.file
    
    with open(file,'r') as infile:
    	l1 = infile.readline()

    cols = l1.split(',')

    for i,c in enumerate(cols):
    	print("[{: >2d}] {:s}".format(i,c))
