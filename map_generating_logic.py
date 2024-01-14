from random import randint as rnd

import math
import os
import pygame

from abstract import Object, ANGLE, SHIFT


class LevelGenerator:
    def __init__(self, screen, width=100, height=100):
        self.borders = None
        self.deco_list = []
        self.deco_lib = os.listdir('decorations\\')
        self.screen = screen
        self.size = width, height
        self.plat = pygame.transform.scale_by(pygame.image.load('ntile.png'), 0.5)
        self.rect = self.plat.get_rect()
        self.w, self.h = self.rect.size
        self.st_pos = (-width * self.w / 2 + self.screen.get_width() / 2,
                       -height * self.h / 4 + self.screen.get_height() / 2)
        self.main_surf = pygame.Surface((width * self.w, height * self.h))
        self.main_surf.set_colorkey((0, 0, 0, 0))
        self.generate_all()

    def generate_all(self):
        pygame.draw.circle(self.main_surf, (255, 0, 0), (0, 0), 20)
        mw, mh = self.main_surf.get_size()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.rect.center = (mw // 2 + (i * self.w + j * self.w * -1) / 2,
                                    self.h // 2 + (i * ANGLE * self.h + j * ANGLE * self.h) / 2)

                deco = rnd(0, 10 * len(self.deco_lib) - 1)
                flip = bool(rnd(0, 1))
                if deco > 9 * len(self.deco_lib):
                    self.deco_list.append(Decoration(self.screen, self,
                                                     self.rect.center,
                                                     self.deco_lib[deco - 9 * len(self.deco_lib)],
                                                     mirror=flip))

                self.main_surf.blit(self.plat, self.rect)

        self.borders = (
            (round(mw // 2 + (0 * self.w + 0 * self.w * -1) / 2),
             round(self.h // 2 + (0 * ANGLE * self.h + 0 * ANGLE * self.h) / 2) - SHIFT),
            (round(mw // 2 + (0 * self.w + (self.size[1]) * self.w * -1) / 2),
             round(self.h // 2 + (0 * ANGLE * self.h + (self.size[1]) * ANGLE * self.h) / 2) - SHIFT),
            (round(mw // 2 + ((self.size[0]) * self.w + 0 * self.w * -1) / 2),
             round(self.h // 2 + ((self.size[0]) * ANGLE * self.h + 0 * ANGLE * self.h) / 2) - SHIFT),
            (round(mw // 2 + ((self.size[0] - 1) * self.w + (self.size[1] - 1) * self.w * -1) / 2),
             round(self.h // 2 + ((self.size[0]) * ANGLE * self.h + (self.size[1]) * ANGLE * self.h) / 2) - SHIFT)
        )

        pygame.draw.circle(self.main_surf, (255, 0, 0), self.borders[0], 20)
        pygame.draw.circle(self.main_surf, (0, 255, 0), self.borders[1], 20)
        pygame.draw.circle(self.main_surf, (0, 0, 255), self.borders[2], 20)
        pygame.draw.circle(self.main_surf, (255, 255, 0), self.borders[3], 20)

    def move(self, dx, dy):
        self.st_pos = self.st_pos[0] + dx, self.st_pos[1] + dy

    def draw(self):
        self.screen.blit(self.main_surf, self.st_pos)

    @staticmethod
    def distance(p1, p2, p0):
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        return abs(dy * p0[0] - dx * p0[1] + p2[0] * p1[1] - p2[1] * p1[0]) / math.hypot(dx, dy)

    def get_cell_pos(self, pos):
        x, y = pos[0] - self.st_pos[0], pos[1] - self.st_pos[1]
        dx = (self.distance(self.borders[0], self.borders[1], (x, y)) / 0.577) / 173.2
        dy = (self.distance(self.borders[0], self.borders[2], (x, y)) / 0.577) / 173.2
        return int(dx), int(dy)

    def inside_map(self, pos):
        x, y = pos[0], pos[1]
        x1, x2, x3 = self.borders[1][0], self.borders[0][0], self.borders[2][0]
        y1, y2, y3 = self.borders[1][1], self.borders[0][1], self.borders[2][1]
        shift = 50

        if x1 < x < x2 and abs(y - y1) < x / (3 ** 0.5) - shift:
            return True
        elif x2 <= x < x3 and abs(y - y1) < (x3 - x) / (3 ** 0.5) - shift:
            return True
        return False


class Decoration(Object):

    def __init__(self, screen, level, pos, image, mirror=False):
        if 'tree' in image:
            hit_rect = pygame.Rect(0, 0, 60, 40)
            name = 'tree'
        elif 'stone' in image:
            hit_rect = pygame.Rect(0, 0, 90, 30)
            name = 'stone'
        elif 'cactus1' in image:
            hit_rect = pygame.Rect(0, 0, 45, 45)
            name = 'cactus'
        elif 'cactus2' in image:
            hit_rect = pygame.Rect(0, 0, 25, 30)
            name = 'cactus'
        elif 'home' in image:
            hit_rect = pygame.Rect(0, 0, 200, 100)
            name = 'home'
        else:
            hit_rect = None
            name = 'None'

        size = pygame.image.load(f'decorations\\{image}').get_size()
        super().__init__(screen, level, '2D', f'decorations\\{image}',
                         pos, size, status=int(image[-5]), name=name, hit_rect=hit_rect)
        if mirror:
            self.image_pack[0] = pygame.transform.flip(self.image_pack[0], mirror, False)
        self.hp = 100

    def draw(self):
        super().draw()
        if 0 < self.hp < 100:
            x, y = self.pos[0] + self.level.st_pos[0] - self.hp // 2, self.pos[1] + self.level.st_pos[1] + 50
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.hp, 10))
        elif self.hp <= 0:
            self.level.deco_list.remove(self)
            del self
