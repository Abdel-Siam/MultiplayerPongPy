from locale import atof, atoi
import socket
import pygame
import sys
# Initialize Pygame

# Define the server's IP address and port number
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50001

# Define the dimensions of the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Create a Pygame display window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Create a socket object and connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))

# Receive the initial game state from the server
data = s.recv(1024).decode('utf-8')
ball_x, ball_y, paddle1_y, paddle2_y = data.split(',')

# Game loop
while True:
    # Send input to the server
    data = f'{paddle1_y}'.encode('utf-8')
    print(f"[ball_x:{ball_x}, ball_y:{ball_y}")

    s.sendall(data)
    # Receive the updated game state from the server
    data = s.recv(1024).decode('utf-8')
    ball_x, ball_y, paddle1_y, paddle2_y = data.split(',')
    
