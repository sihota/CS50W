import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#create an engine with database url passed to session majer
db_engine = create_engine(os.getenv("DATABASE_URL"))

#bind db engine to session maker and create scoped session
db_session = scoped_session(sessionmaker(bind=db_engine))

def main():
    csv_file = open("flights.csv")
    reader = csv.reader(csv_file)
    for origin, destination, duration in reader:
        db_session.execute("INSERT INTO flights (origin, destination, duration) VALUES(:origin,:destination,:duration)",
                            {"origin":origin, "destination": destination, "duration": duration })
        print(f"Added flight from {origin} to {destination} lasting {duration} minutes")
    db_session.commit()

if __name__ == "__main__":
    main()
