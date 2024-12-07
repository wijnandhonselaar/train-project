import network
import uasyncio as asyncio
from microdot import Microdot, Response, Request

class Networking:
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

    async def listen(self, motor):
        print("Starting web server...")
        app = Microdot()

        
        @app.get('/info')
        async def handle_info(request):
            return Response(body="Motor info", status_code=200)

        @app.get('/start')
        async def handle_start(request):
            direction = request.args.get('direction')
            speed = request.args.get('speed')

            if direction is not None and speed is not None:
                motor.start(direction=int(direction), speed=int(speed))
                return Response(body="Motor started", status_code=200)
            else:
                return Response(body="Invalid parameters", status_code=400)

        @app.get('/start_gradually')
        async def handle_start(request):
            direction = request.args.get('direction')
            speed = request.args.get('speed')

            if direction is not None and speed is not None:
                motor.start_gradually(direction=int(direction), speed=int(speed), delay=500)
                return Response(body="Motor started", status_code=200)
            else:
                return Response(body="Invalid parameters", status_code=400)

        @app.get('/stop')
        async def handle_stop(request):
                motor.stop()
                return Response(body="Motor stopped", status_code=200)
    


        await app.start_server(host='0.0.0.0', port=80)
