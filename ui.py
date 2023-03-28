import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong UI')

# Initialize paddles
paddle_a = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)

def main():
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # controls (w and s)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.move_ip(0, -5)
        if keys[pygame.K_s] and paddle_a.bottom < SCREEN_HEIGHT:
            paddle_a.move_ip(0, 5)
        
        # Send the paddle_a position (x, y) to the gRPC client
        # send_position_to_grpc_client(paddle_a.x, paddle_a.y)

        draw_objects()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
