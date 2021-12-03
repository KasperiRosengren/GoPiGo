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

    if(event.path.startswith("/position")):
        myX = event.data['realPosition']['x']
        myY = event.data['realPosition']['y']
        print("Updated my location!################################################")
    elif(event.path.startswith("/target")):
        print("CalculateRoute!")
        newX = event.data['realTarget']['x']
        newY = event.data['realTarget']['y']
        calculateRoute(newX, newY)

    


        


def calculateRoute(x,y):
    global myX
    global myY
    print(f"Calculating new route to: {x}, {y}")
    print(f"From: {myX}, {myY}")


carnumber= 0

number = 0

try:
    ourthread = firebase_admin.db.reference('cars/car0').listen(listener)
    ref = db.reference('cars')
    cartarg_ref = ref.child('car0/target')
    carpos_ref = ref.child('car0/position')
    while True:
        print("hi")
        number = number +1
        cartarg_ref.update({
            'realTarget': {'x': number, 'y': number}
        })
        carpos_ref.update({
            'realPosition': {'x': number+1, 'y': number+1, 'heading': 0}
        })
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print('Interrupted')
    ourthread.close()
    print("Thread closed")
    sys.exit()
