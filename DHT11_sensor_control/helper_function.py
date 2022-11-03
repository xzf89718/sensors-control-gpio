try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as error:
    pass

import numpy as np
values_from_DH11 = np.zeros((40,), dtype=int)


def ReadDH11Once():
    pass


def CheckError():
    pass
