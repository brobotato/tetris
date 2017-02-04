import os, sys, pygame, random
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


# check if blocks are above each other
def vcol(a, b):
    if b[0] == a[0] and b[1] + 1 == a[1]:
        return True
    else:
        return False


# check if blocks are right next to each other
def hcol_l(a, b):
    if a[1] == b[1] and a[0] - b[0] == 1:
        return True


# check if blocks are right next to each other
def hcol_r(a, b):
    if a[1] == b[1] and a[0] - b[0] == -1:
        return True


# returns true if any part of the tetronimo is right above another block
def acol(a, b):
    if vcol(a, b.a) or vcol(a, b.b) or vcol(a, b.c) or vcol(a, b.d):
        return True
    else:
        return False


# returns true if 2 blocks are exaclty on top of eacother
def intersect(a, b):
    if b.a == a[:2] or b.b == a[:2] or b.c == a[:2] or b.d == a[:2]:
        return True
    else:
        return False


# rotate a block around a center
def rotate(a, b):
    if a[0] > b[0]:
        if a[1] < b[1]:
            a[1] += 2
        elif a[1] > b[1]:
            a[0] -= 2
        elif a[0] == 1 + b[0]:
            a[0] -= 1
            a[1] += 1
        elif a[0] == 2 + b[0]:
            a[0] -= 2
            a[1] += 2
    elif a[0] < b[0]:
        if a[1] < b[1]:
            a[0] += 2
        elif a[1] > b[1]:
            a[1] -= 2
        elif a[0] == b[0] - 1:
            a[0] += 1
            a[1] -= 1
        elif a[0] == b[0] - 2:
            a[0] += 2
            a[1] -= 2
    else:
        if a[1] == b[1] - 1:
            a[0] += 1
            a[1] += 1
        elif a[1] == b[1] - 2:
            a[0] += 2
            a[1] += 2
        elif a[1] == b[1] + 1:
            a[0] -= 1
            a[1] -= 1
        elif a[1] == b[1] + 2:
            a[0] -= 2
            a[1] -= 2


# returns true if any part of the tetronimo is to the left of another block
def adj_l(a, b):
    for block in b:
        if hcol_l(a.a, block) or hcol_l(a.b, block) or hcol_l(a.c, block) or hcol_l(a.d, block):
            return True
            break
        else:
            pass


# returns true if any part of the tetronimo is to the right of another block
def adj_r(a, b):
    for block in b:
        if hcol_r(a.a, block) or hcol_r(a.b, block) or hcol_r(a.c, block) or hcol_r(a.d, block):
            return True
            break
        else:
            pass


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


# auto fill dictionary with sprites from resources
img_dict = {}
for filename in os.listdir('resources'):
    if filename[-4:] == '.png':
        update_dict(filename[:-4], img_dict)

blocks = []
block_dict = {}


class tetronimo_obj():
    def __init__(self):
        self.i = ([4, 0], [4, 1], [4, 2], [4, 3], 'i')
        self.o = ([4, 0], [5, 0], [4, 1], [5, 1], 'o')
        self.t = ([4, 0], [5, 0], [6, 0], [5, 1], 't')
        self.j = ([4, 0], [4, 1], [4, 2], [5, 2], 'j')
        self.l = ([4, 0], [4, 1], [4, 2], [3, 2], 'l')
        self.s = ([4, 0], [4, 1], [5, 1], [5, 2], 's')
        self.z = ([5, 0], [5, 1], [4, 1], [4, 2], 'z')
        self.x = random.choice([self.i])  # , self.o, self.t, self.j, self.l, self.s, self.z])
        self.a = self.x[0]
        self.b = self.x[1]
        self.c = self.x[2]
        self.d = self.x[3]
        self.color = self.x[4]

    def render(self):
        render(self.a[0], self.a[1], img_dict[self.color])
        render(self.b[0], self.b[1], img_dict[self.color])
        render(self.c[0], self.c[1], img_dict[self.color])
        render(self.d[0], self.d[1], img_dict[self.color])

    def reset(self):
        blocks.append([self.a[0], self.a[1], self.color, False, 0])
        blocks.append([self.b[0], self.b[1], self.color, False, 0])
        blocks.append([self.c[0], self.c[1], self.color, False, 0])
        blocks.append([self.d[0], self.d[1], self.color, False, 0])
        self.__init__()

    def rotate(self):
        if self.color != 'o' and 0 < self.b[0] < 9:
            rotate(self.a, self.b)
            rotate(self.c, self.b)
            rotate(self.d, self.b)

    def fall(self):
        self.a[1] += 1
        self.b[1] += 1
        self.c[1] += 1
        self.d[1] += 1

    def rise(self):
        self.a[1] -= 1
        self.b[1] -= 1
        self.c[1] -= 1
        self.d[1] -= 1

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
    if tetronimo.a[0] > 9 or tetronimo.b[0] > 9 or tetronimo.c[0] > 9 or tetronimo.d[0] > 9:
        tetronimo.move_left()
    if tetronimo.a[0] < 0 or tetronimo.b[0] < 0 or tetronimo.c[0] < 0 or tetronimo.d[0] < 0:
        tetronimo.move_right()
    if tetronimo.a[1] > 19 or tetronimo.b[1] > 19 or tetronimo.c[1] > 19 or tetronimo.d[1] > 19:
        tetronimo.rise()
    if (tetronimo.a[1] > 18 or tetronimo.b[1] > 18 or tetronimo.c[1] > 18 or tetronimo.d[1] > 18) and time % 40 == 0:
        tetronimo.reset()
    for b in blocks:
        if acol(b, tetronimo) and time % 40 == 0:
            tetronimo.reset()
            break
    if pygame.key.get_pressed()[pygame.K_UP] != 0:
        if time % 3 == 0:
            tetronimo.rotate()
    if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
        if tetronimo.a[0] >= 1 <= tetronimo.b[0] and tetronimo.c[0] >= 1 <= tetronimo.d[0] and time % 3 == 0:
            if not adj_l(tetronimo, blocks):
                tetronimo.move_left()
    if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
        if tetronimo.a[0] <= 8 >= tetronimo.b[0] and tetronimo.c[0] <= 8 >= tetronimo.d[0] and time % 3 == 0:
            if not adj_r(tetronimo, blocks):
                tetronimo.move_right()
    if pygame.key.get_pressed()[pygame.K_DOWN] != 0 and time % 3 == 0:
        if tetronimo.a[1] < 19 and tetronimo.b[1] < 19 and tetronimo.c[1] < 19 and tetronimo.d[1] < 19:
            tetronimo.fall()
    if time % 30 == 0 and pygame.key.get_pressed()[pygame.K_DOWN] == 0:
        tetronimo.fall()
    for x in range(0, 20, 1):
        if sum(b[1] == x for b in blocks) >= 10:
            for b in blocks:
                if b[1] == x:
                    b[3] = True
                    b[4] = -20
                elif b[1] < x:
                    b[3] = False
                    b[4] += 1
    for b in blocks:
        if b[3]:
            blocks.remove(b)
        else:
            render(b[0], b[1], img_dict[b[2]])
            if intersect(b, tetronimo):
                tetronimo.rise()
            if b[4] > 0:
                b[1] += b[4]
                b[4] = 0
            if b[1] < 1:
                crashed = True
    tetronimo.render()
    time += 1
    pygame.display.update()
    fps_clock.tick(30)
