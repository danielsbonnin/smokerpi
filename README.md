# 🔥 SmokerPi - IoT BBQ Temperature Control System

<div align="center">

**Because perfect BBQ is a control theory problem**

*Transform your electric smoker into a precision cooking machine with Raspberry Pi, PID control, and a dash of maker spirit.*

</div>

---

## 🎯 What Makes This Cool

SmokerPi is the intersection of three awesome things:
1. **Control Theory in Action** - Real-world PID algorithm maintaining stable temperatures
2. **Full-Stack IoT** - Hardware sensors → GPIO control → Database logging → Real-time feedback
3. **Practical Maker Project** - Solves the actual problem of inconsistent smoker temperatures

### The Problem
Electric smokers are notoriously bad at maintaining consistent temperatures. Manual control means babysitting your smoker all day, checking every 15 minutes, adjusting the heat. That's not relaxing BBQ - that's work.

### The Solution
**Set it and forget it.** SmokerPi uses a PID controller to automatically adjust heating elements, maintaining your target temperature within a few degrees for hours. No more overcooked brisket. No more raw chicken. Just perfectly consistent BBQ.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        SmokerPi System                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌─────────────┐     ┌────────────┐ │
│  │ Thermometers │ ───▶ │  InfluxDB   │────▶│   smokerpi │ │
│  │  - K-Type    │      │  Time Series│     │   Main Loop│ │
│  │  - 1-Wire    │      │   Database  │     └─────┬──────┘ │
│  │  - Thermistor│      └─────────────┘           │        │
│  └──────────────┘                                │        │
│                                                   │        │
│                                          ┌────────▼──────┐ │
│                                          │  PID Controller│ │
│                                          │  (Error → Heat)│ │
│                                          └────────┬──────┘ │
│                                                   │        │
│                                          ┌────────▼──────┐ │
│                                          │  Duty Cycle   │ │
│                                          │   Converter   │ │
│                                          └────────┬──────┘ │
│                                                   │        │
│                                          ┌────────▼──────┐ │
│                                          │     Heater    │ │
│  ┌──────────────┐                       │  GPIO Control │ │
│  │ Solid State  │ ◀──────────────────── │  (Pin 17/BCM) │ │
│  │    Relay     │                       └───────────────┘ │
│  └──────┬───────┘                                         │
│         │                                                 │
│         ▼                                                 │
│  ┌─────────────┐                                         │
│  │   Heating   │                                         │
│  │   Element   │                                         │
│  └─────────────┘                                         │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Component Overview

- **influxlogger.py** - Continuously reads thermometers and logs to time-series database
- **smokerpi.py** - Main control loop: reads temps → PID calculation → duty cycle → heater control
- **pid.py** - Classic PID algorithm (Proportional-Integral-Derivative control)
- **dutycycle.py** - Converts PID output to heating duty cycle with smart max limits
- **heater.py** - GPIO control for solid-state relay switching
- **thermometers/** - Pluggable thermometer implementations (K-type, 1-wire, thermistor)

---

## 🛠️ Hardware Setup

### Required Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Raspberry Pi** | Brain of the operation | Any model with GPIO (I use Model B) |
| **Temperature Sensor(s)** | Measure smoker & meat temps | K-type thermocouple (smoker), thermistor (meat) |
| **Heating Element** | Generate heat | Rotisserie heating element or similar |
| **Solid State Relay** | Switch high-voltage heating element | 40A SSR rated for your heater voltage |
| **MAX6675 Breakout** | K-type thermocouple amplifier | For K-type sensors |

### Wiring Diagram

```
Raspberry Pi GPIO 17 ──┬──▶ [SSR Input +]
                       │
Raspberry Pi GND ──────┴──▶ [SSR Input -]

AC Line (HOT) ──▶ [SSR Load In] ─┐
                                 │
[Heating Element] ◀──────────────┘
                ▼
              AC Neutral
```

⚠️ **Safety Warning**: The relay switches mains voltage. If you're not comfortable with electrical work, get help from someone who is. Improper wiring can cause fire or electrocution.

### Temperature Sensor Setup

**K-Type Thermocouple** (for smoker chamber temperature)
- Connect MAX6675 breakout to SPI pins
- Can handle high temperatures (up to 500°F+)
- Best for PID feedback loop

**1-Wire DS18B20** (optional, for relay monitoring)
- Connect to GPIO 4 (or configure w1-gpio)
- Enable 1-wire in raspi-config
- Find serial number: `ls /sys/bus/w1/devices/`

**Thermistor** (for meat probe)
- Connect to ADC (analog-to-digital converter)
- Good for monitoring meat internal temp

---

## 💻 Software Setup

### Prerequisites

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade

# Install Python dependencies
sudo apt-get install python3 python3-pip python3-rpi.gpio

# Install InfluxDB (time-series database)
sudo apt-get install influxdb influxdb-client
sudo systemctl start influxdb
sudo systemctl enable influxdb
```

### InfluxDB Setup

```bash
# Connect to InfluxDB
influx

# Create database
CREATE DATABASE smokerpi_temps
CREATE USER your_username WITH PASSWORD 'your_password'
GRANT ALL ON smokerpi_temps TO your_username
```

### Installation

```bash
# Clone repository
git clone https://github.com/danielsbonnin/smokerpi.git
cd smokerpi

# Install Python dependencies
pip3 install -r requirements.txt
# (or manually: pip3 install influxdb RPi.GPIO)

# Configure credentials
cp creds.py.template creds.py
nano creds.py  # Fill in your InfluxDB credentials and sensor serial numbers

# Install as package
python3 setup.py install
```

### Running the Temperature Logger

Option 1: **Direct execution** (for testing)
```bash
python3 thermometers/influxlogger.py
```

Option 2: **systemd service** (recommended for production)
```bash
# Copy service file
sudo cp influxlogger.service /lib/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable influxlogger
sudo systemctl start influxlogger

# Check status
sudo systemctl status influxlogger
```

---

## 🎮 Usage

### Basic Operation

```bash
# Set target temperature to 225°F with default PID parameters
python3 smokerpi.py 225

# Adjust PID tuning for your specific setup
python3 smokerpi.py 225 --prop 1.2 --integral 0.1 --deriv 0.05

# Account for cold weather
python3 smokerpi.py 225 --outside_temp 40
```

### PID Tuning Guide

The PID controller has three parameters you can adjust:

- **P (Proportional)** - How aggressively to react to current error
  - Higher = more aggressive, faster response, potential overshoot
  - Start with: `1.0`

- **I (Integral)** - How much to account for accumulated error over time
  - Eliminates steady-state error
  - Too high = oscillation and instability
  - Start with: `0.0` (tune P first)

- **D (Derivative)** - How much to react to rate of change
  - Dampens oscillation, smooths response
  - Often not needed for smoker (slow thermal system)
  - Start with: `0.0`

**Tuning Process:**
1. Start with P=1.0, I=0, D=0
2. Run a test cook, watch for oscillation or sluggish response
3. If too slow: increase P
4. If oscillating: decrease P
5. If steady-state error remains: add small I (0.05-0.1)
6. Save your working parameters for future cooks

### Monitoring

```bash
# Check logs
tail -f smokerpi/logs/pid.log
tail -f smokerpi/logs/thermometers.log

# Query temperature data from InfluxDB
influx -database smokerpi_temps -execute 'SELECT * FROM autosmoker_temps ORDER BY time DESC LIMIT 10'
```

---

## 📊 Understanding the Output

During operation, you'll see output like:
```
***temp 223.5 duty_prop 0.52
```

This means:
- Current temperature: 223.5°F
- Heater duty cycle: 52% (on for 31s, off for 29s per 60s cycle)

The system adapts the maximum duty cycle based on ambient conditions. On a cold day, it might allow up to 90% duty. On a warm day, maybe only 60% max.

---

## 🐛 Troubleshooting

**Temperature not reading**
- Check sensor wiring
- Verify 1-wire device shows up: `ls /sys/bus/w1/devices/`
- For K-type: ensure SPI is enabled in raspi-config

**Heater not switching**
- Test GPIO: `python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.OUT); GPIO.output(17, GPIO.HIGH)"`
- Check SSR LED indicator
- Verify power to heating element

**Temperature oscillating**
- Reduce P parameter
- Increase duty cycle duration for slower response

**Database connection errors**
- Check InfluxDB is running: `sudo systemctl status influxdb`
- Verify credentials in `creds.py`
- Test connection: `influx -username your_user -password your_pass -database smokerpi_temps`

---

## 🔬 Technical Details

### PID Algorithm

Classic textbook PID implementation:

```
u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de/dt

where:
  u(t) = control output (heat level)
  e(t) = error (setpoint - measured temperature)
  Kp, Ki, Kd = tunable gains
```

### Duty Cycle Management

Smart features:
- **Adaptive maximum** - Adjusts based on ambient temp vs target
- **Sigmoid transformation** - Smooth PID output → duty cycle mapping
- **Windup protection** - Prevents integral term from accumulating excessively
- **Outlier filtering** - Ignores wild PID swings during transients

---

## 📝 Configuration Files

### creds.py

```python
# Copy from creds.py.template and customize
INFLUX_DB = "smokerpi_temps"
INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
INFLUX_USER = "your_username"
INFLUX_PASS = "your_password"
ONE_WIRE_THERM_SERIAL = "28-xxxxxxxxxxxx"
```

### smokerpi/settings.py

Key settings:
- `PID_CONTROL_THERM` - Which sensor to use for PID feedback
- `INFLUX_SESSION` - Database measurement name
- Logging configuration

---

## 🎓 Learning Resources

Want to understand the magic behind this?

**PID Control:**
- [Wikipedia: PID Controller](https://en.wikipedia.org/wiki/PID_controller)
- [Control Theory Basics](https://www.ni.com/en-us/innovations/white-papers/06/pid-theory-explained.html)

**Raspberry Pi GPIO:**
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [GPIO Pin Layout](https://pinout.xyz/)

**Time-Series Databases:**
- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/)

---

## 🤝 Contributing

Found a bug? Have an improvement? PRs welcome!

This is a hobby project born from the desire to cook better BBQ. Feel free to fork, modify, and adapt for your own setup.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IvPID** - PID controller implementation by Caner Durmusoglu
- The BBQ and maker communities for inspiration
- My family for taste-testing all the experimental cooks

---

## 🚀 Future Ideas

- [ ] Web dashboard for remote monitoring
- [ ] Mobile app integration
- [ ] Multi-zone temperature control
- [ ] Smoke density monitoring
- [ ] Recipe profiles and automatic temp schedules
- [ ] Cloud data logging and analytics

---

<div align="center">

**Built with ❤️ and a craving for perfectly smoked brisket**

*Have questions? Open an issue or reach out!*

</div>
