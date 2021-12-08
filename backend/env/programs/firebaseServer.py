import firebase_admin
from firebaseConfFile import config
from firebase_admin import credentials
from firebase_admin import db
import time
import sys
# Fetch the service account key JSON file contents
cred = credentials.Certificate('gopigo-f9d4f-firebase-adminsdk-bd305-0c23e9d9c4.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, config)


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

    if(len(event.path) > 4):
        topicHandler(event.path, event.data)



def topicHandler(topic, data):
    topicSplitted = topic.split("/")
    print(topicSplitted)
    productNumber = topicSplitted[1]
    #dataTopic = topicSplitted[2]
    print(f"Product {productNumber} w´With data: {data}")

    if(dataTopic == "position"):
        print("Change position")
    elif(dataTopic == "id"):
        print("new ID")
    elif(dataTopic == "name"):
        print("new Name")
    elif(dataTopic == "target"):
        print("new target")
    elif(dataTopic == "status"):
        print("new Status")


try:
    ourthread = firebase_admin.db.reference('currentorder').listen(listener)
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