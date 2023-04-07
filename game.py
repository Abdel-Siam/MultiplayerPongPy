import pygame
from network import Network
import Player as p




class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        print(self.net.id)
        if(self.net.id == "1"):
            self.player = p.Player(1240,310)
            self.player2 = p.Player(20, 50)

        else:
            self.player = p.Player(20, 310)
            self.player2 = p.Player(1240,310)

        self.canvas = Canvas(self.width, self.height, "Distributed Pong")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.player.y  >= 0:
                    self.player.move(1)

            if keys[pygame.K_DOWN]:
                if self.player.y + 175 <= self.height :
                    self.player.move(3)

            # Send Network Stuff
            self.player2.x, self.player2.y, self.ballx , self.bally, self.score1, self.score2 = self.parse_data(self.send_data())
            
            # Draw non player assets.
            # Generate Game Component for score board.
            Score_one_text = str(self.score1)
            img1, pos1 = self.canvas.draw_text(str(Score_one_text),60,320,80)
            # Score two
            Score_two_text = str(self.score2)
            img2, pos2 = self.canvas.draw_text(str(Score_two_text),60,960,80)
            
            
            self.canvas.draw_background()
            ball = pygame.Rect(self.ballx,self.bally,25,25)
            pygame.draw.rect(self.canvas.get_canvas(), (255,255,255), ball)
            self.player.draw(self.canvas.get_canvas())
            self.canvas.screen.blit(img1, pos1)
            self.canvas.screen.blit(img2, pos2)

            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split("/")
            playerScore = d[2].split(",")
            player2pos = d[0].split(":")[1].split(",")
            ballpos = d[1].split(":")[1].split(",")
            d = data.split(":")[1].split(",")
            return int(player2pos[0]), int(player2pos[1]), float(ballpos[0]), float(ballpos[1]), int(playerScore[0]) , int(playerScore[1])
        except:
             return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)
        pygame.font.init()
        font = pygame.font.SysFont("retro.ttf",40)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("retro.ttf", size)
        text_render = font.render(text, True, (255, 255, 255))
        img = font.render(text, True, (255,255,255))
        position = img.get_rect()
        position.center = (x, y)
        return img, position


    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0,0,0))
