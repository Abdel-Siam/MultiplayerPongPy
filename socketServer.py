# Import the necessary modules
import socket
import threading
import time
# Define the IP address and port number
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50001        # The port used by the server

# Define the game state variables
ball_x = 0.5
ball_y = 0.5
paddle1_y = 0.5
paddle2_y = 0.5

# Define a variable to keep track of the number of connected clients
num_clients = 0
def iterateBall():
    global ball_x, ball_y
    while True:
        ball_x += 1
        ball_y += 1
        time.sleep(0.00005)
# Define a function to handle each client connection
def handle_client(conn, addr):
    global num_clients
    global ball_x, ball_y, paddle1_y, paddle2_y
    
    # Send the current game state to the client
    conn.sendall(f'{ball_x},{ball_y},{paddle1_y},{paddle2_y}'.encode('utf-8'))
    
    # Increment the number of connected clients
    num_clients += 1
    
    # Wait for both clients to connect
    while num_clients < 2:
        pass
    
    # Game loop
    while True:
        # Receive input from the client
        data = conn.recv(1024)
        if not data:
            break
            
        # Update the game state based on the client's input
        paddle1_y += 0.1  # Example: move the paddle up
        
        # Send the updated game state to both clients
        game_state = f'{ball_x},{ball_y},{paddle1_y},{paddle2_y}'
        conn.sendall(game_state.encode('utf-8'))
        # todo: send to the other client
        
    # Decrement the number of connected clients
    num_clients -= 1
    conn.close()

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the IP address and port number
    s.bind((HOST, PORT))
    
    # Listen for incoming connections
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    
    # Wait for client connections
    while True:
        conn, addr = s.accept()
        print(f'Connected by {addr}')
        ball_thread = threading.Thread(target=iterateBall)
        ball_thread.start()
        # Create a new thread to handle the client connection
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

