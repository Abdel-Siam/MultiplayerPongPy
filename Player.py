import pygame
class Player():
    width = 20
    height = 175

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 6
        self.color = color
        self.ballx = 0
        self.bally = 0
        self.score1 = 0
        self.score2 = 0

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        if dirn == 1:
            self.y -= self.velocity
        else:
            self.y += self.velocity