# Implement manually in GPIO
import RPi.GPIO as GPIO
# Implement in adafruit_dht class
import adafruit_dht
from DHT11_sensor_control.helper_function import *


class DHT11_wrapper():

    def __init__(self):
        pass
    
    def ReadAndRetry(self, n_retry):
        pass

class DHT11_wrapper_adafruit_dht(DHT11_wrapper):

    def __init__(self):
        super().__init__()
    
    def ReadAndRetry(self, n_retry):
        pass

class DHT11_wrapper_xzf8971(DHT11_wrapper):
    
    def __init__(self):
        super().__init__()
    
    def ReadAndRetry(self, n_retry):
        pass