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
MILLIS_PER_MIN = 60000.0 # milliseconds per a minute

# Motor and clock parameters
STEP = 32.0 # steps of a single rotation of motor
GEAR_RATIO = 64.0 # 32.0 / 9.0 * 22.0 / 11.0 * 26.0 / 9.0 * 31.0 / 10.0
REDUCTION = GEAR_RATIO / 4.0 # reduction ratio in the motor
RATIO = 15.0 # minutes per a rotation


motor = Motor(IN1, IN2, IN3, IN4)

TWELVE_HR_MS = 12 * 60 * 60000
MAX_POS = int(STEP * REDUCTION * TWELVE_HR_MS * 2 / MILLIS_PER_MIN / RATIO)

SECONDS_PER_STEP = MILLIS_PER_MIN * RATIO / STEP / REDUCTION / 1000.0

def ms():
    now = datetime.now()
    return ((now.hour * 60 + now.minute) * 60 + now.second) * 1000 + now.microsecond / 1000

def setup():
    millisec = ms()
    mstostep = millisec

    if mstostep >= TWELVE_HR_MS: # don't step another 12 hours when it's not necessary
        mstostep -= TWELVE_HR_MS

    motor.forward(int(STEP * REDUCTION * mstostep / MILLIS_PER_MIN / RATIO))

    return int(STEP * REDUCTION * millisec / MILLIS_PER_MIN / RATIO)

def loop():
    print(datetime.now().minute)
    current_step = setup()
    while True:
        motor.microstep(SECONDS_PER_STEP);
        current_step += 1

        millisec = ms()
        pos = int(STEP * REDUCTION * millisec / MILLIS_PER_MIN / RATIO)
        if pos < current_step and millisec >= 3600000: # if time went back and its 1AM or later (daylight savings)
            motor.backward(current_step - pos)
            print('dst backward adjust')
        elif pos < current_step: # if time went back then its now AM/PM
            current_step -= MAX_POS 
            print('am/pm reset step count')
        elif current_step < pos: # if behind (due to set up or daylight savings) go forward
            motor.forward(pos - current_step)
            current_step = pos
            print('forward adjust')
        # current_step = pos

@atexit.register
def cleanup():
    motor.cleanup()

loop()