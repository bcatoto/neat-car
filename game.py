import pygame
import os
import time
import neat
import math
pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEA Racing")
STAT_FONT = pygame.font.SysFont("arial", 50)

CAR_IMG = pygame.image.load(os.path.join("imgs", "car.png")).convert_alpha()
TRACK_IMG = pygame.image.load(os.path.join("imgs", "track.png")).convert_alpha()
BG_IMG = pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha()

GEN = 0

class Car:
    """
    Car class representing car player
    """
    VEL = 5
    IMG = pygame.transform.scale(CAR_IMG, (20, 44))
    MASK = pygame.mask.from_surface(IMG)
    TRACK_MASK = pygame.mask.from_surface(TRACK_IMG)

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dir = (0, -1)
        self.rotate()

    def rotate(self):
        x = self.dir[0]
        y = self.dir[1]
        new_x = math.cos(self.angle) * x - math.sin(self.angle) * y
        new_y = math.sin(self.angle) * x + math.cos(self.angle) * y
        self.dir = (new_x, new_y)

    def draw(self, win):
        img = pygame.transform.rotate(self.IMG, self.angle)
        new_rect = img.get_rect(center = img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(img, new_rect.topleft)

def draw_window(win, car):
    # draw level
    win.blit(BG_IMG, (0, 0))
    win.blit(TRACK_IMG, (0, 0))

    # draw cars
    car.draw(win)

    pygame.display.update()

def eval_genomes():
    car = Car(100, 100, -90)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        draw_window(WIN, car)

if __name__ == "__main__":
    eval_genomes()
