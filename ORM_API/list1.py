import os
import csv
from flask import Flask, request, render_template
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL1")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    flights = Flight.query.all()
    print(flights)
    for flight in flights:
        print(f"Flight from {flight.origin} to {flight.destination} , {flight.duration}  minutes")

if __name__ == "__main__":
    with app.app_context():
        main()
