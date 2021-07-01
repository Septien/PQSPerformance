import os
import csv
import numpy as np

folder = "memoryPerformance/"
ciphers = ["SABER=1", "KYBER=1", "NTRU=1", "NTRUP=1", "FRODO=1"]
massiffile = ["saber/saber", "kyber/kyber", "ntru/ntru", "ntrup/ntrup", "frodo/frodo"]
operation = ["TOTAL=1", "KEYGEN=1", "ENC=1", "DEC=1"]
ext = ".out"
rm = "rm test"
make = "make test "
valgrind = "valgrind --tool=massif --stacks=yes --massif-out-file="
N = 1

def measureMemory():
    # For each cipher, measure its memory consumption
    for i in range(5):
        for j in range(N):
            # make with the memory option enabled, and desired operation
            for k in range(1):
                # Remove test binary
                os.system(rm)
                cmd = make + "test " + ciphers[i] + " MEMORY=1 DEBUG=1 RPI=1" + operation[k]
                os.system(cmd)

                # Profile memory with valgrind
                cmd = valgrind + folder + massiffile[i] + "_" + operation[k].split("=")[0] + "_" + str(j) + ext + " ./test"
                print(cmd)
                os.system(cmd)

def readThreeLines(file):
    file.readline()
    file.readline()
    file.readline()

def getTotalMemory(file):
    heap = int(file.readline().split("=")[1])
    heapExtra = int(file.readline().split("=")[1])
    stack = int(file.readline().split("=")[1])
    return heap + heapExtra + stack

def getMemoryUsageAll():
    # Read the generated output file, and get the maximum amount of memory used per KEM
    for i in range(4):
        # Get the array of values per operation
        memUsageAll = []
        for k in range(4):
            # Get the maximum value for each iteration
            memUsage = []   # Stores the max values for all files
            for j in range(N):
                fileN = folder + massiffile[i] + "_" + operation[k].split("=")[0] + "1_" + str(j) + ext
                print(fileN)
                memUsageOp = []
                with open(fileN, "r") as file:
                    # Read the first three lines:
                    readThreeLines(file)
                    # Find the max value
                    for line in file:
                        # Search the following '#' character
                        if line[0] == "#":
                            # Read the following three lines
                            readThreeLines(file)
                            # Get the total amount of memory
                            total = getTotalMemory(file)
                            memUsageOp.append(total)
                memUsage.append(memUsageOp.copy())
                print(memUsage)
        memUsageAll.append(memUsage.copy())
    print(memUsageAll)
    return memUsageAll

def getMemoryUsageMax():
    """
    Get the maximum memory used for all files.
    """
    # Read the generated output file, and get the maximum amount of memory used
    memUsageAll = []
    for i in range(4):
        memUsage = []   # Stores the max values for each file
        for j in range(N):
            fileN = memory + massiffile[i] + "_" + str(j) + ext
            maxM = 0
            with open(fileN, "r") as file:
                # Read the first three lines:
                readThreeLines(file)
                # Find the max value
                for line in file:
                    # Search the following '#' character
                    if line[0] == "#":
                        # Read the following three lines
                        readThreeLines(file)
                        # Get the total amount of memory
                        total = getTotalMemory(file)
                        if (total > maxM):
                            maxM = total
            memUsage.append(maxM)
        memUsageAll.append(memUsage.copy())
    return memUsageAll

def getMemoryUsageKEM():
    """
    Get the data of memory usage per KEM, all the operations
    """
    # For each kem
    totalValues = []
    for i in range(5):
        fileN = folder + massiffile[i] + "_TOTAL_0" + ext
        values = []
        print(fileN)
        with open(fileN, "r") as file:
            readThreeLines(file)
            for line in file:
                if line[0] == "#":
                    readThreeLines(file)
                    total = getTotalMemory(file)
                    values.append(total)
        totalValues.append(values.copy())
    return totalValues

def saveData(data, file, delimiter, op=True):
    m = np.array(data, dtype=object)
    mT = m.transpose()
    with open(file, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        cipherS = ["LightSaber", "Kyber512", "NTRUhps2048509", "NTRULPr653", "Frodo640"]
        writer.writerow(cipherS)
        if op:
            operationS = [c.split("=")[0] for c in operation]
            writer.writerow(operationS)
        writer.writerows(mT)

if __name__ == '__main__':
    #measureMemory()
    m = getMemoryUsageKEM()
    saveData(m, "memoryPerformance/memoryPerformance.csv", ",", False)
