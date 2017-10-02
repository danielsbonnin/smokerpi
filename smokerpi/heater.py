"""
Turns on and off heating element according to a duty cycle
"""
import os
import time
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin = 17 
GPIO.setup(pin, GPIO.OUT)
class Heater:
    
    def __init__(self, dur=10, prop=0.5):
        
        self.dur = dur
        self.setCycle(prop)
        """self.prop = prop
        self.on_time = self.dur * self.prop
        self.off_time = self.dur - self.on_time"""
        self.on = False
 
    def setCycle(self, prop):
        """ Set duration and on/off proportion """
        if prop > 1 or prop < 0:
            raise ValueError("Duty Cycle proportion must be between 0 and 1")
        self.prop = prop
        self.on_time = self.dur * self.prop
        self.off_time = self.dur - self.on_time
        
    def runCycle(self):
        print("Starting new duty cycle")
        if self.on_time > 0:
            if self.on == False:
                self.on = True
                self.heatOn()
            time.sleep(self.on_time)
        if self.off_time > 0:
            if self.on == True:
                self.on = False
                self.heatOff()
            time.sleep(self.off_time)
            
    def heatOn(self):
        if os.name == 'nt': # for testing on windows
            print("turn on heater")
        else:
            GPIO.output(pin, GPIO.HIGH)
    def heatOff(self):
        if os.name == 'nt': # for testing on windows
            print("turn off heater")
        else:
            GPIO.output(pin, GPIO.LOW) 
            print("turning off heater")
    
    def stayOn(self, goal, heater, client, dur):
        print("temp is low: full blast")
        temp = get_f(client)
        h.heatOn()
        counter = 0
        while (temp - goal) < -20:
            counter += 1
            time.sleep(1)
            temp = get_f(client)
            if counter % 5 == 0:
                print("*** full blast ***\ntemp: " + str(temp))
        self.heatOff()

    def stayOff(goal, heater, client, dur):
        print("temp is high, no heat")
        temp = get_f(client)
        self.heatOff()
        counter = 0
        while (temp - goal) > 10:
            counter += 1
            time.sleep(1)
            temp = get_f(client)
            if counter % 5 == 0:
                print("*** heat off ***\ntemp: " + str(temp))
