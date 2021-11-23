import easygopigo3 as easy
from di_sensors.easy_line_follower import EasyLineFollower
import time
import random

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

def NeedToChangeX():
    global myLocationX
    global myLocationY
    global destinationX
    global destinationY
    global myHeading
    needToChangeX = True
    while needToChangeX:
            if(IsItSafeToCross()==False):
                print("Seina perkele")
                while(True):
                    time.sleep(1)
            if(destinationX > myLocationX):
                #We need to increase X => go right on grid
                if(myHeading == 90):
                    needToDrive = True
                    while(needToDrive):
                        linevalues = lf.position_01()
                        print(str(linevalues[0])+" "+str(linevalues[1])+" "+str(linevalues[2])+" "+str(linevalues[3])+" "+str(linevalues[4]))
                        #GOForward(linevalues)
                        
                        time.sleep(0.01)
                        if(linevalues[3] + linevalues[4] + linevalues[2] ==0 or linevalues[0] + linevalues[1] + linevalues[2] ==0):
                        #if(linevalues[3] + linevalues[4]==0 or linevalues[0] + linevalues[1] ==0):
                            gpg.stop()
                            gpg.drive_cm(5)
                            
                            print("Grid forward on X")
                            myLocationX = myLocationX + 1
                            print("new location: "+str(myLocationX)+"."+str(myLocationY))
                            gpg.open_left_eye()
                            time.sleep(0.1)
                            gpg.close_left_eye()
                            if(myLocationX == destinationX):
                                print("X is correct")
                                gpg.stop()
                                needToChangeX = False
                                needToDrive = False
                            else:
                                if(IsItSafeToCross()==False):
                                    print("Seina perkele")
                                    while(True):
                                        time.sleep(1)
                        else:
                            GOForward(linevalues)
                            
                else:
                    DecideTurn("right")
                    
            
            elif(destinationX < myLocationX):
                #we need to decrease X => go left on grid
                if(myHeading == 270):
                    needToDrive = True
                    while(needToDrive):
                        linevalues = lf.position_01()
                        print(str(linevalues[0])+" "+str(linevalues[1])+" "+str(linevalues[2])+" "+str(linevalues[3])+" "+str(linevalues[4]))
                        #GOForward(linevalues)
                        if(linevalues[3] + linevalues[4] + linevalues[2] ==0 or linevalues[0] + linevalues[1] + linevalues[2] ==0):
                        #if(linevalues[3] + linevalues[4]==0 or linevalues[0] + linevalues[1] ==0):
                            gpg.stop()
                            gpg.drive_cm(5)
                            print("Grid backward on X")
                            myLocationX = myLocationX - 1
                            print("new location: "+str(myLocationX)+"."+str(myLocationY))
                            gpg.open_left_eye()
                            time.sleep(0.1)
                            gpg.close_left_eye()
                            if(myLocationX == destinationX):
                                print("X is correct")
                                gpg.stop()
                                needToChangeX=False
                                needToDrive = False
                            else:
                                if(IsItSafeToCross()==False):
                                    print("Seina perkele")
                                    while(True):
                                        time.sleep(1)
                        else:
                            GOForward(linevalues)
                
                else:
                    DecideTurn("left")




def NeedToChangeY():
    global myLocationX
    global myLocationY
    global destinationX
    global destinationY
    global myHeading
    needToChangeY = True
    while needToChangeY:
        if(IsItSafeToCross()==False):
            print("Seina perkele")
            while(True):
                time.sleep(1)
        if(destinationY > myLocationY):
            #We need to increase Y => go up on grid
            if(myHeading == 0):
                needToDrive = True
                while(needToDrive):
                    linevalues = lf.position_01()
                    print(str(linevalues[0])+" "+str(linevalues[1])+" "+str(linevalues[2])+" "+str(linevalues[3])+" "+str(linevalues[4]))
                    #GOForward(linevalues)
                    if(linevalues[3] + linevalues[4] + linevalues[2] ==0 or linevalues[0] + linevalues[1] + linevalues[2] ==0):
                    #if(linevalues[3] + linevalues[4]==0 or linevalues[0] + linevalues[1] ==0 or linevalues[1] + linevalues[2] + linevalues[3] ==0 ):
                        gpg.stop()
                        gpg.drive_cm(5)
                        print("Grid forward on Y")
                        myLocationY = myLocationY + 1
                        print("new location: "+str(myLocationX)+"."+str(myLocationY))
                        gpg.open_left_eye()
                        time.sleep(0.1)
                        gpg.close_left_eye()
                        if(myLocationY == destinationY):
                            print("Y is correct")
                            gpg.stop()
                            needToChangeY = False
                            needToDrive = False
                        else:
                            if(IsItSafeToCross()==False):
                                print("Seina perkele")
                                while(True):
                                    time.sleep(1)
                    else:
                        GOForward(linevalues)
                        
            else:
                DecideTurn("up")
                
        
        elif(destinationY < myLocationY):
            #we need to decrease Y => Go down on grid
            if(myHeading == 180):
                #print("Drive forward")
                needToDrive = True
                while(needToDrive):
                    linevalues = lf.position_01()
                    print(str(linevalues[0])+" "+str(linevalues[1])+" "+str(linevalues[2])+" "+str(linevalues[3])+" "+str(linevalues[4]))
                    #GOForward(linevalues)

                    if(linevalues[3] + linevalues[4] + linevalues[2] ==0 or linevalues[0] + linevalues[1] + linevalues[2] ==0):
                    #if(linevalues[3] + linevalues[4]==0 or linevalues[0] + linevalues[1] ==0):
                        #newGrid = False
                        gpg.stop()
                        gpg.drive_cm(5)
                        print("Grid backward on Y")
                        myLocationY = myLocationY - 1
                        print("new location: "+str(myLocationX)+"."+str(myLocationY))
                        gpg.open_left_eye()
                        time.sleep(0.1)
                        gpg.close_left_eye()
                        if(myLocationY == destinationY):
                            print("Y is correct")
                            gpg.stop()
                            needToChangeY = False
                            needToDrive = False
                        else:
                            if(IsItSafeToCross()==False):
                                print("Seina perkele")
                                while(True):
                                    time.sleep(1)
                    else:
                        GOForward(linevalues)
            
            else:
                DecideTurn("down")


def NavigateToLocation():
    NeedToNavigate=True
    while NeedToNavigate:
        if(destinationX != myLocationX):
            NeedToChangeX()
        elif(destinationY != myLocationY):
            NeedToChangeY()
        else:
            NeedToNavigate = False
           

    
def Main():
    global destinationX
    global destinationY
    
    while True:
        x = random.randint(0, 4)
        y = random.randint(0, 8)
        destinationX = x
        destinationY = y
        print("Destination: "+str(x)+"."+str(y))
        NavigateToLocation()
        print("IMHERE")
        time.sleep(1)
        

Main()