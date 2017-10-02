#! /usr/bin/python
import os
import time
import sys
import datetime
from creds import *
from influxdb import InfluxDBClient
import onewire 
import ktype
INFLUX_SESSION = "autosmoker_temps"
interval = 4  
now = datetime.datetime.now()
runNo = now.strftime("%Ym%d%H%M")

print("Session: " + INFLUX_SESSION)
print("RunNo: " + runNo)
t = onewire.OneWire()
kt = ktype.Ktype()
client = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PASS,
        INFLUX_DB)
try:
    while True:
        k = kt.get_f()
        f = t.get_f()
        iso = time.ctime()
        json_body = [
            {
                "measurement": INFLUX_SESSION,
                "tags": {
                    "run": runNo,
                },
                "time": iso,
                "fields": {
                    "temperature": f,
                    "ktypeTemp": k,
                }
            }
        ]
	print(json_body)
        client.write_points(json_body)
        time.sleep(interval)
except KeyboardInterrupt:
    print("logging interrupting via keyboard")
    exit()

