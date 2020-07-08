import os

from flask import Flask
from flask import render_template
from flask import request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL1")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html",message="Invalid Flight Number")
    #make sure selected flight exists
    flight = Flight.query.get(flight_id)
    if not flight:
        return render_template("error.html",message="No flight exits with id:"+str(flight_id))
    #if everything okay INSERT
    flight.add_passenger(name)
    return render_template("success.html",message = "You have successfully booked your flight")

@app.route("/flights")
def flights():
    #list all flights
    flights = Flight.query.all()
    return render_template("flights.html",flights=flights)

@app.route("/flight/<int:flight_id>")
def flight(flight_id):
    #list single flight information
    flight =  Flight.query.get(flight_id)
    if not flight:
        return render_template("error.html",message = "No Flight exists")

    passengers = Passenger.query.filter_by(flight_id = flight_id).all()
    #list flight  passengers
    return render_template("flight.html",flight=flight,passengers=passengers)

@app.route("/flight/<string:sflight_id>")
def sflight(sflight_id):
    return render_template("error.html",message="Invalid Flight Number")
