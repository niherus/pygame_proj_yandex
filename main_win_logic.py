import pygame.locals
from character_logic import *
from enemy_logic import Enemy
from map_generating_logic import *
from gui_logic import *
from random import randint as rnd
from tower_logic import Tower


class ShooterWin:

    def __init__(self):
        width, height = 1660, 900  # 1920, 1080
        pygame.init()
        pygame.font.init()
        self.n_crokos = 5
        self.n_dinos = 5
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.locals.DOUBLEBUF | pygame.SCALED | pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.textures = self.all_texture_preload()
        self.level = LevelGenerator(self.screen, self.textures, 20, 20)
        pos_towers = self.level.get_tower_coords()
        self.player = Player(self.screen, self.level, self.textures['player'], (width // 2, height // 2),
                             self.textures['rocket'])
        self.heal_tower = Tower(self.screen, self.level, self.player, self.textures['heal_tower'],
                                pos_towers['heal_tower'],
                                name='heal_tower')
        self.energy_tower = Tower(self.screen, self.level, self.player, self.textures['energy_tower'],
                                  pos_towers['energy_tower'], name='energy_tower')
        self.crokos = [Enemy(self.screen, self.level, self.textures['croko'], (rnd(0, width), rnd(0, height)),
                             self.player, name='croko', z_scale=1, attack_type='close') for _ in range(self.n_crokos)]
        self.dinos = [Enemy(self.screen, self.level, self.textures['dino'], (rnd(0, width), rnd(0, height)),
                            self.player, name='dino', bullet_image=self.textures['red_orb'], z_scale=1,
                            attack_type='range') for _ in range(self.n_dinos)]
        self.dino_respawn_cooldown = 60
        self.dino_is_respawn = False
        self.croko_respawn_cooldown = 60
        self.croko_is_respawn = False
        self.player.add_enemies(self.crokos)
        self.player.add_enemies(self.dinos)
        for croko in self.crokos:
            croko.add_enemies([self.player, self.heal_tower, self.energy_tower])
        for dino in self.dinos:
            dino.add_enemies([self.player, self.heal_tower, self.energy_tower])

        self.hud = HUD(self.screen, self.player)
        self.lava = pygame.transform.scale(pygame.image.load('lava.jpg'), self.screen.get_size())

    def draw_priority(self):
        enemy_bullets = []
        for dino in self.dinos:
            enemy_bullets.extend(dino.bullets_in_shoot)
        to_draw = [
            self.player,
            *self.player.bullets_in_shoot,
            *self.level.deco_list,
            *self.dinos,
            *enemy_bullets,
            *self.crokos,

        ]
        if self.heal_tower.hp > 0:
            to_draw.append(self.heal_tower)
        if self.energy_tower.hp > 0:
            to_draw.append(self.energy_tower)
        to_draw.sort(key=lambda obj: (obj.status, obj.pos[1], obj.pos[0]))
        for img in to_draw:
            x1, x, x2 = (-self.player.move_frame[0],
                         img.pos[0] + self.level.st_pos[0],
                         self.screen.get_width() + self.player.move_frame[0])
            y1, y, y2 = (-self.player.move_frame[1],
                         img.pos[1] + self.level.st_pos[1],
                         self.screen.get_height() + self.player.move_frame[1])
            if x1 < x < x2 and y1 < y < y2:
                img.draw()

    def run(self):
        while True:
            self.clock.tick(30)
            self.screen.fill("red")
            self.screen.blit(self.lava, (0, 0))
            self.level.draw()
            self.draw_priority()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    return

                self.player.control(ev)
            self.player.rotate_space()
            self.player.move_space()
            for dino in self.dinos:
                dino.follow_char()
                if dino.hp <= 0:
                    self.player.score += 50
            for croko in self.crokos:
                croko.follow_char()
                if croko.hp <= 0:
                    self.player.score += 50
            self.dinos = list(filter(lambda x: not x.to_kill, self.dinos))
            self.crokos = list(filter(lambda x: not x.to_kill, self.crokos))

            if len(self.dinos) < self.n_dinos and not self.dino_is_respawn:
                pos = (rnd(0, self.level.main_surf.get_width()), rnd(0, self.level.main_surf.get_height()))

                if (self.level.inside_map(pos) and
                        math.hypot(pos[0] - self.player.pos[0], pos[1] - self.player.pos[1]) > 2000):
                    enemy = Enemy(self.screen, self.level, self.textures['dino'], pos,
                                  self.player, name='dino', bullet_image=self.textures['red_orb'], z_scale=1,
                                  attack_type='range')
                    enemy.add_enemies([self.player, self.heal_tower, self.energy_tower])
                    self.player.add_enemies([enemy])
                    self.dinos.append(enemy)
                    self.dino_is_respawn = True

            if len(self.crokos) < self.n_crokos and not self.croko_is_respawn:
                pos = (rnd(0, self.level.main_surf.get_width()), rnd(0, self.level.main_surf.get_height()))

                if (self.level.inside_map(pos) and
                        math.hypot(pos[0] - self.player.pos[0], pos[1] - self.player.pos[1]) > 2000):
                    enemy = Enemy(self.screen, self.level, self.textures['croko'], pos,
                                  self.player, name='croko', z_scale=1, attack_type='close')
                    enemy.add_enemies([self.player, self.heal_tower, self.energy_tower])
                    self.player.add_enemies([enemy])
                    self.crokos.append(enemy)
                    self.croko_is_respawn = True
            if self.croko_is_respawn and self.croko_respawn_cooldown > 0:
                self.croko_respawn_cooldown -= 1
            elif self.croko_is_respawn:
                self.croko_is_respawn = False
                self.croko_respawn_cooldown = 30

            if self.dino_is_respawn and self.dino_respawn_cooldown > 0:
                self.dino_respawn_cooldown -= 1
            elif self.dino_is_respawn:
                self.dino_is_respawn = False
                self.dino_respawn_cooldown = 30

            self.hud.draw()
            if self.player.score > 3000:
                self.n_crokos = 1
                self.n_dinos = 1
            elif self.player.score > 2000:
                self.n_crokos = 10
                self.n_dinos = 10
            elif self.player.score > 1000:
                self.n_crokos = 7
                self.n_dinos = 7

            pygame.display.update()

    def all_texture_preload(self):
        return {
            'player': self.load_texture('alien2', '3D', (63, 60)),
            'rocket': self.load_texture('rocket', '3D', (50, 16)),
            'dino': self.load_texture('dino', '3D', (50, 42)),
            'red_orb': self.load_texture('dino\\red_orb.png', '2D', (25, 25)),
            'croko': self.load_texture('croko', '3D', (90, 28)),
            'bone1': self.load_texture('decorations\\bone1_0.png', '2D', (200, 84)),
            'bone2': self.load_texture('decorations\\bone2_0.png', '2D', (60, 38)),
            'cactus1': self.load_texture('decorations\\cactus1_1.png', '2D', (70, 110)),
            'cactus2': self.load_texture('decorations\\cactus2_1.png', '2D', (70, 308)),
            'home': self.load_texture('decorations\\home_1.png', '2D', (200, 250)),
            'stone1': self.load_texture('decorations\\stone1_1.png', '2D', (100, 56)),
            'stone2': self.load_texture('decorations\\stone2_1.png', '2D', (100, 58)),
            'tree1': self.load_texture('decorations\\tree1_1.png', '2D', (300, 744)),
            'tree2': self.load_texture('decorations\\tree2_1.png', '2D', (300, 698)),
            'heal_tower': self.load_texture('towers\\tower_hp_1.png', '2D', (225, 661)),
            'energy_tower': self.load_texture('towers\\tower_energy_1.png', '2D', (225, 661)),
        }

    @staticmethod
    def load_texture(path, dim, size):
        if dim.upper() == '2D':
            return tuple([pygame.transform.scale(pygame.image.load(path), size)])
        elif dim.upper() == '3D':
            return tuple([pygame.transform.scale(pygame.image.load(f'{path}\\{i}.png'), size)
                          for i in range(len(os.listdir(path))) if os.path.exists(f'{path}\\{i}.png')])
        raise ValueError("Wrong dimension type.\nIt's '2D' or '3D' only")


if __name__ == '__main__':
    ShooterWin().run()

#######################
# Добавить щит при рывке
# Добавить эффекты попадания (побеление)
# Сделать босса
# Сделать стартовое меню + база данных и рекорды
# Сделать конечное окно с перезапуском
# Сделать меню паузы
# Добавить звуки
# Сделать лончер (PyQT5)
