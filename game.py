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
    INITIAL_DIR = pygame.Vector2(0, 1)
    IMG = pygame.transform.scale(CAR_IMG, (20, 44))
    HEIGHT = IMG.get_height()
    WIDTH = IMG.get_width()
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
        self.dir = self.INITIAL_DIR.rotate(self.angle)
        self.img = pygame.transform.rotate(self.IMG, self.angle)

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

    def rotate(self, angle):
        self.angle += angle
        self.update_angle()

    def move(self):
        self.x += round(self.dir.x * self.VEL)
        self.y -= round(self.dir.y * self.VEL)
        self.collide()

    def collide(self):
        if self.TRACK_MASK.overlap(self.mask, (self.x, self.y)):
            x = 1

    def radar(self, angle):
        center_x, center_y = self.img.get_rect().center
        vec = self.INITIAL_DIR.rotate(self.angle + angle)
        start_x = self.x + center_x + vec.x * (self.HEIGHT / 2)
        start_y = self.y + center_y + vec.y * (self.HEIGHT / 2)
        end_x = self.x + center_x + vec.x * (self.HEIGHT / 2 + 100)
        end_y = self.y + center_y + vec.y * (self.HEIGHT / 2 + 100)
        pygame.draw.line(WIN, (255, 255, 255), (start_x, start_y), (end_x, end_y))
        print("x: ", start_x)
        print("y: ", start_y)
        print("eX: ", end_x)
        print("eX: ", end_y)

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
        # car.radar(0)
        draw_window(WIN, car)
        count += 1

if __name__ == "__main__":
    eval_genomes()
