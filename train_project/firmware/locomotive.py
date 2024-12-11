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

async def broadcast_address():
    import socket
    import json
    message = json.dumps({"id": 1, "type": "locomotive"})
    broadcast_address = ('192.168.2.255', 37020)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        sock.sendto(message.encode(), broadcast_address)
        await asyncio.sleep(10)

async def main():
    motor.stop()
    try:
        # Connect to WiFi
        await server.connect()

        # Start broadcasting address
        asyncio.create_task(broadcast_address())

        # Start listening for instructions
        await server.listen(motor)

    except KeyboardInterrupt:
        print("Program interrupted")
        motor.stop()

# Run the main asyncio event loop
asyncio.run(main())
