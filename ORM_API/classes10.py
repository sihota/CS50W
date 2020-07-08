class Flight:
    
    def __init__(self,origin,destination,duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def printinfo(self):
        print(f"Flight origin:{self.origin}")
        print(f"Flight destination:{self.destination}")
        print(f"Flight duration:{self.duration}")

def main():
    #create a flight object
    flight = Flight(origin = "New York", destination = "Paris", duration=540)
    #change the variable value
    flight.duration += 10

    #print the flight details using function
    flight.printinfo()

if __name__ == "__main__":
    main()
