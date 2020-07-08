class Flight:
    #declare counter static  or class variable
    counter = 1

    def __init__(self,origin,destination,duration):

        #keep track of id number
        self.id = Flight.counter
        Flight.counter += 1

        #keep track of passengers
        self.passengers = []

        #details about flight
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def printinfo(self):
        print(f"Flight id:{self.id}")
        print(f"Flight origin:{self.origin}")
        print(f"Flight destination:{self.destination}")
        print(f"Flight duration:{self.duration}")

        print()
        print("passengers")
        for passenger in self.passengers:
            print(f"{passenger.name}")

    def add_passenger(self,p):
        self.passengers.append(p)
        p.flight_id = self.id

    def delay(self,amount):
        self.duration += amount

class Passenger:

    def __init__(self,name):
        self.name = name

def main():

    #create a flight object
    flight1 = Flight(origin = "New York", destination = "Paris", duration=540)

    #create passenger
    passenger1 = Passenger(name="Alice")
    passenger2 = Passenger(name="Bob")

    #add passengers to flight
    flight1.add_passenger(passenger1)
    flight1.add_passenger(passenger2)

    #print the flight details using function
    flight1.printinfo()

    #accessing class variable outside class
    print(f"\nNext Flight Id:{Flight.counter}")
    print()
    print("--------------------------")

    #create a flight object
    flight2 = Flight(origin = "Shanghai", destination = "Tokyo", duration=340)

    #create passenger
    passenger1 = Passenger(name="Chalie")
    passenger2 = Passenger(name="Adam")
    passenger3 = Passenger(name="Hob")

    #add passengers to flight
    flight2.add_passenger(passenger1)
    flight2.add_passenger(passenger2)
    flight2.add_passenger(passenger3)

    #print the flight details using function
    flight2.printinfo()


if __name__ == "__main__":
    main()
