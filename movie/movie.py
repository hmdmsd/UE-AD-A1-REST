from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
from flask_swagger_ui import get_swaggerui_blueprint
import os
import uuid

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
    movies_data = json.load(jsf)["movies"]

# Convert movies to a dictionary for faster lookup
movies = {movie['id']: movie for movie in movies_data}

@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

@app.route("/json", methods=['GET'])
def get_json():
    return jsonify({"movies": list(movies.values())})

@app.route("/movies/<string:movieid>", methods=['GET'])
def get_movie_byid(movieid):
    movie = movies.get(movieid)
    if movie:
        return jsonify(movie)
    return make_response(jsonify({"error": "Movie not found"}), 400)

@app.route("/movies/<string:movieid>", methods=['POST'])
def create_movie(movieid):
    if movieid in movies:
        return make_response(jsonify({"error": "Movie already exists"}), 409)
    
    content = request.json
    movie = {
        "id": movieid,
        "title": content["title"],
        "rating": content["rating"],
        "director": content["director"]
    }
    movies[movieid] = movie
    return jsonify(movie), 200

@app.route("/movies/<string:movieid>", methods=['DELETE'])
def del_movie(movieid):
    if movieid in movies:
        del movies[movieid]
        return make_response("", 200)
    return make_response(jsonify({"error": "Movie not found"}), 400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    title = request.args.get('title')
    if not title:
        return make_response(jsonify({"error": "Title parameter is required"}), 400)
    
    for movie in movies.values():
        if movie['title'].lower() == title.lower():
            return jsonify(movie)
    
    return make_response(jsonify({"error": "Movie not found"}), 400)

@app.route("/movies/<string:movieid>/<int:rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    if movieid not in movies:
        return make_response(jsonify({"error": "Movie not found"}), 400)
    
    if rate < 0 or rate > 10:
        return make_response(jsonify({"error": "Rating must be between 0 and 10"}), 400)
    
    movies[movieid]['rating'] = rate
    return make_response("", 200)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'  # This should be the path to your OpenAPI YAML file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Movie Service API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)