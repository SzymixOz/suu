from flask import Flask, jsonify, request

app = Flask(__name__)

# Dane w pamięci
movies = {
    1: {"id": 1, "title": "Inception", "director": "Christopher Nolan", "duration": 148, "genre": "Sci-Fi"},
    2: {"id": 2, "title": "The Shawshank Redemption", "director": "Frank Darabont", "duration": 142, "genre": "Drama"}
}
next_movie_id = 3

@app.route('/movies', methods=['GET'])
def getMovies():
    """Pobierz listę wszystkich filmów"""
    return jsonify(list(movies.values()))

@app.route('/movies/<int:movie_id>', methods=['GET'])
def getMovie(movie_id):
    """Pobierz pojedynczy film"""
    movie = movies.get(movie_id)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@app.route('/movies', methods=['POST'])
def addMovie():
    """Dodaj nowy film"""
    global next_movie_id
    data = request.get_json()
    
    if not all(key in data for key in ['title', 'director', 'duration', 'genre']):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_movie = {
        "id": next_movie_id,
        "title": data['title'],
        "director": data['director'],
        "duration": data['duration'],
        "genre": data['genre']
    }
    
    movies[next_movie_id] = new_movie
    next_movie_id += 1
    return jsonify({"id": new_movie["id"]}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)