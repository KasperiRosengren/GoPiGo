
class Tile:
    def __init__(self, row, column):
        self.status = 1
        self.row = row
        self.column = column
        self.color = 'White'
    
    def ChangeStatus(self, status, color="White"):
        self.status = status
        self.color = color

    def ChangeToActive(self):
        self.status = 2
        self.color = "Yellow"

    

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[Tile(y, x) for x in range(self.columns)]for y in range(self.rows)]

    def PrintGrid(self):
        for row in self.grid:
            thisrow = []
            for tile in row:
                thisrow.append(tile.row)
            print(thisrow)


mainGrid = Grid(5, 5)
mainGrid.PrintGrid()
print("hello")
