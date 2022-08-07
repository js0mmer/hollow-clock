import RPi.GPIO as GPIO
from time import sleep

class Motor:
    in1 = 6
    in2 = 13
    in3 = 19
    in4 = 26
    delay = 0.001

    def __init__(self, in1=6, in2=13, in3=19, in4=26, delay=0.001):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.delay = delay
        self.setupGPIO()

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, False)
        GPIO.output(self.in3, False)
        GPIO.output(self.in4, False)

    def step1(self):
        GPIO.output(self.in4, True)
        sleep(self.delay)
        GPIO.output(self.in4, False)

    def step2(self):
        GPIO.output(self.in4, True)
        GPIO.output(self.in3, True)
        sleep(self.delay)
        GPIO.output(self.in4, False)
        GPIO.output(self.in3, False)

    def step3(self):
        GPIO.output(self.in3, True)
        sleep(self.delay)
        GPIO.output(self.in3, False)

    def step4(self):
        GPIO.output(self.in2, True)
        GPIO.output(self.in3, True)
        sleep(self.delay)
        GPIO.output(self.in2, False)
        GPIO.output(self.in3, False)

    def step5(self):
        GPIO.output(self.in2, True)
        sleep(self.delay)
        GPIO.output(self.in2, False)

    def step6(self):
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, True)
        sleep(self.delay)
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, False)

    def step7(self):
        GPIO.output(self.in1, True)
        sleep(self.delay)
        GPIO.output(self.in1, False)

    def step8(self):
        GPIO.output(self.in4, True)
        GPIO.output(self.in1, True)
        sleep(self.delay)
        GPIO.output(self.in4, False)
        GPIO.output(self.in1, False)
    
    def forward(self, step):
        for i in range(step):   
            self.step1()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            self.step6()
            self.step7()
            self.step8()
    
    def backward(self, step):
        for i in range(step):
            self.step8()
            self.step7()
            self.step6()
            self.step5()
            self.step4()
            self.step3()
            self.step2()
            self.step1()
    
    def microstep(self, seconds):
        GPIO.output(self.in3, True);
        sleep(seconds / 8.0);
        GPIO.output(self.in4, False);
        sleep(seconds / 8.0);
        GPIO.output(self.in2, True);
        sleep(seconds / 8.0);
        GPIO.output(self.in3, False);
        sleep(seconds / 8.0);
        GPIO.output(self.in1, True);
        sleep(seconds / 8.0);
        GPIO.output(self.in2, False);
        sleep(seconds / 8.0);
        GPIO.output(self.in4, True);
        sleep(seconds / 8.0);
        GPIO.output(self.in1, False);
        sleep(seconds / 8.0);
    
    def cleanup(self):
        GPIO.cleanup()
