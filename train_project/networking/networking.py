
from networking.networking_interface import INetworking
import network
import uasyncio as asyncio
from microdot import Microdot, Response, Request

class Networking(INetworking):
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    async def connect(self):
        print("Connecting to WiFi...")
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected():
            await asyncio.sleep(1)
        print("Connected to WiFi:", self.wlan.ifconfig())
        return self.wlan.ifconfig()[0]

    async def listen(self, device):
        pass  # This method will be overridden by subclasses