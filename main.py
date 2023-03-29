# -*- coding: utf-8 -*-

#Potato#8999
#id = 694246129906483311
#public key = 70c7073417dc12f36435054a09b02e269b85acb1f89ded5724a8f9a20122f0e1

###
#   Booting bots
###

import subprocess
import os, sys
import multiprocessing

def run_bot(file):
    subprocess.run([sys.executable, file])

if __name__ == "__main__":
    files = ["Potabot.py", "Eventbot.py"]
    processes = []
    for f in files:
        p = multiprocessing.Process(target=run_bot, args=(f,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()