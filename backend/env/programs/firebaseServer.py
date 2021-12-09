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
        print("Event type")
        print(event.event_type)  # can be 'put' or 'patch'
        print("Event path")
        print(event.path)  # relative to the reference, it seems
        print("Event data")
        print(event.data)  # new data at /reference/event.path. None if deleted

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


    def printCarInfo(self):
        print(f"Car: {self.callName}")
        print(f"\tID{self.id}")
        print(f"\tStatus: {self.status}")
        print(f"\tPosition: {self.position}")


    


class Manager:
    def __init__(self):
        self.orders = []
        self.testList = []
        self.carList = [
            {'car0': Car(0, 0, 0, 'car0', 'Niilo')},
            {'car1': Car(1, 0, 1, 'car1', 'Pate')},
            {'car2': Car(2, 0, 2, 'car2', 'NewGreatCar')},
            ]
        #self.car0 = Car(0, 0, 0, 'car0', 'Pate')
        #self.car0 = {'status': 'warehouse', 'coordinates': {'x': 0, 'y': 0}}
        #self.car1 = {'status': 'warehouse', 'coordinates': {'x': 1, 'y': 0}}
        """
        self.carList = [
            {'car0': {'status': 'warehouse', 'coordinates': {'x': 0, 'y': 0}}},
            {'car1': {'status': 'warehouse', 'coordinates': {'x': 1, 'y': 0}}},
            {'car2': {'status': 'warehouse', 'coordinates': {'x': 2, 'y': 0}}}
            ]
        """
        try:
            print("Adding listener for shopping list")
            self.orderThread = firebase_admin.db.reference('orderList').listen(self.orderListener)
        except:
            print("Can't listen to orderlist")

        print(self.testList)

    def orderListener(self, event):
        print(f"OrderListener:\ttype: {event.type}\t")
        print("Event type")
        print(event.event_type)  # can be 'put' or 'patch'
        print("Event path")
        print(event.path)  # relative to the reference, it seems
        print("Event data")
        print(event.data)  # new data at /reference/event.path. None if deleted

        path = event.path
        newData = event.data
        if(path == "/"):
            self.listInit(newData)
        else:
            self.changesToOrder(path, newData)

        
    def listInit(self, newData):
        print("Creating new order list!")
        self.testList = newData

    def changesToOrder(self, path, newData):
        print(f"order {path} changed with data {newData}")

        

    def addProduct(self, prodNumber, car, ):
        self.orders.append({'prodID': prodNumber, 'gopigo': car, 'status': status})
    
    def getCarStatus(self, carNumber):
        return (self.carList[carNumber]['status'])

    def changeCarStatus(self, carNumber, newStatus):
        self.carList[carNumber]['status'] = newStatus
    

myX = 0
myY = 0

def listener(event):
    global myX
    global myY
    print("Event type")
    print(event.event_type)  # can be 'put' or 'patch'
    print("Event path")
    print(event.path)  # relative to the reference, it seems
    print("Event data")
    print(event.data)  # new data at /reference/event.path. None if deleted

    if(event.path == "/"):
        topicHandler(event.path, event.data)
    else:
        print("Something else!")



def topicHandler(topic, data):
    topicSplitted = topic.split("/")
    print(topicSplitted)
    productNumber = topicSplitted[1]
    #dataTopic = topicSplitted[2]
    print(f"New order list: {data}")
    print(f"Length:{len(data)}")
    #print(data['product1']['item'])

    for iteration in range(len(data)):
        #thisProduct = 'product'+iteration+1
        #prodID = iteration+1
        print(data['prod'+str(iteration)])
        
    #pleaseerror
    """
    print("############################")
    for product in data:
        print(f"{product}:")
        #print(f"\tDesignated car: {product.gopigo}")
        #print(f"\tItem: {product.item}")
        #print(f"\tProgress: {product.status}")
    for product in res:
        print(f"{product}:")

    print("###########################")
    """
    


try:
    carHandler = Manager()
    ourthread = firebase_admin.db.reference('orderList').listen(listener)
    #ref = db.reference('cars')
    #cartarg_ref = ref.child('car0/target')
    #carpos_ref = ref.child('car0/position')
    while True:
        time.sleep(0.1)
        
except KeyboardInterrupt:

    print('Interrupted')
    ourthread.close()
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