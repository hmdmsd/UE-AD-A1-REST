from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
    return jsonify({"users": users})

@app.route("/users/<user_id>", methods=['GET'])
def get_user_by_id(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    else:
        raise NotFound("User not found")

@app.route("/users/<user_id>/bookings", methods=['GET'])
def get_user_bookings(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise NotFound("User not found")

    try:
        booking_response = requests.get(f"http://booking:3201/bookings/{user_id}")
        booking_response.raise_for_status()
        bookings = booking_response.json()
        return jsonify(bookings)
    except requests.RequestException as e:
        return jsonify({"error": "Error fetching bookings", "details": str(e)}), 500

@app.route("/users/<user_id>/bookings/movies", methods=['GET'])
def get_user_bookings_with_movies(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise NotFound("User not found")

    try:
        booking_response = requests.get(f"http://booking:3201/bookings/{user_id}")
        booking_response.raise_for_status()
        bookings = booking_response.json()

        for date in bookings.get('dates', []):
            movie_ids = date.get('movies', [])
            movies = []
            for movie_id in movie_ids:
                movie_response = requests.get(f"http://movie:3200/movies/{movie_id}")
                if movie_response.status_code == 200:
                    movies.append(movie_response.json())
            date['movie_info'] = movies

        return jsonify(bookings)
    except requests.RequestException as e:
        return jsonify({"error": "Error fetching bookings or movies", "details": str(e)}), 500

@app.errorhandler(NotFound)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)