from flask import Flask
from flask import render_template

import datetime

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.datetime.now()
    if now.month == 1 and now.day == 1:
        newyear = 1
    else:
        newyear = 0
    return render_template("index.html",newyear = newyear)
