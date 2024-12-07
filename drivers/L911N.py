from drivers.MotorDriver import MotorDriver
import machine
import uasyncio as asyncio

class L911N(MotorDriver):
    def __init__(self, pwm_pin, direction_pin, frequency=500):
        """
        Initialize a two-pin motor driver.
        :param pwm_pin: GPIO pin for PWM control.
        :param direction_pin: GPIO pin for direction control.
        :param frequency: PWM frequency.
        """
        self.pwm = machine.PWM(machine.Pin(pwm_pin), freq=frequency)
        self.direction = machine.Pin(direction_pin, machine.Pin.OUT)

    async def actuate(self, direction, speed):
        """
        Control the motor with the specified direction and speed.
        :param direction: 1 for forward, 0 for reverse.
        :param speed: Speed of the motor (0-1023).
        """
        self.direction.value(0 if direction == 1 else 1)  # Set direction
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
    
        self.direction.value(0 if direction == 1 else 1)  # Set direction

        for i in range(steps):
            self.pwm.duty(min + i * step)
            await asyncio.sleep_ms(delay)
        
        self.pwm.duty((i * step) + mod)

    def stop(self):
        """
        Stop the motor.
        """
        self.pwm.duty(0)
        self.direction.value(0)
