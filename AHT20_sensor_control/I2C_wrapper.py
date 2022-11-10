from smbus2 import SMBus
import logging
AHT20_helper_logger = logging.getLogger("AHT20_sensor_control_helper")

class I2CWrapper():
    def __init__(self, I2C_bus_id):
        self.I2C_bus_id = I2C_bus_id

    @classmethod
    def InitWithBus(cls):
        """
        A interface to init wrapper with specified bus package
        """
        pass

    # Implement read block data from i2c here
    def _read_i2c_block_data(self, i2c_addr, register=0x0, length=1):
        pass

    # Implement wirte block data to i2c here
    def _write_i2c_block_data(self, i2c_addr, register=0x0, data=[]):
        pass


class I2CWrapeprsmbus2(I2CWrapper):

    def __init__(self, I2C_bus_id):
        super().__init__(I2C_bus_id=I2C_bus_id)

    @classmethod
    def InitWithBus(cls, bus_number):
        # try to open I2C bus?
        with SMBus(bus_number):
            AHT20_helper_logger.info(
                "Successfully open I2C bus with SMBus in {0}".format(bus_number))
        wrapper = cls(bus_number)
        return wrapper

    def _write_i2c_block_data(self, i2c_addr, register=0, data=[]):
        with SMBus(self.I2C_bus_id) as bus:
            bus.write_i2c_block_data(
                i2c_addr=i2c_addr, register=register, data=data)

    def _read_i2c_block_data(self, i2c_addr, register=0, length=1):
        with SMBus(self.I2C_bus_id) as bus:
            i2c_read_values = bus.read_i2c_block_data(
                i2c_addr=i2c_addr, register=register, length=length)
        return i2c_read_values
