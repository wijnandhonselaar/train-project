import machine
import time
import uasyncio as asyncio
import random

# Initialize sensor pin (assuming it's a digital sensor)
# sensor_pin = machine.Pin(10, machine.Pin.IN)

# Initialize motor control pins
motor_pwm = machine.PWM(machine.Pin(18))      # PWM pin (ENA)
motor_in1 = machine.Pin(19, machine.Pin.OUT)  # Direction pin 1 (IN1)
motor_in2 = machine.Pin(21, machine.Pin.OUT)  # Direction pin 2 (IN2)
motor_pwm.freq(1000)                          # Set PWM frequency to 1kHz

# Motor state variables
motor_direction = 1  # 1 for forward, 0 for backward

# Sensor and trigger flags
sensor_triggered = False
consecutive_zeros = 0
consecutive_ones = 0

# def read_sensor():
#     """
#     Read the sensor value from GPIO10.
#     Return 1 if sensor is HIGH, 0 if LOW.
#     """
#     return sensor_pin.value()

async def motor_control(direction, speed):
    """
    Asynchronous function to run the motor in the specified direction.
    """
    if direction == 1:
        motor_in1.value(1)
        motor_in2.value(0)
    else:
        motor_in1.value(0)
        motor_in2.value(1)

    motor_pwm.duty(speed)  # Set motor speed (0 to 1023 for ESP32)
    print(f"Motor running {'forward' if direction == 1 else 'backward'}")
    
def motor_control(direction, speed):
    """
    Asynchronous function to run the motor in the specified direction.
    """
    if direction == 1:
        motor_in1.value(1)
        motor_in2.value(0)
    else:
        motor_in1.value(0)
        motor_in2.value(1)

    motor_pwm.duty(speed)  # Set motor speed (0 to 1023 for ESP32)
    print(f"Motor running {'forward' if direction == 1 else 'backward'}")

def motor_stop():
    """
    Stop the motor by setting both IN1 and IN2 to LOW.
    """
    motor_in1.value(0)
    motor_in2.value(0)
    motor_pwm.duty(0)  # Set speed to 0 to stop the motor
    print("Motor stopped")

# async def sensor_monitor():
#     global motor_direction, sensor_triggered, consecutive_zeros, consecutive_ones
    
#     sensorValue = 1
    
#     while True:
#         sensor_value = sensorValue
        
#         print(f"Sensor value: {sensor_value}")

#         # Handle train passing (detect 3 consecutive 0's)
#         if sensor_value == 0:
#             consecutive_zeros += 1
#             consecutive_ones = 0  # Reset ones counter

#             if consecutive_zeros >= 3:
#                 sensor_triggered = True  # Allow switch action on next train pass
#                 consecutive_zeros = 0    # Reset zeros counter

#         # Handle switch toggle (detect 3 consecutive 1's after 3 zeros)
#         elif sensor_value == 1 and sensor_triggered:
#             consecutive_ones += 1
#             consecutive_zeros = 0  # Reset zeros counter

#             if consecutive_ones >= 3:
#                 # Run the motor asynchronously
#                 asyncio.create_task(motor_control(motor_direction))
                
#                 # Toggle direction for next pass
#                 motor_direction = 1 - motor_direction

#                 # Reset flags
#                 sensor_triggered = False
#                 consecutive_ones = 0  # Reset ones counter

#         await asyncio.sleep(0.1)  # Check sensor every 100ms

async def main():
    while True:
        # print("Motor running forward")/
        motor_control(1, 840)
        # asyncio.create_task(motor_control(624))
        time.sleep(random.randrange(30, 90))  # Run for 5 seconds

        # print("Motor stopping...")
        motor_stop()  # Stop the motor
        
        time.sleep(random.randrange(10, 30))  # Run for 5 seconds

    # await sensor_monitor()
        
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program interrupted")
    motor_stop()