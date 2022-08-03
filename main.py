import time
from datetime import datetime
import atexit
from motor import Motor

# motor ports
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26

# Tune the following value if the clock gains or loses.
# Theoretically, standard of this value is 60000.
MILLIS_PER_MIN = 60000 # milliseconds per a minute

# Motor and clock parameters
STEP = 32 # steps of a single rotation of motor
REDUCTION = 64 / 4 # reduction ratio in the motor
RATIO = 15 # minutes per a rotation


motor = Motor(IN1, IN2, IN3, IN4)

TWELVE_HR_MS = 12 * 60 * 60000
MAX_POS = round(STEP * REDUCTION * TWELVE_HR_MS * 2 / MILLIS_PER_MIN / RATIO)

def ms():
    now = datetime.now()
    print(now.hour)
    return ((now.hour * 60 + now.minute) * 60 + now.second) * 1000 + now.microsecond / 1000

def setup():
    millisec = ms()
    mstostep = millisec

    if mstostep >= TWELVE_HR_MS: # don't step another 12 hours when it's not necessary
        mstostep -= TWELVE_HR_MS

    motor.forward(round(STEP * REDUCTION * mstostep / MILLIS_PER_MIN / RATIO))

    return round(STEP * REDUCTION * millisec / MILLIS_PER_MIN / RATIO)

def loop():
    current_step = setup()

    while True:
        millisec = ms()
        pos = round(STEP * REDUCTION * millisec / MILLIS_PER_MIN / RATIO)
        if pos < current_step and millisec >= 3600000: # if time went back and its 1AM or later (daylight savings)
            motor.backward(current_step - pos)
        elif pos < current_step: # if time went back then its a new day
            motor.forward(MAX_POS - current_step + pos) # move forward remainder of previous day + amount into new day
        else: # regular
            motor.forward(pos - current_step)
        current_step = pos

        time.sleep(20) # wait so motor doesn't run hot

@atexit.register
def cleanup():
    motor.cleanup()

loop()