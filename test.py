import time
from datetime import datetime
import atexit
from motor import Motor

# Tune the following value if the clock gains or loses.
# Theoretically, standard of this value is 60000.
MILLIS_PER_MIN = 60000 # milliseconds per a minute

# Motor and clock parameters
STEP = 32 # steps of a single rotation of motor
REDUCTION = 64 / 4 # reduction ratio in the motor
RATIO = 15 # minutes per a rotation

IN1 = 26
IN2 = 19
IN3 = 13
IN4 = 6

motor = Motor(IN1, IN2, IN3, IN4)


def ms():
    return 30 * 60 * 1000

def test():
    current_step = 0
    current_sec = 0
    pos = 0
    sec = ms() / 1000
    if sec != current_sec:
        current_sec = sec
        pos = round(STEP * REDUCTION * ms() / MILLIS_PER_MIN / RATIO)
        if pos < current_step: # ms() laps around
            current_step = pos
        motor.forward(pos - current_step)
        current_step = pos

    motor.cleanup()

test()