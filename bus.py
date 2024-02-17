from flask import Flask, request
import yaml
import time
import os
import glob
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Ensure the logs directory exists
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

@app.route('/message', methods=['POST'])
def post_message():
    message = request.json
    message['timestamp'] = time.time()
    file_path = os.path.join(logs_dir, f"log_{message['timestamp']}_{message['bus']}_{message['layer']}.yaml")
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(message, file)
    logging.info(f"Received POST message: bus={message['bus']}, layer={message['layer']}, message={message['message']}")
    return 'Message received', 200

@app.route('/message', methods=['GET'])
def get_messages():
    bus = request.args.get('bus')
    layer = int(request.args.get('layer'))
    logging.info(f"Received GET request: bus={bus}, layer={layer}")
    files = glob.glob(os.path.join(logs_dir, '*.yaml'))
    messages = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            message = yaml.safe_load(f)
            messages.append(message)
    if bus == 'north':
        # Adjusted to include messages with a layer equal to or greater than the specified layer for bus=north
        filtered_messages = [m for m in messages if m['bus'] == 'north' and m['layer'] >= layer]
    else:
        filtered_messages = [m for m in messages if m['bus'] == 'south' and m['layer'] < layer]
    sorted_messages = sorted(filtered_messages, key=lambda m: m['timestamp'], reverse=True)
    logging.info(f"Sending {len(sorted_messages)} messages in response to GET request.")
    return {'messages': sorted_messages[:20]}, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
