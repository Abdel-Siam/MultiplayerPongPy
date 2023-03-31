from threading import Timer
from typing import overload


class PlayerState():
    

    def __init__(self, id):
        self.id = id
        self.pos = []
        self.score = 0
        self.timer = Timer()
        self.timer.start()
        self.playingAgainst = None
    
    @overload
    def __init_(self,id,x,y):
        self.id = id
        self.pos = [x,y]
        self.score = 0
        self.timer = Timer()
        self.timer.start()
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
        self.timer = Timer()
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