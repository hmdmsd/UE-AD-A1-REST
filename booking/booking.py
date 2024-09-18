from flask import Flask, jsonify, request, abort
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Server parameters
PORT = 3201
HOST = '0.0.0.0'

# Load data from JSON database
with open('./databases/bookings.json', 'r') as jsf:
    bookings = json.load(jsf)["bookings"]

# Home route
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

# Route to get all bookings
@app.route("/bookings", methods=['GET'])
def get_bookings():
    return jsonify({"bookings": bookings})

# Route to get bookings for a specific user
@app.route("/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    user_booking = next((booking for booking in bookings if booking["userid"] == userid), None)
    if user_booking is None:
        abort(404, description=f"No bookings found for user {userid}")
    return jsonify(user_booking)

# Route to add a new booking for a user
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking(userid):
    if not request.json or 'date' not in request.json or 'movieid' not in request.json:
        abort(400, description="Invalid input: date and movieid are required")

    user_booking = next((booking for booking in bookings if booking["userid"] == userid), None)
    
    if user_booking is None:
        new_booking = {
            "userid": userid,
            "dates": [{
                "date": request.json['date'],
                "movies": [request.json['movieid']]
            }]
        }
        bookings.append(new_booking)
        return jsonify(new_booking), 201

    date_entry = next((date for date in user_booking['dates'] if date['date'] == request.json['date']), None)
    
    if date_entry:
        if request.json['movieid'] not in date_entry['movies']:
            date_entry['movies'].append(request.json['movieid'])
        else:
            abort(409, description="Booking already exists")
    else:
        user_booking['dates'].append({
            "date": request.json['date'],
            "movies": [request.json['movieid']]
        })

    return jsonify(user_booking)

# Error handling for 404
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Error handling for 400
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Error handling for 409
@app.errorhandler(409)
def conflict(e):
    return jsonify(error=str(e)), 409

# Launch the server
if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)