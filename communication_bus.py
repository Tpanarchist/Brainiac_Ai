from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for messages
southbound_bus = {
    "aspirational_layer": [],
    "global_strategy_layer": [],
    "agent_model_layer": [],
    "executive_function_layer": [],
    "cognitive_control_layer": []
}

northbound_bus = {
    "task_prosecution_layer": [],
    "cognitive_control_layer": [],
    "executive_function_layer": [],
    "agent_model_layer": [],
    "global_strategy_layer": [],
    "aspirational_layer": []
}

@app.route('/southbound/<layer>', methods=['POST'])
def send_southbound(layer):
    """Endpoint for sending southbound messages to a specific layer."""
    if layer not in southbound_bus:
        return jsonify({"error": "Invalid southbound layer"}), 404

    message = request.json.get('message')
    southbound_bus[layer].append(message)
    return jsonify({"status": "success", "detail": f"Message sent to {layer} layer."})

@app.route('/northbound/<layer>', methods=['POST'])
def send_northbound(layer):
    """Endpoint for sending northbound messages to a specific layer."""
    if layer not in northbound_bus:
        return jsonify({"error": "Invalid northbound layer"}), 404

    message = request.json.get('message')
    northbound_bus[layer].append(message)
    return jsonify({"status": "success", "detail": f"Message sent to {layer} layer."})

@app.route('/receive/southbound/<layer>', methods=['GET'])
def receive_southbound(layer):
    """Endpoint for receiving southbound messages for a specific layer."""
    if layer not in southbound_bus:
        return jsonify({"error": "Invalid southbound layer"}), 404

    layer_messages = southbound_bus[layer]
    southbound_bus[layer] = []  # Clear messages after retrieval
    return jsonify({"status": "success", "messages": layer_messages})

@app.route('/receive/northbound/<layer>', methods=['GET'])
def receive_northbound(layer):
    """Endpoint for receiving northbound messages for a specific layer."""
    if layer not in northbound_bus:
        return jsonify({"error": "Invalid northbound layer"}), 404

    layer_messages = northbound_bus[layer]
    northbound_bus[layer] = []  # Clear messages after retrieval
    return jsonify({"status": "success", "messages": layer_messages})

if __name__ == '__main__':
    app.run(debug=True)
