import math
import pygame
from abstract import Object, Bullet


class Player(Object):
    def __init__(self, screen, level, path, pos, size, z_scale=1.5):
        x, y = pos[0] - level.st_pos[0], pos[1] - level.st_pos[1]
        super().__init__(screen, level, '3D', path, (x, y), size, name='player', z_scale=z_scale)
        self.move = ''
        self.rotate = ''
        self.move_frame = 400, 400
        self.speed_mv = 0
        self.max_speed_mv = 5
        self.accel_up = 1
        self.accel_down = 0.5
        self.speed_rt = 1
        self.energy = 100
        self.hp = 100
        self.bullets_in_shoot = []
        self.keys = set()
        self.status = 1
        self.hit_rect = pygame.Rect(0, 0, 53, 50)
        self.deco_to_hit = [deco for deco in level.deco_list if deco.status == 1]
        self.enemies = []

    def add_enemies(self, list_of_enemies):
        self.enemies.extend(list_of_enemies)

    def hit_deco(self):
        for deco in self.deco_to_hit:
            if self.hit_obj(deco.hit_rect):
                return False
        return True

    def draw(self):
        super().draw()
        for bullet in self.bullets_in_shoot:
            bullet.update()

    def shoot(self):
        shift = 20
        up = 20
        vec = -math.cos(self.angle * math.pi / 180), math.sin(self.angle * math.pi / 180)
        ovec = -vec[1], vec[0]

        pos = self.pos[0] + ovec[0] * shift, self.pos[1] + ovec[1] * shift - up
        self.bullets_in_shoot.append(Bullet(self.screen, self, self.level, '3D', 'rocket', pos,
                                            (50, 16), vector=vec, hit_rect=pygame.Rect(0, 0, 16, 16)))
        pos = self.pos[0] - ovec[0] * shift, self.pos[1] - ovec[1] * shift - up
        self.bullets_in_shoot.append(Bullet(self.screen, self, self.level, '3D', 'rocket', pos,
                                            (50, 16), vector=vec, hit_rect=pygame.Rect(0, 0, 16, 16)))

    def rotate_space(self):
        if self.rotate == 'left':
            self.angle -= self.speed_rt

        if self.rotate == 'right':
            self.angle += self.speed_rt

    def move_space(self):
        self.deco_to_hit = [deco for deco in self.level.deco_list if deco.status == 1]
        dx, dy = (self.speed_mv * math.cos(self.angle * math.pi / 180),
                  self.speed_mv * math.sin(self.angle * math.pi / 180))
        x, y = self.pos[0], self.pos[1]
        xx, yy = self.pos[0] + self.level.st_pos[0], self.pos[1] + self.level.st_pos[1]
        if self.move == 'forward':
            if self.speed_mv < self.max_speed_mv:
                self.speed_mv += self.accel_up

        elif self.move == 'backward':
            if self.speed_mv > -self.max_speed_mv:
                self.speed_mv -= self.accel_up
        elif self.speed_mv > 0:
            self.speed_mv -= self.accel_down
        elif self.speed_mv < 0:
            self.speed_mv += self.accel_down

        self.hit_rect.center = (x - dx, y + dy)
        if self.level.inside_map((x - dx, y + dy)) and self.hit_deco():
            if self.move_frame[0] < xx - dx < self.screen.get_width() - self.move_frame[0] and \
                    self.move_frame[1] < yy + dy < self.screen.get_height() - self.move_frame[1]:
                self.pos = x - dx, y + dy
            elif not self.move_frame[0] < xx - dx < self.screen.get_width() - self.move_frame[0] and not \
                    self.move_frame[1] < yy + dy < self.screen.get_height() - self.move_frame[1]:
                self.pos = x - dx, y + dy
                self.level.move(dx, -dy)
            elif not self.move_frame[0] < xx - dx < self.screen.get_width() - self.move_frame[0]:
                self.pos = x - dx, y + dy
                self.level.move(dx, 0)
            elif not self.move_frame[1] < yy + dy < self.screen.get_height() - self.move_frame[1]:
                self.pos = x - dx, y + dy
                self.level.move(0, -dy)
        else:
            self.speed_mv *= -1

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys.add(event.key)
            if event.key == pygame.K_d:
                self.rotate = 'left'
            if event.key == pygame.K_a:
                self.rotate = 'right'
            if event.key == pygame.K_w:
                self.move = 'forward'
            if event.key == pygame.K_s:
                self.move = 'backward'
            if event.key == pygame.K_LSHIFT:
                self.max_speed_mv = 15
            if event.key == pygame.K_LCTRL:
                self.angle += 180
            if event.key == 32:
                self.shoot()

        if event.type == pygame.KEYUP:
            self.keys.discard(event.key)
            if not {pygame.K_a, pygame.K_d} & self.keys:
                self.rotate = ''
            if not {pygame.K_w, pygame.K_s} & self.keys:
                self.move = ''
            if not {pygame.K_LSHIFT} & self.keys:
                self.max_speed_mv = 5

    def is_dead(self):
        return self.hp > 0 and self.energy > 0
