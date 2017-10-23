import OPi.GPIO as GPIO
import time


class Stepper():
    """
    Interface to a stepper motor
    using a driver with 4 pins for 4 coils
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

        """
        Signals for the 4 coils in the stepper motor.
        TODO: Clockwise is forward?

            # move forward
            for i in self.half:
                GPIO.output(self.inp, i)

            # move forward
            for i in reversed(self.half):
                GPIO.output(self.inp, i)
        """
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

        """
        Accelerate to full speed in 1000 steps
        """
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

    def move(self, speed=300, steps=1, direction=1):
        """
        speed :: int, steps per second (Hz)
        steps :: int, steps to move
        direction :: int 
        """
        if direction >= 0:
            d = 1
        else:
            d = -1
        refspeed = speed

        self.actspeed = 1
        dec = self.dec

        if steps <= self.dec:
            dec = steps/2

        """
        Every step of the movement this happens
        """
        for s in range(0, steps):
            # incerement position
            self.numstep += d
            # we are there
            if s == steps - dec:
                refspeed = 0
            # next step is in
            t = 1.0/self.actspeed
            actacc = speed/self.acc
            print(self.numstep, t)
            fase = self.numstep % 8
            GPIO.output(self.inp, self.half[fase])
            if self.actspeed < refspeed:
                self.actspeed = min(self.actspeed + actacc, speed)

            elif self.actspeed > refspeed:
                self.actspeed = max(self.actspeed - actacc, 0)
                if not self.actspeed:
                    return
            time.sleep(t)
