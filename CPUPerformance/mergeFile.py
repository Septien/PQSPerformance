"""
"""

import csv
import numpy as np

def mergeFiles(file, unit, delimiter):
    """
    Read the files corresponding to the CPU performance of the KEMs,
    get the columns corresponding to 'unit' unit, and merge in 'file'.
    -unit: unit of performance. sec -> second, cyc -> cycles
    """
    kem = ["ligthsaber", "kyber512", "ntruhps2048509", "ntrulpr653", "frodoKEM640"]
    perf = "Performance"
    ext = ".csv"
    with open(unit + file, "w") as File:
        writer = csv.writer(File, delimiter=delimiter)
        # Write the operations and units
        if unit == "time":
            writer.writerow(["KeyGen (uS)", "Enc (uS)", "Dec (uS)"])
        if unit == 'cycles':
            writer.writerow(["KeyGen (cycles)", "Enc (cycles)", "Dec (cycles)"])
        for k in kem:
            kemF = k + perf + ext
            with open(kemF, "r") as f:
                reader = csv.reader(f, delimiter=delimiter)
                r = next(reader)
                #Write the name of the KEM
                writer.writerow([k])
                # Get the data
                row = [next(reader)]
                row.append(next(reader))
                row.append(next(reader))
                if unit == 'cycles':
                    r = next(reader) # read first line
                    row = [next(reader)]
                    row.append(next(reader))
                    row.append(next(reader))
                writer.writerows(row)

if __name__ == '__main__':
    mergeFiles("CPUPerformance.csv", "time", delimiter=',')
    mergeFiles("CPUPerformance.csv", "cycles", delimiter=',')
