import firebase_admin
#from firebaseConfFile import config
#from firebaseConfFile import confSJON

from firebaseDemoConf import config
from firebaseDemoConf import confSJON

from firebase_admin import credentials
from firebase_admin import db
import time
import sys
import json
import paho.mqtt.client as mqtt
# Fetch the service account key JSON file contents
cred = credentials.Certificate(confSJON)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, config)

MQTT_BROKER_IP = "192.168.0.102"

class Product:
    def __init__(self, productID, car, item, status):
        self.status = "ordered"
        self.car = "none"
        self.id = productID
        self.status = status

        #client.subscribe("gopigo/car2/#")

        try:
            #print(f"Adding product listener for {self.id}")
            self.productListenerThread = firebase_admin.db.reference(f'orderList/{self.id}').listen(self.productListener)

        except:
            print(f"Firebase listener failed for {self.id}")

    def productListener(self, event):
        print(f"ProductListener:\ttype: {event.event_type}\tpath: {event.path}\tdata: {event.data}")
        try:
            if(event.path == "/status"):
                print(f"{self.id} status changed")
                if(event.data == "loaded"):
                    print(f"{self.id} was loaded on {self.car.carName}")
                    self.car.fetchItem()
                elif(event.data == "unloaded"):
                    print(f"{self.id} was unloaded from {self.car.carName}")
                    self.car.deliverItem()
            elif(event.path == "/"):
                print(f"{self.id} status changed")
                if(event.data=="None" or event.data == None):
                    print(f"{self.id} was unloaded from {self.car.carName}")
                    self.car.deliverItem()
                elif(event.data['status'] == "loaded"):
                    print(f"{self.id} was loaded on {self.car.carName}")
                    self.car.fetchItem()
                elif(event.data['status'] == "unloaded"):
                    print(f"{self.id} was unloaded from {self.car.carName}")
                    self.car.deliverItem()
        except Exception as e:
            print("Product listener failed")
            print(e)





class Car:
    def __init__(self, posX, posY, carID, carName, callName, carManager):
        global MQTT_BROKER_IP
        self.position = {'x': posX, 'y': posY}
        self.status = 'standby'
        self.id = carID
        self.carName = carName
        self.callName = callName
        self.carManager = carManager
        self.deliveryPackage = "none"
        

        try:
            self.client = mqtt.Client(client_id=f"gopigo{self.carName}")
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(MQTT_BROKER_IP, 1883, 60)
            self.client.loop_start()
        except Exception as e:
            print("Car MQTT connection failed")
            print(e)

        try:
            print(f"Adding car listener for {self.carName}")
            self.carListenerThread = firebase_admin.db.reference(f'cars/{carName}').listen(self.carListener)

        except:
            print(f"Firebase listener failed for {self.carName}")

    def carListener(self, event):
        print(f"CarListener:\ttype: {event.event_type}\tpath: {event.path}\tdata: {event.data}")

        path = event.path
        newData = event.data
        try:
            if(path=="/status"):
                if(newData == "loaded"):
                    self.leaveItem()
                elif(newData == "unloaded"):
                    self.leaveUnload()
                elif(newData == "standby"):
                    print("Need to go to pit")
                    self.goToPit()
            elif(path=="/" and event.event_type =="patch"):
                if(newData['status']=="standby"):
                    print("NeedToGoPit")
                    self.goToPit()
                #self.status = newData
            elif(path=="/position/x"):
                self.position.x = newData
            elif(path=="/position/y"):
                self.position.y = newData
            elif(path=="/position/heading"):
                self.position.heading = newData
        except Exception as e:
            print("listener data failed!")
            print(e)
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        cartopic = f"gopigo/{self.carName}/#"

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(cartopic)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        message = str(msg.payload)
        #print("Topic: "+topic)
        #print("Message: "+message)
        print(f"MQTT message, Topic: {topic}, message: {message}")

        if(topic == f"gopigo/{self.carName}/status"):
            if(message == "b'loading'"):
                print(f"{self.carName} is ready to receive package")
                firebase_admin.db.reference(f"cars/{self.carName}").update({'status': 'loading'})
                firebase_admin.db.reference(f"orderList/{self.deliveryPackage.id}").update({'status': 'loading'})
            elif(message == "b'unloading'"):
                print(f"{self.carName} is ready to unload")
                firebase_admin.db.reference(f"cars/{self.carName}").update({'status': 'unloading'})
                firebase_admin.db.reference(f"orderList/{self.deliveryPackage.id}").update({'status': 'unloading'})
            elif(message == "b'leftunloading'"):
                print(f"{self.carName} has left unloading")
                if(self.carManager.isAnyOrderedPackage(self)==False):
                    self.status = "standby"
                    firebase_admin.db.reference(f"cars/{self.carName}").update({'status': 'standby'})
    
    def getNewPackage(self, package):
        self.deliveryPackage = package
        firebase_admin.db.reference(f"orderList/{self.deliveryPackage.id}").update({'gopigo': self.carName})
        print(f"{self.carName} New package {self.deliveryPackage}")

    def goToPit(self):
        print(f"{self.carName} Is going back to pit")
        self.client.publish(f"gopigo/{self.carName}/command/delivery", "pit")

    def getItem(self):
        self.status = "travel_loading"
        self.deliveryPackage.status = "assigned"
        firebase_admin.db.reference(f"orderList/{self.deliveryPackage.id}").update({'status': 'assigned'})
        print(f"{self.carName} Is headed to loading bay!")
        self.client.publish(f"gopigo/{self.carName}/command/delivery", "load")


    def fetchItem(self):
        firebase_admin.db.reference(f"cars/{self.carName}").update({'status': 'loaded'})
        self.leaveItem()

    def deliverItem(self):
        firebase_admin.db.reference(f"cars/{self.carName}").update({'status': 'unloaded'})
        self.leaveUnload()



    def leaveItem(self):
        self.status = "travel_unloading"
        print(f"{self.carName} Is headed to unloading bay!")
        self.client.publish(f"gopigo/{self.carName}/command/delivery", "unload")

    def leaveUnload(self):
        self.status = "leave_unloading"
        print(f"{self.carName} Is leaving unload")
        self.client.publish(f"gopigo/{self.carName}/command/delivery", "leaveunload")


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
        """
        self.carList = [
            Car(0, 0, 0, 'car0', 'Niilo', self),
            Car(1, 0, 1, 'car1', 'Pate', self),
            Car(2, 0, 2, 'car2', 'Petri', self),
            Car(3, 0, 3, 'car3', 'Pekka', self)
            ]
        """
        self.carList = [Car(0, 0, 0, 'car0', 'Niilo', self)]
        try:
           # print("Adding listener for shopping list")
            self.orderThread = firebase_admin.db.reference('orderList').listen(self.orderListener)
        except:
            print("Can't listen to orderlist")

    def orderListener(self, event):
        print(f"OrderListener:\ttype: {event.event_type}\tpath: {event.path}\tdata: {event.data}")
        path = event.path
        newData = event.data
        if(path == "/" and event.data != None):
            if(event.data != "0"):
                self.listInit(newData)
        elif(path == "/" or event.data != None):
            if(event.data == "0" or event.data == None):
                self.orders = []
        else:
            try:
                print("New Single product")
                productName = path[1:]
                self.AddNewProduct(productName, newData)
            except Exception as e:
                print(e)
        #else:
            #self.changesToOrder(path, newData)

    def AddNewProduct(self, productID, data):
        prodCar = data['gopigo']
        prodItem = data['item']
        prodStatus = data['status']
        thisProduct = Product(productID, prodCar, prodItem, prodStatus)
        self.orders.append(thisProduct)
        self.assignCars()

    def listInit(self, newData):
        print("Creating new order list!")

        for iteration in range(len(newData)):
            #thisProduct = 'product'+iteration+1
            productID = "product"+str(iteration)
            print(newData[productID]['gopigo'])
            prodCar = newData[productID]['gopigo']
            prodItem = newData[productID]['item']
            prodStatus = newData[productID]['status']

            
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
                    print("#########################################")
                    print(self.orders[item])
                    assignedCar.getNewPackage(self.orders[item])
                    assignedCar.getItem()
                    time.sleep(3)
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

    def isAnyOrderedPackage(self, thisCar):
        for item in range(len(self.orders)):
            if(self.orders[item].status == "ordered"):
                self.orders[item].car = thisCar
                thisCar.getNewPackage(self.orders[item])
                thisCar.getItem()
                return True
        print("No undelivered packages!")
        return False

    def changesToOrder(self, path, newData):
        print(f"order {path} changed with data {newData}")

    def addProduct(self, prodNumber, car, ):
        self.orders.append({'prodID': prodNumber, 'gopigo': car, 'status': status})
    
    def getCarStatus(self, carNumber):
        return (self.carList[carNumber]['status'])

    def changeCarStatus(self, carNumber, newStatus):
        self.carList[carNumber]['status'] = newStatus
  


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("gopigo/car2/#")



def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload)
    print("Topic: "+topic)
    print("Message: "+message)
    """
    if(topic=="gopigo/car2/command/go"):
        print("go somewhere topic")
        tempMes = message.split(",")
        coordinateX = tempMes[0]
        coordinateX = coordinateX[2:]
        coordinateY = tempMes[1]
        coordinateY = coordinateY[:-1]

        calculateRoute(int(coordinateX), int(coordinateY))
    """



try:
    print("#################################")
    print("#################################")
    print("#################################")
    print("#################################")
    print("#################################")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.0.102", 1883, 60)
    carHandler = Manager()
    client.loop_start()
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