from enum import Enum, unique
from AHT20_sensor_control.helper_function import get_bit_from_int

# Command for AHT20 sensor
CMD_INITIALIZE = [0xBE, 0x08, 0x00]
CMD_TRIGGER = [0xAC, 0x33, 0x00]
CMD_SOFTRESET = [0xBA]
CMD_READ = [0x71]

# Parameter of AHT20
AHT20_ADDRESS = 0x38
AHT20_NDATA = 7
AHT20_NSTATUS = 1
AHT20_TURNON_DELAY = 40 * 10 ** -3
AHT20_SOFTRESET_DELAY = 20 * 10 ** -3
AHT20_MEASURE_DELAY = 100 * 10 ** -3
AHT20_NORMAL_DELAY = 50 * 10 ** -3
AHT20_TIMEOUT = 1
# Status bits checker


@unique
class AHT20Status(Enum):

    AHT20_CALI = 0
    AHT20_NOTCALI = 1
    AHT20_MODE_NOR = 2
    AHT20_MODE_CYC = 3
    AHT20_MODE_CMD = 4
    AHT20_BUSY = 5
    AHT20_FREE = 6
    AHT20_CRCOK = 7
    AHT20_CRCNOTOK = 8
    AHT20_SUCCESSINIT = 9
    AHT20_FAILINIT = 10


class ATH20_status_bit_checker():
    def __init__(self, int_status_bit):
        self.int_status_bit = int_status_bit

    def checkBusy(self):
        bit_busy = get_bit_from_int(self.int_status_bit, 7)
        if bit_busy == 1:
            return AHT20Status.AHT20_BUSY
        elif bit_busy == 0:
            return AHT20Status.AHT20_FREE

    def CheckCali(self):
        bit_cali = get_bit_from_int(self.int_status_bit, 3)
        if bit_cali == 1:
            return AHT20Status.AHT20_CALI
        elif bit_cali == 0:
            return AHT20Status.AHT20_NOTCALI

    def checkMode(self):
        bit_busy_6 = get_bit_from_int(self.int_status_bit, 6)
        bit_busy_5 = get_bit_from_int(self.int_status_bit, 5)
        if bit_busy_6 == 1:
            return AHT20Status.AHT20_MODE_CMD
        if bit_busy_6 == 0 and bit_busy_5 == 1:
            return AHT20Status.AHT20_MODE_CYC
        else:
            return AHT20Status.AHT20_MODE_NOR
