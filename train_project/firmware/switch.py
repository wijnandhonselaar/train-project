import uasyncio as asyncio
from drivers.L928N import L928N
from models.switch import Switch
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

async def broadcast_address(ip):
    import socket
    import json
    
    # Replace the last digit of the IP address with 255
    ip_parts = ip.split('.')
    ip_parts[-1] = '255'
    broadcast_ip = '.'.join(ip_parts)
    
    message = json.dumps({"id": 2, "type": "switch"})
    broadcast_address = (broadcast_ip, 37020)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        sock.sendto(message.encode(), broadcast_address)
        await asyncio.sleep(10)

async def main():
    motor.stop()
    try:
        await asyncio.sleep(0.3)
        motor.stop()
        # Connect to WiFi
        ip = await server.connect()

        # Start broadcasting address
        asyncio.create_task(broadcast_address(ip))

        # Start listening for instructions
        await server.listen(switch)

    except KeyboardInterrupt:
        print("Program interrupted")
        motor.stop()

# Run the main asyncio event loop
asyncio.run(main())
