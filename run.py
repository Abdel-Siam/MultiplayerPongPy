import game
import pygame
import sys
import os


pygame.init()

screen = pygame.display.set_mode((1280, 720))
def startScreen():
        intro = True

        text = 'DISTRIBUTED PONG'
        font = pygame.font.Font('retro.ttf', 48)
        img = font.render(text, True, (255,255,255))
        pos = img.get_rect()
        pos.center = (1280//2, 720//2-200)

        text_lower = 'PRESS ANY KEY TO START'
        # Ensure proper read/write perms on this file
        font_lower = pygame.font.Font('retro.ttf', 20)
        img_lower = font_lower.render(text_lower, True, (255,255,255))
        pos_lower = img_lower.get_rect()
        pos_lower.center = (1280//2, 720//2)
        texterror = ""
        font_error = pygame.font.Font('retro.ttf', 20)
        img_error = font_lower.render(text_lower, True, (255,255,255))
        pos_error = img_lower.get_rect()
        pos_error.center = (1280//2, 720+400//2)



        while intro:
            for event in pygame.event.get():
                event = pygame.event.wait()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    # Sends control to main game
                    return

            screen.fill((0,0,0))
            screen.blit(img, pos)
            screen.blit(img_lower, pos_lower)
            screen.blit(img_error, pos_error)

            pygame.display.update()

if __name__ == "__main__":
    startScreen()
    try:
        g = game.Game(1280,720)
        g.run()
    except ConnectionRefusedError:
        print("[ERROR] Server Not Available")

