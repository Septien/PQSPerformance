"""
Get files from list command
"""

import os

def readFile(file1, file2):
    with open(file1, "r") as file:
        with open(file2, "w") as w:
            for line in file:
                row = line.split()
                w.write(row[-1] + " ")

def getfiles():
    os.system("ls -r *.c >> c.txt")
    readFile("c.txt", "sources.txt")
    os.system("ls -r *.h >> h.txt")
    readFile("h.txt", "headers.txt")

if __name__ == '__main__':
    os.system("rm *.txt")
    getfiles()