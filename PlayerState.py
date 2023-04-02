import time


class PlayerState:
    def __init__(self,id,x,y):
        print("Player State Created")
        self.id = id
        self.pos = [x,y]
        self.score = 0
        #Epoch time
        self.lastUpdated = 0
        self.playingAgainst = None    

    # Other player id -> Points to the index on the server
    def setPlayingAgainst(self,id):
        self.playingagainst = id

    def resetTimer(self):
        self.timer.cancel()
        self.timer.start()
    
    def getTimer(self):
        return self.timer
    
    def resetState(self):
        self.id = id
        self.pos = []       # x,y | width,height size(4)
        self.score = 0
        self.timer = time.time()
        self.timer.start()
        self.playingAgainst = None
    
    
    def getx(self):
        return self.pos[0]
    
    def gety(self):
        return self.post[1]
    
    def setx(self, x):
        self.pos[0] = x
    
    def sety(self, x):
        self.pos[0] = x
    """
    def updateTime(self):
        self.lastUpdated = time.time()
        """
class BallState:
    def __init__(self):
        self.BALLPOS = []
        self.BALLPOS[0] = 1280 // 2
        self.BALLPOS[1] = 720 // 2
        self.BALLVECTOR = [0,0]
        