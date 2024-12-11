import uasyncio as asyncio
from drivers.L928N import L928N
from motor import Motor
from networking import Networking

# WiFi credentials
SSID = "VODAFONE_2926"
PASSWORD = "bikesbikesbikes"

# Create a driver and a motor
driver = L928N(pwm_pin=18, in1_pin=19, in2_pin=21)
print("Driver created")
motor = Motor(driver)
print("Motor created")

# Create a networking instance
# networking = Networking(SSID, PASSWORD)

async def main():
    motor.stop()
    try:
        motor.start(direction=1, speed=500)
        await asyncio.sleep(0.04)
        motor.stop()
        
        await asyncio.sleep(1)
        motor.start(direction=0, speed=500)
        await asyncio.sleep(0.035)
        motor.stop()
        # Connect to WiFi
        # await networking.connect()

        # # Start listening for instructions
        # await networking.listen(motor)

    except KeyboardInterrupt:
        print("Program interrupted")
        motor.stop()

# Run the main asyncio event loop
asyncio.run(main())
