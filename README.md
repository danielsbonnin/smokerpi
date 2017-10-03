# smokerpi
Collection of scripts for automating and monitoring a diy electric smoker

# Things you will need:
* **Raspberry Pi** (Any version will work, however, I'm currently using a model B (J8 header)
* **Temperature sensor(s)** (I am using a thermistor (meat probe), a k-type thermocouple (top of smoker), and a 1-wire integrated temperature sensor (monitor for solid state relay))
  * You only actually need one thermometer, to be used for PID feedback. The k-type thermocouple can handle the high temps, so it's a good type to use for that.
* Mains-pluggabe **heat source** (I'm using the heating element from a countertop rotisserie) 
* A way to **switch the heat** on and off (I'm using a solid state relay, but a 433 Mhz wireless outlet can work as well)
* An **influxdb** installation (or any lightweight database you can get to work with your front-end of choice)
# Optional (*nice to have*)
* **Grafana** installation (for pretty graphs and remote monitoring)

# Installing the temperature logger
* influxlogger.service path: /lib/systemd/system/influxlogger.service

# Configuring 1-wire temperature sensor
* The DS18B20 temperature sensor that I use uses the 1-wire protocol.
* After installing the device on your Raspberry Pi, you will need to get the serial number. You can find this by navigating to the /sys/bus/w1/devices folder, and listing its contents.
* Copy this value to ONE_WIRE_THERM_SERIAL in creds.py 
