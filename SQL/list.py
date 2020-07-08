import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
#export DATABASE_URL = "postgres+psycopg2://postgres:root123@localhost:5432/postgres"
#https://docs.sqlalchemy.org/en/13/core/engines.html

db_engine = create_engine(os.getenv("DATABASE_URL"))

#https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session
#https://docs.sqlalchemy.org/en/13/orm/contextual.html?highlight=scoped_session#sqlalchemy.orm.scoping.scoped_session
db_session = scoped_session(sessionmaker(bind=db_engine))

def main():
    flights = db_session.execute("SELECT origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print (f"{flight.origin} to {flight.destination} in {flight.duration} minutes")

if __name__ == "__main__":
    main()
