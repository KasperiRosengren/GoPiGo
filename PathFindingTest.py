import time


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid[rows][columns]
        for row in rows:
            for column in columns:
                


    def PrintGrid(self):
        for row in self.rows:
            for column in self.columns:
                print(f"[{self.grid[row][column].status}]")


#Tile statuses:
#   0. Wall / unavailable tile
#   1. Available / free
#   2. Occupied
class Tile:
    def __init__(self, row, column, status):
        self.row = row
        self.column = column
        self.status = status
    
    def ChangeStatus(self, newStatus):
        self.status

class Car:
    def __init__(self):
        self.locationX = 0
        self.locationY = 0
        self.targetX = 0
        self.targetY = 0
        self.heading = 0

    def SetLocation(self, newX, newY):
        self.locationX = newX
        self.locationY = newY
        print(f"New location at {self.locationX}.{self.locationY}")

    def SetTarget(self, newX, newY):
        self.targetX = newX
        self.targetY = newY
        print(f"New target at {self.targetX}.{self.targetY}")

    def Navigation(self):
        distanceX = self.targetX - self.locationX
        distanceY = self.targetY - self.locationY
        atDestination = False
        while(not atDestination):
            if(distanceX > 0):
                print("increase X")
            elif(distanceX < 0):
                print("decrease X")
            elif(distanceX == 0):
                print("X is correct")

        


    def MoveForward(self):
        print("Driving forward")

    def MoveBackwards(self):
        print("Reversing")

    def TurnLeft(self):
        print("Turning left")

    def TurnRight(self):
        print("Turning right")