try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as error:
    pass
import board
import numpy as np
values_from_DH11 = np.zeros((40,), dtype=int)


def readDH11Once():
    pass


def checkError():
    pass

def getPin(pin_in_str):

    pin_in_board = eval("board.{0}".format(pin_in_str))
    return pin_in_board