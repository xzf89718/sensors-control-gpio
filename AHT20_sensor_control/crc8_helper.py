# A total of 6 * 8 bits data need to check
N_DATA = 6
# 1 * 8 bits CRC
N_CRC = 1
# Initial value. Equal to bit negation the first data (status of AHT20)
INIT = 0xFF
# Useful value to help calculate
LAST_8_bit = 0xFF


# Devide number retrieve from CRC-8 MAXIM G(x) = x8 + x5 + x4 + 1
CRC_DEVIDE_NUMBER = 0x131

# Data and CRC taken from AHT20, use this for testing?
TEST_DATA = [[28, 184, 245, 165, 156, 208, 163], [28, 185, 16, 149, 156, 83, 112], [
    28, 184, 249, 85, 156, 114, 213], [28, 185, 9, 53, 156, 54, 45], [28, 185, 70, 117, 156, 189, 33]
, [28, 185, 64, 165, 156, 61, 209]]


def AHT20_crc8_check(all_data_int, init_value=0xFF):
    """
    The input data shoule be:
    Status Humidity0 Humidity1 Humidity2|Temperature0 Temperature1 Temperature2 CRCCode
    In python's int64.
    """
    # Preprocess all the data and CRCCode from AHT20
    DATA_FROM_AHT20 = 0x00
    # Preprocessing the first data (status)
    DATA_FROM_AHT20 = DATA_FROM_AHT20 | all_data_int[0]
    print(bin(DATA_FROM_AHT20))
    DATA_FROM_AHT20 = DATA_FROM_AHT20 ^ init_value
    print(bin(DATA_FROM_AHT20))
    for i_data in range(1, N_DATA + N_CRC):
        DATA_FROM_AHT20 = DATA_FROM_AHT20 << 8 | all_data_int[i_data]
    print(bin(DATA_FROM_AHT20))
    mod_value = DATA_FROM_AHT20 % CRC_DEVIDE_NUMBER
    print(mod_value)
    if (mod_value == 0):
        return True
    else:
        return False


def AHT20_crc8_calculate(all_data_int):
    pass

if __name__ == "__main__":
    for data in TEST_DATA:
        AHT20_crc8_check(data, INIT)