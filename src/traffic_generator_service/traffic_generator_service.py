import requests
import random
import time
import logging
from threading import Thread
from flask import Flask

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

USER_NAMES = ["Jan Kowalski", "Anna Nowak", "Piotr Wiśniewski", "Maria Dąbrowska", "Tomasz Lewandowski"]
USER_EMAILS = [f"user{i}@example.com" for i in range(1, 6)]
MOVIE_TITLES = ["Inception", "The Shawshank Redemption", "The Godfather", "Pulp Fiction", "The Dark Knight"]
MOVIE_GENRES = ["Sci-Fi", "Drama", "Crime", "Action", "Thriller"]
ROOMS = ["A1", "A2", "B1", "B2", "C1"]
DATES = ["2023-12-15", "2023-12-16", "2023-12-17", "2023-12-18", "2023-12-19"]
TIMES = ["10:00", "14:00", "18:00", "20:00", "22:00"]

class TrafficGenerator:
    def __init__(self):
        self.services = {
            'user_service': {
                'url': 'http://user_service:5001',
                'endpoints': [
                    {'path': '/users', 'method': 'GET'},
                    {'path': '/users', 'method': 'POST'},
                    {'path': '/users/{user_id}', 'method': 'GET'},
                    {'path': '/users/{user_id}/profile', 'method': 'PUT'}
                ]
            },
            'movie_service': {
                'url': 'http://movie_service:5002',
                'endpoints': [
                    {'path': '/movies', 'method': 'GET'},
                    {'path': '/movies', 'method': 'POST'},
                    {'path': '/movies/{movie_id}', 'method': 'GET'}
                ]
            },
            'booking_service': {
                'url': 'http://booking_service:5003',
                'endpoints': [
                    {'path': '/bookings', 'method': 'GET'},
                    {'path': '/bookings', 'method': 'POST'},
                    {'path': '/bookings/{booking_id}', 'method': 'DELETE'},
                    {'path': '/users/{user_id}/bookings', 'method': 'GET'}
                ]
            },
            'screening_service': {
                'url': 'http://screening_service:5004',
                'endpoints': [
                    {'path': '/screenings', 'method': 'GET'},
                    {'path': '/screenings', 'method': 'POST'}
                ]
            },
            'notification_service': {
                'url': 'http://notification_service:5005',
                'endpoints': [
                    {'path': '/sendEmail', 'method': 'POST'},
                    {'path': '/sendSMS', 'method': 'POST'}
                ]
            }
        }
        self.users = []
        self.movies = []
        self.screenings = []
        self.bookings = []
        self.initialized = False
        self.init_resources()

    def init_resources(self):
        try:
            for service in self.services.values():
                requests.get(service['url'], timeout=2)
            
            if not self.users:
                user_data = self.generate_random_user()
                response = requests.post(f"{self.services['user_service']['url']}/users", json=user_data)
                if response.status_code == 201:
                    self.users.append({"id": response.json().get('id'), **user_data})
            
            if not self.movies:
                movie_data = self.generate_random_movie()
                response = requests.post(f"{self.services['movie_service']['url']}/movies", json=movie_data)
                if response.status_code == 201:
                    self.movies.append({"id": response.json().get('id'), **movie_data})
            
            self.initialized = True
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            time.sleep(5)
            self.init_resources()

    def generate_random_user(self):
        return {
            "name": random.choice(USER_NAMES),
            "email": random.choice(USER_EMAILS),
            "phone": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}",
            "profile": {"newsletter": random.choice([True, False])}
        }

    def generate_random_movie(self):
        return {
            "title": random.choice(MOVIE_TITLES),
            "director": "Director " + random.choice(USER_NAMES).split()[1],
            "duration": random.randint(90, 180),
            "genre": random.choice(MOVIE_GENRES)
        }

    def generate_random_screening(self):
        if not self.movies:
            return None
        return {
            "movie_id": random.choice(self.movies)['id'],
            "room": random.choice(ROOMS),
            "date": random.choice(DATES),
            "time": random.choice(TIMES),
            "available_seats": random.randint(50, 150)
        }

    def generate_random_booking(self):
        if not self.users or not self.screenings:
            return None
        return {
            "user_id": random.choice(self.users)['id'],
            "screening_id": random.choice(self.screenings)['id'],
            "seats": random.randint(1, 5)
        }

    def call_service(self, service_name, endpoint):
        try:
            if not self.initialized:
                return

            url = f"{self.services[service_name]['url']}{endpoint['path']}"
            
            if '{user_id}' in endpoint['path']:
                if not self.users:
                    return
                user_id = random.choice(self.users)['id']
                url = url.replace('{user_id}', str(user_id))
            
            if '{movie_id}' in endpoint['path']:
                if not self.movies:
                    return
                movie_id = random.choice(self.movies)['id']
                url = url.replace('{movie_id}', str(movie_id))
            
            if '{booking_id}' in endpoint['path']:
                if not self.bookings:
                    return
                booking_id = random.choice(self.bookings)['id']
                url = url.replace('{booking_id}', str(booking_id))
            
            if endpoint['method'] == 'GET':
                response = requests.get(url, timeout=2)
            elif endpoint['method'] == 'POST':
                data = {}
                if 'users' in endpoint['path']:
                    data = self.generate_random_user()
                elif 'movies' in endpoint['path']:
                    data = self.generate_random_movie()
                elif 'screenings' in endpoint['path']:
                    data = self.generate_random_screening()
                    if not data:
                        return
                elif 'bookings' in endpoint['path']:
                    data = self.generate_random_booking()
                    if not data:
                        return
                elif 'sendEmail' in endpoint['path']:
                    if not self.users:
                        return
                    data = {
                        "to": random.choice(self.users)['email'],
                        "subject": "Booking confirmation",
                        "message": "Thank you for booking!"
                    }
                elif 'sendSMS' in endpoint['path']:
                    if not self.users:
                        return
                    data = {
                        "to": random.choice(self.users)['phone'],
                        "message": "Booking confirmation"
                    }
                
                response = requests.post(url, json=data, timeout=2)
                
                if response.status_code == 201:
                    if 'users' in endpoint['path']:
                        self.users.append({"id": response.json().get('id'), **data})
                    elif 'movies' in endpoint['path']:
                        self.movies.append({"id": response.json().get('id'), **data})
                    elif 'screenings' in endpoint['path']:
                        self.screenings.append({"id": response.json().get('id'), **data})
                    elif 'bookings' in endpoint['path']:
                        self.bookings.append({"id": response.json().get('id'), **data})
            
            elif endpoint['method'] == 'PUT':
                if 'profile' in endpoint['path'] and self.users:
                    data = {"newsletter": random.choice([True, False])}
                    response = requests.put(url, json=data, timeout=2)
            
            elif endpoint['method'] == 'DELETE':
                response = requests.delete(url, timeout=2)
            
            logger.info(f"Called {service_name} {endpoint['method']} {url} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error calling {service_name}: {str(e)}")
        except Exception as e:
            logger.error(f"Error calling {service_name}: {str(e)}")

    def generate_traffic(self):
        while True:
            if not self.initialized:
                time.sleep(5)
                continue
                
            service_name = random.choice(list(self.services.keys()))
            endpoint = random.choice(self.services[service_name]['endpoints'])
            
            self.call_service(service_name, endpoint)
            time.sleep(random.uniform(0.1, 1))

@app.route('/')
def health_check():
    return "Traffic Generator is running"

def run_generator():
    generator = TrafficGenerator()
    generator.generate_traffic()

if __name__ == '__main__':
    Thread(target=run_generator, daemon=True).start()
    app.run(host='0.0.0.0', port=5006)