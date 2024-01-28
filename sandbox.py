import os
import pygame.locals
import pygame
from abstract import WaveStrike
from map_generating_logic import *
import numpy as np
from enemy_logic import Enemy, Boss
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
        return [pygame.transform.scale(pygame.image.load(path), size).convert_alpha()]
    elif dim.upper() == '3D':
        return [pygame.transform.scale(pygame.image.load(f'{path}\\{i}.png').convert_alpha(), size)
                for i in range(len(os.listdir(path))) if os.path.exists(f'{path}\\{i}.png')]
    raise ValueError("Wrong dimension type.\nIt's '2D' or '3D' only")


# from map_generating_logic import *
import tracemalloc, gc
import numpy
from random import randint as rnd, choice as ch


class Particles:

    def __init__(self, screen, level, color_list, radius, count, size, pos, vector, particle_time, name,
                 life_time=-1, random_particle_size=.0, random_particle_time=.0):
        self.screen = screen
        self.level = level
        self.color_list = color_list
        self.radius = radius
        self.count = count
        self.size = size
        self.pos = pos
        self.vector = vector
        self.particle_time = particle_time
        self.name = name
        self.life_time = life_time
        if 0 <= random_particle_size < 1:
            self.random_particle_size = random_particle_size
        if 0 <= random_particle_time < 1:
            self.random_particle_time = random_particle_time
        self.particles = []
        for _ in range(self.count):
            self.particles.append(self.make_particle())
        self.to_kill = False

    def make_particle(self):
        pos = (rnd(-self.radius, self.radius), rnd(-self.radius, self.radius))
        size = self.size + rnd(-int(self.size * self.random_particle_size),
                               int(self.size * self.random_particle_size))
        color = ch(self.color_list)
        time = self.particle_time + rnd(-int(self.particle_time * self.random_particle_time),
                                        int(self.particle_time * self.random_particle_time))
        return {
            'pos': pos,
            'size': size,
            'color': color,
            'time': time
        }

    def update_particle(self):
        for particle in self.particles:
            x, y = particle['pos']
            particle['pos'] = x + self.vector[0], y + self.vector[1]
            particle['time'] -= 1

        self.particles = [p for p in self.particles if p['time'] != 0]
        while len(self.particles) < self.count:
            self.particles.append(self.make_particle())

        if self.life_time > 0:
            self.life_time -= 1
        elif self.life_time == 0:
            self.count = 0
            self.particles.clear()
            self.to_kill = True

    def draw(self):
        for particle in self.particles:
            x, y = particle['pos']
            pygame.draw.circle(self.screen, particle['color'],
                               (self.pos[0] + x + self.level.st_pos[0], self.pos[1] + y + self.level.st_pos[1]),
                               particle['size'])


pygame.init()

WIDTH, HEIGHT = 1000, 800
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

textures = {
    'player': load_texture('images\\alien', '3D', (63, 60)),
    'rocket': load_texture('images\\rocket', '3D', (50, 16)),
    'dino': load_texture('images\\dino', '3D', (50, 42)),
    'red_orb': load_texture('images\\dino\\red_orb.png', '2D', (25, 25)),
    'croko': load_texture('images\\croko', '3D', (90, 28)),
    'bone1': load_texture('images\\decorations\\bone1_0.png', '2D', (200, 84)),
    'bone2': load_texture('images\\decorations\\bone2_0.png', '2D', (60, 38)),
    'cactus1': load_texture('images\\decorations\\cactus1_1.png', '2D', (70, 110)),
    'cactus2': load_texture('images\\decorations\\cactus2_1.png', '2D', (70, 308)),
    'home': load_texture('images\\decorations\\home_1.png', '2D', (200, 250)),
    'stone1': load_texture('images\\decorations\\stone1_1.png', '2D', (100, 56)),
    'stone2': load_texture('images\\decorations\\stone2_1.png', '2D', (100, 58)),
    'tree1': load_texture('images\\decorations\\tree1_1.png', '2D', (300, 744)),
    'tree2': load_texture('images\\decorations\\tree2_1.png', '2D', (300, 698)),
    'heal_tower': load_texture('images\\towers\\tower_hp_1.png', '2D', (225, 661)),
    'energy_tower': load_texture('images\\towers\\tower_energy_1.png', '2D', (225, 661)),
    'turtle': load_texture('images\\boss', '3D', (540, 348)),
}


fps_label = pygame.font.SysFont('Comic Sans MS', 20)

level = LevelGenerator(screen, textures, 1, 1)
Clock = pygame.time.Clock()
player = Player(screen, level, textures['player'], (0 // 2, 0 // 2), textures['rocket'])
fire = Particles(screen, level, [(255, 64, 0), (255, 128, 0), (255, 192, 0)],
                 10, 50, 5, (0, 0), (0, -2), 20, 'fire', life_time=30,
                 random_particle_size=0.5, random_particle_time=0.7)

waves = []
while True:
    Clock.tick(30)
    screen.fill("black")
    for wave in waves:
        wave.draw()
        wave.update()
    waves = [wave for wave in waves if wave.to_kill]
    text_surface = fps_label.render(f'FPS: {Clock.get_fps():.2f} ', False, (255, 255, 255))
    screen.blit(text_surface, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos[0] - level.st_pos[0], event.pos[1] - level.st_pos[1]
            waves.append(WaveStrike(screen, level, pos, (20, 20), (500, 500), 300))

    pygame.display.update()
