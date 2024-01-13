import math
import pygame
import abstract


class Player(abstract.Object):
    def __init__(self,  screen, level, path, pos, size, hit_rect=None, z_scale=1):
        x, y = pos[0] - level.st_pos[0], pos[1] - level.st_pos[1]
        super().__init__(screen, level, '3D', path, (x, y), size, z_scale=z_scale)
        self.move = ''
        self.rotate = ''
        self.move_frame = 400, 400
        self.speed_mv = 5
        self.speed_rt = 1
        self.energy = 100
        self.hp = 100
        self.bullets_in_shoot = []
        self.keys = set()
        self.status = '1'

    def draw(self):
        super().draw()
        for bullet in self.bullets_in_shoot:
            bullet.update()

    def shoot(self):
        pos = self.pos[0], self.pos[1]
        vec = -math.cos(self.angle * math.pi / 180), math.sin(self.angle * math.pi / 180)
        self.bullets_in_shoot.append(Bullet(self.screen, self, self.level, 'rocket', pos, (50, 16), vector=vec))

    def rotate_space(self):
        if self.rotate == 'left':
            self.angle -= self.speed_rt

        if self.rotate == 'right':
            self.angle += self.speed_rt

    def move_space(self):
        dx, dy = (self.speed_mv * math.cos(self.angle * math.pi / 180),
                  self.speed_mv * math.sin(self.angle * math.pi / 180))
        x, y = self.pos[0], self.pos[1]
        xx, yy = self.pos[0] + self.level.st_pos[0], self.pos[1] + self.level.st_pos[1]
        if self.move == 'forward':
            if self.level.inside_map((x - dx, y + dy)):
                if self.move_frame[0] < xx - dx < self.screen.get_width() - self.move_frame[0] and self.move_frame[1] < yy + dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x - dx, y + dy
                elif not self.move_frame[0] < xx - dx < self.screen.get_width() - self.move_frame[0] and not self.move_frame[1] < yy + dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x - dx, y + dy
                    self.level.move(dx, -dy)
                elif not self.move_frame[0] < xx - dx < self.screen.get_width() - self.move_frame[0]:
                    self.pos = x - dx, y + dy
                    self.level.move(dx, 0)
                elif not self.move_frame[1] < yy + dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x - dx, y + dy
                    self.level.move(0, -dy)

        if self.move == 'backward':
            if self.level.inside_map((x + dx, y - dy)):
                if self.move_frame[0] < xx + dx < self.screen.get_width() - self.move_frame[0] and self.move_frame[1] < yy - dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x + dx, y - dy
                elif not self.move_frame[0] < xx + dx < self.screen.get_width() - self.move_frame[0] and not self.move_frame[1] < yy - dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x + dx, y - dy
                    self.level.move(-dx, dy)
                elif not self.move_frame[0] < xx + dx < self.screen.get_width() - self.move_frame[0]:
                    self.pos = x + dx, y - dy
                    self.level.move(-dx, 0)
                elif not self.move_frame[1] < yy - dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x + dx, y - dy
                    self.level.move(0, dy)

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
                self.speed_mv = 15
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
                self.speed_mv = 5


class Bullet(abstract.Object):
    def __init__(self, screen, char, level, path, pos, size, damage=10, speed=25, vector=None, hit_rect=None, z_scale=0.5):
        super().__init__(screen, level, '3D', path, pos, size, z_scale=z_scale)
        self.char = char
        self.damage = damage
        self.speed = speed
        self.vector = vector
        self.status = '1'
        self.angle = pygame.Vector2(self.vector).angle_to((pygame.Vector2((1, 0))))

    def update(self):
        if self.vector is not None:
            x, y = self.pos
            dx, dy = self.vector
            self.pos = x + dx * self.speed, y + dy * self.speed
            if self.pos[0] + self.level.st_pos[0] < -200 or self.pos[1] + self.level.st_pos[1] < -200 or self.pos[0] + self.level.st_pos[0] > self.screen.get_width() + 200 or  self.pos[1] + self.level.st_pos[1] > self.screen.get_height() + 200:
                self.char.bullets_in_shoot.remove(self)
                del self
