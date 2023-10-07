from flask import Flask, jsonify, request
import requests
import json

API_BASE_URL = "http://127.0.0.1:58000/api/v1"
def get_credentials():
    with open('credentials.json', 'r') as file:
        creds = json.load(file)
        return creds['username'], creds['password'], creds['ticket']

def api_request(method, endpoint, data=None):
    username, password, ticket = get_credentials()
    headers = {
        "X-Auth-Token": ticket
    }
    url = f"{API_BASE_URL}/{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=headers, auth=(username, password))
    elif method == "POST":
        response = requests.post(url, json=data, headers=headers, auth=(username, password))
    return response


app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Flask API Forwarder!"

@app.route('/network-device', methods=['GET', 'POST'])
def network_device():
    if request.method == 'GET':
        response = api_request("GET", "network-device")
    elif request.method == 'POST':
        data = request.json
        response = api_request("POST", "network-device", data)
    return jsonify(response.json()), response.status_code

@app.route('/assurance/health', methods=['GET'])
def health_status():
    response = api_request("GET", "assurance/health")
    return jsonify(response.json()), response.status_code

@app.route('/topology/physical-topology', methods=['GET'])
def physical_topology():
    response = requests.get("GET", "topology/physical-topology")
    return jsonify(response.json()), response.status_code

@app.route('/discovery', methods=['GET'])
def discoveries():
    response = requests.get("GET", "discovery")
    return jsonify(response.json()), response.status_code

@app.route('/assurance/health-issues', methods=['GET'])
def health_issues():
    response = requests.get("GET", "assurance/health-issues")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
