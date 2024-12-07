import uasyncio as asyncio
from drivers.L911N import L911N
from motor import Motor
import random

# Create a driver and a motor
loc_a_driver = L911N(18, 19)
print("Driver created")
locomotive_a = Motor(loc_a_driver)
print("Motor created")

async def main():
    try:
        # Start motor A forward at 70% speed for 5 seconds
        locomotive_a.start(direction=1, speed=350)

        # Wait for all tasks to complete
        await asyncio.sleep(5)#random.randrange(30, 90))

        # Stop both motors
        locomotive_a.stop()

        await asyncio.sleep(5)#random.randrange(10, 30))
        # Start motor A forward at 70% speed for 5 seconds
        locomotive_a.start(direction=1, speed=350)

        # Wait for all tasks to complete
        await asyncio.sleep(5)#random.randrange(30, 90))

        # Stop both motors
        locomotive_a.stop()

    except KeyboardInterrupt:
        print("Program interrupted")
        locomotive_a.stop()

# Run the main asyncio event loop
asyncio.run(main())
