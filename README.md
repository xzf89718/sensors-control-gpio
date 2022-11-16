# sensors-control-gpio
This is a repository desgined for the arduino 37 sensors bundle for raspberry pi 4. This package implemented in raspberry pi 4B GPIO with RPi.GPIO.
# Get started
```bash
pip install sensors-control-gpio-xzf8971
```
# AHT20
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
Only support backen adafruit now, the error rate of DHT11 is quite high. DHT11 is only recommendded as pedagogical one in 2022
## How to
```bash
python -m DHT11_sensor_control -p pin -b adafruit 
```
# serial_monitor
This is a very simple scripts developed for arduino serial monitoring (like serial monitor in Arduino IDE, but this one will save data into file)
## How to
```bash
# I suppose your serial port want to monitor is ttyACM0
sudo chmod 666 /dev/ttyACM0
# port is /dev/ttyACM0 bautrate is 9600 (this is default for arduino UNO) timeout is 1s
python -m serial_monitor -p /dev/ttyACM0 -b 9600 -t 1
