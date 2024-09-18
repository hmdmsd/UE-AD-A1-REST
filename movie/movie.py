from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
from flask_swagger_ui import get_swaggerui_blueprint
import os 

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<ph1 style='color:blue'>Welcome to the Movie service!</ph1>",200)

# Flask routes for your Movie service
@app.route('/movies', methods=['GET'])
def get_all_movies():
    """Retourne tous les films."""
    return jsonify(movies)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    """Retourne un film spécifique par ID."""
    movie = next((movie for movie in movies if movie['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Film non trouvé"}), 404

@app.route('/movies/genre/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    """Retourne tous les films d'un genre spécifique."""
    movies = [movie for movie in movies if movie['genre'].lower() == genre.lower()]
    return jsonify(movies)

@app.route('/movies/director/<director>', methods=['GET'])
def get_movies_by_director(director):
    """Retourne tous les films d'un certain réalisateur."""
    movies = [movie for movie in movies if movie['director'].lower() == director.lower()]
    return jsonify(movies)

@app.route('/help', methods=['GET'])
def get_help():
    """Retourne une liste des routes disponibles dans le service Movie."""
    routes = {
        "GET /movies": "Récupère tous les films",
        "GET /movies/<movie_id>": "Récupère un film par ID",
        "GET /movies/genre/<genre>": "Récupère les films par genre",
        "GET /movies/director/<director>": "Récupère les films par réalisateur",
        "GET /help": "Retourne la liste des points d'entrée"
    }
    return jsonify(routes)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # Swagger UI endpoint
API_URL = os.path.join(os.getcwd(), 'UE-archi-distribuees-Movie-1.0.0-resolved.yaml')

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static path
    API_URL,  # OpenAPI spec path
    config={  # Swagger UI config overrides
        'app_name': "Movie Service API"
    }
)

# Register Swagger UI blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)