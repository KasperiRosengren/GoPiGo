from car import Car


def Main():
    auto = Car()
    while True:
        x = random.randint(0, 4)
        y = random.randint(0, 7)
        auto.destinationX = x
        auto.destinationY = y
        print("Destination: "+str(x)+"."+str(y))
        NavigateToLocation()
        print("IMHERE")
        time.sleep(1)
        

Main()