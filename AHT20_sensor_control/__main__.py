import argparse
import time
import logging

from custom_logger import CustomLoggerWrapper, FMT_NO_MODULENAME

from AHT20_sensor_control.AHT20_sensor_parameters import AHT20Status
from AHT20_sensor_control.AHT20_sensor_wrapper import AHT20_wrapper, triggerAndMeasure, triggerAndMeasureAndCRCcheck

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AHT20 sensor console. Author: Zifeng XU, email: zifeng.xu@cern.ch.")
    parser.add_argument(
        "-n", "--number-bus", help="I2C bus number for smbus2", default=1)
    parser.add_argument("-o", "--outfile-name",
                        default="AHT20_sensor_data.log")
    parser.add_argument("-t", "--measure-interval", default=60)
    parser.add_argument("-c", "--crc8-maxim-enable", action="store_true")

    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    NUMBER_BUS = int(args.number_bus)
    OUTFILE_NAME = args.outfile_name
    MEASURE_INTERVAL = float(args.measure_interval)
    CRC8_MAXIM_ENABLE = args.crc8_maxim_enable

    logger_wrapper = CustomLoggerWrapper(
        "ATH20_sensor_control_console", logger_level=logging.INFO, logger_fmt=FMT_NO_MODULENAME, log_filename=OUTFILE_NAME)
    logger_wrapper.InitLogger()
    mylogger = logger_wrapper.GetInitedLogger()

    my_wrapper = AHT20_wrapper.InitWithBus(NUMBER_BUS)
    init_status = my_wrapper.InitSensor()
    if (init_status == AHT20Status.AHT20_SUCCESSINIT):
        try:
            while True:
                if (not CRC8_MAXIM_ENABLE):
                    temperature, humidity = triggerAndMeasure(my_wrapper)
                    mylogger.info("{0:.2f} C\t{1:.2f} %RH".format(temperature, humidity * 100))
                else:
                    CRC8_check = AHT20Status.AHT20_CRCNOTOK
                    while (CRC8_check == AHT20Status.AHT20_CRCNOTOK):
                        temerature, humidity, CRC8_check = triggerAndMeasureAndCRCcheck(my_wrapper)
                    mylogger.info("{0:.2f} C\t{1:.2f} %RH".format(temperature, humidity * 100))
                time.sleep(MEASURE_INTERVAL)
        except KeyboardInterrupt:
            mylogger.warning("Stop by keyboard.")

    else:
        print("Fail init AHT20.")
        mylogger.error("Fail init AHT20.")
