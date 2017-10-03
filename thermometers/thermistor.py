import time
import math
import Adafruit_ADS1x15
from thermometer import Thermometer
beta = 4132.04
SAMPLE_SIZE = 5
NEUTRAL_RESISTANCE = 100000 # 100K ohms. Adjust as needed.
MAX_AGE = 5 # update if time since last reading > MAX_AGE
class Thermistor(Thermometer):
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.update()
        self.last_reading

    def read_temp(self):
        accum = 0

        # Take average reading over SAMPLE_SIZE samples
        for i in range(SAMPLE_SIZE):
            accum += self.adc.read_adc(0, gain=1)
            time.sleep(0.25)
        res = accum / SAMPLE_SIZE

        volts = (float(res) * 4.09) / 2**15
        # using voltage divider with 100kOhms resistor
        ohms = 1/volts * 330000 - NEUTRAL_RESISTANCE
        lnohms = math.log(ohms)
        self.k = beta / math.log(ohms/(neutral_resistance*math.exp(-beta/298)))
        self.c = self.k - 273.15
        self.f = (self.c * 1.8) + 32
        self.last_reading = time.time()
        return self.c

    def get_f(self):
        if time.time() - self.last_reading > 10:
            self.update()
        return self.f
