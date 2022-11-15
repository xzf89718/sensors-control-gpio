import time
import logging

from AHT20_sensor_control.helper_function import get_bit_from_int, calculate_humidity, calculate_temperature
from AHT20_sensor_control.I2C_wrapper import I2CWrapeprsmbus2
from AHT20_sensor_control.crc8_helper import AHT20_crc8_check
# All parameters for AHT20 is ave in this module
from AHT20_sensor_control.AHT20_sensor_parameters import *
from custom_logger import CustomLoggerWrapper, FMT_WITH_MODULENAME

logger_wrapper = CustomLoggerWrapper(
    "AHT20_DEBUG", logger_level=logging.INFO, log_filename="test_AHT20.log", logger_fmt=FMT_WITH_MODULENAME)
logger_wrapper.InitLogger()
AHT20_logger = logger_wrapper.GetInitedLogger()

def checkisBusyAndRetry(AHT20_sensor):
    isBusy, isCali = AHT20_sensor.CheckStatus()
    if (isBusy is AHT20Status.AHT20_BUSY):
        AHT20_logger.debug(
            "AHT20 is busy now. Wait 75 ms and retry.")
        time.sleep(AHT20_MEASURE_DELAY)
        isBusy, isCali = AHT20_sensor.CheckStatus()
        if (isBusy is AHT20Status.AHT20_BUSY):
            AHT20_logger.error("AHT20 is still busy after wait anotehr 75 ms.")
            raise RuntimeError("AHT20 is still busy after wait anotehr 75 ms.")
    return isBusy


def checkisCaliAndRety(AHT20_sensor):
    isBusy, isCali = AHT20_sensor.CheckStatus()
    if (isCali is AHT20Status.AHT20_NOTCALI):
        AHT20_logger.warning(
            "AHT20 is not cali. Wait 40 ms and InitSensor().")
        time.sleep(AHT20_TURNON_DELAY)
        # Try to InitSensor
        AHT20_sensor.InitSensor()
        isBusy, isCali = AHT20_sensor.CheckStatus()
        if (isCali is AHT20Status.AHT20_NOTCALI):
            AHT20_logger.error("Fail to cali AHT20 after InitSensor().")
            raise RuntimeError("Fail to cali AHT20 even InitSensor().")
    return isCali


def triggerAndMeasure(AHT20_sensor):
    """
    Send trigger signal to 
    """
    if not isinstance(AHT20_sensor, AHT20_wrapper):
        AHT20_logger.error("Should be a AHT20_wrapper")
        raise NotImplementedError("Should be a AHT20_wrapper")
    # Check status first
    checkisCaliAndRety(AHT20_sensor=AHT20_sensor)
    # Check AHT20 isBusy
    checkisBusyAndRetry(AHT20_sensor=AHT20_sensor)
    # Trigger a measurement now!
    AHT20_sensor.TriggerCmd()
    # Readcmd is required
    AHT20_sensor.ReadCmd()
    # Get status and checkStatus
    checkisBusyAndRetry(AHT20_sensor=AHT20_sensor)
    # If all status check is passed, read data and decode data
    AHT20_sensor.ReadStatusAndData()
    AHT20_logger.debug(AHT20_sensor.all_data)
    temp, humi = AHT20_sensor.DecodeData()
    AHT20_logger.debug("{0}\t{1}".format(temp, humi))
    # Data after decoded is store in self.temperature_value and self.humidity_value
    return AHT20_sensor.temperature_value, AHT20_sensor.humidity_value


def triggerAndMeasureAndCRCcheck(AHT20_sensor):
    if not isinstance(AHT20_sensor, AHT20_wrapper):
        AHT20_logger.error("Should be a AHT20_wrapper")
        raise NotImplementedError("Should be a AHT20_wrapper")
    temperature, humidity = triggerAndMeasure(AHT20_sensor)
    CRCStatus = AHT20_sensor.CheckCRC()
    if (CRCStatus == AHT20Status.AHT20_CRCNOTOK):
        AHT20_logger.warning("CRC8 check fail")
    return temperature, humidity, CRCStatus


class AHT20_wrapper(I2CWrapeprsmbus2):

    def __init__(self, I2C_bus):
        super().__init__(I2C_bus)
        self.all_data = None
        self.status = None
        self.humidity_value = None
        self.temperature_value = None

    def InitializeCmd(self):

        AHT20_logger.info("Send initialize cmd to AHT20")
        self._write_i2c_block_data(AHT20_ADDRESS, 0, CMD_INITIALIZE)
        time.sleep(AHT20_NORMAL_DELAY)

    def SoftResetCmd(self):
        """
        Reset ATH20 status without turn off and on the sensor.
        """

        AHT20_logger.info("Send softreset cmd to AHT20")
        self._write_i2c_block_data(AHT20_ADDRESS, 0, CMD_SOFTRESET)
        time.sleep(AHT20_SOFTRESET_DELAY)
        isBusy, isCali = self.CheckStatus()
        AHT20_logger.info("Softreset already. {0}\t{1}".format(
            str(isBusy), str(isCali)))

    def ReadCmd(self):

        AHT20_logger.info("Send read cmd to AHT20")
        self._write_i2c_block_data(AHT20_ADDRESS, 0, CMD_READ)
        time.sleep(AHT20_NORMAL_DELAY)

    def TriggerCmd(self):
        """
        Trigger a measurement.
        """
        AHT20_logger.info("Send trigger cmd to AHT20")
        self._write_i2c_block_data(AHT20_ADDRESS, 0, CMD_TRIGGER)
        time.sleep(AHT20_MEASURE_DELAY)

    def InitSensor(self):
        """
        Only check status when init sensor!
        """
        # Wait 40 ms when turn on.
        time.sleep(AHT20_TURNON_DELAY)
        # Check is Cali first
        self.ReadCmd()
        isBusy, isCali = self.CheckStatus()
        if (isBusy == AHT20Status.AHT20_BUSY):
            AHT20_logger.warning("AHT20 is busy, wait 75 ms and retry.")
            time.sleep(AHT20_MEASURE_DELAY)
            isBusy, isCali = self.CheckStatus()
            if (isBusy == AHT20Status.AHT20_BUSY):
                AHT20_logger.error("AHT20 is busy. Fail init")
                return AHT20Status.AHT20_FAILINIT

        # Check Cali status. If NOTCALI, send init cmd.
        if (isCali == AHT20Status.AHT20_NOTCALI):
            self.InitializeCmd()
            isBusy, isCali = self.CheckStatus()
            if (isCali == AHT20Status.AHT20_NOTCALI):
                AHT20_logger.error("Fail to Cali AHT20.")
                return AHT20Status.AHT20_FAILINIT
        AHT20_logger.info("InitSensor() success.")
        return AHT20Status.AHT20_SUCCESSINIT

    def CheckStatus(self):
        """
        Read all data after
        """
        status_value = self.ReadStatus()[0]
        AHT20_logger.debug("{0}\t{1}".format(status_value, bin(status_value)))
        status_checker = ATH20_status_bit_checker(status_value)
        AHT20_logger.debug(status_checker.checkBusy())
        AHT20_logger.debug(status_checker.CheckCali())

        return [status_checker.checkBusy(), status_checker.CheckCali()]

    def ReadStatusAndData(self):
        """
        Read all 7 bytes data in to self.all_data
        """
        self.all_data = self._read_i2c_block_data(
            AHT20_ADDRESS, 0, AHT20_NDATA)
        time.sleep(AHT20_NORMAL_DELAY)
        return self.all_data

    def ReadStatus(self):
        """
        Read status only
        """
        self.status = self._read_i2c_block_data(
            AHT20_ADDRESS, 0, AHT20_NSTATUS)
        time.sleep(AHT20_NORMAL_DELAY)
        return self.status

    def DecodeData(self):
        """
        Decode data and calculate them into human readable(C and realative humidity).
        return: self.temperature_value, self.humidity_value
        """
        _humidity_before_decode = (
            self.all_data[1] << 8 | self.all_data[2]) << 4 | (self.all_data[3] >> 4)
        _temperature_before_decode = (
            (self.all_data[3] & 0x0F) << 8 | self.all_data[4]) << 8 | self.all_data[5]
        self.humidity_value = calculate_humidity(_humidity_before_decode)
        self.temperature_value = calculate_temperature(
            _temperature_before_decode)
        return self.temperature_value, self.humidity_value

    def CheckCRC(self):
        """
        CheckCRC. In CRC8/MAXIM. Ref: http://www.aosong.com/products-61.html.
        """
        # Get all 6 bytes data and 1 bytes CRC code
        frame_for_CRC8_check = 0x00
        # for i in range(0, 7):
        #     frame_for_CRC8_check << 8 | self.all_data[i]
        isCRCOK = AHT20_crc8_check(self.all_data)
        if (isCRCOK):
            return AHT20Status.AHT20_CRCOK
        else:
            return AHT20Status.AHT20_CRCNOTOK
