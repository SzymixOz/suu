import subprocess
import time
import sys
from signal import signal, SIGINT

services = [
    {"name": "user_service", "port": 5001, "command": ["python", "src/user_service.py"]},
    {"name": "movie_service", "port": 5002, "command": ["python", "src/movie_service.py"]},
    {"name": "booking_service", "port": 5003, "command": ["python", "src/booking_service.py"]},
    {"name": "screening_service", "port": 5004, "command": ["python", "src/screening_service.py"]},
    {"name": "notification_service", "port": 5005, "command": ["python", "src/notification_service.py"]}
]

processes = []

def start_services():
    print("Starting all cinema microservices...")
    for service in services:
        try:
            process = subprocess.Popen(service["command"])
            processes.append(process)
            print(f"Started {service['name']} on port {service['port']} (PID: {process.pid})")
            time.sleep(0.5)  # Małe opóźnienie między uruchamianiem serwisów
        except Exception as e:
            print(f"Failed to start {service['name']}: {e}")
            shutdown_services()
            sys.exit(1)
    
    print("\nAll services are running. Press Ctrl+C to stop all services.\n")
    print("Available services:")
    for service in services:
        print(f"- {service['name']}: http://localhost:{service['port']}")

def shutdown_services():
    print("\nShutting down all services...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=3)
        except:
            pass
    print("All services have been stopped.")

def handler(signal_received, frame):
    shutdown_services()
    sys.exit(0)

if __name__ == "__main__":
    signal(SIGINT, handler)
    start_services()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass