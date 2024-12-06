import machine
import time

# Initialize motor pins
motor_pwm = machine.PWM(machine.Pin(10), freq=1000)  # PWM on GPIO10
# motor_pwm.freq(1000)  # Set frequency
motor_in2 = machine.Pin(11, machine.Pin.OUT)  # IN2

def motor_start(speed=512, direction=1):
    """
    Start the motor with the specified speed and direction.
    Speed range: 0 (stopped) to 1023 (full speed).
    """
    if direction == 1:  # Forward
        motor_pwm.duty(speed)  # Set PWM speed
        motor_in2.value(0)  # IN2 LOW
    else:  # Reverse
        motor_pwm.duty(speed)  # Set PWM speed
        motor_in2.value(1)  # IN2 HIGH
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
        motor_start(1023, 1)  # Start motor at 80% speed (0-1023)
        time.sleep(2)  # Run for 5 seconds

        motor_stop()  # Stop the motor
        time.sleep(1)  # Wait for 3 seconds before restarting
        
        motor_start(1023, 0)  # Start motor at 80% speed (0-1023)
        time.sleep(2)  # Run for 5 seconds

        motor_stop()  # Stop the motor
        time.sleep(1)  # Wait for 3 seconds before restarting

except KeyboardInterrupt:
    print("Program interrupted")
    motor_stop()  # Ensure motor stops if program is interrupted
