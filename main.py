import math, os, sys, pygame, random
from pygame.locals import *

pygame.init()
fps_clock = pygame.time.Clock()

display_width = 240
display_height = 480

title = 'Tetris'
crashed = False

font_obj = pygame.font.SysFont('Times New Roman', 15)
window_surface_obj = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('{0}'.format(title))

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)


# returns true if the two values are within a certain range of each other
def collision(a, b):
    if b[0] == a[0] and b[1] + 1 == a[1]:
        return True
    else:
        return False


def allcol(a, b):
    if collision(a, b.a) or collision(a, b.b) or collision(a, b.c) or collision(a, b.d):
        return True
    else:
        return False

# adds png to sprite dictionary
def update_dict(sprite_name, dict):
    dict[sprite_name] = pygame.image.load('resources/{0}.png'.format(sprite_name))


# just blit rewritten for convenience
def render(x, y, sprite):
    window_surface_obj.blit(sprite, (x * 24, y * 24))


# render a variable as text onscreen
def display_data(x, y, data, font, color):
    datatext = font.render("{0}".format(data), True, color)
    window_surface_obj.blit(datatext, (x, y))


# autofill dictionary with sprites from resources
block_dict = {}
for filename in os.listdir('resources'):
    if filename[-4:] == '.png':
        update_dict(filename[:-4], block_dict)

blocks = []


class tetronimo_obj():
    i = [[4, 0], [4, 1], [4, 2], [4, 3]]
    o = [[4, 0], [5, 0], [4, 1], [5, 1]]
    t = [[4, 0], [5, 0], [6, 0], [5, 1]]
    j = [[4, 0], [4, 1], [4, 2], [5, 2]]
    l = [[4, 0], [4, 1], [4, 2], [3, 2]]
    s = [[4, 0], [4, 1], [5, 1], [5, 2]]
    z = [[5, 0], [5, 1], [4, 1], [4, 2]]

    def __init__(self):
        x = random.choice([self.i, self.o, self.t, self.j, self.l, self.s, self.z])
        self.a = x[0]
        self.b = x[1]
        self.c = x[2]
        self.d = x[3]

    def reset(self):
        blocks.append([self.a[0], self.a[1]])
        blocks.append([self.b[0], self.b[1]])
        blocks.append([self.c[0], self.c[1]])
        blocks.append([self.d[0], self.d[1]])
        self.__init__()

    def fall(self):
        self.a[1] += 1
        self.b[1] += 1
        self.c[1] += 1
        self.d[1] += 1

    def move_left(self):
        self.a[0] -= 1
        self.b[0] -= 1
        self.c[0] -= 1
        self.d[0] -= 1

    def move_right(self):
        self.a[0] += 1
        self.b[0] += 1
        self.c[0] += 1
        self.d[0] += 1


time = 1
tetronimo = tetronimo_obj()

while not crashed:
    window_surface_obj.fill(black)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
        if time % 3 == 0:
            tetronimo.move_left()
    if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
        if time % 3 == 0:
            tetronimo.move_right()
    if pygame.key.get_pressed()[pygame.K_DOWN] != 0:
        if time % 3 == 0:
            tetronimo.fall()
    if time % 30 == 0 and pygame.key.get_pressed()[pygame.K_DOWN] == 0:
        tetronimo.fall()
    if tetronimo.a[1] > 18 or tetronimo.b[1] > 18 or tetronimo.c[1] > 18 or tetronimo.d[1] > 18:
        tetronimo.reset()
    for b in blocks:
        if allcol(b, tetronimo):
            tetronimo.reset()
            break
    for b in blocks:
        render(b[0], b[1], block_dict['block'])
    render(tetronimo.a[0], tetronimo.a[1], block_dict['block'])
    render(tetronimo.b[0], tetronimo.b[1], block_dict['block'])
    render(tetronimo.c[0], tetronimo.c[1], block_dict['block'])
    render(tetronimo.d[0], tetronimo.d[1], block_dict['block'])
    time += 1
    pygame.display.update()
    fps_clock.tick(30)
