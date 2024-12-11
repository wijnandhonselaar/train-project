from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['GET'])
def start():
    direction = request.args.get('direction', 1)
    speed = request.args.get('speed', 720)
    ip = request.args.get('ip', '192.168.2.6')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/start?direction={direction}&speed={speed}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return jsonify(message="Motor started successfully", direction=direction, speed=speed)
            else:
                return jsonify(message=response.text, status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

@app.route('/api/start_gradually', methods=['GET'])
def start_gradually():
    direction = request.args.get('direction', 1)
    speed = request.args.get('speed', 720)
    ip = request.args.get('ip', '192.168.2.6')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/start_gradually?direction={direction}&speed={speed}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return jsonify(message="Motor started successfully", direction=direction, speed=speed)
            else:
                return jsonify(message=response.text, status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

@app.route('/api/stop', methods=['GET'])
def stop():
    ip = request.args.get('ip', '192.168.2.6')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/stop"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return jsonify(message="Motor stopped successfully")
            else:
                return jsonify(message=response.text, status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

@app.route('/api/switch/open', methods=['GET'])
def open():
    ip = request.args.get('ip', '192.168.2.6')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/switch"
        payload = {
            "action": "open"
        }
        try:
            response = requests.get(url, json=payload)
            if response.status_code == 200:
                return jsonify(message=response.text)
            else:
                return jsonify(message=response.text, status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

@app.route('/api/switch/close', methods=['GET'])
def close():
    ip = request.args.get('ip', '192.168.2.6')  # Get the IP address from the URL parameters

    if ip:
        url = f"http://{ip}/switch"
        payload = {
            "action": "close"
        }
        try:
            response = requests.get(url, json=payload)
            if response.status_code == 200:
                return jsonify(message=response.text)
            else:
                return jsonify(message=response.text, status=response.status_code), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(message="Request failed", error=str(e)), 500
    else:
        return jsonify(message="IP address not provided"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)