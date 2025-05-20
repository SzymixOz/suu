from flask import Flask, jsonify, request

app = Flask(__name__)

# Dane w pamięci
users = {
    1: {"id": 1, "name": "Jan Kowalski", "email": "jan@example.com", "phone": "123456789", "profile": {"newsletter": True}},
    2: {"id": 2, "name": "Anna Nowak", "email": "anna@example.com", "phone": "987654321", "profile": {"newsletter": False}}
}
next_user_id = 3

@app.route('/users', methods=['GET'])
def getUsers():
    """Pobierz listę wszystkich użytkowników"""
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def getUser(user_id):
    """Pobierz pojedynczego użytkownika"""
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def createUser():
    """Utwórz nowego użytkownika"""
    global next_user_id
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'email']):
        return jsonify({"error": "Missing required fields"}), 400
    
    if any(u['email'] == data['email'] for u in users.values()):
        return jsonify({"error": "Email already exists"}), 400
    
    new_user = {
        "id": next_user_id,
        "name": data['name'],
        "email": data['email'],
        "phone": data.get('phone', ''),
        "profile": data.get('profile', {})
    }
    
    users[next_user_id] = new_user
    next_user_id += 1
    return jsonify({"id": new_user["id"]}), 201

@app.route('/users/<int:user_id>/profile', methods=['PUT'])
def updateProfile(user_id):
    """Zaktualizuj profil użytkownika"""
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    users[user_id]["profile"] = {**users[user_id]["profile"], **data}
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)