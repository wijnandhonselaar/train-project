from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

@app.route('/api/start', methods=['GET'])
def start():
    direction = request.args.get('direction', 1)
    speed = request.args.get('speed', 720)
    ip = request.args.get('ip', '192.168.2.5')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/do"
        payload = {
            "direction": direction,
            "speed": speed
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return jsonify(message="Motor started successfully", direction=direction, speed=speed)
            else:
                return jsonify(message="Failed to start motor", status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

@app.route('/api/stop', methods=['GET'])
def stop():
    ip = request.args.get('ip', '192.168.2.5')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/do"
        payload = {
            "stop": "stop"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return jsonify(message="Motor stopped successfully")
            else:
                return jsonify(message=response.text, status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)