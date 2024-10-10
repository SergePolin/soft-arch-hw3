import os
from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=1)

class MessageService:
    @staticmethod
    def post_message(username, content):
        if len(content) > 400:
            return False
        message = json.dumps({"user": username, "content": content, "likes": 0})
        redis_client.lpush('messages', message)
        redis_client.ltrim('messages', 0, 999)  # Keep last 1000 messages
        return True

    @staticmethod
    def like_message(message_index):
        message = redis_client.lindex('messages', message_index)
        if message:
            message_data = json.loads(message)
            message_data['likes'] += 1
            redis_client.lset('messages', message_index, json.dumps(message_data))
            return True
        return False

    @staticmethod
    def get_messages(count=10):
        messages = redis_client.lrange('messages', 0, count-1)
        return [json.loads(m) for m in messages]

@app.route('/post', methods=['POST'])
def post_message():
    data = request.json
    if MessageService.post_message(data['username'], data['content']):
        return jsonify({"message": "Message posted successfully"}), 201
    return jsonify({"message": "Message too long"}), 400

@app.route('/like/<int:index>', methods=['POST'])
def like_message(index):
    if MessageService.like_message(index):
        return jsonify({"message": "Message liked successfully"}), 200
    return jsonify({"message": "Message not found"}), 404

@app.route('/messages', methods=['GET'])
def get_messages():
    count = request.args.get('count', default=10, type=int)
    messages = MessageService.get_messages(count)
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)))