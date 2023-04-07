import socket
from _thread import *
import sys
import time
import Ball as b
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 175


    
def checkCollision(paddleOne, paddleTwo, ball):
    paddleOne = paddleOne.split(",")
    paddleTwo = paddleTwo.split(",")
    print(f"PaddleOne: {paddleOne}\nPaddleTwo: {paddleTwo}\nBall:{ball.x, ball.y}")

    ball.checkPaddleCollision(int(paddleOne[0]),int(paddleOne[1]),1)
    ball.checkPaddleCollision(int(paddleTwo[0]),int(paddleTwo[1]),2)
    
    
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")
# -- Init position -- # 
ball_obj = b.Ball()
ball_pos = start_ball_pos = ball_obj.serialize()
paddle_one = f"0:{20},{SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2}"
paddle_two = f"1:{SCREEN_WIDTH - 20 - PADDLE_WIDTH},{SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2}"
p1Score = p2Score = "0"
currentId = "0"
pos = [paddle_one, paddle_two, ball_pos, p1Score, p2Score]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    paddleOne = pos[0].split(":")[1]
    paddleTwo = pos[1].split(":")[1]
    while True:
        ball_obj.move()
        ball_obj.increaseBallSpeed()
        
        pos[3] = str(ball_obj.SCORE[0])
        pos[4] = str(ball_obj.SCORE[1])
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                conn.send(str.encode("Goodbye"))
                break

            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply
                pos[2] = ball_obj.serialize()

                if id == 0: nid = 1
                if id == 1: nid = 0
                # Format of string 
                # opponentNumber:x,y/b:x,y[s]P1Score,P2Score
                reply = pos[nid][:] +"/"+ pos[2] + "/" + pos[3]+","+ pos[4]
                

                print("Sending: " + reply)
            paddleOne = pos[0].split(":")[1]
            paddleTwo = pos[1].split(":")[1]
            
            checkCollision(paddleOne, paddleTwo , ball_obj)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    currentId = "0"
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
    

    