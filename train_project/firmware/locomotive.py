import uasyncio as asyncio
from drivers.L911N import L911N
from models.motor import Motor
from networking.locomotive_server import LocomotiveServer

# WiFi credentials
SSID = "VODAFONE_2926"
PASSWORD = "bikesbikesbikes"

# Create a driver and a motor
driver = L911N(pwm_pin=18, direction_pin=19)
print("Driver created")
motor = Motor(driver)
print("Motor created")

# Create a networking instance
server = LocomotiveServer(SSID, PASSWORD)

async def main():
    motor.stop()
    try:
        # Connect to WiFi
        await server.connect()

        # Start listening for instructions
        await server.listen(motor)

    except KeyboardInterrupt:
        print("Program interrupted")
        motor.stop()

# Run the main asyncio event loop
asyncio.run(main())
