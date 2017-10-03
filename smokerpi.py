import time
import math
import os
import argparse
from influxdb import InfluxDBClient
from importlib import import_module
import smokerpi.heater as heater
import smokerpi.pid as pid 
import smokerpi.dutycycle as dutycycle
from creds import *
import thermometers 
from smokerpi.settings import *
DUTY_CYCLE_DURATION = 60 
DEAD_TIME = 120
LOW_THRESHOLD = 10
SECS_PER_DEGREE_F = 5 
parser = argparse.ArgumentParser()
parser.add_argument("temp", type=int, help="the temperature to set")
parser.add_argument("-p", "--prop", type=float, help="proportional input to pid")
parser.add_argument("-i", "--integral", type=float, help="integral input to pid")
parser.add_argument("-d", "--deriv", type=float, help="derivative input to pid")
parser.add_argument("-o", "--outside_temp", type=float, help="outside temperature")
args = parser.parse_args()
tempsetting = args.temp
if args.prop:
    p = args.prop
else:
    p = 1.0
if args.integral:
    i = args.integral
else:
    i = 0
if args.deriv:
    d = args.deriv
else:
    d = 0
if args.outside_temp:
    outside_temp = args.outside_temp
else:
    outside_temp = 75

def get_f(client):
    temp_query = 'select last({}) from {} where timestamp > now() - 1h'.format(PID_CONTROL_THERM, INFLUX_SESSION)
    q = client.query(temp_query)
    l = list(q.get_points())
    temp = l[0]['last']
    return temp

dc = dutycycle.DutyCycle(tempsetting, DUTY_CYCLE_DURATION, outside_temp)
# set pid proportion, integral, derivative
pid = pid.PID(p, i, d)
h = heater.Heater(DUTY_CYCLE_DURATION, dc.duty_prop)
client = InfluxDBClient(
    INFLUX_HOST, 
    INFLUX_PORT, 
    INFLUX_USER, 
    INFLUX_PASS, 
    INFLUX_DB)
session = INFLUX_SESSION
pid.SetPoint = tempsetting 
pid.setSampleTime(1)
pid.setWindup(5)
proceed = True
temp = get_f(client)
if (tempsetting - temp) > LOW_THRESHOLD: 
    h.heatOn()
    time.sleep((tempsetting - temp) * SECS_PER_DEGREE_F)
    h.heatOff()
    time.sleep(DEAD_TIME)
while proceed == True:
    try:
        temp = get_f(client)
        pid.update(temp)
        duty_prop = dc.process_pid_output(pid.output)
        h.setCycle(duty_prop)
        print("***temp " + str(temp) + " duty_prop " + str(duty_prop))
        iso = time.ctime()
        json_body = [
                {
                    "measurement": session,
                    "time": iso,
                    "fields": {
                        "tempsetting": tempsetting,
                        "dutyprop": duty_prop,
                        "pidoutput": pid.output
                        }
                    }
                ]
        client.write_points(json_body)            
        h.runCycle()
    except KeyboardInterrupt:
        proceed = False
        h.heatOff()
time.sleep(1)
h.heatOff()
