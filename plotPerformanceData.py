"""
Plot the data corresponding to the performance of the KEMs.
The performance data available corresponds to the following variables:
    -CPU cycles and time.
    -Memory usage.
    -Packet size.

The data for the CPU usage is at:
    -CPUPerformance/cyclesCPUPerformance.csv
    -CPUPerformance/timeCPUPerformance.csv

The data for the memory usage is at:
    -memoryPerformance/memoryPerformance.csv

The data for the packet size is at:
    -packetsPerformance/packetPerformance.csv

The CPU and packet performance files, have the following format:
    -Fields.
    -KEM.
    -Data.
The firs row contains the name of the fields measured, for each variable.
Then comes the name of the KEM for all of them, and finally the data 
associated to the field and the KEM. The first entry of the "Fields" row 
corresponds to the first row of the Data section, and so on.

The file containing data about the memory has a similar format:
    -KEM.
    -Data.
The KEM row indicates the name of the KEM under measure, and the Data section
contains the data. The first row corresponds to the first KEM, and so on. The
units are in bytes.
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd

def loadDataCPUPerformance(file, delimiter, nKEM):
    """
    Load the data for CPU performance following the established format.
    Return a matrix of size (3 * m) * N, where m is the number of kems, and 
    N is the number of executions; the name of the fields; and the units.
    """
    fields = []
    unit = []
    kem = []
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        # Get the fields and units
        r = next(reader)
        fields = [r[0].split(" ")[0], r[1].split(" ")[0], r[2].split(" ")[0]]
        unit = r[0].split(" ")[1]
        for i in range(nKEM):
            # Get the name of the KEM
            kem.append(next(reader))
            # Get the data
            data.append(next(reader))
            data.append(next(reader))
            data.append(next(reader))
    return fields, unit, kem, np.array(data, dtype=object)

def loadDataMemory(file, delimiter):
    """
    Loads data of memory performance for each of the KEMs.
    Returns a 5 * N matrix, where N is the number of executions.
    """
    data = []
    kem = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        kem = next(reader)
        maxLen = 0
        for row in reader:
            if len(row) > maxLen:
                maxLen = len(row)
            d = [int(r) for r in row]
            data.append(d)
        maxLen += 1
        # Normalize the length of the rows
        for i in range(len(data)):
            for j in range(len(data[i]), maxLen):
                data[i].append(0)
    return kem, np.array(data, dtype=object)
        
def loadDataPacket(file, delimiter):
    """
    Loads the data corresponding to the packet performance.
    We currently are only interestedi in the following variables:
        -Number of bytes transmitted.
        -Duration of the connection.
        -Number of packets sent.
    Returns the name of the fields, the name of the KEMs, and a 
    matrix of size (m * 3) * N, where m is the number of KEMS, 
    and N the number of runs.
    """
    kemData = []
    kem = []
    fields = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        # Get the field information
        row = next(reader)
        fields = [row[0], row[1], row[6]]
        i = 0
        for row in reader:
            # Get the KEMs name
            if i % 10 == 0:
                kem.append(row)
            # Get the number of packets
            if i % 10 == 1:
                d = [int(r) for r in row]
                kemData.append(d)
            # Get the number of bytes
            if i % 10 == 2:
                d = [int(r) for r in row]
                kemData.append(d)
            # Get the duration of the connection
            if i % 10 == 6:
                d = [int(r) for r in row]
                kemData.append(d)
            
            i += 1
    return kem, fields, np.array(kemData)

def computeStatistics(data, pkt=False):
    """
    Computes the statistics for each variable of interest. As each 
    variable has different fields, and for each field the statistics 
    are computed, it is needed to indicate the current variable.
    Returns an array with statistics in the following order:
        -Mean.
        -Maximum.
        -Standard Deviation.
        -Variance.
    """
    statistics = []
    for row in data:
        st = [np.mean(row), np.amax(row), np.std(row), np.var(row)]
        statistics.append(st)
    return statistics


def saveStatistics(filename, delimiter, kems, data, fields=None):
    """
    Save the statistics data on a file called 'filename', a csv file.
    On the first row, the name of the kems will be stored. If the variable
    has fields, the following road contains the name of them. On the
    rest of the file, the statistics data are stored.
    """
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(kems)
        if fields:
            writer.writerow(fields)
        writer.writerows(data)


if __name__ == '__main__':
    #fields, unit, kem, data = loadDataCPUPerformance("CPUPerformance/cyclesCPUPerformance.csv", ',', 5)
    #kem, data = loadDataMemory("memoryPerformance/memoryPerformance.csv", ',')
    kem, fields, kemData = loadDataPacket("packetsPerformance/packetPerformance.csv", ',')
    statistics = computeStatistics(kemData)
    saveStatistics("packetStt.csv", ',', kem, statistics, fields)
