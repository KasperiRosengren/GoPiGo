from firebase import Firebase
from firebaseConfFile import *

"""
firebase = Firebase(config)
db = firebase.database()
thisCarList = db.child("cars").get()

print("Original data from firebase: ")
print(thisCarList.val())
print("")


print("######################")
for car in thisCarList.each():
    print(f"Car: {car.key()}")
    print(f"\tID: {car.val()['id']}")
    print(f"\tName: {car.val()['name']}")
    print(f"\tPosition:")
    print(f"\t\tX: {car.val()['position']['x']}")
    print(f"\t\tY: {car.val()['position']['y']}")
    print(f"\t\tHeading: {car.val()['position']['heading']}")
    print("")
    print("##############END OF CAR#################")
    print("")

"""


def printCarInfo(car):
    print("")
    print("##############Start of car##############")
    print(f"##############{car.key()}##############")
    print("")
    print(f"Car: {car.key()}")
    print(f"\tID: {car.val()['id']}")
    print(f"\tName: {car.val()['name']}")
    print(f"\tPosition:")
    print(f"\t\tX: {car.val()['position']['x']}")
    print(f"\t\tY: {car.val()['position']['y']}")
    print(f"\t\tHeading: {car.val()['position']['heading']}")
    print("")
    print(f"##############{car.key()}##############")
    print("##############END OF CAR##############")
    print("")

def printDriveControls():
    print("Drive controls:")
    print("\tW: Drive forward")
    print("\tS: Turn 180 deg.")
    print("\tD: Turn 90 deg. to right")
    print("\tA: Turn 90 deg. to left")

def driveCar():
    chooseCar = True
    global db
    vechicle = "0"
    while chooseCar:
        print("Choose which car you want to drive (use ID):")
        thisCarList = db.child("cars").get()
        for car in thisCarList.each():
            printCarInfo(car)
        vechicle = input("Choice: ")
        try:
            driving = True
            while driving:
                printDriveControls()
                vechicle = int(vechicle)
                db.child("cars").child(f"car{vechicle}").update({"status": "Driving"})
                control = input("Control: ")
                if(control == "w" or control == "W"):
                    driveForward(carID)
                elif(control == "s" or control == "S"):
                    turn180(carID)
                elif(control == "d" or control == "D"):
                    turnR90(carID)
                elif(control == "a" or control == "A"):
                    turnL90(carID)
        except:
            print("Something went wrong with ID selection")
            continue

    


def askContinue():
    while True:
        answer = input("Do you want to continue? (Y/N)")
        if(answer == "Y" or answer == "y"):
            return True
        elif(answer == "N" or answer == "n"):
            return False
        else:
            print("Not aceptable answer")

def printMenu():
    print("Control")
    print("1: drive car")
    print("2: rename car")
    print("0: Exit")

def handleMenu():
    while True:
        printMenu()
        answer = input("Your choice: ")
        if(answer == "1"):
            driveCar()
            break
        elif(answer == "2"):
            print("Not supported yet")
            #changeCarName()
            break
        elif(answer == "0"):
            print("Exit")
            break
        
firebase = Firebase(config)
db = firebase.database()
number = 0
thisCar = db.child("cars").child(f"car{number}").get()
#print(thisCarList)

for info in thisCar.each():
    print(f"{info.key()}")
    #print(info.val()['position']['x'])

orgX = thisCar.val()['position']['x']
orgY = thisCar.val()['position']['y']
orgHeading = thisCar.val()['position']['heading']
newX = orgX + 1
db.child("cars").child(f"car{number}").update({"position": {'x': newX, 'y': orgY, 'heading': orgHeading}})
"""
try:
    
    firebase = Firebase(config)
    db = firebase.database()
    keepLooping = True
    while keepLooping:
        thisCarList = db.child("cars").get()
        for car in thisCarList.each():
            printCarInfo(car)
        
        handleMenu()
        keepLooping = askContinue()
        

except:
    print("Something went oopsie!")
"""