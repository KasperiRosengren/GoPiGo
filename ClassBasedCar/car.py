from navigationHandler import NavigationHandler
import easygopigo3 as easy
from di_sensors.easy_line_follower import EasyLineFollower
import time
import random


class Car(NavigationHandler):
    def __init__(self, heading, positionX, positionY):
        NavigationHandler.__init__(self, heading, positionX, positionY)
        print("I have been created")