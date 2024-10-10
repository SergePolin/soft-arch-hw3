import os
from flask import Flask, request, jsonify
import redis
import json
import logging

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class UserService:
    @staticmethod
    def register_user(username):
        if redis_client.sismember('users', username):
            return False
        redis_client.sadd('users', username)
        return True

    @staticmethod
    def is_user_registered(username):
        return redis_client.sismember('users', username)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    app.logger.debug(f"Received registration data: {data}")  # Log the received data

    if not data:
        app.logger.error("Invalid registration data: empty request")
        return jsonify({"error": "Invalid registration data: empty request"}), 400

    username = data.get('username')

    if not username:
        app.logger.error("Invalid registration data: missing username")
        return jsonify({"error": "Invalid registration data: missing username"}), 400

    # Check if the username already exists
    if redis_client.sismember('users', username):
        app.logger.warning(f"Username '{username}' already exists")
        return jsonify({"error": "Username already exists"}), 400

    # Store the user
    redis_client.sadd('users', username)

    app.logger.info(f"User '{username}' registered successfully")
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/check', methods=['GET'])
def check_user():
    username = request.args.get('username')
    if UserService.is_user_registered(username):
        return jsonify({"registered": True}), 200
    return jsonify({"registered": False}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))