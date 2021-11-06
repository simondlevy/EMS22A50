#!/usr/bin/env python3
'''
Reads data from EMS22A50 and sends it over a serial port as ASCII

Uses '*' character as delimiter

Copyright (c) 2021 Simon D. Levy

MIT License
'''


import time
import serial
import RPi.GPIO as GPIO
from ems22a50 import EMS22A50


def main():

    # -------------- CLK DAT CS
    encoder = EMS22A50(2, 3, 4)

    encoder.start()

    time.sleep(0.5)

    print('GPIO configuration enabled')

    port = serial.Serial('/dev/ttyAMA0', 115200)

    while True:
        try:
            msg = str(encoder.readpos()) + '*'
            port.write(msg.encode('utf-8'))
            time.sleep(0.001)
        except KeyboardInterrupt:
            break

    GPIO.cleanup()
    port.close()


if __name__ == '__main__':
    main()
