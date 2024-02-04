# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 19:25:49 2021

@author: isnl
"""

# Daemon threads

import threading
import time

def timer():
    print()
    count = 0
    while True:
        time.sleep(1)
        count+=1
        print("logged in for: ",count,"seconds")
        
x = threading.Thread(target=timer)
x.setDaemon(True)
print(x.isDaemon())
x.start()



answer = input("Do you wish to exit?")