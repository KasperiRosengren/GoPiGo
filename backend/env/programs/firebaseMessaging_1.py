import firebase_admin
from firebaseConfFile import config
from firebase_admin import credentials, db, messaging, auth
#from firebase_admin import db
import time
import sys
# Fetch the service account key JSON file contents
cred = credentials.Certificate('gopigo-f9d4f-firebase-adminsdk-bd305-0c23e9d9c4.json')
# Initialize the app with a service account, granting admin privileges
fireApp = firebase_admin.initialize_app(cred, config)

"""
def listener(event):
    print("Event type")
    print(event.event_type)  # can be 'put' or 'patch'
    print("Event path")
    print(event.path)  # relative to the reference, it seems
    print("Event data")
    print(event.data)  # new data at /reference/event.path. None if deleted

    

car0Listener = firebase_admin.db.reference('cars/car0').listen(listener)
ref = db.reference('cars')
cartarg_ref = ref.child('car0/target')
"""

testClient = firebase_admin.auth.Client(fireApp)
testClient.create_custom_token(uid="wawaaa")


print(cred.get_access_token())
myToken=cred.get_access_token()
myTokenAccess = myToken[:1]
print(myTokenAccess[0])

tokens = [myTokenAccess[0]]

TestMessenger = firebase_admin.messaging.subscribe_to_topic(tokens, 'testTopic', app=fireApp)

testMessage = firebase_admin.messaging.Message(data={'message': 'ThisIsMyMessage'}, topic='testTopic')

print(TestMessenger)
print(testMessage)

while True:
    print("Hi")
    firebase_admin.messaging.Message(data={'message': 'ThisIsMyMessage'}, topic='testTopic')
    time.sleep(1)