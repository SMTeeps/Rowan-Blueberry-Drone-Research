import random

class DotSim:

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.x = random.randint(-xSize/2, xSize/2)
        self.y = random.randint(-ySize/2, ySize/2)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def updateX(self, dx):
        self.x = self.x - dx
    
    def updateY(self, dy):
        self.y = self.y - dy