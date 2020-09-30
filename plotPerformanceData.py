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
            kem.append(next(reader)[0])
            # Get the data
            row = next(reader)
            data.append([float(r) for r in row[:-1]])
            row = next(reader)
            data.append([float(r) for r in row[:-1]])
            row = next(reader)
            data.append([float(r) for r in row[:-1]])
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
    return np.array(statistics)


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

def barGraph(dictionary, kems, units, imageName, logy):
    """
    Uses matplotlib to plot data on a graph bar.
    https://markhneedham.com/blog/2018/09/18/matplotlib-remove-axis-legend/
    https://stackoverflow.com/questions/30228069/how-to-display-the-value-of-the-bar-on-each-bar-with-pyplot-barh
    https://www.reddit.com/r/learnpython/comments/9l948p/having_a_bit_of_trouble_sorting_bars_in/
    """
    # Plot the performance of each cipher with a logarithmic scale
    dfTFastest = pd.DataFrame(dictionary, index=kems)
    fig, ax = plt.subplots()
    dfTFastest.plot(kind="bar", ax=ax, rot=45, grid=True, logy=True)
    plt.ylabel(units)
    plt.tight_layout()
    plt.savefig(imageName + ".svg")
    plt.close()

def plotStatisticsOnBarGraph(statistics, statisticsNames, fields, variable, kems, imageName, units, logy=False):
    """
    Plot all the statistics on a bar graph, and save the image to 'imageName'.
    Inputs:
        -statistics: array containing the statistics.
        -statisticsName: name of each statistic.
        -fields: array containing the name of the fields for each variable.
        -variable: name of the variable under study.
        -kems: name of the kem under study.
        -imageName: name of the image to save.
        -logy: logarithmic scale on y-axis?
    Group by field, if necessary
    """
    for i in range(len(statisticsNames)):
        df = {}
        # Get the ith statistics
        ithSt = statistics[:, i]
        # Group by field
        nFields = len(fields)
        for j in range(nFields):
            fieldStatistics = []
            for k in range(len(kems)):
                fieldStatistics.append(ithSt[j + (k * nFields)])
            df[fields[j]] = fieldStatistics.copy()
        barGraph(df, kems, unit, imageName + statisticsNames[i] , logy)


if __name__ == '__main__':
    # For CPU performance
    fields, unit, kem, data = loadDataCPUPerformance("CPUPerformance/cyclesCPUPerformance.csv", ',', 5)
    statistics = computeStatistics(data)
    plotStatisticsOnBarGraph(statistics, ["Mean", "Max", "SD", "Var"], fields, "CPU", kem, "images/cpuPerformance", unit, True)
    saveStatistics("statistics/cpuStat.csv", ',', kem, statistics, fields)

    # For memory performance
    kem, data = loadDataMemory("memoryPerformance/memoryPerformance.csv", ',')
    statistics = computeStatistics(data)
    plotStatisticsOnBarGraph(statistics, ["Mean", "Max", "SD", "Var"], ["Memory"], "Memory", kem, "images/memoryPerformance", "bytes", True)
    saveStatistics("statistics/memoryStat.csv", ',', kem, statistics)
    # For packet performance
    kem, fields, kemData = loadDataPacket("packetsPerformance/packetPerformance.csv", ',')
