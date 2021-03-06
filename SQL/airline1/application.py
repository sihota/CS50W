import os

from flask import Flask
from flask import render_template
from flask import request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

app = Flask(__name__)

db_engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=db_engine))

@app.route("/")
def index():
    flights = db_session.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html",message="Invalid Flight Number")
    #make sure selected flight exists
    if db_session.execute("SELECT * FROM flights WHERE id = :id",{"id":flight_id}).rowcount == 0:
        return render_template("error.html",message="No flight exits with id:"+str(flight_id))
    #if everything okay INSERT
    db_session.execute("INSERT INTO passengers(name,flight_id) VALUES (:name,:flight_id)",
                        {"name":name,"flight_id":flight_id})
    db_session.commit()
    return render_template("success.html",message = "You have successfully booked your flight")

@app.route("/flights")
def flights():
    #list all flights
    flights = db_session.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html",flights=flights)

@app.route("/flight/<int:flight_id>")
def flight(flight_id):
    #list single flight information
    flight = db_session.execute("SELECT * FROM flights WHERE id = :id",{"id":flight_id}).fetchone()
    if flight is None:
        return render_template("error.html",message = "No Flight exists")
    #list flight  passengers
    passengers = db_session.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",{"flight_id":flight_id}).fetchall()
    return render_template("flight.html",flight=flight,passengers=passengers)

@app.route("/flight/<string:sflight_id>")
def sflight(sflight_id):
    return render_template("error.html",message="Invalid Flight Number")
