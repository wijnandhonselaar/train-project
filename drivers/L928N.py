from drivers.MotorDriver import MotorDriver
import machine
import uasyncio as asyncio

class L928N(MotorDriver):
    def __init__(self, pwm_pin, in1_pin, in2_pin, frequency=500):
        """
        Initialize a three-pin motor driver.
        :param pwm_pin: GPIO pin for PWM control.
        :param in1_pin: GPIO pin for IN1.
        :param in2_pin: GPIO pin for IN2.
        :param frequency: PWM frequency.
        """
        self.pwm = machine.PWM(machine.Pin(pwm_pin), freq=frequency)
        self.in1 = machine.Pin(in1_pin, machine.Pin.OUT)
        self.in2 = machine.Pin(in2_pin, machine.Pin.OUT)

    async def actuate(self, direction, speed):
        """
        Control the motor with the specified direction and speed.
        :param direction: 1 for forward, 0 for reverse.
        :param speed: Speed of the motor (0-1023).
        """
        if direction == 1:  # Forward
            self.in1.value(1)
            self.in2.value(0)
        elif direction == 0:  # Reverse
            self.in1.value(0)
            self.in2.value(1)
        else:  # Brake
            self.in1.value(1)
            self.in2.value(1)

        self.pwm.duty(speed)  # Set PWM speed

    async def gradualy_actuate(self, direction, speed, delay=100):
        """
        Gradually increase the speed of the motor to the specified value.
        :param direction: 1 for forward, 0 for reverse.
        :param speed: Speed of the motor (0-1023).
        :param delay: Delay between increasing the speed to reach the specified speed.
        """
        min=200
        step = 50  # PWM step size
        mod = (speed - min) % step
        steps = (speed - min) // step
    
        
        if direction == 1:  # Forward
            self.in1.value(1)
            self.in2.value(0)
        elif direction == 0:  # Reverse
            self.in1.value(0)
            self.in2.value(1)
        else:  # Brake
            self.in1.value(1)
            self.in2.value(1)

        for i in range(steps):
            self.pwm.duty(min + i * step)
            await asyncio.sleep_ms(delay)
        
        self.pwm.duty((i * step) + mod)

    def stop(self):
        """
        Stop the motor.
        """
        self.in1.value(0)
        self.in2.value(0)
        self.pwm.duty(0)
