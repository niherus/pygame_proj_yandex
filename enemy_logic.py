import math
import pygame
from abstract import Object, Bullet, ANGLE


class Enemy(Object):
    def __init__(self, screen, level, image_pack, pos, char, name, bullet_image=None, attack_type='close', z_scale=1):
        x, y = pos[0] - level.st_pos[0], pos[1] - level.st_pos[1]
        super().__init__(screen, level, image_pack, (x, y), name=name, z_scale=z_scale, status=1)
        self.hit_rect = pygame.Rect(0, 0, 53, 50)
        self.char = char
        self.attack_type = attack_type
        if attack_type == 'range':
            self.bullet_image = bullet_image
            self.bullets_in_shoot = []
        self.speed = 5
        self.deco_to_hit = [deco for deco in level.deco_list if deco.status == 1]
        self.cool_down = 50
        self.strike_frame = 0
        self.damage = 10
        self.hp = 100
        self.bullets_in_shoot = []
        self.enemies = []
        self.obj_to_kill = None
        self.speed_rt = 5

    def add_enemies(self, list_of_enemies):
        self.enemies.extend(list_of_enemies)

    def hit_deco(self):
        for deco in self.deco_to_hit:
            if self.hit_obj(deco.hit_rect):
                return False, deco
        return True, None

    def follow_char(self):
        self.deco_to_hit = [deco for deco in self.level.deco_list if deco.status == 1]
        self.enemies = [x for x in self.enemies if x.hp > 0]
        if self.enemies:
            self.obj_to_kill = min(self.enemies,
                                   key=lambda x: math.hypot(x.pos[0] - self.pos[0], x.pos[1] - self.pos[1]) -
                                                 (lambda y: 200 if y == 'player' else 0)(x.name))
            x0, y0 = self.obj_to_kill.pos
            x1, y1 = self.pos
            dx, dy = x1 - x0, y1 - y0

            dist = math.hypot(dx, dy)
            vec = dx / dist, dy / dist

            dr, dangle = self.get_dangle(self.angle, pygame.Vector2(vec).angle_to((1, 0)))

            if dangle < self.speed_rt:
                self.angle = pygame.Vector2(vec).angle_to((1, 0))

            elif dr:
                self.angle += self.speed_rt
            else:
                self.angle -= self.speed_rt

            vec = math.cos(self.angle * math.pi / 180), -math.sin(self.angle * math.pi / 180)
            self.hit_rect.center = (x1 - vec[0] * self.speed, y1 - vec[1] * self.speed)
            can_move, hit_thing = self.hit_deco()
            if self.attack_type == 'boss' and not can_move:
                hit_thing.to_kill = True

            elif ((self.attack_type == 'close' and dist > 70) or dist > 500) and can_move:
                self.pos = x1 - vec[0] * self.speed, y1 - vec[1] * self.speed
            elif not can_move:
                self.bite_object(hit_thing)

            self.action(dist)

    def action(self, dist):
        if dist < 100 and self.attack_type == 'close':
            self.bite_object(self.obj_to_kill)
        if dist < 500 and self.attack_type == 'range':
            self.shoot_object()

    def shoot_object(self):
        if self.strike_frame:
            self.strike_frame -= 1
        else:
            self.strike_frame = self.cool_down
            up = 20
            vec = -math.cos(self.angle * math.pi / 180), math.sin(self.angle * math.pi / 180)
            pos = self.pos[0], self.pos[1] - up
            self.bullets_in_shoot.append(Bullet(self.screen, self, self.level, self.bullet_image, pos, 'red_orb',
                                                vector=vec, hit_rect=pygame.Rect(0, 0, 20, 20)))

    def bite_object(self, other):
        if self.strike_frame:
            self.strike_frame -= 1
        else:
            other.hp -= self.damage
            self.strike_frame = self.cool_down

    def draw(self):
        super().draw()
        self.bullets_in_shoot = list(filter(lambda x: not x.to_kill, self.bullets_in_shoot))
        for bullet in self.bullets_in_shoot:
            bullet.update()

    @staticmethod
    def get_dangle(alpha1, alpha2):
        if alpha1 > alpha2:
            r1 = alpha1 - alpha2
            r2 = alpha2 - alpha1 + 360
            return r1 > r2, min(r1, r2)
        else:
            r1 = alpha2 - alpha1
            r2 = alpha1 - alpha2 + 360
            return r1 < r2, min(r1, r2)


class Boss(Enemy):

    def __init__(self, screen, level, image_pack, pos, char, z_scale=5):
        super().__init__(screen, level, image_pack, pos, char, name='boss_turtle', attack_type='boss', z_scale=z_scale)
        self.speed_rt = 1
        self.hit_rect = pygame.Rect(0, 0, 200, 200)