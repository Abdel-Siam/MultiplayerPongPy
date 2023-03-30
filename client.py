import sys
import grpc
import pongps_pb2
import pongps_pb2_grpc
from concurrent import futures

NUM_WORKERS = 2

players = []
ballxPos = 0
ballyPos = 0
ballvx = 0
ballvy = 0


class PlayerState():
    def __init__(self, id):
        self.id = id
        self.pos = 0
        self.score = 0


class GameServicerServicer(pongps_pb2_grpc.GameServiceServicer):
    def connectClient(self, request, context):
        if len(players) == 0:
            players.append(PlayerState(0))
            return pongps_pb2.clientId(whoami=0)
        elif len(players) == 1:
            players.append(PlayerState(1))
            return pongps_pb2.clientId(whoami=1)
        else:
            # Maybe raise an error instead?
            return pongps_pb2.clientId(whoami=-1)

    def updateClientPos(self, request, context):
        playerId = request.id
        newPos = request.pos

        players[playerId].pos = newPos
        return pongps_pb2.currGameState(
            pos1=players[0].pos
            pos2=players[1].pos
            ballx=ballxPos
            bally=ballyPos
            ballVx=ballvx
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

    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(NUM_WORKERS)))

    pongps_pb2_grpc.add_GameServiceServicer_to_server(
        GameServicerServicer(), server)

    server.add_insecure_port(f'[::]:{PORT}')
    server.start()

    # Should have the code for actually playing the game here?

    server.wait_for_termination()