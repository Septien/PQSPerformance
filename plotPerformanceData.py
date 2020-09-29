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
    Return a matrix of size 3*m*N, where m is the number of kems, and 
    N is the number of executions; the name of the fields; and the units.
    """
    fields = []
    unit = []
    kem = []
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(file, delimiter=delimiter)
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
    return fields, unit, kem, data

if __name__ == '__main__':
    loadDataCPUPerformance("")