"""         IMPORTS        """
from concurrent import futures
from time import sleep
import pygame
import sys
import os
import grpc
import google
import pongps_pb2_grpc
import pongps_pb2
import random
from server import GameServicerServicer
pygame.init()

"""    COSNTS    """

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong UI')
channel = None


class UI():
    SCORE = [0, 0]
    TIMEOUT_SEC = 1

    def draw_objects(self, RenderSet):
        font = pygame.font.Font('retro.ttf', 60)
        screen.fill(BLACK)
        # print(RenderSet)
        for i in RenderSet:
            try:
                pygame.draw.rect(screen, WHITE, RenderSet[i])
            except TypeError:
                screen.blit(RenderSet[i][0], RenderSet[i][1])

    def grpc_server_on(self, channel) -> bool:
        try:
            grpc.channel_ready_future(channel).result(timeout=self.TIMEOUT_SEC)
            return True
        except grpc.FutureTimeoutError:
            return False

    def GenerateGameComponents(self):
        RenderSet = {}
        # Generate Game Component for Paddle One
        paddle_one = pygame.Rect(20,
                                 SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                 PADDLE_WIDTH,
                                 PADDLE_HEIGHT)
        RenderSet['paddle_one'] = paddle_one

        # Generate Game Component for Paddle Two
        paddle_two = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH,
                                 SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                 PADDLE_WIDTH,
                                 PADDLE_HEIGHT)
        RenderSet['paddle_two'] = paddle_two

        # Generate Game Component for Ball.
        ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT // 2, 25, 25)
        RenderSet['ball'] = ball

        # Generate Game Component for score board.
        Score_one_text = str(self.SCORE[0])

        font = pygame.font.Font('retro.ttf', 48)
        score_one = font.render(Score_one_text, True, WHITE)
        img = font.render(str(self.SCORE[0]), True, WHITE)
        position_score_one = img.get_rect()
        position_score_one.center = (320, 80)
        RenderSet['score_one'] = [img, position_score_one]

        # Score two

        score_one = font.render(Score_one_text, True, WHITE)
        img = font.render(str(self.SCORE[1]), True, WHITE)
        position_score_one = img.get_rect()
        position_score_one.center = (960, 80)
        RenderSet['score_two'] = [img, position_score_one]
        return RenderSet

    def gameState(self, channel):
        """
        RenderSet: A render set is defined as all key assets of the game to be rendered by pygame. The paddles, the ball, scores, etc.
        The set is stored in a dictionary, primarily for ease of human-readability (as opposed to indexing each of the components and 
        keeping track of the index).

        ================ MAPPINGS IN RENDERSET ==================
        RenderSet['paddle_one'] : Maps to left Paddle
        RenderSet['paddle_two'] : Maps to right Paddle
        RenderSet['ball']       : Maps to the ball in play.
        RenderSet['score_one']  : Maps to the left score value
        RenderSet['score_two']  : Maps to the right score value
        =========================================================
        """
        RenderSet = self.GenerateGameComponents()
        # Draw objects before start of game.
        self.draw_objects(RenderSet)
        clock = pygame.time.Clock()
        BALLVECTOR = [0, 0]  # XY COMPONENT OF VELOCITY.
        empty = pongps_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        stub = pongps_pb2_grpc.GameServiceStub(channel)

        player = stub.connectClient(empty)
        print(player.whoami)
        # ternary operator for selecting which player you are.
        player_paddle = 'paddle_one' if int(player.whoami) == 0 else 'paddle_two'

        while True:
            paddle_velocity = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            """
            
            Key binding logic
            
            """
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and RenderSet[player_paddle].top > 0:
                paddle_velocity = -5
                RenderSet[player_paddle].move_ip(0, -5)
                movement_message = pongps_pb2_grpc.updatePaddlePos(
                    id=player.whoami, pos=[0, -5])
                pongps_pb2.updateClientPos(movement_message)
            if keys[pygame.K_s] and RenderSet[player_paddle].bottom < SCREEN_HEIGHT:
                paddle_velocity = 5
                movement_message = pongps_pb2_grpc.updateClientPos(
                    id=player.whoami, pos=[0, 5])
                stub.updateClientPos(movement_message)
                RenderSet[player_paddle].move_ip(0, 5)

            """
            
            Ball Logic

            """
           
                
            ballposition = stub.ballmoved(empty)

            
            """

            COLLISION LOGIC

            """
            if (pygame.Rect.collidelist(RenderSet[player_paddle], RenderSet['ball'])) != -1:
                    BALLVECTOR[0] = -BALLVECTOR[0]+0.5*paddle_velocity
                    BALLVECTOR[1] = -BALLVECTOR[1]+0.5*paddle_velocity

            else:
                RenderSet['ball'].move_ip(BALLVECTOR[0], BALLVECTOR[1])
                # print(f"X coordinate : {ball.x}. Y coordinate : {ball.y}")

            # Send the paddle_a position (x, y) to the gRPC client
            # send_position_to_grpc_client(paddle_a.x, paddle_a.y)
            self.draw_objects(RenderSet)
            pygame.display.flip()
            clock.tick(60)

    def startScreen(self):
        intro = True

        text = 'DISTRIBUTED PONG'
        font = pygame.font.Font('retro.ttf', 48)
        img = font.render(text, True, WHITE)
        pos = img.get_rect()
        pos.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-200)

        text_lower = 'PRESS ANY KEY TO START'
        # Ensure proper read/write perms on this file
        font_lower = pygame.font.Font('retro.ttf', 20)
        img_lower = font_lower.render(text_lower, True, WHITE)
        pos_lower = img_lower.get_rect()
        pos_lower.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        while intro:
            for event in pygame.event.get():
                event = pygame.event.wait()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    # Sends control to main game
                    return

            screen.fill(BLACK)
            screen.blit(img, pos)
            screen.blit(img_lower, pos_lower)

            pygame.display.update()

    def waitScreen(self, channel):
        clock = pygame.time.Clock()

        waiting = True
        LoadingText = ['Connecting to Server', 'Connecting to Server.',
                       'Connecting to Server..', 'Connecting to Server...', 'Connecting to Server....']
        font = pygame.font.Font('retro.ttf', 48)
        img = font.render(LoadingText[0], True, WHITE)
        pos = img.get_rect()
        pos.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        counter = 0
        while waiting:
            # Check first for the server to connect to the client. Terminate Loading sequence.
            if self.grpc_server_on(channel):
                # Sends control to main game
                print("Connecting to Server!")
                return

            # Check for exit
            for event in pygame.event.get():
                event = pygame.event.wait()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Dynamic Loading... while waiting for the server.
            img = font.render(LoadingText[counter % 4], True, WHITE)
            pos = img.get_rect()
            pos.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            counter = (counter + 1) % 4
            # print(counter)

            screen.fill(BLACK)
            screen.blit(img, pos)
            sleep(0.3)
            pygame.display.update()

# MAIN ENTRY


def run():
    ui_session = UI()
    ui_session.startScreen()
    channel = grpc.insecure_channel('localhost:50051')
    if (ui_session.grpc_server_on(channel)):
        print("Connection Established!")
        ui_session.gameState(channel)
    else:
        # gameState()
        ui_session.waitScreen(channel)
        ui_session.gameState(channel)
