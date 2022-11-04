from DHT11_sensor_control.DHT11_wrapper import DHT11_wrapper_adafruit_dht
from DHT11_sensor_control.helper_function import getPin
import argparse
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Serial monitoring backen by pyserial. Author: Zifeng XU, email: zifeng.xu@cern.ch.")
    parser.add_argument(
        "-p", "--pin", help="Pin for adafruit board", required=True)
    parser.add_argument("-b", "--backen",
                        help="adafruit or zifeng", required=True, choices=["adafruit", "zifeng"])
    parser.add_argument("-r", "--retry_max",
                        default=100)

    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    PIN = args.pin
    BACKEN = args.backen
    RETRY_MAX = int(args.retry_max)

    if (BACKEN == "adafruit"):
        sensor_wrapper = DHT11_wrapper_adafruit_dht()
        sensor_wrapper.InitSensor(getPin(PIN))
        temperature, humidity = sensor_wrapper.ReadAndRetry(RETRY_MAX)
        print("temperature is {0}, humidity is {1}".format(
            temperature, humidity))
        sensor_wrapper.CloseDevice()
