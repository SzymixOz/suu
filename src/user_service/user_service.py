from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

users = {
    1: {"id": 1, "name": "Jan Kowalski", "email": "jan@example.com", "phone": "123456789", "profile": {"newsletter": True}},
    2: {"id": 2, "name": "Anna Nowak", "email": "anna@example.com", "phone": "987654321", "profile": {"newsletter": False}}
}
next_user_id = 3

@app.route('/users', methods=['GET'])
def getUsers():
    logging.info("GET all users")
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def getUser(user_id):
    user = users.get(user_id)
    if user:
        logging.info(f"GET user: {user_id}")
        return jsonify(user)
    logging.warning(f"User not found: {user_id}")
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def createUser():
    global next_user_id
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'email']):
        logging.error("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400
    
    if any(u['email'] == data['email'] for u in users.values()):
        logging.warning(f"Email already exists: {data['email']}")
        return jsonify({"error": "Email already exists"}), 400
    
    new_user = {
        "id": next_user_id,
        "name": data['name'],
        "email": data['email'],
        "phone": data.get('phone', ''),
        "profile": data.get('profile', {})
    }
    
    users[next_user_id] = new_user
    logging.info(f"New user created: {new_user}")
    next_user_id += 1
    return jsonify({"id": new_user["id"]}), 201

@app.route('/users/<int:user_id>/profile', methods=['PUT'])
def updateProfile(user_id):
    if user_id not in users:
        logging.warning(f"User not found: {user_id}")
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    users[user_id]["profile"] = {**users[user_id]["profile"], **data}
    logging.info(f"user profile updated {user_id}: {data}")
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)