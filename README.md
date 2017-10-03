# smokerpi
_Collection of scripts for automating and monitoring a diy electric smoker_

## Python Modules
* influxlogger.py
    * Read thermometers
    * Log temperatures to database
* heater.py
    * Turn on and off a GPIO pin according to a dutycycle (To switch a relay, in my implementation)
* pid.py
    * The P.I.D. algorithm that determines how much heat is needed
* dutycycle.py
    * Convert real-number into appropriate heater duty cycle
* smokerpi.py
    * Get temperature setting from user
    * Initialize pid.py with temperature setting
    * loop:
        1. Get temps from database
        2. Send temps to pid.py, get heat number
        3. Send heat number to dutycycle.py, get 0 < dutycycle < 1
        4. Send dutycycle to heater.py
* creds.py
    * Contains sensitive database credentials
        * **INFLUX_DB** name of database set up in influxdb
        * **INFLUX_HOST** probably "localhost"
        * **INFLUX_PASS** password for database "INFLUx_db"
        * **INFLUX_USER** username for owner of "INFLUX_DB"
        * **INFLUX_PORT** port number set up in influxdb
        * **ONE_WIRE_THERM_SERIAL** serial number for 1-wire thermometer (if you are using one) (see below)
* thermometer.py
    * Contains Thermometer base class
        * Inheriting classes must implement read_temp(), which returns current temperature in Celsius
* onewire.py
    * Thermometer subclass that reads a 1-wire thermometer via "/sys/bus/w1/devices"
* ktype.py
    * Thermometer subclass that reads a k-type thermocouple via C module (see below), via MAX6675 chip breakout board
* meatprobe.py
    * Thermometer subclass that reads a thermistor via an ADC
## C Modules
* kType.c
    * Print temperature value to stdout (will output Fahrenheit if argv[1] == "F").
    * Depends on wiringPi library
    
 ** Other
 * influxlogger.service
     * systemd unit file for running influxlogger.py as a service, on Linux
 
## Things you will need:
* **Raspberry Pi** (Any version will work, however, I'm currently using a model B (J8 header)
* **Temperature sensor(s)** (I am using a thermistor (meat probe), a k-type thermocouple (top of smoker), and a 1-wire integrated temperature sensor (monitor for solid state relay))
  * You only actually need one thermometer, to be used for PID feedback. The k-type thermocouple can handle the high temps, so it's a good type to use for that.
* **Heat source** with a wall plug (I'm using the heating element from a countertop rotisserie) 
* A way to **switch the heat** on and off (I'm using a solid state relay, but a 433 Mhz wireless outlet can work as well)

## Setting up the temperature logger

### Configuring thermometers
* TODO

### Logging 
You have some choices, in order of increasing complexity:
1. Run influxlogger.py in a terminal window, or via ssh, and stay logged in while using smokerpi
2. Run influxlogger.py in a detached"screen" session. "screen" is a Linux utility that allows you to "detach" from a terminal session, running a process in the background.
3. **recommended** Install influxlogger.service in /lib/systemd/system/ and register it via systemctl

# Configuring 1-wire temperature sensor
* The DS18B20 temperature sensor that I use uses the 1-wire protocol.
* After installing the device on your Raspberry Pi, you will need to get the serial number. You can find this by navigating to the /sys/bus/w1/devices folder, and listing its contents.
* Copy this value to ONE_WIRE_THERM_SERIAL in creds.py 
