from flask import Flask, jsonify, request

app = Flask(__name__)

bookings = {
    1: {"id": 1, "user_id": 1, "screening_id": 1, "seats": 2, "status": "confirmed"},
    2: {"id": 2, "user_id": 2, "screening_id": 2, "seats": 3, "status": "confirmed"}
}
next_booking_id = 3

@app.route('/bookings', methods=['POST'])
def createBooking():
    global next_booking_id
    data = request.get_json()
    
    if not all(key in data for key in ['user_id', 'screening_id', 'seats']):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_booking = {
        "id": next_booking_id,
        "user_id": data['user_id'],
        "screening_id": data['screening_id'],
        "seats": data['seats'],
        "status": "confirmed"
    }
    
    bookings[next_booking_id] = new_booking
    next_booking_id += 1
    
    requests.post('http://localhost:5005/sendEmail', json={
        "to": "user@example.com",
        "subject": "Booking confirmation",
        "message": f"Thank You for booking! Booking number: {new_booking['id']}"
    })
    
    return jsonify({"id": new_booking["id"]}), 201

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def cancelBooking(booking_id):
    if booking_id not in bookings:
        return jsonify({"error": "Booking not found"}), 404
    
    bookings[booking_id]["status"] = "cancelled"
    return jsonify({"success": True})

@app.route('/bookings', methods=['GET'])
def getBookings():
    return jsonify(list(bookings.values()))

@app.route('/users/<int:user_id>/bookings', methods=['GET'])
def getUserBookings(user_id):
    user_bookings = [b for b in bookings.values() if b['user_id'] == user_id]
    return jsonify(user_bookings)

if __name__ == '__main__':
    import requests
    app.run(host='0.0.0.0', port=5003)