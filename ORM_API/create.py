import os
from flask import Flask, request, render_template
#import all the model classes to create tables
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL1")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#tie this database with this flask application
db.init_app(app)

def main():
    #create table from model classes
    db.create_all()

if __name__ == "__main__":
    # create application context for command line
    # interact with flask application
    with app.app_context():
        main()
