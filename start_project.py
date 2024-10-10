import subprocess
import time
import os
import sys

def start_service(service_name, port):
    env = os.environ.copy()
    env['FLASK_APP'] = f'services/{service_name}_service.py'
    env['PORT'] = str(port)
    return subprocess.Popen(['flask', 'run', f'--port={port}'], env=env)

def main():
    print("Starting Twitter-like system...")

    try:
        import redis
        redis.Redis(host='localhost', port=6379).ping()
        print("Redis is running.")
    except:
        print("Error: Redis is not running. Please start Redis before running this script.")
        sys.exit(1)

    services = [
        ('user', 5000),
        ('message', 5001),
        ('feed', 5002)
    ]

    processes = []
    for service, port in services:
        print(f"Starting {service} service on port {port}...")
        process = start_service(service, port)
        processes.append(process)
        time.sleep(2) 

    print("\nAll services are running.")
    print("To interact with the system, run 'python cli.py' in a new terminal window.")
    print("Press Ctrl+C to stop all services.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all services...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()
        print("All services stopped.")

if __name__ == "__main__":
    main()