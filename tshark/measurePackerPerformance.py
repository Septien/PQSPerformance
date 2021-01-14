"""
"""

import os
import time

def runClient(tshrkcmd, clientcmd, killcmd):
    """
    """
    os.system(tshrkcmd)
    time.sleep(5)
    os.system(clientcmd)
    time.sleep(15)
    os.system(killcmd)

def configStrings():
    """
    Set all the necessary configuration
    """
    kems = ["lightsaber", "ntru_hps2048509", "P-256", " X25519"]
    # For tshark
    host = "host 13.65.102.222"
    interface = "-i eth0 "
    options = "-c 8 -t ad -w "
    captureFRoute = "/home/pi/Documents/Maestria/tshark/"
    baseFilename = "_capture.pcapng "

    # For the client
    client = "/home/pi/Documents/Maestria/client/client "
    # Send kill signal to the process with name client
    kill = "kill -s signal $(ps -C client -o pid=)"

    for kem in kems:
        filename = kem + baseFilename
        tsharkcmd = "sudo tshark " + interface + options + captureFRoute + filename + host + " &"
        clientcmd = client + kem + " &"
        runClient(tsharkcmd, clientcmd, kill)

if __name__ == '__main__':
    configStrings()