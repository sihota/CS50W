import os
import sys

from flask import render_template,request
from flask import Flask, session, redirect, url_for, escape, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
#https://flask-bcrypt.readthedocs.io/en/latest/
from flask_bcrypt import Bcrypt



app = Flask(__name__)
bcrypt = Bcrypt(app)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'any random string'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/<string:isbn>")
def api_isbn(isbn):
    reviews = db.execute("SELECT max(books.title) as title, max(books.author) as Author,max(books.year) as Year, MAX(books.isbn) as isbn,"\
                        " COUNT(reviews.rating) as review_count, AVG(reviews.rating) AS average_score" \
                        " FROM reviews LEFT JOIN books on reviews.book_id = books.id"\
                        " GROUP BY reviews.book_id"\
                        " HAVING reviews.book_id = ( SELECT id FROM books WHERE isbn = :isbn) ",
                        {"isbn":isbn}).fetchone()
    if reviews is None:
        return jsonify({"error":"No results found"}),404

    return jsonify({
            "title": reviews.title,
            "author": reviews.author,
            "year": reviews.year,
            "isbn": reviews.isbn,
            "review_count": reviews.review_count,
            "average_score": float(reviews.average_score)
        })

@app.route("/book/<int:book_id>", methods=["GET","POST"])
def book(book_id):
    if request.method == "GET":
        book = db.execute("SELECT * FROM books WHERE id = :book_id",
                        {"book_id": book_id }).fetchone()
        if not book:
            return render_template("error.html", error_message = "No book found.")

        #get review counts from goodreads
        isbn = book["isbn"]
        key = os.getenv("GOODREADS_API_KEY")
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns":isbn})
        data = response.json()
        json_book = data["books"][0]
        user_id = session["user_id"]
        show_review_form = False
        error_message = ""
        #error = request.args.get("error")
        #if error == "rating":
        #    error_message = "Please provide atleast one star rating."
        #else:
        #    error_message = None

        #check review for a book
        if db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id",{"book_id":book_id,"user_id":user_id}).rowcount == 0:
            show_review_form = True

        #get all users review for a book
        reviews = db.execute("SELECT reviews.*, users.id,users.username FROM reviews JOIN users ON users.id = reviews.user_id WHERE book_id = :book_id",
                                {"book_id":book_id}).fetchall()

        return render_template("book.html",book = book, json_book = json_book, show_review_form = show_review_form, reviews = reviews, error_message = error_message )

    elif request.method == "POST":
        rating = request.form.get("rating")

        if len(rating.strip()) == 0:
            return redirect(url_for("book",book_id = book_id))

        if not rating.isnumeric():
            return redirect(url_for("book",book_id = book_id))

        rating = int(rating)

        if not rating in range(1,5):
            return redirect(url_for("book",book_id = book_id))

        review = request.form.get("review")
        user_id = session["user_id"]
        #print("POST", file=sys.stderr)
        db.execute("INSERT INTO reviews (rating,review,book_id,user_id) VALUES(:rating,:review,:book_id,:user_id)",
                    {"rating":rating,"review":review,"book_id":book_id,"user_id":user_id})
        db.commit()
        return redirect(url_for("book",book_id = book_id))


@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        if session.get("username") is None:
            #return render_template("error.html",message = "Sorry, snd\jjj\jgn in required for this page.")
            return redirect(url_for('index'))
        username = session["username"]
        return render_template("search.html",message = "Welcome "+str(username)+"!")
    elif request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")

        if len(isbn) == 0 and len(title) == 0 and len(author) == 0 :
            return render_template("search.html",error_message = "Please enter atleast one field.")

        if len(isbn) != 0 and len(title) != 0 and len(author) != 0 :
            books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :title AND author LIKE :author",
                            {"isbn": '%' + isbn + '%', "title": '%' + title + '%', "author": '%' + author + '%' }).fetchall()
        # if only isbn
        elif len(isbn) != 0 and len(title) == 0 and len(author) == 0 :
            books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn",
                            {"isbn": '%' + isbn + '%'}).fetchall()
        #if isbn and title
        elif len(isbn) != 0 and len(title) != 0 and len(author) == 0 :
            books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :title",
                            {"isbn": '%' + isbn + '%', "title": '%' + title + '%'}).fetchall()
        #only isbn and author
        elif len(isbn) != 0 and len(title) == 0 and len(author) != 0 :
            books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND author LIKE :author",
                            {"isbn": '%' + isbn + '%', "author": '%' + author + '%' }).fetchall()
        #only title and author
        elif len(isbn) == 0 and len(title) != 0 and len(author) != 0 :
            books = db.execute("SELECT * FROM books WHERE title LIKE :title AND author LIKE :author",
                            {"title": '%' + title + '%', "author": '%' + author + '%' }).fetchall()
        #only author
        elif len(isbn) == 0 and len(title) == 0 and len(author) != 0 :
            books = db.execute("SELECT * FROM books WHERE author LIKE :author",
                            {"author": '%' + author + '%' }).fetchall()
        #only title
        elif len(isbn) == 0 and len(title) != 0 and len(author) == 0 :
            books = db.execute("SELECT * FROM books WHERE title LIKE :title",
                            {"title": '%' + title + '%'}).fetchall()

        if len(books) == 0:
            return render_template("search.html",error_message = "No match results found.")

        return render_template("search.html",books = books)

@app.route("/logout")
def logout():
    if not session.get("username") is None:
        session.pop("username",None)
        session.pop("user_id",None)

    return  redirect(url_for("index"))

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html",message = "Log in for Project1")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #if usename doesn't exists then show error
        user = db.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(:username)", {"username":username}).fetchone()
        if user is None:
            return render_template("login.html", error_message = "Sorry, username or password does not match.")
        #if user exists then check the enetered password with hash password match
        pw_hash = user["password"]
        if not bcrypt.check_password_hash(pw_hash, password):
            return render_template("login.html", error_message = "Sorry, username or password does not match.")

        session['username'] = username
        session['user_id'] = user["id"]
        return redirect(url_for('search'))
        #return render_template("search.html", message = "Welcome "+str(username)+"!")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message = "Register for Project1")
    elif request.method == "POST":
        #print("POST", file=sys.stderr)
        username = request.form.get("username")
        password = request.form.get("password")
        # if name exists show error message
        if  db.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(:username)", {"username":username}).rowcount:
            return render_template("error.html",message = "Sorry, that name already been used to signup for Project1.")
        #generate password hash
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username":username, "password":pw_hash})
        db.commit()

        return render_template("success.html",message = "Register successfully.")
