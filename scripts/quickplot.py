#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Plot data in a file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', type=str, help='data filename')

    args = parser.parse_args()
    file = args.file
    
    plt.ioff()

    data = pd.read_csv(file, index_col=0)

    plt.plot(data, '.-')
    
    plt.show()