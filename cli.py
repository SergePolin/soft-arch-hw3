import os
import requests
import time

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5000')
MESSAGE_SERVICE_URL = os.getenv('MESSAGE_SERVICE_URL', 'http://localhost:5001')
FEED_SERVICE_URL = os.getenv('FEED_SERVICE_URL', 'http://localhost:5002')

def register_user(username):
    try:
        response = requests.post(f"{USER_SERVICE_URL}/register", json={"username": username})
        response.raise_for_status()
        print("User registered successfully.")
    except requests.RequestException as e:
        print(f"Failed to register user: {e}")

def check_user_exists(username):
    try:
        response = requests.get(f"{USER_SERVICE_URL}/check", params={"username": username})
        return response.status_code == 200
    except requests.RequestException:
        return False

def post_message(username, content):
    if not check_user_exists(username):
        print("Error: User does not exist. Please register first.")
        return

    try:
        response = requests.post(f"{MESSAGE_SERVICE_URL}/post", json={"username": username, "content": content})
        response.raise_for_status()
        print("Message posted successfully.")
    except requests.RequestException as e:
        print(f"Failed to post message: {e}")

def get_feed():
    try:
        response = requests.get(f"{FEED_SERVICE_URL}/feed")
        response.raise_for_status()
        messages = response.json()
        for msg in messages:
            print(f"{msg['user']}: {msg['content']} (Likes: {msg['likes']})")
    except requests.RequestException as e:
        print(f"Failed to fetch feed: {e}")

def main():
    while True:
        command = input("Enter command (register/post/feed/exit): ")
        if command == "register":
            username = input("Enter username: ")
            register_user(username)
        elif command == "post":
            username = input("Enter username: ")
            content = input("Enter message: ")
            post_message(username, content)
        elif command == "feed":
            get_feed()
        elif command == "exit":
            break
        else:
            print("Unknown command.")
        time.sleep(1)  # Add a small delay to avoid overwhelming the services

if __name__ == "__main__":
    main()