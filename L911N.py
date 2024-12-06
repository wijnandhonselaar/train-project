import machine
import time
import uasyncio as asyncio
import random

# Initialize motor pins
motor_pwm = machine.PWM(machine.Pin(18), freq=500)  # PWM on GPIO18 (IN1)
motor_in2 = machine.Pin(19, machine.Pin.OUT)  # IN2

def motor_control(direction=1, speed=512):
    """
    Start the motor with the specified speed and direction.
    Speed range: 0 (stopped) to 1023 (full speed).
    """
    if direction == 1:  # Forward
        motor_in2.value(0)  # IN2 LOW
    else:  # Reverse
        motor_in2.value(1)  # IN2 HIGH

    motor_pwm.duty(speed)  # Set PWM speed

    print(f"Motor started with speed {speed}, direction {'forward' if direction == 1 else 'backward'}")

def motor_stop():
    """
    Stop the motor.
    """
    motor_pwm.duty(0)  # Set speed to 0 to stop the motor
    motor_in2.value(0)  # IN2 LOW
    print("Motor stopped")

try:
    while True:
        # print("Motor running forward")/
        motor_control(1, 720)
        # asyncio.create_task(motor_control(624))
        time.sleep(random.randrange(30, 90))  # Run for 5 seconds

        # print("Motor stopping...")
        motor_stop()  # Stop the motor
        
        time.sleep(random.randrange(10, 30))  # Run for 5 seconds

except KeyboardInterrupt:
    print("Program interrupted")
    motor_stop()  # Ensure motor stops if program is interrupted
