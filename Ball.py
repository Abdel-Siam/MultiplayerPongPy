SCREEN_HEIGHT = 720  
SCREEN_WIDTH = 1280
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 10 # set the radius of the ball

    def update_position(self):
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Check for collisions with walls
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > SCREEN_HEIGHT:
            self.vy = -self.vy
    def paddleCollision(self,paddle):
        """
        Check for collision between a paddle object and 
        """
        raise NotImplementedError

        
    def setspeed(self,vx,vy):
        self.vx = vx 
        self.vy = vy
