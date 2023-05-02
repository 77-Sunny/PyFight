import pygame
import time

pygame.init()

def text(txt, font, txt_col):
    img = font.render(txt, True, txt_col)
    return img

def menu(win, font, fist):

    going = True
    Clock = pygame.time.Clock()
    while going:
        
        font2 = pygame.font.SysFont("arialblack", 20)
        title = text("PYFIGHT", font, "black")
        start_prompt = text("BY 77-SUNNY", font2, "black")
        start_in = [text("STARTING IN 3", font2, "black"), text("2", font2, "black"), text("1", font2, "black")]
        win.fill((255, 255, 255))
        win.blit(title, (160, 250))
        win.blit(start_prompt, (160, 325))
        win.blit(fist, (355, 255))
        
        Clock.tick(60) / 1000

        win.blit(start_in[0], (190, 425))
        time.sleep(2)
        pygame.display.update()

        win.blit(start_in[1], (342.5, 450))
        time.sleep(2)
        pygame.display.update()

        win.blit(start_in[2], (342.5, 475))
        time.sleep(2)
        pygame.display.update()
        time.sleep(1)
        break