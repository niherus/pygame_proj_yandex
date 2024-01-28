import math
import pygame
from abstract import Object, Bullet, Particles, WaveStrike


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
            if dist:
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

                if ((self.attack_type == 'close' and dist > 70) or dist > 500) and can_move:
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


class Boss(Object):

    def __init__(self, screen, level, image_pack, pos, char, z_scale=5):
        self.obj_to_kill = None
        pos = pos[0] - level.st_pos[0], pos[1] - level.st_pos[1]
        super().__init__(screen, level, image_pack, pos, name='boss_turtle', z_scale=z_scale)
        self.deco_to_hit = [deco for deco in level.deco_list if deco.status == 1]
        self.enemies = []
        self.speed_rt = 2
        self.hit_rect = pygame.Rect(0, 0, 200, 200)
        self.status = 1
        self.hp = 5000
        self.timing_max = 30
        self.timing = self.timing_max
        self.speed = 7
        self.vec = 1, 0
        self.actions = set()
        self.strike_frame = None
        self.cool_down = None

    def add_enemies(self, list_of_enemies):
        self.enemies.extend(list_of_enemies)

    def follow_char(self):
        self.deco_to_hit = [deco for deco in self.level.deco_list if deco.status == 1]
        self.enemies = [x for x in self.enemies if x.hp > 0]

        if self.enemies:
            self.timing -= 1
            self.obj_to_kill = min(self.enemies, key=lambda x: math.hypot(x.pos[0] - self.pos[0],
                                                                          x.pos[1] - self.pos[1]) - (
                                                                   lambda y: 200 if y == 'player' else 0)(x.name))
            x0, y0 = self.obj_to_kill.pos
            x1, y1 = self.pos
            dx, dy = x1 - x0, y1 - y0
            dist = math.hypot(dx, dy)
            if not dist:
                dist = 1

            dr, dangle = self.get_dangle(self.angle, pygame.Vector2(dx, dy).angle_to((1, 0)))
            next_pos = x1 - self.vec[0] * self.speed, y1 - self.vec[1] * self.speed
            count_fire = sum([1 for vfx in self.level.vfx_list if vfx.name == 'fire_breath'])
            if 'move' in self.actions and not count_fire and self.level.inside_map(next_pos):
                x, y = self.pos
                self.pos = x - self.vec[0] * self.speed, y - self.vec[1] * self.speed
                can_move, hit_thing = self.hit_deco()
                if not can_move:
                    hit_thing.to_kill = True

            if 'rotate' in self.actions and not count_fire:
                if dr:
                    self.angle += self.speed_rt
                else:
                    self.angle -= self.speed_rt
                self.vec = math.cos(self.angle * math.pi / 180), -math.sin(self.angle * math.pi / 180)

            if 'wave' in self.actions:
                self.level.vfx_list.append(WaveStrike(self.screen, self.level, self.pos, (200, 200),
                                                      (700, 700), 30))
                self.actions.discard('wave')

            if 'fire_breath' in self.actions:
                vec = -self.vec[0] * 20, -self.vec[1] * 20
                pos = self.pos[0] - self.vec[0] * 150, self.pos[1] - self.vec[1] * 150 - 50
                self.level.vfx_list.append(
                    Particles(self.screen, self.level, [(255, 64, 0), (255, 128, 0), (255, 192, 0)],
                              10, 200, 25, pos, vec, 20, 'fire_breath', life_time=50,
                              random_particle_size=0.5, random_particle_time=0.7, random_particle_angle=30))
                self.actions.discard('fire_breath')

            if not self.timing:
                self.timing = self.timing_max
                if dist > 200:
                    self.actions.add('move')
                else:
                    self.actions.discard('move')

                if dist < 300:
                    self.actions.add('wave')
                if 300 <= dist < 800 and abs(dangle) <= self.speed_rt:
                    self.actions.add('fire_breath')

                if abs(dangle) > self.speed_rt:
                    self.actions.add('rotate')
                else:
                    self.actions.discard('rotate')

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

    def hit_deco(self):
        for deco in self.deco_to_hit:
            if self.hit_obj(deco.hit_rect):
                return False, deco
        return True, None
