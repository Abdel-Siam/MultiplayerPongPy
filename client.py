from concurrent import futures
import sys
import pongps_pb2_grpc
import grpc
import ui
from server import GameServicerServicer




def Pong():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(1)))
    pongps_pb2_grpc.add_GameServiceServicer_to_server(GameServicerServicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    ui.run()
    server.wait_for_termination()


if __name__ == '__main__':
    PORT = str(sys.argv[1])

    print(f"Starting Game Server on port {PORT}")

    Pong()
