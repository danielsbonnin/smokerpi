import os
import time
import threading
from thermometer import Thermometer
SAMPLE_SIZE = 10 
INTERVAL = 2 
LOW_CUTOFF = -30.0
HI_CUTOFF = 600.0
ERR_VAL = -666
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Ktype(Thermometer):
    """
    K Type thermocouple using MAX6675 amplifier
    Runs an executable "kType" from the local directory.
    See README for installation info
    """
    def __init__(self, interval=INTERVAL):
        Thermometer.__init__(self, interval)
    def read_temp(self):
        try:
            c = os.popen(os.path.join(BASE_DIR, 'kType') + ' C').readline()
            c = float(c)
        except Exception as e:
            print("There was an exception in ktype.py")
            raise
        if abs(c - ERR_VAL) > 1:
            self.c = c
            self.f = round(self.c * 9.0 / 5.0 + 32.0, 3)
            self.time_last_read = time.time()
        else:
            print("Thermocouple may be unplugged.")
            raise ValueError("kType returning error value")
        
if __name__ == "__main__":
    k = Ktype()
    print("The current temperature in Fahrenheit is {}".format(k.get_f()))
