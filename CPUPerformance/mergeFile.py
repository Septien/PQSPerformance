"""
"""

import csv
import numpy as np

kem = ["kyber", "ntrup", "ntru", "saber", "frodo"]
perf = "Performance"
ext = ".csv"

def mergeFiles(file, unit, delimiter):
    """
    Read the files corresponding to the CPU performance of the KEMs,
    get the columns corresponding to 'unit' unit, and merge in 'file'.
    -unit: unit of performance. sec -> second, cyc -> cycles
    """
    with open(unit + file, "w") as File:
        writer = csv.writer(File, delimiter=delimiter)
        for k in kem:
            kemF = k + perf + ext
            with open(kemF, "r") as f:
                reader = csv.reader(f, delimiter=delimiter)
                writer.writerow([k])
                row = [next(reader)]
                row.append(next(reader))
                row.append(next(reader))
                if unit == 'cycles':
                    row = [next(reader)]
                    row.append(next(reader))
                    row.append(next(reader))
                writer.writerows(row)

if __name__ == '__main__':
    mergeFiles("CPUPerformance.csv", "time", delimiter=',')
