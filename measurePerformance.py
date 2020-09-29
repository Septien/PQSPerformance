"""
"""

import os

def measurePerformance():
    """
    For each cipher, execute the performances tests.
    """
    ciphers = ["NTRUP=1", "NTRU=1", "SABER=1", "KYBER=1", "FRODO=1"]
    files = ["ntrulpr653", "ntruhrss701", "ligthsaber", "kyber512", "frodoKEM640"]
    perf = "Performance.csv"
    folder = "CPUPerformance/"
    for i in range(len(ciphers)):
        os.system("rm test")
        cmd = "make test " + ciphers[i] + " TIME=1"
        os.system(cmd)
        output = folder + files[i] + perf
        cmd = "./test " + output
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    measurePerformance()