# Implement manually in GPIO
import RPi.GPIO as GPIO
# Implement in adafruit_dht class
import adafruit_dht
from DHT11_sensor_control.helper_function import readDH11Once, checkError
import time


class DHT11_wrapper():

    def __init__(self):
        pass
    
    def ReadAndRetry(self, pin):
        pass

    def CloseDevice(self):
        pass

class DHT11_wrapper_adafruit_dht(DHT11_wrapper):

    def __init__(self):
        super().__init__()
        self.sensor = None

    def InitSensor(self, pin):
        self.sensor = adafruit_dht.DHT11(pin, use_pulseio=False)

    def ReadAndRetry(self, max_retry):
        i = 0
        while i < max_retry:
            is_Error = False
            temperature, humidity = [None, None]
            try:
                temperature, humidity =[self.sensor.temperature, self.sensor.humidity]
                time.sleep(1)
            except RuntimeError as error:
                print(error)
                is_Error = True
            if (is_Error == False and temperature != None and humidity != None):
                break
            i = i + 1
        return temperature, humidity
    
    def CloseSensor(self):
        self.sensor.exit()
        

class DHT11_wrapper_xzf8971(DHT11_wrapper):
    
    def __init__(self):
        super().__init__()
    
    def ReadAndRetry(self, n_retry):
        pass