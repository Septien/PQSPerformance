"""
Merge the files containing information about packets.
The fields we are interested are:
    -Total packets sent (5).
    -Total bytes sent (6).
    -Bytes sent from A to B (client -> server) (7).
    -Packets A->B (8).
    -Bytes sent from B to A (9).
    -Packets B->A (10).
    -Duration (11).
    -Bits/s A->B (12).
    -Bits/s B->A (13).

The data is saved on the files kemPacket.csv, where kem is either of:
kyber512, frodoKEM640, lightsaber, ntruhrss701.
"""

import csv
import numpy as np

def mergeFiles(outputfile, delimiter):
    """
    Load the files containing the package data, gather the required fields (indicated on top),
    and save them on a single file.
    """
    kems = ["kyber512", "lightSaber", "p256", "ntru", "x25519"]
    packet = ".csv"
    # Open the file containing the information
    with open(outputfile, "w") as out:
        writer = csv.writer(out, delimiter=delimiter)
        # Write the information of the columns (from right to left -> up to down)
        writer.writerow(["Packets","Bytes","Packets A → B","Bytes A → B","Packets B → A","Bytes B → A","Duration","Bits/s A → B","Bits/s B → A"])
        for k in kems:
            # Write what kem is the data from
            writer.writerow([k])
            file = k + packet
            with open(file, "r") as f:
                reader = csv.reader(f, delimiter=delimiter)
                # Get the header row
                r = next(reader)
                # Read all the file and the required data
                data = []
                for row in reader:
                    r = row[4:10] + row[11:]
                    data.append(r)
                m = np.array(data, dtype=object)
                mT = m.transpose()
                writer.writerows(mT)

if __name__ == '__main__':
    mergeFiles("packetPerformance.csv", ',')
