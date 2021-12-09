import firebase_admin
from firebaseConfFile import config
from firebase_admin import credentials
from firebase_admin import db
import time
import sys
import json
# Fetch the service account key JSON file contents
cred = credentials.Certificate('gopigo-f9d4f-firebase-adminsdk-bd305-0c23e9d9c4.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, config)

class Product:
    def __init__(self, productID, car, item, status):
        self.status = "ordered"
        self.car = "none"
        self.id = productID
        self.status = status

        try:
            #print(f"Adding product listener for {self.id}")
            self.productListenerThread = firebase_admin.db.reference(f'orderList/{self.id}').listen(self.productListener)

        except:
            print(f"Firebase listener failed for {self.id}")

    def productListener(self, event):
         print(f"ProductListener:\ttype: {event.event_type}\tpath: {event.path}\tdata: {event.data}")

         if(event.data=="loaded"):
             self.car.leaveItem()




class Car:
    def __init__(self, posX, posY, carID, carName, callName):
        self.position = {'x': posX, 'y': posY}
        self.status = 'standby'
        self.id = carID
        self.carName = carName
        self.callName = callName

        try:
            print(f"Adding car listener for {self.carName}")
            self.carListenerThread = firebase_admin.db.reference(f'cars/{carName}').listen(self.carListener)

        except:
            print(f"Firebase listener failed for {self.carName}")

    def carListener(self, event):
        #print(f"CarListener:\ttype: {event.event_type}\tpath: {event.path}\tdata: {event.data}")

        path = event.path
        newData = event.data
        if(path=="/status"):
            self.status = newData
        elif(path=="/position/x"):
            self.position.x = newData
        elif(path=="/position/y"):
            self.position.y = newData
        elif(path=="/position/heading"):
            self.position.heading = newData
    

    def getItem(self):
        self.status = "travel_loading"
        print(f"{self.carName} Is headed to loading bay!")
    

    def leaveItem(self):
        self.status = "travel_unloading"
        print(f"{self.carName} Is headed to unloading bay!")


    def printCarInfo(self):
        print(f"Car: {self.callName}")
        print(f"\tID{self.id}")
        print(f"\tStatus: {self.status}")
        print(f"\tPosition: {self.position}")


    


class Manager:
    def __init__(self):
        self.orders = []
        self.testList = []
        """
        self.carList = [
            {'car0': Car(0, 0, 0, 'car0', 'Niilo')},
            {'car1': Car(1, 0, 1, 'car1', 'Pate')},
            {'car2': Car(2, 0, 2, 'car2', 'NewGreatCar')}
            ]
        """
        self.carList = [
            Car(0, 0, 0, 'car0', 'Niilo'),
            Car(1, 0, 1, 'car1', 'Pate'),
            Car(2, 0, 2, 'car2', 'NewGreatCar')
            ]
        try:
           # print("Adding listener for shopping list")
            self.orderThread = firebase_admin.db.reference('orderList').listen(self.orderListener)
        except:
            print("Can't listen to orderlist")

    def orderListener(self, event):
        #print(f"OrderListener:\ttype: {event.event_type}\tpath: {event.path}\tdata: {event.data}")
        path = event.path
        newData = event.data
        if(path == "/"):
            self.listInit(newData)
        #else:
            #self.changesToOrder(path, newData)

        
    def listInit(self, newData):
        print("Creating new order list!")

        for iteration in range(len(newData)):
            #thisProduct = 'product'+iteration+1
            productID = "prod"+str(iteration)
            print(newData[productID]['gopigo'])
            prodCar = newData[productID]['gopigo']
            prodItem = newData[productID]['item']
            prodStatus = newData[productID]['progress']

            
            thisProduct = Product(productID, prodCar, prodItem, prodStatus)
            self.orders.append(thisProduct)
        
        #print(self.orders)
        #print(self.orders[0].status)

        self.assignCars()
        #self.printProductsCar()
        #for product in newData:
            #self.testList.append(product)
        #print(self.testList)
        #self.testList = newData


    def assignCars(self):
        print("Assigning cars for products")

        for item in range(len(self.orders)):
            if(self.orders[item].status == "ordered"):
                assignedCar = self.getFirstAvailableCar()
                if(assignedCar == "No available car at the moment!"):
                    print("No available car at the moment!")
                else:
                    self.orders[item].car = assignedCar
                    assignedCar.getItem()
    ##########################################################
    def printProductsCar(self):
        for item in range(len(self.orders)):
            if(self.orders[item].car != "none"):
                print(self.orders[item].car.carName)
    ##########################################################
    def getFirstAvailableCar(self):
        for car in range(len(self.carList)):
            if(self.carList[car].status=="standby"):
                return self.carList[car]
        return "No available car at the moment!"

    def changesToOrder(self, path, newData):
        print(f"order {path} changed with data {newData}")

    def addProduct(self, prodNumber, car, ):
        self.orders.append({'prodID': prodNumber, 'gopigo': car, 'status': status})
    
    def getCarStatus(self, carNumber):
        return (self.carList[carNumber]['status'])

    def changeCarStatus(self, carNumber, newStatus):
        self.carList[carNumber]['status'] = newStatus
  


try:
    carHandler = Manager()
    #ourthread = firebase_admin.db.reference('orderList').listen(listener)
    #ref = db.reference('cars')
    #cartarg_ref = ref.child('car0/target')
    #carpos_ref = ref.child('car0/position')
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:

    print('Interrupted')
    #ourthread.close()
    print("Thread closed")
    sys.exit()



"""
    Keeps track of where all cars are located and where they are going. Assigns new targets


    Pepper or mobile app notifies that customer has arrived to fetch their order.
        -Check how many orders for unloading and loading docks
            -Assign docks to the least used one
        -Check for available cars
            -Available:
                -Assign first available car for the order
                -Send the cordinates to car
            -Not available:
                -Try again in 10 seconds
    



"""