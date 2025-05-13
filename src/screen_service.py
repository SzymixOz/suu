from flask import Flask, jsonify, request

app = Flask(__name__)

# Dane w pamięci
screenings = {
    1: {"id": 1, "movie_id": 1, "room": "A1", "date": "2023-12-15", "time": "18:00", "available_seats": 100},
    2: {"id": 2, "movie_id": 2, "room": "B2", "date": "2023-12-16", "time": "20:00", "available_seats": 80}
}
next_screening_id = 3

@app.route('/screenings', methods=['GET'])
def getScreenings():
    """Pobierz listę wszystkich seansów"""
    return jsonify(list(screenings.values()))

@app.route('/screenings', methods=['POST'])
def createScreening():
    """Utwórz nowy seans"""
    global next_screening_id
    data = request.get_json()
    
    if not all(key in data for key in ['movie_id', 'room', 'date', 'time', 'available_seats']):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_screening = {
        "id": next_screening_id,
        "movie_id": data['movie_id'],
        "room": data['room'],
        "date": data['date'],
        "time": data['time'],
        "available_seats": data['available_seats']
    }
    
    screenings[next_screening_id] = new_screening
    next_screening_id += 1
    return jsonify({"id": new_screening["id"]}), 201

if __name__ == '__main__':
    app.run(port=5004)