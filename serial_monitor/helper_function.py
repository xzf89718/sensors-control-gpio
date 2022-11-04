import serial
import time
import logging
pyserial_monitoring_logger = logging.getLogger("pyserial_monitoring_logger")
pyserial_monitoring_logger.propagate = False
pyserial_monitoring_logger.setLevel(level=logging.INFO)
logger_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# Add file_handler
file_handler = logging.FileHandler("pyserial_monitoring.log")
file_handler.setFormatter(logger_fmt)
pyserial_monitoring_logger.addHandler(file_handler)
pyserial_monitoring_logger.info(
    "Begin read data from port")
pyserial_monitoring_logger.info(
    "Recording values is stored in pyserial_monitoring.log")


class SerialMonitor():

    def __init__(self, port, baudrate, timeout):
        self.serial = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def InitMonitor(self):
        self.serial = serial.Serial(
            self.port, baudrate=self.baudrate, timeout=self.timeout)

    def CloseMonitor(self):
        self.serial.close()

    def WriteToFile(self):
        while True:
            line = str(self.serial.readline().strip(), encoding="utf-8")
            if (line == ""):
                continue
            else:
                pyserial_monitoring_logger.info(line)
            time.sleep(1)
