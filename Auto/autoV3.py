import easygopigo3 as easy
from di_sensors.easy_line_follower import EasyLineFollower
import time
import random
import paho.mqtt.client as mqtt

gpg = easy.EasyGoPiGo3()
lf = EasyLineFollower()
dist_sens = gpg.init_distance_sensor()
serv=gpg.init_servo()

#gpg.set_speed(250)

setpoint = 0.5
integralArea = 0.0
previousError = 0.0
motorBaseSpeed = 300
loopTime = 1.0 / 100

Kp = 4200.0 # a value suitable for this component
Ki = 0.0 # ditto
Kd = 2500.0 # ditto as above

NeedToNavigate = True
myLocationX = 4
myLocationY = 8
destinationX = 0
destinationY = 3
myHeading = 270
NeedToChangeX = False
NeedToChangeY = False
newGrid = True

ServoPosRight = 160
ServoPosLeft = 40
ServoPosCenter = 100

MinDistance = 150
AllWhiteCounter = 0


maze = [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("gopigo/car1/#")



def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload)
    print("Topic: "+topic)
    print("Message: "+message)

    if(topic=="gopigo/car1/command/go"):
        print("go somewhere topic")
        tempMes = message.split(",")
        coordinateX = tempMes[0]
        coordinateY = tempMes[1]

        calculateRoute(coordinateX, coordinateY)

def AlterHeading(degrees):
    global myHeading
    tempHeading = myHeading + degrees
    if(tempHeading >= 360):
        myHeading = tempHeading - 360
    elif(tempHeading < 0):
        myHeading = tempHeading + 360
    else:
        myHeading = tempHeading

def DecideTurn(direction):
    global myHeading
    if(direction == "right"):
        if(myHeading==90):
            pass
        elif(myHeading==180):
            TurnLeft()
        elif(myHeading==270):
            Turn180()
        elif(myHeading==0):
            TurnRight()

    elif(direction == "left"):
        if(myHeading==90):
            Turn180()
        elif(myHeading==180):
            TurnRight()
        elif(myHeading==270):
            pass
        elif(myHeading==0):
            TurnLeft()


    elif(direction == "up"):
        if(myHeading==90):
            TurnLeft()
        elif(myHeading==180):
            Turn180()
        elif(myHeading==270):
            TurnRight()
        elif(myHeading==0):
            pass


    elif(direction == "down"):
        if(myHeading==90):
            TurnRight
        elif(myHeading==180):
            pass
        elif(myHeading==270):
            TurnLeft()
        elif(myHeading==0):
            Turn180()

    time.sleep(0.3)



def GOForward(values):
    global AllWhiteCounter
    if(IsItSafeToGoForward()==True):
        #values = lf.position_01()
        #print(str(values[0])+" "+str(values[1])+" "+str(values[2])+" "+str(values[3])+" "+str(values[4]))
        #print(" "+str(values[0])+" "+str(values[1])+" "+str(values[2])+" "+str(values[3])+" "+str(values[4]))
        if(values[1]==0 or values[2]==0 or values[3]==0):
            if(values[1]==0 and values[2]==1):
                gpg.steer(30, 100)
            elif(values[3]==0 and values[2]==1):
                gpg.steer(100, 30)
            else:
                gpg.forward()
            AllWhiteCounter=0
            #print("Driving forward")
        elif(values[4]==0 and values[3]==1):
            gpg.right()
            AllWhiteCounter=0
            
            #print("Driving right")
        elif(values[0]==0 and values[1]==1):
            gpg.left()
            AllWhiteCounter=0
            
        elif(values[0]==1 and values[1]==1 and values[2]==1 and values[3]==1 and values[4]==1):
            AllWhiteCounter += 1
            if(AllWhiteCounter <= 40):
                gpg.steer(100, 40)
            else:
                print("Hjalp, Im lost :( ")
                while(True):
                    gpg.stop()
        else:
            AllWhiteCounter=0
    else:
        gpg.stop()
        
    #time.sleep(0.02)
            
            
def TurnRight():
    gpg.turn_degrees(95)
    AlterHeading(90)
    
def TurnLeft():
    gpg.turn_degrees(-95)
    AlterHeading(-90)

def Turn180():
    gpg.turn_degrees(193)
    AlterHeading(180)


def IsItSafeToGoForward():
    global MinDistance
    #global ServoPosCenter
    #serv.rotate_servo(ServoPosCenter)
    return True
    
    #dist = dist_sens.read_mm()
    #if(dist <= MinDistance):
        #return False
    #else:
        #return True
    

            
def IsItSafeToCross():
    global ServoPosRight
    global ServoPosLeft
    global ServoPosCenter
    global MinDistance
    
    dist = dist_sens.read_mm()
    
    serv.rotate_servo(ServoPosLeft)
    time.sleep(0.5)
    dist = dist_sens.read_mm()
    if(dist <= MinDistance):
        print("Obstacle Left")
        serv.rotate_servo(ServoPosCenter)
        return False
    
    serv.rotate_servo(ServoPosCenter)
    time.sleep(0.5)
    dist = dist_sens.read_mm()
    if(dist <= MinDistance):
        print("Obstacle Center")
        serv.rotate_servo(ServoPosCenter)
        return False
    
    serv.rotate_servo(ServoPosRight)
    time.sleep(0.5)
    dist = dist_sens.read_mm()
    if(dist <= MinDistance):
        print("Obstacle Right")
        serv.rotate_servo(ServoPosCenter)
        return False
    
    serv.rotate_servo(ServoPosCenter)
    return True


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)     


def DriveToNextGrid():
    drive = True
    while(drive):
        linevalues = lf.position_01()
        print(str(linevalues[0])+" "+str(linevalues[1])+" "+str(linevalues[2])+" "+str(linevalues[3])+" "+str(linevalues[4]))
        if(linevalues[3] + linevalues[4] + linevalues[2] ==0 or linevalues[0] + linevalues[1] + linevalues[2] ==0):
            gpg.drive_cm(5)
            gpg.stop()
            print("new location: "+str(myLocationX)+"."+str(myLocationY))
            drive = False
        else:
            GOForward(linevalues)


def  calculateRoute(coordinateX, coordinateY):
    global maze
    global myLocationX
    global myLocationY
    global destinationX
    global destinationY

    start = (myLocationY, myLocationX) 
    end = (coordinateY, coordinateX)

    path = astar(maze, start, end)

    while(len(path) > 0):
        destinationX = path[0][1]
        destinationY = path[0][0]

        if(destinationX != myLocationX):
            if(destinationX > myLocationX):
                #needs to go right
                DecideTurn("right")
            elif(destinationX < myLocationX):
                #needs to go left
                DecideTurn("left")
        elif(destinationY != myLocationY):
            if(destinationY > myLocationY):
                #needs to go up
                DecideTurn("up")
            elif(destinationY < myLocationY):
                #needs to go down
                DecideTurn("down")

        del path[0]
        print("next stop")
    
def Main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.43.195", 1883, 60)
    client.loop_forever()

Main()