class MovementController():
    def __init__(self):
        self.servoPosRight = 160
        self.servoPosLeft = 40
        self.servoPosCenter = 100
        self.minDistance = 10
        print("Ready to move")

    def IsItSafeToCross(self):
        #
        #Used to determine if the path from current grid position is clear to the next.
        #


        #First we need to move the servo to check front left
        serv.rotate_servo(ServoPosLeft)
        #Sleep is needed so the servo can fully turn before we measure distance
        time.sleep(0.5)
        #Measure the distance from the distance sensor and store it in a variable
        dist = dist_sens.read_mm()
        #Checks whether the distance to next obstacle is smaller than the pre defined minimum distance
        #Returns False to method caller since it is not safe to drive to next grid position
        #Also returns the servo back to center front position
        if(dist <= self.minDistance):
            print("Obstacle Left")
            serv.rotate_servo(self.servoPosCenter)
            return False
        
        #Same as first, but for center front
        serv.rotate_servo(self.servoPosCenter)
        time.sleep(0.5)
        dist = dist_sens.read_mm()
        if(dist <= self.minDistance):
            print("Obstacle Center")
            serv.rotate_servo(self.servoPosCenter)
            return False
        
        #Same as first, but we chenck right front
        serv.rotate_servo(self.servoPosRight)
        time.sleep(0.5)
        dist = dist_sens.read_mm()
        if(dist <= self.minDistance):
            print("Obstacle Right")
            serv.rotate_servo(self.servoPosCenter)
            return False
        
        #If all three were clear, then we can return True, since it is safe to drive to the next location
        #We also need to turn the servo back to center front decision.
        serv.rotate_servo(self.servoPosCenter)
        return True

    def IsItSafeToGoForward(self):
        #
        # Used to check whether it is safe to continue driving forward
        #

        #Servo should always be already in center position, so no need to turn it
        #Measure distance from Distance sensor and store it in a variable
        dist = dist_sens.read_mm()
        #Check if the distance is smaller than the pre defined minimum distance variable
        #If it is smaller, return False to caller since it is not safe, and True if it is greater and safe
        if(dist <= self.minDistance):
            return False
        else:
            return True


    def GoForward(self):
        self.allWhiteCounter
    if(IsItSafeToGoForward()==True):
        values = lf.position_01()
        print(str(values[0])+" "+str(values[1])+" "+str(values[2])+" "+str(values[3])+" "+str(values[4]))
        #print(" "+str(values[0])+" "+str(values[1])+" "+str(values[2])+" "+str(values[3])+" "+str(values[4]))
        if(values[1]==0 or values[2]==0 or values[3]==0):
            if(values[1]==0 and values[2]==1):
                gpg.steer(30, 100)
            elif(values[3]==0 and values[2]==1):
                gpg.steer(100, 30)
            else:
                gpg.forward()
            self.allWhiteCounter=0
            #print("Driving forward")
        elif(values[4]==0 and values[3]==1):
            gpg.right()
            self.allWhiteCounter=0
            
            #print("Driving right")
        elif(values[0]==0 and values[1]==1):
            gpg.left()
            self.allWhiteCounter=0
            
        elif(values[0]==1 and values[1]==1 and values[2]==1 and values[3]==1 and values[4]==1):
            self.allWhiteCounter += 1
            if(self.allWhiteCounter <= 40):
                gpg.steer(100, 40)
            else:
                print("Hjalp, Im lost :( ")
                while(True):
                    gpg.stop()
        else:
            self.allWhiteCounter=0
    else:
        gpg.stop()

    time.sleep(0.02)