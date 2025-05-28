from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/sendEmail', methods=['POST'])
def sendEmail():
    """Wyślij email"""
    data = request.get_json()
    
    if not all(key in data for key in ['to', 'subject', 'message']):
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"Email sent to {data['to']} with subject '{data['subject']}'")
    print(f"Message: {data['message']}")
    return jsonify({"success": True})

@app.route('/sendSMS', methods=['POST'])
def sendSMS():
    """Wyślij SMS"""
    data = request.get_json()
    
    if not all(key in data for key in ['to', 'message']):
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"SMS sent to {data['to']}")
    print(f"Message: {data['message']}")
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)