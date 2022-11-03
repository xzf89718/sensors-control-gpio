import argparse
from serial_monitor.helper_function import SerialMonitor
from serial_monitor.helper_function import pyserial_monitoring_logger
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Serial monitoring backen by pyserial. Author: Zifeng XU, email: zifeng.xu@cern.ch.")
    parser.add_argument("-p", "--port", help="Port for monitoring serial.", required=True)
    parser.add_argument("-b", "--baudrate", help="Baudrate for monitoring serial.", required=True)
    parser.add_argument("-t", "--timeout", help="Timeout for monitoring serial.", required=True)
    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    PORT = args.port
    BAUDRATE = args.baudrate
    TIMEOUT = args.timeout

    my_monitor = SerialMonitor(PORT, int(BAUDRATE), float(TIMEOUT))
    my_monitor.InitMonitor()

    try:
        my_monitor.WriteToFile()
    except KeyboardInterrupt as error:
        my_monitor.CloseMonitor()
        pyserial_monitoring_logger.warn("End monitoring")



