import random
import sys
import threading
import grpc
import pongps_pb2
import pongps_pb2_grpc
from concurrent import futures
import PlayerState as pb
import time 
import Ball

NUM_WORKERS = 2
playerUTC = []
players = []
ballxPos = 0
ballyPos = 0
ballvx = 0
ballvy = 0
scoreone = 0
scoretwo = 0



"""
def TimerHelper():
    while(True):
20,310 -> Rect Player 1 init pos

1240,310 -> Rect Player 2 init pos
Note :
"""               


# DIMENSIONS
SCREEN_HEIGHT = 720  
SCREEN_WIDTH = 1280


        
        # Add your game logic to handle collisions with other objects here.      

class GameServicerServicer(pongps_pb2_grpc.GameServiceServicer):
    def __init__(self):
        value = random.randint(-10, 10)
        self.ball = Ball.Ball(640, 360, value, value)
        players = []
        self.semaphore = threading.Semaphore()
        self.ready = False
            

    def StreamBallPosition(self, request, context):
        while True:
            self.semaphore.acquire()
            self.ball.update_position()

            ball_position = pongps_pb2.ballPosition(ball_x=self.ball.x, ball_y=self.ball.y)
            #print(f"x = {self.ball.x}, y = {self.ball.y}")
            yield ball_position
            self.semaphore.release()

            time.sleep(0.00001)

    def otherClientConnected(self, request,context):
        print(len(players))
        if(len(players)) != 2:
            return pongps_pb2.clientStatus(isConnected = -1)
        else:
            return pongps_pb2.clientStatus(isConnected = 1)

        
    def updateBallPos(self):
            while True:
                self.semaphore.acquire()

                if(self.ready):
                self.semaphore.release()



    def connectClient(self, request, context):
        print("Entering Connect Client")
        print(len(players))
        if len(players) == 0:
            print("Appending 1")

            connectTime_p1 = time.time()
            players.append([pb.PlayerState(0,20,310), connectTime_p1])
            return pongps_pb2.clientId(whoami = 0)
        elif len(players) == 1:
            connectTime_p2 = time.time()
            # reset p1 time
            players[0][1] = time.time()
            print("Appending 2")
            players.append([pb.PlayerState(1,1240,310), connectTime_p2])
            self.ready = True

            return pongps_pb2.clientId(whoami = 1)

        elif len(players) >= 2:
            return pongps_pb2.clientId(whoami = -1)

    def updateClientPos(self, request, context):
        # TODO: Put in semaphore?
        print("Recieved Client Update Call")
        print(request.id)
        print(request.pos)
        playerId = request.id
        newPos = request.pos
        #players[playerId].pos = newPos

        # Check every update request if the other client has not updated via checking time delta. If so, return None
        # None treated as a disconnect for the requesting client
        """TIMEOUT LOGIC"""

        if(len(players)>=2 and request.id > 0):
            if abs(players[int(id)][1]-players[int(id)-1][1]) < 15:
                players[int(id)+1] = players[0]
                return -1
        if(len(players)!=2):
            return pongps_pb2.currGameState(pos1=-1,pos2=None,ballx=None,bally=None,ballVx=None,ballVy=None)
        if(request.id > 1):
            return pongps_pb2.currGameState(pos1=-1,pos2=None,ballx=None,bally=None,ballVx=None,ballVy=None)
        # decouple ball position, in own message. on timer 
        # Player doesn't have to ping server for update
        # Server doesnt have to tell the player the new 
        # Server will always tell ball position
        # ONLY CLIENT WILL SEND TO SERVER ITS NEW PLAYER POSITION
        # SEND BALL AND PLAYER POSITION
        # SERVER DEALS WITH COLLISION LOGIC
        # server on two threads sends ball position
        # other thread 2 threads, for each player, send the opponents position
        # semaphores eliminated.
        # ball position always updated
        # only position of player updated
        return pongps_pb2.currGameState(pos1=players[0][0].pos,
                                        pos2=players[1][0].pos,
                                        ballx=ballxPos,
                                        bally=ballyPos,
                                        ballVx=ballvx,
                                        ballVy=ballvy
                                        )

    def clientScored(self, request, context):
        # The server should not receive this type of message
        # clientScored is to be sent to the clients after the math
        # shows that one of the clients got a point
        # Client gprc servicer should implement this
        raise NotImplementedError('Method not implemented!')
    
    # implemented on server for testing purposes.

   
    

    # LEN 2 X Y



    
if __name__ == '__main__':
    PORT = str(sys.argv[1])
    print(f"Starting Game Server on port {PORT}")
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(NUM_WORKERS)))
    # Game class.
    certified_gamer_moment = GameServicerServicer()
    pongps_pb2_grpc.add_GameServiceServicer_to_server(certified_gamer_moment, server)
    
    BALLVECTOR = [0,0]
    BALLPOS  = [0,0]
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    ball_thread = threading.Thread(certified_gamer_moment.updateBallPos())

    ball_thread.start()


    server.wait_for_termination()