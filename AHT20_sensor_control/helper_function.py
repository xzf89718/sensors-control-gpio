import numpy as np
from smbus2 import SMBus
import logging
from custom_logger import CustomLoggerWrapper, FMT_WITH_MODULENAME

logger_wrapper = CustomLoggerWrapper(
    "AHT20_sensor_control_helper", logger_level=logging.INFO, log_filename="AHT20_helper.log", logger_fmt=FMT_WITH_MODULENAME)
logger_wrapper.InitLogger()
AHT20_helper_logger = logger_wrapper.GetInitedLogger()
def get_bit_from_int(int_value, bit_index):
    """
    For examle: 5 -> 0b101
    get_specified_bit_from(5, 0) = 1
    get_specified_bit_from(5, 1) = 0
    get_specified_bit_from(5, 2) = 1
    """
    return int_value >> bit_index & 1

# def get_bit_from_I2C_message(int_value, I2C_bit_index):

#     return get_bit_from_int(int_value, 7 - I2C_bit_index)


def calculate_temperature(value):
    value = float(value)
    return (value / 2 ** 20) * 200 - 50


def calculate_humidity(value):
    value = float(value)
    return (value / 2 ** 20)


