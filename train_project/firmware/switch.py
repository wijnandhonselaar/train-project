import uasyncio as asyncio
from drivers.L928N import L928N
from models.Switch import Switch
from models.motor import Motor
from networking.switch_server import SwitchServer

# WiFi credentials
SSID = "VODAFONE_2926"
PASSWORD = "bikesbikesbikes"

# Create a driver and a motor
driver = L928N(pwm_pin=18, in1_pin=19, in2_pin=21)
print("Driver created")
motor = Motor(driver)
print("Motor created")
switch = Switch(driver)

# Create a networking instance
server = SwitchServer(SSID, PASSWORD)

async def main():
    motor.stop()
    try:
        await asyncio.sleep(0.3)
        motor.stop()
        # Connect to WiFi
        await server.connect()

        # Start listening for instructions
        await server.listen(switch)

    except KeyboardInterrupt:
        print("Program interrupted")
        motor.stop()

# Run the main asyncio event loop
asyncio.run(main())
