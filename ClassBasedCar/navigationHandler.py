from movementController import MovementController

class NavigationHandler(MovementController):
    def __init__(self, heading, positionX, positionY, targetX, targetY):
        print("Ready to navigate")
        self.positionX = positionX
        self.positionY = positionY
        self.targetX = targetX
        self.targetY = targetY
        self.heading = heading

    def WhereAmI(self):
        print("I am at: "+self.positionX+"."+self.positionY)

    def SetNewLocation(self, newX, newY):
        self.positionX = newX
        self.positionY = newY
        print("My new location is at: "+self.positionX+"."+self.positionY)
    
    def SetNewTarget(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY
        print("My new target is at: "+self.targetX+"."+self.targetY)


    def AlterHeading(self, degrees):
        tempHeading = self.heading + degrees
        if(tempHeading >= 360):
            self.heading = tempHeading - 360
        elif(tempHeading < 0):
            self.heading = tempHeading + 360
        else:
            self.heading = tempHeading

    def TurnRight(self):
        gpg.turn_degrees(95)
        AlterHeading(90)
        
    def TurnLeft(self):
        gpg.turn_degrees(-95)
        AlterHeading(-90)

    def Turn180(self):
        gpg.turn_degrees(193)
        AlterHeading(180)
