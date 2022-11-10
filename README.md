# sensors-control-gpio
This is a repository desgined for the arduino 37 sensors bundle for raspberry pi 4. This package implemented in raspberry pi 4B GPIO with RPi.GPIO.
# Get started
```bash
pip install sensors-control-gpio-xzf8971
```
# AHT20
AHT20 CRC8/MAXIM is still work in proress.
## How to
For help infromation
```bash
python -m AHT20_sensor_control --help
```
```bash
# Open I2C bus1. Save data into example.log. Measure data every 60s. 
python -m AHT20_sensor_control -n 1 -o example.log -t 60 
# Enable CRC8 check. Only save data when crc check is OK
python -m AHT20_sensor_control -n 1 -o example.log -t 60 -c
```
# DHT11
## How to
```bash
python -m DHT11_sensor_control -p pin -b adafruit 
```