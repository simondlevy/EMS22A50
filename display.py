#!/usr/bin/env python3
'''
Reads and displays data from EMS22A50 

Copyright (c) 2021 Simon D. Levy

MIT License
'''

import time
import RPi.GPIO as GPIO
from ems22a50 import EMS22A50


def main():

    # -------------- CLK DAT CS
    encoder = EMS22A50(2, 3, 4)

    encoder.start()

    time.sleep(0.5)

    print('GPIO configuration enabled')

    while True:
        try:
            print(encoder.readpos())
            time.sleep(0.001)
        except KeyboardInterrupt:
            break

    GPIO.cleanup()
    port.close()


if __name__ == '__main__':
    main()
