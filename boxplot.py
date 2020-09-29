import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

def loadData(filename, delimiter):
    """
    -filename: a csv file which contains the data from the
                ciphers' performance
    -delimiter: indicates how the csv file separates fields
    """
    assert type(filename) is str
    # Open the file
    operations = []
    values = []
    ciphers = None
    with open(filename, newline='', mode='r', encoding='utf-8-sig') as data:
        reader = csv.reader(data, delimiter=delimiter)
        ciphers = next(reader)[0:3]
        for row in reader:
            operations.append(row[0])
            nvalues = [float(r) for r in row[1:]]
            values.append(nvalues)
    op = [operations[0], operations[3], operations[6]]
    return values, op, ciphers

def setBoxColor(bp, color):
    """
    """
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

def plotData(data, operation, ciphers, units):
    """
    Plot the performance of the cipher using a boxplot.
    data:           Data to plot.
    operation:      Cipher operation.
    Ciphers:        name of the cipher.
    units:          Units of measurement,
    colors:         Colors of each category
    
    References
    https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
    # colors are from http://colorbrewer2.org/
    """
    newhope = [data[0], data[3], data[6]]
    round5 = [data[1], data[4], data[7]]
    frodokem = [data[2], data[5], data[8]]

    # Boxplot for keygen
    bpkg = plt.boxplot(newhope, positions=[1,4,7], sym='', widths=0.6)
    setBoxColor(bpkg, 'blue')
    # Boxplot for enc
    bpen = plt.boxplot(round5, positions=[2,5,8], sym='', widths=0.6)
    setBoxColor(bpen, 'red')
    # Boxplot for dec
    bpde = plt.boxplot(frodokem, positions=[3,6,9], sym='', widths=0.6)
    setBoxColor(bpde, 'green')

    # Set the labels
    plt.plot([], c='blue', label=ciphers[0])
    plt.plot([], c='red', label=ciphers[1])
    plt.plot([], c='green', label=ciphers[2])
    plt.legend()

    plt.xticks([1, 4, 6], operation)
    plt.tight_layout()
    plt.yscale('log')
    plt.show()

if __name__ == '__main__':
    values, operations, ciphers = loadData(filename="timing_sec.csv", delimiter=',')
    plotData(values, operations, ciphers, 'uS')
