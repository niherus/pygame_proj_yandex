import os
import pygame.locals
import pygame
import abstract

import numpy as np
from enemy_logic import Enemy
from character_logic import Player

'''
class Rain:
    def __init__(self, screen, speed):
        self.screen = screen
        self.speed = speed
        self.effect = pygame.Surface(self.screen.get_size())
        self.color = (0, 0, 50)
        self.effect.fill(self.color)
        self.effect.set_alpha(50)
        self.rain1 = self.make_rain(pygame.Surface(self.screen.get_size()))
        self.rain1.set_colorkey((0, 0, 0))
        self.rain2 = self.make_rain(pygame.Surface(self.screen.get_size()))
        self.rain1.set_colorkey((0, 0, 0))
        self.y1 = -self.screen.get_size()[1]
        self.y2 = 0
        self.time = random.randint(500, 1000)
        self.k = 6

    def make_rain(self, image):
        for i in range(1000):
            x, y = random.randint(0, self.screen.get_size()[0]), random.randint(0, self.screen.get_size()[1])
            pygame.draw.line(image, (0, 0, 50), (x, y), (x, y + 4), 2)
        return image

    def update(self):
        self.time -= 1
        if not self.time and self.color == (0, 0, 50) and self.k == 4:
            self.color = (255, 255, 255)
            self.effect.fill(self.color)
            self.time = 10
            self.k -= 1
        elif not self.time and self.color == (255, 255, 255) and self.k > 0:
            self.color = (0, 0, 50)
            self.effect.fill(self.color)
            self.time = 5
            self.k -= 1
        elif not self.time and self.color == (0, 0, 50) and self.k > 0:
            self.color = (255, 255, 255)
            self.effect.fill(self.color)
            self.time = 10
            self.k -= 1
        elif self.k == 0:
            self.color = (0, 0, 50)
            self.effect.fill(self.color)
            self.time = random.randint(500, 1000)
            self.k = 4

        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= self.screen.get_size()[1]:
            self.y1 -= 2 * self.screen.get_size()[1]
        if self.y2 >= self.screen.get_size()[1]:
            self.y2 -= 2 * self.screen.get_size()[1]
    def draw(self):
        self.screen.blit(self.effect, (0, 0))
        self.screen.blit(self.rain1, (0, self.y1))
        self.screen.blit(self.rain1, (0, self.y2))
colors = {
    'window': (40, 40, 150)
}
'''
import tracemalloc


def load_texture(path, dim, size):
    if dim.upper() == '2D':
        return [pygame.transform.scale(pygame.image.load(path), size)]
    elif dim.upper() == '3D':
        return [pygame.transform.scale(pygame.image.load(f'{path}\\{i}.png'), size)
                for i in range(len(os.listdir(path))) if os.path.exists(f'{path}\\{i}.png')]
    raise ValueError("Wrong dimension type.\nIt's '2D' or '3D' only")


from map_generating_logic import *
import tracemalloc, gc

tracemalloc.start()
pygame.init()

WIDTH, HEIGHT = 1900, 1060
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

textures = {
    'player': load_texture('alien2', '3D', (63, 60)),
    'rocket': load_texture('rocket', '3D', (50, 16)),
    'dino': load_texture('dino', '3D', (50, 42)),
    'red_orb': load_texture('dino\\red_orb.png', '2D', (50, 16)),
    'croko': load_texture('croko', '3D', (90, 28)),
    'bone1': load_texture('decorations\\bone1_0.png', '2D', (200, 84)),
    'bone2': load_texture('decorations\\bone2_0.png', '2D', (60, 38)),
    'cactus1': load_texture('decorations\\cactus1_1.png', '2D', (70, 110)),
    'cactus2': load_texture('decorations\\cactus2_1.png', '2D', (70, 308)),
    'home': load_texture('decorations\\home_1.png', '2D', (200, 250)),
    'stone1': load_texture('decorations\\stone1_1.png', '2D', (100, 56)),
    'stone2': load_texture('decorations\\stone2_1.png', '2D', (100, 58)),
    'tree1': load_texture('decorations\\tree1_1.png', '2D', (300, 744)),
    'tree2': load_texture('decorations\\tree2_1.png', '2D', (300, 698)),
}
level = LevelGenerator(screen, textures, 20, 20)
player = Player(screen, level, textures['player'], (1000, 1000),
                textures['rocket'])
class Obj:
    id = 0
    def __init__(self):
        self.id = Obj.id
        Obj.id += 1
    def __del__(self):
        print(self.id)


crokos = []
Clock = pygame.time.Clock()
while True:
    print(tracemalloc.get_tracemalloc_memory(), len(crokos))
    Clock.tick(60)
    screen.fill("white")
    level.draw()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                crokos.append(Obj())
            if event.key == pygame.K_LCTRL:
                if crokos:
                    crokos.pop()
                    gc.collect()

    pygame.event.clear()
    #for croko in crokos:
    #    croko.draw()
    pygame.display.update()
tracemalloc.stop()