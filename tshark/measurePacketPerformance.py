"""
"""

import os
import time

def runClient(clientcmd):
    """
    """
    os.system(clientcmd)
    time.sleep(15)

def configStrings():
    """
    Set all the necessary configuration
    """
    kems = ["kyber512", "lightsaber", "ntru_hps2048509", "P-256", " X25519"]
    # For tshark
    host = "host 13.65.102.222"
    interface = "-i wlan0 "
    options = " -t ad -w "
    captureFRoute = "/home/pi/Documents/Maestria/tshark/"
    baseFilename = "_capture.pcapng "

    # For the client
    client = "/home/pi/Documents/Maestria/client/client "
    # Send kill signal to the process with name client
    kill = "kill -9 $(ps -C client -o pid=)"
    killtshark = "kill -9 $(ps -C tshark -o pid=)"

    N = 1000
    filename = "captureConnection.pcapng "
    tsharkcmd = "sudo tshark " + interface + options + captureFRoute + filename + host + " &"
    # Execute tshark command
    print(tsharkcmd)
    os.system(tsharkcmd)
    time.sleep(10)
    for kem in kems:
        clientcmd = client + kem + " &"
        for n in range(N):
            runClient(clientcmd)
    os.system(killtshark)

if __name__ == '__main__':
    configStrings()
