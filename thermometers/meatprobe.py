import time
import math
import Adafruit_ADS1x15
beta = 4132.04
SAMPLE_SIZE = 5
MAX_AGE = 5 # update if time since last reading > MAX_AGE
class Probe:
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.update()
        self.last_reading

    def update(self):
        accum = 0
        for i in range(SAMPLE_SIZE):
            accum += self.adc.read_adc(0, gain=1)
            time.sleep(0.25)
        res = accum / SAMPLE_SIZE
        volts = (float(res) * 4.09) / 2**15
        # using voltage divider with 100kOhms resistor
        ohms = 1/volts * 330000 - 100000
        lnohms = math.log(ohms)
        self.k = beta / math.log(ohms/(100000*math.exp(-beta/298)))
        self.c = self.k - 273.15
        self.f = (self.c * 1.8) + 32
        self.last_reading = time.time()

    def get_f(self):
        if time.time() - self.last_reading > 10:
            self.update()
        return self.f
    
    def get_c(self):
        if time.time() - self.last_reading > 10:
            self.update()
        return self.c

    def get_k(self):
        if time.time() - self.last_reading > 10:
            self.update()
        return self.k
