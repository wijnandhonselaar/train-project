from networking.networking import Networking
from microdot import Microdot, Response

class LocomotiveServer(Networking):
    async def listen(self, locomotive):
        print("Starting web server for locomotive...")
        app = Microdot()

        @app.get('/info')
        async def handle_info(request):
            return Response(body="Motor info", status_code=200)

        @app.get('/start')
        async def handle_start(request):
            direction = request.args.get('direction')
            speed = request.args.get('speed')

            if direction is not None and speed is not None:
                locomotive.start(direction=int(direction), speed=int(speed))
                return Response(body="Motor started", status_code=200)
            else:
                return Response(body=request.args, status_code=400)

        @app.get('/start_gradually')
        async def handle_start_gradually(request):
            direction = request.args.get('direction')
            speed = request.args.get('speed')

            if direction is not None and speed is not None:
                locomotive.start_gradually(direction=int(direction), speed=int(speed), delay=500)
                return Response(body="Motor started", status_code=200)
            else:
                return Response(body="Invalid parameters", status_code=400)

        @app.get('/stop')
        async def handle_stop(request):
            locomotive.stop()
            return Response(body="Motor stopped", status_code=200)

        await app.start_server(host='0.0.0.0', port=80)