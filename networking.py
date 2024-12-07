import network
import uasyncio as asyncio
from microdot import Microdot, Response

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
        async def handle_info_get(request):
            return Response(body="Motor info", status_code=200)

        @app.post('/do')
        async def handle_do_post(request):
            try:
                request_data = await request.json
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return Response(body="Invalid JSON", status_code=400)
            
            stop = request_data.get('stop', None)

            if stop != None:
                print(f"Stopping the train")
                motor.stop()
                return Response(body="Motor stopped", status_code=200)
            
            direction = request_data.get('direction')
            speed = request_data.get('speed')
            duration = request_data.get('duration', None)
            
            print(f"Staring the train")

            if direction is not None and speed is not None:
                if duration is not None:
                    motor.start(direction=int(direction), speed=int(speed), duration=int(duration))
                else:
                    motor.start(direction=int(direction), speed=int(speed))
                return Response(body="Motor started", status_code=200)
            else:
                return Response(body="Invalid parameters", status_code=400)

        await app.start_server(host='0.0.0.0', port=80)
