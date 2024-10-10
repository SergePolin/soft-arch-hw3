import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

MESSAGE_SERVICE_URL = os.getenv('MESSAGE_SERVICE_URL', 'http://localhost:5001')

class FeedService:
    @staticmethod
    def get_feed():
        try:
            response = requests.get(f"{MESSAGE_SERVICE_URL}/messages")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching messages: {e}")
            return []

@app.route('/feed', methods=['GET'])
def get_feed():
    messages = FeedService.get_feed()
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)))