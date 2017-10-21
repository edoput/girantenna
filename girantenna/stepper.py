import wiringpi as w
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

        w.wiringPiSetup()
        self.inp = pins
        for i in self.inp:
            w.pinMode(i, w.OUTPUT)
        for i in self.inp:
            w.digitalWrite(i, 0)
        self.numstep = 0
        self.half = [
            [1, 0, 0, 1],  # setp 0
            [1, 0, 0, 0],  # step 1
            [1, 1, 0, 0],  # step 2
            [0, 1, 0, 0],  # step 3
            [0, 1, 1, 0],  # step 4
            [0, 0, 1, 0],  # step 5
            [0, 0, 1, 1],  # step 6
            [0, 0, 0, 1],  # step 7
        ]
        self.acc = 1000  # steps
        self.dec = self.acc  # steps
        self.actspeed = 0

    def stop(self):
        """
        Stop the movement
        """
        w.digitalWrite(self.inp[0], 0)
        w.digitalWrite(self.inp[2], 0)
        w.digitalWrite(self.inp[3], 0)
        w.digitalWrite(self.inp[1], 0)

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
                #print k, self.inp[k],self.half[fase][k]
                w.digitalWrite(self.inp[k], self.half[fase][k])
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
