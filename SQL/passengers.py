import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db_engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=db_engine))

def main():
    #list all the flights
    flights = db_session.execute("SELECT id, origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f"Flight ID: {flight.id}  {flight.origin} to {flight.destination} , {flight.duration} minutes.")

    #select the flight from list
    flight_id = int(input("\n Flight id: "))

    #get flight info by entered ID
    flight = db_session.execute("SELECT id FROM flights where id = :id",{"id":flight_id}).fetchone()
    if flight is None:
        print(f"\nError: No flight exists.")
        return

    #if exits list all the flight passengers of that flight
    passengers = db_session.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                                    {"flight_id": flight_id}).fetchall()

    print(f"\nPassengers:")
    for passenger in passengers:
        print(f"{passenger.name}")

    if len(passengers) == 0:
        print(f"\nNo passengers.")

if __name__ == "__main__":
    main()
