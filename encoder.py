#!/usr/bin/env python3

# https://hareshmiriyala.wordpress.com/2018/02/19/interfacing-an-absolute-encoder-to-raspberry-pi/

import time
import serial
import RPi.GPIO as GPIO


class EMS22A50:

    def __init__(self, clk, dat, cs, delay=0.0000005):

        self.clk = clk
        self.dat = dat
        self.cs = cs

        self.delay = delay

    def start(self):

        GPIO.setmode(GPIO.BCM)

        # pin setup done here
        try:
            GPIO.setup(self.clk, GPIO.OUT)
            GPIO.setup(self.dat, GPIO.IN)
            GPIO.setup(self.cs, GPIO.OUT)
            GPIO.output(self.cs, 1)
            GPIO.output(self.clk, 1)
        except Exception:
            print('ERROR. Unable to setup the configuration requested')

    def clockup(self):
        GPIO.output(self.clk, 1)

    def clockdown(self):
        GPIO.output(self.clk, 0)

    def MSB(self):
        # Most Significant Bit
        self.clockdown()

    def readpos(self):
        GPIO.output(self.cs, 0)
        time.sleep(self.delay*2)
        self.MSB()
        data = 0

        for i in range(0, 16):
            if i < 10:
                self.clockup()
                data <<= 1
                data |= GPIO.input(self.dat)
                self.clockdown()
            else:
                for k in range(0, 6):
                    self.clockup()
                    self.clockdown()
        GPIO.output(self.cs, 1)
        return data


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
            print(msg)
            port.write(msg.encode('utf-8'))
            time.sleep(0.001)
        except KeyboardInterrupt:
            break

    GPIO.cleanup()
    port.close()


if __name__ == '__main__':
    main()
