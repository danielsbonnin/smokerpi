#! /usr/bin/python
import os
k = os.popen('./readTemp')
k = k.readline()
ftemp = k.split(" ")[7]
print(ftemp)
