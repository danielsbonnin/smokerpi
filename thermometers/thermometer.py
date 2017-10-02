import os
import time
import threading
SAMPLE_SIZE = 10 
INTERVAL = 2 
LOW_CUTOFF = -30.0
HI_CUTOFF = 600.0
ERR_VAL = -666
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Thermometer:
    """
    A base class for relevant thermometer functions for smokerpi
    """
    def __init__(self, interval=INTERVAL):
        self.time_last_read = 0
        self.f = -500
        self.c = -500
        self.interval = interval
        self.read_temp()
    def read_temp(self):
        raise NotImplemented()
        
    def get_f(self):
        if time.time() - self.time_last_read > self.interval:
            t = threading.Thread(target=self.read_temp)
            t.start()
        return self.f
    
    def get_c(self):
        if time.time() - self.time_last_read > self.interval:
            t = threading.Thread(target=self.read_temp)
            t.start()
        return self.c
    
    def read_continuous(self):
        while True:
            self.read_temp()
            print((self.c, self.f))
            time.sleep(1)
if __name__ == "__main__":
    k = Ktype()
    print(k.get_f())
