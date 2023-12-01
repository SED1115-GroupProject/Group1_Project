'''Example usage
pin = Pin(2, Pin.OUT)
pin.value(1)  # Set pin high

pwm = PWM(pin)
pwm.freq(1000)
pwm.duty(512)

adc = ADC(Pin(34))
adc_value = adc.read()'''


class Pin:
    OUT = 0
    IN = 1

    def __init__(self, pin, mode=OUT):
        self.pin = pin
        self.mode = mode
        self.state = None

    def value(self, val=None):
        if val is not None:
            self.state = val
            print(f"Set pin {self.pin} to {val}")
        return self.state

class PWM:
    def __init__(self, pin):
        self.pin = pin
        self.duty_cycle = 0
        print(f"Initialized PWM on pin {self.pin}")

    def freq(self, frequency):
        print(f"Set frequency to {frequency}Hz")

    def duty(self, duty_cycle):
        self.duty_cycle = duty_cycle
        print(f"Set duty cycle to {duty_cycle}")

class ADC:
    def __init__(self, pin):
        self.pin = pin
        print(f"Initialized ADC on pin {self.pin}")

    def read(self):
        # Simulate ADC read
        simulated_value = 512  # Example value
        print(f"Read value {simulated_value} from ADC pin {self.pin}")
        return simulated_value


