from flask import Flask, jsonify, request, render_template
import requests
import csv
import socket
import threading

app = Flask(__name__)
app.secret_key = 'train_manager_1'  # Set a secret key for session management
listener_started = False  # Flag to ensure the listener starts only once
last_broadcast = None  # Global variable to store the last broadcast message
connected_devices = []  # List to store all connected devices

def listen_for_broadcasts():
    global connected_devices
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 37020))
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        device_info = {"message": message, "ip": addr[0]}
        
        # Parse the message to extract id and type
        try:
            import json
            message_data = json.loads(message)
            device_id = message_data.get("id")
            device_type = message_data.get("type")
            
            # Check if the device already exists in the list
            if not any(d['id'] == device_id and d['type'] == device_type for d in connected_devices):
                connected_devices.append({"id": device_id, "type": device_type, "ip": addr[0]})
        except json.JSONDecodeError:
            pass

@app.before_request
def start_broadcast_listener():
    global listener_started
    if not listener_started:
        thread = threading.Thread(target=listen_for_broadcasts)
        thread.daemon = True
        thread.start()
        listener_started = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', connected_devices=connected_devices)

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

@app.route('/api/clear_devices', methods=['POST'])
def clear_devices():
    global connected_devices
    connected_devices = []
    return jsonify(message="Connected devices cleared"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)