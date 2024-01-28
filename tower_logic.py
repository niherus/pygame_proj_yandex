import math

from abstract import *


class Tower(Object):

    def __init__(self, screen, level,  char, image_pack, pos, name):
        super().__init__(screen, level, image_pack, pos, name, status=1, hit_rect=pygame.Rect(*pos, 200, 100))
        self.to_kill = False
        if self.name == 'heal_tower':
            self.effect = 10
            self.corruption = 0.2
            self.max_effect = 10
            self.cooldown = 30
        elif self.name == 'energy_tower':
            self.effect = 10
            self.corruption = 0.1
            self.max_effect = 10
            self.cooldown = 30
        self.distance = 500
        self.hp = 200
        self.char = char
        self.char.level.deco_list.append(self)

    def draw(self):
        super().draw()
        if 0 < self.hp < 200:
            x, y = self.pos[0] + self.level.st_pos[0] - self.hp // 2, self.pos[1] + self.level.st_pos[1] + 50
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.hp, 10))
            self.hp += 0.5
        elif self.hp <= 0:
            self.to_kill = True
        self.hit_rect.center = self.pos
        self.cooldown -= 1
        dx, dy = self.pos[0] - self.char.pos[0], self.pos[1] - self.char.pos[1]
        if math.hypot(dx, dy) <= self.distance and self.cooldown <= 0:
            if self.name == 'heal_tower':
                self.char.hp = min(self.effect + self.char.hp, 100)
                self.effect = max(self.effect - self.corruption, 0)
                self.cooldown = 60
            elif self.name == 'energy_tower':
                self.char.energy = min(self.effect + self.char.energy, 100)
                self.effect = max(self.effect - self.corruption, 0)
                self.cooldown = 60
        elif math.hypot(dx, dy) > self.distance:
            self.effect = min(self.effect + self.corruption, self.max_effect)






