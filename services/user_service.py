import os
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)

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
    username = request.json.get('username')
    if UserService.register_user(username):
        return jsonify({"message": "User registered successfully"}), 201
    return jsonify({"message": "Username already exists"}), 400

@app.route('/check', methods=['GET'])
def check_user():
    username = request.args.get('username')
    if UserService.is_user_registered(username):
        return jsonify({"registered": True}), 200
    return jsonify({"registered": False}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))