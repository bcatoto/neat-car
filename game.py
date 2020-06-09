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
    VEL = 10
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
        self.offset = (x, y)
        self.update_angle()
        self.update_mask()

    def update_angle(self):
        self.dir = self.INITIAL_DIR.rotate(self.angle)
        self.img = pygame.transform.rotate(self.IMG, self.angle)
        self.offset = self.img.get_rect(center = self.IMG.get_rect(topleft = (self.x, self.y)).center).topleft

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.img)

    def rotate(self, angle):
        self.angle += angle
        self.update_angle()

    def move(self):
        self.x += round(self.dir.x * self.VEL)
        self.y -= round(self.dir.y * self.VEL)
        self.offset = self.img.get_rect(center = self.IMG.get_rect(topleft = (self.x, self.y)).center).topleft
        self.collide()

    def collide(self):
        if self.TRACK_MASK.overlap(self.mask, self.offset):
            return True
        return False

    def radar(self, angle):
        toggle = 0
        if abs(angle) == 45:
            toggle = -7
        elif abs(angle) == 90:
            toggle = -14

        center_x, center_y = self.img.get_rect().center
        vec = self.INITIAL_DIR.rotate(self.angle + angle)
        start_x = self.offset[0] + center_x + vec.x * (self.HEIGHT / 2 + toggle)
        start_y = self.offset[1] + center_y - vec.y * (self.HEIGHT / 2 + toggle)

        for i in range(0, 100):
            x = round(self.offset[0] + center_x + vec.x * (self.HEIGHT / 2 + toggle + i))
            y = round(self.offset[1] + center_y - vec.y * (self.HEIGHT / 2 + toggle + i))
            if self.TRACK_MASK.get_at((x, y)):
                return math.sqrt((x - start_x) ** 2 + (y - start_y) ** 2)

        return -1

        # end_x = self.offset[0] + center_x + vec.x * (self.HEIGHT / 2 + toggle + 100)
        # end_y = self.offset[1] + center_y - vec.y * (self.HEIGHT / 2 + toggle + 100)
        # pygame.draw.line(WIN, (255, 255, 255), (start_x, start_y), (end_x, end_y), 3)

    def data(self):
        return (self.x, self.y, self.radar(-90), self.radar(-45), self.radar(0), self.radar(45), self.radar(90))

    def draw(self, win):
        win.blit(self.img, self.offset)

def draw_window(win, cars, gen, alive):
    # draw level
    win.blit(BG_IMG, (0, 0))
    win.blit(TRACK_IMG, (0, 0))

    # draw cars
    for car in cars:
        car.draw(win)
        car.radar(-90)
        car.radar(-45)
        car.radar(0)
        car.radar(45)
        car.radar(90)

    # generations
    gen_label = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(gen_label, (10, 10))

    # alive
    alive_label = STAT_FONT.render("Alive: " + str(alive), 1, (255,255,255))
    win.blit(alive_label, (10, 50))

    pygame.display.update()

def eval_genomes(genomes, config):
    global GEN
    ROTATION = 10

    nets = []
    cars = []
    gens = []

    for i, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(350, 80, -90))
        gens.append(genome)

    clock = pygame.time.Clock()

    run = True
    while run and len(cars) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for i, car in enumerate(cars):
            # calculate fitness
            gens[i].fitness += 1

            # send car data
            output = nets[i].activate(car.data())

            # moves player based on output
            if output[0] > 0:
                car.rotate(ROTATION)
            elif output[0] < 0:
                car.rotate(-ROTATION)

            # move car
            car.move()

            # check for collision with wall
            if car.collide():
                gens[i].fitness -= 5
                nets.pop(i)
                gens.pop(i)
                cars.pop(i)

        draw_window(WIN, cars, GEN, len(cars))

    GEN += 1

def run(config_file):
    """
    Runs the NEAT algorithm to train a neural network to play the World's
    Hardest Game
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    # Run indefinitely.
    winner = p.run(eval_genomes)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    """
    Determine path to configuration file. This path manipulation is here so that
    the script will run successfully regardless of the current working
    directory.
    """
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
