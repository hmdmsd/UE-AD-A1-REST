from flask import Flask, jsonify, request, abort
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Paramètres du serveur
PORT = 3202
HOST = '0.0.0.0'

# Charger les données de la base de données JSON
with open('./databases/times.json', 'r') as jsf:
    schedule = json.load(jsf)["schedule"]

# Route d'accueil
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# Route pour récupérer l'intégralité du planning (showtimes)
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    return jsonify({"schedule": schedule})

# Route pour récupérer les films à une date donnée
@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_by_date(date):
    # Cherche les films pour une date spécifique dans le JSON
    for entry in schedule:
        if entry['date'] == date:
            return jsonify(entry)
    abort(404, description=f"No movies found for date {date}")

# Gestion des erreurs 404
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Lancement du serveur
if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)
