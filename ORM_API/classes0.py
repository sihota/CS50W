class Flight:
    def __init__(self,origin,destination,duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration

def main():
    #create a flight object
    flight = Flight(origin = "New York", destination = "Paris", duration=540)
    #change the variable value
    flight.duration += 10

    #print the flight details
    print(flight.origin)
    print(flight.destination)
    print(flight.duration)

if __name__ == "__main__":
    main()    
