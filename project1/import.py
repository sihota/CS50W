import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#check for an environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL environment variable is not set.")

#create an engine using environment variable
engine = create_engine(os.getenv("DATABASE_URL"))

#setup a database session object
db = scoped_session(sessionmaker(bind=engine))


def main():
    #open books.csv in reading mode
    f = open("books.csv")
    #read csv file data
    books = csv.reader(f)

    # This skips the first row of the CSV file.
    # csvreader.next() also works in Python 2.
    next(books)

    #read each row of csv file and insert to database
    for isbn,title,author,year in books:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn,:title,:author,:year)",
                    {"isbn":isbn,"title":title,"author":author,"year":year})
        print(f"Added book {isbn}, {title}, {author}, {year}")
    #save the changes to database
    db.commit()

if __name__ == "__main__":
    main()
