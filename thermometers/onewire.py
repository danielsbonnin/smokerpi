import os
import time
import threading
import creds
from thermometer import Thermometer
INTERVAL = 2
DEVICE_NAME = creds.ONE_WIRE_THERM_SERIAL

class OneWire(Thermometer):
    """
    1-wire temperature sensor using w1_therm kernel module
    """
    def __init__(self, interval=INTERVAL, d_name=DEVICE_NAME):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.d_name = d_name
        self.temp_sensor = os.path.join('/sys/bus/w1/devices', self.d_name,'w1_slave')
        Thermometer.__init__(self, interval)
    
    def temp_raw(self):
        f = open(self.temp_sensor, 'r')
        lines = f.readlines()
        # sample output: ['73 01 4b 46 7f ff 0c 10 85 : crc=85 YES\n', '73 01 4b 46 7f ff 0c 10 85 t=23187\n']
        f.close()
        return lines

    def read_temp(self):
        lines = self.temp_raw()
        while lines[0].strip()[-3:]!='YES':
            time.sleep(0.5)
            lines = self.temp_raw()
        temp_output = lines[1].find('t=')

        if temp_output != -1:
            # temp in Kelvin is last number in second line
            temp_string = lines[1].strip()[temp_output+2:]
            self.c = round(float(temp_string)/1000.0, 3)
            self.f = round(self.c * 9.0 / 5.0 + 32.0, 3)
            self.time_last_read = time.time()
        else:
            raise ValueError("Unable to read {} at path {}".format(self.d_name, self.temp_sensor))

if __name__ == "__main__":
    t = OneWire()
    print("The current temperature in Fahrenheit is: {}".format(t.get_f()))
