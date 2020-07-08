import os
import csv
from flask import Flask, request, render_template
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL1")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for origin, destination, duration in reader:
        flight = Flight(origin=origin,destination=destination,duration=duration)
        db.session.add(flight)
        print(f"Added flight from {flight.origin} to {flight.destination} lasting {flight.duration} minutes.")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
