from AHT20_sensor_control.AHT20_sensor_wrapper import AHT20_wrapper, triggerAndMeasure, AHT20Status
import time

my_wrapper = AHT20_wrapper.InitWithBus(1)
init_status = my_wrapper.InitSensor()
if (init_status == AHT20Status.AHT20_SUCCESSINIT):
    while True:
        temperature, humidity = triggerAndMeasure(my_wrapper)
        print("{0:.2f} C {1:.2f} %RH".format(temperature, humidity * 100))
        time.sleep(1)
else:
    print("Fail init AHT20")
