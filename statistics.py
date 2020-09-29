
import csv
import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def loadDataTime(inputfile, delimiter):
    """
    Loads data from a csv file.
    If execution is True, the name of the file indicates the KEM, and the 
    format of the file is the following:
        Op (units), ...
        values, ...
    It has six rows, the first three correspond to seconds units, and the
    last three correspond to cycle count.
    """
    operation = []
    valuesuS = []
    valuesCy = []
    units = []
    with open(inputfile, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        row1 = next(reader)
        operation = [r.split(" ")[0] for r in row1[0:3]]
        units = [row1[0].split(" ")[1], row1[3].split(" ")[1]]
        row1 = next(reader)
        for row1 in reader:
            valuesuS.append(row1[0:3])
            valuesCy.append(row1[3:])

    return operation, units, valuesuS, valuesCy

def loadDataMem(inputfile, delimiter):
    """
    If the execution is False, the file corresponds to memory data, and the
    format is the following.
        KEM1,KEM2,...
        dataKem1,
        dataKEM2,
        ...
    """
    kem = []
    values = []
    with open(inputfile, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        kem = next(reader)
        for row in reader:
            row1 = [int(r) for r in row]
            values.append(row1)

    return kem, values

def computeMean(data):
    """
    Data is a single-row array
    """
    assert type(data) is list
    total = 0
    n = len(data)
    for d in data:
        total += d
    return total / n

def Variance(data):
    """
    Computes the variance of the data
    """
    mean = computeMean(data)
    v = 0
    for d in data:
        v += m.pow(d - mean, 2)
    return v / len(data)

def SD(data):
    """
    Computes the Standard Deviation
    """
    assert type(data) is list
    return m.sqrt(Variance(data))

def max(data):
    """
    """
    assert type(data) is list
    maxD = 0
    for d in data:
        if d > maxD:
            maxD = d
    return maxD

def plotMemoryBar(values, ciphers, outputfile, title):
    """
    """
    # Plot the performance of each cipher with a logarithmic scale
    #colors = 'rgbkymc'
    dfTFastest = pd.DataFrame({'Memory Usage' : values}, index=ciphers)
    fig, ax = plt.subplots()
    dfTFastest.plot(kind="bar", ax=ax, rot=45, grid=True, logy=True)
    plt.title(title)
    plt.ylabel("Bytes")
    plt.tight_layout()
    plt.savefig(outputfile) #'./images/KEM_microseconds_FL.svg'
    plt.close()

def getMaxLen(values):
    data = [len(values[0]), len(values[1]), len(values[2]), len(values[3])]
    return max(data)

def fillZeros(data, Len):
    """
    Fill the array "data" with zeros, until the desired Len is reach
    """
    n = Len - len(data)
    assert n >= 0, "Incorrect input"
    if n == 0:
        return

    for i in range(n):
        data.append(0)

def plotMemoryLine(values, ciphers, outputfile):
    """
    """
    maxL = getMaxLen(values) + 1
    fillZeros(values[0], maxL)
    fillZeros(values[1], maxL)
    fillZeros(values[2], maxL)
    fillZeros(values[3], maxL)
    df = pd.DataFrame({ciphers[0] : values[0], ciphers[1] : values[1], ciphers[2] : values[2], ciphers[3] : values[3]}, index=range(maxL))
    fig, ax = plt.subplots()
    df.plot(kind="line", ax=ax, rot=0, grid=True, logy=True)
    plt.title("Memory usage of the ciphers across time")
    plt.ylabel("Bytes")
    plt.xlabel("Snapshots")
    plt.tight_layout()
    plt.savefig(outputfile)
    plt.close()


def plotDataBoxplot(data, ciphers, outputfile, log=False):
    """
    Plots the data in a boxplot
    """
    fig = plt.figure(1, figsize=(9,6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data)
    ax.set_xticklabels(ciphers)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    if log:
        plt.yscale('log')
    plt.xlabel("Cipher")
    plt.ylabel("Bytes")
    plt.grid(True)
    plt.tight_layout()
    fig.savefig(outputfile, bbox_inches='tight')

if __name__ == '__main__':
    #
    kem, values = loadDataMem("memoryPerformance3.csv", delimiter=",")
    #
    valuesMax = [max(values[0]), max(values[1]), max(values[2]), max(values[3])]
    valuesSD = [SD(values[0]), SD(values[1]), SD(values[2]), SD(values[3])]
    valuesV = [Variance(values[0]), Variance(values[1]), Variance(values[2]), Variance(values[3])]
    #
    plotMemoryBar(valuesMax, kem, "imagesMem/memoryMax.svg", "Maximum Memory Usage")
    plotMemoryBar(valuesSD, kem, "imagesMem/memorySD.svg", "Memory Standard Deviation")
    plotMemoryBar(valuesV, kem, "imagesMem/memoryV.svg", "Memory Variance")
    plotMemoryLine(values, kem, "imagesMem/memoryBh.svg")
    plotDataBoxplot(values, kem, "imagesMem/memoryDist.svg", True)
    plotDataBoxplot(values[0:3], kem, "imagesMem/memoryDist2.svg")
