import grpc
import pongps_pb2_grpc
import pongps_pb2
import time
def testFunction():
    listFailed = []

    channel = grpc.insecure_channel('localhost:50051')

    empty = pongps_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    print("Empty created")
    stub = pongps_pb2_grpc.GameServiceStub(channel)
    print("Stub Created")
    player = stub.connectClient(empty)
    # Test One , Player Generation
    if(player.whoami == 0 or player.whoami == 1):
        print("1. Connect Client Passed.")
        print(f"whoami {player.whoami}")
    else:
        print("1. Connect Client Failed")

    # print(type(player.whoami))
    # Movement test
    if(player.whoami == 0 or player.whoami == 1):

        movement_message = pongps_pb2.updatePaddlePos(id = 1 , pos = -5)
        print("Sending movement Message")

        # Malformed request
        response = stub.updateClientPos(movement_message)
        print(response)
        if(response.pos1==-1):
            print("2. Update Client Failed")
        else:
            print("3. Update Client Position Passed")
   
   
    ball_x = 500
    ball_y = 500

    movement_message = pongps_pb2.ballPosition(ball_x = ball_x , ball_y = ball_y)

    request = pongps_pb2.StreamBallPositionRequest(client_id=0)
    for ball_position in stub.StreamBallPosition(request):
            print(f'Client {0}: Ball Position:\nBall X: {ball_position.ball_x}\nBall Y:{ball_position.ball_y}')
            time.sleep(0.00001)

testFunction()