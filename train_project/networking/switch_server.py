from networking.networking import Networking
from microdot import Microdot, Response

class SwitchServer(Networking):
    async def listen(self, switch):
        print("Starting web server for switch...")
        app = Microdot()

        @app.get('/info')
        async def handle_info(request):
            return Response(body="Switch info", status_code=200)

        @app.get('/switch')
        async def handle_switch(request):
            action = request.args.get('action')

            if action in ["open", "close"]:
                await switch.switch(action)
                return Response(body=f"Switch {action}ed", status_code=200)
            else:
                return Response(body="Invalid action", status_code=400)

        await app.start_server(host='0.0.0.0', port=80)