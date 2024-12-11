import uasyncio as asyncio
from drivers.L911N import L911N
from motor import Motor
from networking import Networking

# WiFi credentials
SSID = "VODAFONE_2926"
PASSWORD = "bikesbikesbikes"

# Create a driver and a motor
driver = L911N(pwm_pin=18, direction_pin=19)
print("Driver created")
motor = Motor(driver)
print("Motor created")

# Create a networking instance
networking = Networking(SSID, PASSWORD)

async def main():
    motor.stop()
    try:
        # Connect to WiFi
        await networking.connect()

        # Start listening for instructions
        await networking.listen(motor)

    except KeyboardInterrupt:
        print("Program interrupted")
        motor.stop()

# Run the main asyncio event loop
asyncio.run(main())
