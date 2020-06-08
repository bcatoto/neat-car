import pygame
import os
import time
import neat
import math
pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEAT Racing")
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
    INITIAL_DIR = (0, 1)
    IMG = pygame.transform.scale(CAR_IMG, (20, 44))
    TRACK_MASK = pygame.mask.from_surface(TRACK_IMG)

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dir = self.INITIAL_DIR
        self.img = self.IMG
        self.update_angle()
        self.update_mask()

    def update_angle(self):
        x = self.INITIAL_DIR[0]
        y = self.INITIAL_DIR[1]
        sin = math.sin(math.radians(self.angle))
        cos = math.cos(math.radians(self.angle))
        self.dir = (cos * x - sin * y, sin * x + cos * y)
        self.img = pygame.transform.rotate(self.IMG, self.angle)
        print("angle: ", self.angle)

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

    def rotate(self, angle):
        self.angle += angle
        self.update_angle()

    def move(self):
        self.x += round(self.dir[0] * self.VEL)
        self.y -= round(self.dir[1] * self.VEL)
        self.collide()

    def collide(self):
        if self.TRACK_MASK.overlap(self.mask, (self.x, self.y)):
            x = 1

    def draw(self, win):
        rect = self.img.get_rect(center = self.IMG.get_rect(topleft = (self.x, self.y)).center)
        win.blit(self.img, rect.topleft)

def draw_window(win, car):
    # draw level
    win.blit(BG_IMG, (0, 0))
    win.blit(TRACK_IMG, (0, 0))

    # draw cars
    car.draw(win)

    pygame.display.update()

def eval_genomes():
    car = Car(350, 85, -90)
    count = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        car.rotate(-5)
        car.move()
        draw_window(WIN, car)
        count += 1

if __name__ == "__main__":
    eval_genomes()
