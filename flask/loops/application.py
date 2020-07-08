from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    names = ["Amarpal","Jaipal","Satpal"]
    return render_template("index.html",names=names)
