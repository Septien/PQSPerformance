"""
"""

import os
import time

def runClient(clientcmd, killcmd):
    """
    """
    os.system(clientcmd)
    time.sleep(15)
    os.system(killcmd)
    time.sleep(30)

def configStrings():
    """
    Set all the necessary configuration
    """
    kems = ["lightsaber", "ntru_hps2048509", "P-256", " X25519"]
    # For tshark
    host = "host 13.65.102.222"
    interface = "-i eth0 "
    options = " -t ad -w "
    captureFRoute = "/home/pi/Documents/Maestria/tshark/"
    baseFilename = "_capture.pcapng "

    # For the client
    client = "/home/pi/Documents/Maestria/client/client "
    # Send kill signal to the process with name client
    kill = "kill -9 $(ps -C client -o pid=)"
    killtshark = "kill -9 $(ps -C tshark -o pid=)"

    N = 1000
    for kem in kems:
        filename = kem + baseFilename
        tsharkcmd = "sudo tshark " + interface + options + captureFRoute + filename + host + " &"
        clientcmd = client + kem + " &"
        # Execute tshark command
        os.system(tsharkcmd)
        for n in N:
            runClient(clientcmd, kill)
        os.system(killtshark)

if __name__ == '__main__':
    configStrings()