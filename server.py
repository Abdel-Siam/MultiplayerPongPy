import sys
import grpc
import pongps_pb2
import pongps_pb2_grpc
from concurrent import futures
import PlayerState

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
20,310 -> Rect Player 1 init pos

1240,310 -> Rect Player 2 init pos
"""   
class GameServicerServicer(pongps_pb2_grpc.GameServiceServicer):
    def connectClient(self, request, context):
        print("Entering Connect Client")
        if len(players) == 0:
            players.append(PlayerState(0,20,310))
            return pongps_pb2.clientId(whoami=0)
        elif len(players) == 1:
            players.append(PlayerState(1,1240,310))
            return pongps_pb2.clientId(whoami=1)
        elif len(players) >= 2:
            # Maybe raise an error instead?
            return "Server Currently Full"

    def updateClientPos(self, request, context):
        playerId = request.id
        newPos = request.pos
        players[playerId].pos = newPos

        # Check every update request if the other client has not updated via checking time delta. If so, return None
        # None treated as a disconnect for the requesting client
        if(request.id > 0):
            if abs(players[int(id)+1].getTimer()-players[int(id)]) < 15:
                players[int(id)+1] = players[0]
                
                return None
            
        return pongps_pb2.currGameState(
            pos1=players[0].pos,
            pos2=players[1].pos,
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

    def ballmoved(self, request, context):
        # The server should not receive this type of message
        # ballmoved is to be sent to the clients on a set interval
        # within the actual game loop
        # Client gprc servicer should implement this
        raise NotImplementedError('Method not implemented!')

    

if __name__ == '__main__':
    PORT = str(sys.argv[1])
    print(f"Starting Game Server on port {PORT}")
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(NUM_WORKERS)))

    pongps_pb2_grpc.add_GameServiceServicer_to_server(
        GameServicerServicer(), server)

    server.add_insecure_port(f'[::]:{PORT}')
    server.start()


    server.wait_for_termination()