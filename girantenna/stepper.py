import OPi.GPIO as GPIO
import time


class Stepper():
    """
    Interface to a stepper motor
    using a driver with 4 pins
    """
    def __init__(self, pins):
        """
        Set the  four pins used to control the
        stepper motor
        """

        GPIO.setmode(GPIO.BOARD)
        self.inp = pins
        for i in self.inp:
            GPIO.setup(i, GPIO.OUT)
        GPIO.output(self.inp, GPIO.LOW)
        self.numstep = 0
        self.half = [
            [
                GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH
            ],  # phase 0
            [
                GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW
            ],  # phase 1
            [
                GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW
            ],  # phase 2
            [
                GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW
            ],  # phase 3
            [
                GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW
            ],  # phase 4
            [
                GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW
            ],  # phase 5
            [
                GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH
            ],  # phase 6
            [
                GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH
            ],  # phase 7
        ]
        self.acc = 1000  # steps
        self.dec = self.acc  # steps
        self.actspeed = 0

    def stop(self):
        """
        Stop the movement
        """
        GPIO.output(self.inp[0], GPIO.LOW)
        GPIO.output(self.inp[2], GPIO.LOW)
        GPIO.output(self.inp[3], GPIO.LOW)
        GPIO.output(self.inp[1], GPIO.LOW)

    def move(self, speed, rel=1, direction=1):
        """
        speed :: int, steps per second (Hz)
        rel :: int
        direction :: int
        """
        if direction >= 0:
                d = 1
        else:
                d = -1
        refspeed = speed

        self.actspeed = 1
        dec = self.dec

        if rel <= self.dec:
            dec = rel/2

        for s in range(0, rel):
            self.numstep += d
            if s == rel - dec:
                refspeed = 0
            t = 1.0/self.actspeed
            actacc = speed/self.acc
            print(self.numstep, 1.0/self.actspeed)
            fase = self.numstep % 8
            for k in range(0, 4):
                # print k, self.inp[k],self.half[fase][k]
                GPIO.output(self.inp, self.half[fase])
            if self.actspeed < refspeed:
                    print("+ 100")
                    self.actspeed = self.actspeed + actacc
                    if self.actspeed > speed:
                        self.actspeed = speed

            elif self.actspeed > refspeed:
                    print("- 100")
                    self.actspeed = self.actspeed - actacc
                    if self.actspeed < 0:
                        self.actspeed = 0
                        return
            time.sleep(t)
