import gc
import pygame
import math
from random import randint as rnd, choice as ch

ANGLE = math.tan(math.pi / 6)
SHIFT = 50


class Object:

    def __init__(self, screen, level, image_pack, pos, name,
                 angle=0, status=0, hit_rect=None, z_scale=1):
        self.screen = screen
        self.level = level
        self.pos = pos[0], pos[1]
        self.image_pack = image_pack
        self.status = status
        self.hit_rect = hit_rect
        self.z_scale = z_scale
        self.angle = angle
        self.name = name
        self.to_kill = False

    def draw(self):
        self.angle %= 360
        if self.hit_rect is not None:
            # rect = self.hit_rect.copy()
            # rect.center = self.pos[0] + self.level.st_pos[0], self.pos[1] + self.level.st_pos[1]
            # pygame.draw.rect(self.screen, (255, 0, 0), rect)
            self.hit_rect.center = self.pos

        for i, img in enumerate(self.image_pack):
            r_image = pygame.transform.rotate(img, self.angle)
            rect = r_image.get_rect()
            rect.center = (self.pos[0] + self.level.st_pos[0],
                           self.pos[1] - i * self.z_scale + self.level.st_pos[1])

            self.screen.blit(r_image, rect)

    def hit_obj(self, other_rect):
        if other_rect is not None:
            return self.hit_rect.colliderect(other_rect)
        return False


class Bullet(Object):
    def __init__(self, screen, char, level, image_pack, pos, name, damage=10, speed=25, vector=None, hit_rect=None,
                 z_scale=0.5):
        super().__init__(screen, level, image_pack, pos, name=name, z_scale=z_scale, hit_rect=hit_rect)
        self.char = char
        self.damage = damage
        self.speed = speed
        self.vector = vector
        self.status = 1
        self.angle = pygame.Vector2(self.vector).angle_to((pygame.Vector2((-1, 0))))

    def shot_someone(self):
        for enemy in self.char.enemies:
            if self.hit_obj(enemy.hit_rect):
                enemy.hp -= self.damage
                if self.char.name == 'player':
                    self.char.score += 5
                    enemy.strike_frame = enemy.cool_down
                    if enemy.hp <= 0:
                        enemy.to_kill = True
                self.to_kill = True

    def update(self):
        self.shot_someone()
        if self.vector is not None:
            x, y = self.pos
            dx, dy = self.vector
            self.pos = x + dx * self.speed, y + dy * self.speed
            self.hit_rect.center = self.pos
            if self.pos[0] + self.level.st_pos[0] < -200 or self.pos[1] + self.level.st_pos[1] < -200 or self.pos[0] + \
                    self.level.st_pos[0] > self.screen.get_width() + 200 or \
                    self.pos[1] + self.level.st_pos[1] > self.screen.get_height() + 200:
                self.to_kill = True

    def __del__(self):
        if self.char.name not in ['croko', 'dino']:
            self.level.vfx_list.append(Particles(self.screen, self.level, [(255, 64, 0), (255, 128, 0), (255, 192, 0)],
                                                 10, 50, 5, self.pos, (0, -3), 20, 'fire', life_time=20,
                                                 random_particle_size=0.5, random_particle_time=0.7))
        else:
            self.level.vfx_list.append(Particles(self.screen, self.level, [(64, 255, 0), (128, 255, 0), (192, 255, 0)],
                                                 10, 50, 5, self.pos, (0, -3), 20, 'poison', life_time=20,
                                                 random_particle_size=0.5, random_particle_time=0.7))
        gc.collect()


class Particles:

    def __init__(self, screen, level, color_list, radius, count, size, pos, vector, particle_time, name,
                 life_time=-1, random_particle_size=.0, random_particle_time=.0, random_particle_angle=0):
        self.screen = screen
        self.level = level
        self.color_list = color_list
        self.radius = radius
        self.count = count
        self.size = size
        self.pos = pos
        self.vector = vector
        self.particle_time = particle_time
        self.random_particle_angle = random_particle_angle
        self.name = name
        self.life_time = life_time
        self.hit_rect = pygame.Rect(*self.pos, self.radius, self.radius)
        if 0 <= random_particle_size < 1:
            self.random_particle_size = random_particle_size
        if 0 <= random_particle_time < 1:
            self.random_particle_time = random_particle_time
        self.particles = []
        for _ in range(self.count):
            self.particles.append(self.make_particle())
        self.to_kill = False
        self.status = 1

    def make_particle(self):
        pos = (rnd(-self.radius, self.radius), rnd(-self.radius, self.radius))
        size = self.size + rnd(-int(self.size * self.random_particle_size),
                               int(self.size * self.random_particle_size))
        color = ch(self.color_list)
        time = self.particle_time + rnd(-int(self.particle_time * self.random_particle_time),
                                        int(self.particle_time * self.random_particle_time))
        angle = rnd(-self.random_particle_angle, self.random_particle_angle) * math.pi / 180
        return {
            'pos': pos,
            'size': size,
            'color': color,
            'time': time,
            'angle': angle
        }

    def update(self):
        for particle in self.particles:
            x, y = particle['pos']
            particle['pos'] = (x + self.vector[0] * math.cos(particle['angle'])
                               - self.vector[1] * math.sin(particle['angle']),
                               y + self.vector[0] * math.sin(particle['angle'])
                               + self.vector[1] * math.cos(particle['angle']))
            particle['time'] -= 1

        self.particles = [p for p in self.particles if p['time'] != 0]
        while len(self.particles) < self.count:
            self.particles.append(self.make_particle())
        mn_x = min(self.particles, key=lambda obj: obj['pos'][0])['pos'][0]
        mn_y = min(self.particles, key=lambda obj: obj['pos'][1])['pos'][1]
        mx_x = max(self.particles, key=lambda obj: obj['pos'][0])['pos'][0]
        mx_y = max(self.particles, key=lambda obj: obj['pos'][1])['pos'][1]
        rect_size = abs(mx_x - mn_x), abs(mx_y - mn_y)
        pos = self.pos[0] + mn_x, self.pos[1] + mn_y
        self.hit_rect = pygame.Rect(*pos, *rect_size)
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


class WaveStrike:
    def __init__(self, screen, level, pos, base_size, finish_size, time, name='wave'):
        self.screen = screen
        self.level = level
        self.pos = pos
        self.size = base_size
        self.dsize = (finish_size[0] - base_size[0]) / time, (finish_size[1] - base_size[1]) / time
        self.time = time
        self.status = 0
        self.to_kill = False
        self.name = name
        self.hit_rect = pygame.Rect(*self.pos, *self.size)

    def update(self):
        if self.time > 0:
            self.size = self.size[0] + self.dsize[0], self.size[1] + self.dsize[1]
            self.hit_rect = pygame.Rect(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2,
                                        self.size[0], self.size[1])
            self.time -= 1
        else:
            self.to_kill = True

    def draw(self):
        if self.time > 0:
            pygame.draw.ellipse(self.screen, (255, 255, 255),
                                pygame.Rect(self.pos[0] + self.level.st_pos[0] - self.size[0] / 2,
                                            self.pos[1] + self.level.st_pos[1] - self.size[1] / 2,
                                            self.size[0], self.size[1]), 50)

    def __del__(self):
        gc.collect()


