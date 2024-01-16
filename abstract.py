import gc
import pygame
import math

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
        if self.hit_rect is not None:
            #rect = self.hit_rect.copy()
            #rect.center = self.pos[0] + self.level.st_pos[0], self.pos[1] + self.level.st_pos[1]
            #pygame.draw.rect(self.screen, (255, 0, 0), rect)
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
                    self.char.score += 1
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
        gc.collect()
