SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 175

class Ball:
    MAX_VEL = 5
    def __init__(self):
        self.x = self.original_x = 1280//2
        self.y = self.original_y = 720//2
        self.radius = 10
        self.x_vel = 3
        self.y_vel = 3
        self.SCORE= [0,0]
    # def draw(self, win):
    #     pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    def increaseBallSpeed(self):
        self.x_vel = self.x_vel * 1.0000001
        self.y_vel = self.y_vel * 1.0000001

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        if self.x - self.radius < 0: 
            self.SCORE[1] += 1
            self.reset()
        if self.x + self.radius > SCREEN_WIDTH:
            self.SCORE[0] += 1
            self.reset()

        if 0 >= self.y + self.radius or self.y + self.radius >= SCREEN_HEIGHT:
            self.y_vel = -self.y_vel
            

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel *= -1
        self.x_vel *= -1
    
    def checkPaddleCollision(self,paddle_x, paddle_y, playNum):
        paddle_width = 20
        paddle_height = 175
        
        # Player One
        if playNum == 1:
            if (paddle_width+paddle_x > self.x + self.radius > paddle_x and paddle_y < self.y + self.radius < paddle_y + paddle_height):
                self.x_vel = -self.x_vel
                #self.y_vel = -self.y_vel
        # Player Two
        if playNum == 2:
             if (paddle_width+paddle_x > self.x + self.radius > paddle_x and paddle_y < self.y + self.radius < paddle_y + paddle_height):
                self.x_vel = -self.x_vel
                #self.y_vel = -self.y_vel
        
    def recoil(self):
        self.x_vel = -self.x_vel
        self.y_vel = -self.y_vel

    def serialize(self):
        return f'b:{self.x},{self.y}'