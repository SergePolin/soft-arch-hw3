# Twitter-like Distributed System

This project implements a simple Twitter-like system using a service-based architecture. Users can register, post short messages, view a feed of recent messages, and like messages.

## Project Structure

```plaintext
twitter_clone/
│
├── services/
│ ├── user_service.py
│ ├── message_service.py
│ └── feed_service.py
│
├── cli.py
├── start_project.py
└── README.md
```

- `services/`: Contains the individual microservices
  - `user_service.py`: Manages user registration
  - `message_service.py`: Handles posting and retrieving messages
  - `feed_service.py`: Manages the feed of recent messages
- `cli.py`: Command-line interface for interacting with the system
- `start_project.py`: Script to start all services

## Prerequisites

- Python 3.7+
- Redis

## Pre-installation

1. Install Redis

   - On MacOS:

   ```bash
   brew install redis
   ```

   - On Windows:

   ```bash
   choco install redis
   ```

   - On Linux:

   ```bash
   sudo apt-get install redis-server
   ```

2. Start Redis server:

   - On MacOS:

   ```bash
   brew services start redis
   ```

   - On Windows:

   ```bash
   redis-server
   ```

   - On Linux:

   ```bash
   sudo systemctl start redis
   ```

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd twitter_clone
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:

   ```bash
   pip install flask redis requests
   ```

4. Ensure Redis is installed and running on your system.

## Running the Application

1. Start all services using the provided script:

   ```bash
   python start_project.py
   ```

2. In a new terminal window, run the CLI:

   ```bash
   python cli.py
   ```

3. Follow the prompts in the CLI to interact with the system:

   - Register new users
   - Post messages
   - View the feed
   - Like messages

4. To stop all services, press Ctrl+C in the terminal where `start_project.py` is running.

## Services

- User Service: Runs on port 5000
- Message Service: Runs on port 5001
- Feed Service: Runs on port 5002

Each service can be scaled independently based on load requirements.

## Environment Variables

The following environment variables can be set to configure the services:

- `REDIS_HOST`: Redis server host (default: localhost)
- `USER_SERVICE_URL`: URL for the User Service (default: <http://localhost:5000>)
- `MESSAGE_SERVICE_URL`: URL for the Message Service (default: <http://localhost:5001>)
- `FEED_SERVICE_URL`: URL for the Feed Service (default: <http://localhost:5002>)
