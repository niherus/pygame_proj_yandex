import pygame.locals
from character_logic import Player
from enemy_logic import Enemy, Boss
from map_generating_logic import LevelGenerator
from gui_logic import HUD, Button
from random import randint as rnd
from tower_logic import Tower
from time import perf_counter as pf
from base_logic import create_table, insert_row, get_data
import sqlite3
import os
import math


class ShooterWin:

    def __init__(self):
        self.score_base = sqlite3.connect("score_base.db")
        self.cur = self.score_base.cursor()
        create_table(self.cur, 'player_score', [
            'WIN INT',
            'SCORE INT',
            'TIME INT'
        ])

        width, height = 1600, 900
        pygame.init()
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.locals.DOUBLEBUF | pygame.SCALED | pygame.FULLSCREEN)
        self.mode = 'start_screen'
        self.st_time, self.fn_time = 0, 0
        #  start screen settings

        self.start_screen = pygame.transform.scale(pygame.image.load('images\\gui\\start.png'), self.screen.get_size())
        self.start_button = Button(self.screen, (width * 0.12, height * 0.9 - 390), 'START', (358, 132),
                                   'images\\gui\\button.png', 'images\\gui\\button_pressed.png')
        self.controls_button = Button(self.screen, (width * 0.12, height * 0.9 - 260), 'CONTROL', (358, 132),
                                      'images\\gui\\button.png', 'images\\gui\\button_pressed.png')
        self.records_button = Button(self.screen, (width * 0.12, height * 0.9 - 130), 'RECORDS', (358, 132),
                                     'images\\gui\\button.png', 'images\\gui\\button_pressed.png')
        self.exit_button = Button(self.screen, (width * 0.12, height * 0.9), 'EXIT', (358, 132),
                                  'images\\gui\\button.png', 'images\\gui\\button_pressed.png')
        self.control_screen = pygame.transform.scale(pygame.image.load('images\\gui\\controls.png'), (762, 482))
        self.score_screen = pygame.transform.scale(pygame.image.load('images\\gui\\top_ten.png'), (762, 482))
        self.show_control = False
        self.show_records = False
        #  main game setting

        self.clock = pygame.time.Clock()
        self.textures = self.all_texture_preload()

        self.end = False
        self.cooldown = 10
        self.game_stats = {'crokos': 0, 'dinos': 0}

        self.lava = pygame.transform.scale(pygame.image.load('images\\tiles\\lava.jpg'), self.screen.get_size())

        # end screen settings
        self.finish_screen = pygame.transform.scale(pygame.image.load('images\\gui\\finish.png'),
                                                    self.screen.get_size())
        self.res_font = pygame.font.SysFont('Comic Sans MS', 40, True)
        self.stat_font = pygame.font.SysFont('Comic Sans MS', 30, True)
        self.score_font = pygame.font.SysFont('Comic Sans MS', 30, True)

        self.restart_button = Button(self.screen, (width * 0.3, height * 0.9), 'RESTART', (358, 132),
                                     'images\\gui\\button.png', 'images\\gui\\button_pressed.png')
        self.run_away_button = Button(self.screen, (width * 0.72, height * 0.9), 'RUN AWAY', (358, 132),
                                      'images\\gui\\button.png', 'images\\gui\\button_pressed.png')

    def init_game(self):
        self.n_crokos = 2
        self.n_dinos = 1
        self.n_bosses = 0
        width, height = self.screen.get_size()
        self.level = LevelGenerator(self.screen, self.textures, 20, 20)
        self.player = Player(self.screen, self.level, self.textures['player'],
                             (width // 2, height // 2),
                             self.textures['rocket'])

        pos_towers = self.level.get_tower_coords()
        self.level.deco_list = [deco for deco in self.level.deco_list if
                                not self.player.hit_obj(deco.hit_rect)]
        self.bosses = []
        self.heal_tower = Tower(self.screen, self.level, self.player, self.textures['heal_tower'],
                                pos_towers['heal_tower'],
                                name='heal_tower')
        self.energy_tower = Tower(self.screen, self.level, self.player,
                                  self.textures['energy_tower'],
                                  pos_towers['energy_tower'], name='energy_tower')
        self.crokos = [
            Enemy(self.screen, self.level, self.textures['croko'], (rnd(0, width), rnd(0, height)),
                  self.player, name='croko', z_scale=1, attack_type='close') for _ in
            range(self.n_crokos)]
        self.dinos = [
            Enemy(self.screen, self.level, self.textures['dino'], (rnd(0, width), rnd(0, height)),
                  self.player, name='dino', bullet_image=self.textures['red_orb'], z_scale=1,
                  attack_type='range') for _ in range(self.n_dinos)]
        self.player.add_enemies(self.crokos)
        self.player.add_enemies(self.dinos)
        self.player.add_enemies(self.bosses)
        for croko in self.crokos:
            croko.add_enemies([self.player, self.heal_tower, self.energy_tower])
        for dino in self.dinos:
            dino.add_enemies([self.player, self.heal_tower, self.energy_tower])
        for boss in self.bosses:
            boss.add_enemies([self.player])

        self.end = False
        self.cooldown = 10
        self.game_stats = {'crokos': 0, 'dinos': 0}
        self.hud = HUD(self.screen, self.player, self.clock)
        self.dino_respawn_cooldown = 240
        self.dino_is_respawn = False
        self.croko_respawn_cooldown = 240
        self.croko_is_respawn = False
        self.boss_respawn_cooldown = 240

    def draw_priority(self):
        enemy_bullets = []
        for dino in self.dinos:
            enemy_bullets.extend(dino.bullets_in_shoot)
        to_draw = [
            self.player,
            *self.player.bullets_in_shoot,
            *self.level.deco_list,
            *self.level.vfx_list,
            *self.dinos,
            *enemy_bullets,
            *self.crokos,
            *self.bosses
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
            self.screen.fill("black")
            if self.mode == 'start_screen':
                self.screen.blit(self.start_screen, (0, 0))
                self.start_button.draw()
                self.controls_button.draw()
                self.records_button.draw()
                self.exit_button.draw()

                for ev in pygame.event.get():
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button.is_clicked(ev.pos):
                            self.start_button.pressed = True
                        if self.controls_button.is_clicked(ev.pos):
                            self.controls_button.pressed = True
                        if self.records_button.is_clicked(ev.pos):
                            self.records_button.pressed = True
                        if self.exit_button.is_clicked(ev.pos):
                            self.exit_button.pressed = True
                    if ev.type == pygame.MOUSEBUTTONUP:
                        self.start_button.pressed = False
                        self.controls_button.pressed = False
                        self.records_button.pressed = False
                        self.exit_button.pressed = False
                        if self.start_button.is_clicked(ev.pos):
                            self.mode = 'main_game'
                            self.init_game()
                            self.st_time = pf()
                        if self.controls_button.is_clicked(ev.pos):
                            self.show_control ^= True
                            self.show_records = False
                        if self.records_button.is_clicked(ev.pos):
                            self.show_records ^= True
                            self.show_control = False
                        if self.exit_button.is_clicked(ev.pos):
                            self.score_base.close()
                            return

                if self.show_control:
                    self.screen.blit(self.control_screen, (self.screen.get_width() * 0.12 + 360,
                                                           self.screen.get_height() * 0.2))
                if self.show_records:
                    self.screen.blit(self.score_screen, (self.screen.get_width() * 0.12 + 360,
                                                         self.screen.get_height() * 0.2))
                    data = sorted(get_data(self.cur, 'player_score'), key=lambda x: x[1])[-10:]
                    for i, row in enumerate(data[::-1]):
                        res = 'win' if row[0] else 'lose'
                        text = self.score_font.render(f'{i + 1}. {res} {row[1]} - {row[2]} seconds', False,
                                                      (255, 255, 255))
                        self.screen.blit(text,
                                         (self.screen.get_width() * 0.4, self.screen.get_height() * 0.25 + 30 * i))

            elif self.mode == 'main_game':
                self.screen.blit(self.lava, (0, 0))
                self.level.draw()
                self.draw_priority()
                for ev in pygame.event.get():
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        self.mode = 'start_screen'
                    if self.player.hp > 0:
                        self.player.control(ev)

                if self.player.hp <= 0 and not self.end:
                    self.end = True
                    self.fn_time = pf()
                    insert_row(self.cur, 'player_score', [
                        0, self.player.score, int(self.fn_time - self.st_time)
                    ])
                    self.score_base.commit()

                self.player.rotate_space()
                self.player.move_space()
                for dino in self.dinos:
                    dino.follow_char()
                    if dino.hp <= 0:
                        self.player.score += 100
                        self.game_stats['dinos'] += 1
                for croko in self.crokos:
                    croko.follow_char()
                    if croko.hp <= 0:
                        self.player.score += 100
                        self.game_stats['crokos'] += 1

                for boss in self.bosses:
                    boss.follow_char()
                    if boss.hp <= 0:
                        self.player.score += 5000
                for particle in self.level.vfx_list:
                    particle.update()

                self.clear_dead()
                self.respawn()
                self.hud.draw()
                if self.player.score > 8000 and not self.bosses and not self.end:
                    self.n_crokos = 0
                    self.n_dinos = 0
                    self.n_bosses = 0
                    self.end = True
                    self.fn_time = pf()
                    insert_row(self.cur, 'player_score', [
                        1, self.player.score + (self.heal_tower.hp > 0) * 1000 + (self.energy_tower.hp > 0) * 1000,
                        int(self.fn_time - self.st_time)
                    ])
                    self.score_base.commit()
                elif self.player.score > 3000:
                    self.n_crokos = 2
                    self.n_dinos = 2
                    self.n_bosses = 1
                elif self.player.score > 2000:
                    self.n_crokos = 5
                    self.n_dinos = 4
                    self.n_bosses = 0
                elif self.player.score > 1000:
                    self.n_crokos = 3
                    self.n_dinos = 2
                if self.end:
                    self.cooldown -= 1
                if self.cooldown <= 0:
                    self.mode = 'end_screen'
            elif self.mode == 'end_screen':
                self.screen.blit(self.finish_screen, (0, 0))
                if self.player.hp > 0:
                    res_text = self.res_font.render('YOU WIN!!!', False, (0, 0, 0))
                    stat_text = ('KILLED:',
                                 f"    CROKOS - {self.game_stats['crokos']} x 50 = {self.game_stats['crokos'] * 50}",
                                 f"    DINOS - {self.game_stats['crokos']} x 50 = {self.game_stats['crokos'] * 50}",
                                 '    BOSS - 1 x 5000 = 5000',
                                 f"HEATH TOWER - {int(self.heal_tower.hp > 0)} x 1000 = {(self.heal_tower.hp > 0) * 1000}",
                                 f"ENERGY TOWER - {int(self.energy_tower.hp > 0)} x 1000 = {(self.energy_tower.hp > 0) * 1000}",
                                 f'TIME - {int(self.fn_time - self.st_time)} SECONDS',
                                 '_____________________________',
                                 f"RESULT: {self.player.score + (self.heal_tower.hp > 0) * 1000 + (self.energy_tower.hp > 0) * 1000}"
                                 )
                else:
                    res_text = self.res_font.render('YOU LOSE!!!', False, (0, 0, 0))
                    stat_text = ('KILLED:',
                                 f"    CROKOS - {self.game_stats['crokos']} x 50 = {self.game_stats['crokos'] * 50}",
                                 f"    DINOS - {self.game_stats['crokos']} x 50 = {self.game_stats['crokos'] * 50}",
                                 f"TIME - {int(self.fn_time - self.st_time)} SECONDS",
                                 '_____________________________',
                                 f"RESULT: {self.player.score}"
                                 )

                res_text_rect = res_text.get_rect()
                res_text_rect.center = (self.screen.get_width() * 0.5, self.screen.get_height() * 0.35)
                self.screen.blit(res_text, res_text_rect)
                for i, text in enumerate(stat_text):
                    self.screen.blit(self.stat_font.render(text, False, (0, 0, 0)),
                                     (self.screen.get_width() * 0.3, self.screen.get_height() * 0.4 + 40 * i))
                self.restart_button.draw()
                self.run_away_button.draw()

                for ev in pygame.event.get():
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if self.restart_button.is_clicked(ev.pos):
                            self.restart_button.pressed = True
                        if self.run_away_button.is_clicked(ev.pos):
                            self.run_away_button.pressed = True

                    if ev.type == pygame.MOUSEBUTTONUP:
                        self.restart_button.pressed = False
                        self.run_away_button.pressed = False
                        if self.restart_button.is_clicked(ev.pos):
                            self.mode = 'main_game'
                            self.init_game()
                            self.st_time = pf()
                        if self.run_away_button.is_clicked(ev.pos):
                            self.mode = 'start_screen'

            pygame.display.update()

    def respawn(self):
        if len(self.dinos) < self.n_dinos and not self.dino_is_respawn:
            pos = (rnd(0, self.level.main_surf.get_width()), rnd(0, self.level.main_surf.get_height()))

            if (self.level.inside_map(pos) and
                    math.hypot(pos[0] - self.player.pos[0], pos[1] - self.player.pos[1]) > 2000):
                pos = pos[0] + self.level.st_pos[0], pos[1] + self.level.st_pos[1]
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
                pos = pos[0] + self.level.st_pos[0], pos[1] + self.level.st_pos[1]
                enemy = Enemy(self.screen, self.level, self.textures['croko'], pos,
                              self.player, name='croko', z_scale=1, attack_type='close')
                enemy.add_enemies([self.player, self.heal_tower, self.energy_tower])
                self.player.add_enemies([enemy])
                self.crokos.append(enemy)
                self.croko_is_respawn = True
        if self.n_bosses:
            self.boss_respawn_cooldown -= 1
        if len(self.bosses) < self.n_bosses and self.boss_respawn_cooldown <= 0:
            pos = (rnd(0, self.level.main_surf.get_width()), rnd(0, self.level.main_surf.get_height()))

            if (self.level.inside_map(pos) and
                    math.hypot(pos[0] - self.player.pos[0], pos[1] - self.player.pos[1]) > 1000):
                pos = pos[0] + self.level.st_pos[0], pos[1] + self.level.st_pos[1]
                boss = Boss(self.screen, self.level, self.textures['turtle'],
                            pos, self.player)
                boss.add_enemies([self.player])
                self.player.add_enemies([boss])
                self.bosses.append(boss)

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

    def clear_dead(self):
        self.dinos = list(filter(lambda x: not x.to_kill, self.dinos))
        self.crokos = list(filter(lambda x: not x.to_kill, self.crokos))
        self.bosses = list(filter(lambda x: not x.to_kill, self.bosses))
        self.level.vfx_list = list(filter(lambda x: not x.to_kill, self.level.vfx_list))

    def all_texture_preload(self):
        return {
            'player': self.load_texture('images\\alien', '3D', (63, 60)),
            'rocket': self.load_texture('images\\rocket', '3D', (50, 16)),
            'dino': self.load_texture('images\\dino', '3D', (50, 42)),
            'red_orb': self.load_texture('images\\dino\\red_orb.png', '2D', (25, 25)),
            'croko': self.load_texture('images\\croko', '3D', (90, 28)),
            'bone1': self.load_texture('images\\decorations\\bone1_0.png', '2D', (200, 84)),
            'bone2': self.load_texture('images\\decorations\\bone2_0.png', '2D', (60, 38)),
            'cactus1': self.load_texture('images\\decorations\\cactus1_1.png', '2D', (70, 110)),
            'cactus2': self.load_texture('images\\decorations\\cactus2_1.png', '2D', (70, 308)),
            'home': self.load_texture('images\\decorations\\home_1.png', '2D', (200, 250)),
            'stone1': self.load_texture('images\\decorations\\stone1_1.png', '2D', (100, 56)),
            'stone2': self.load_texture('images\\decorations\\stone2_1.png', '2D', (100, 58)),
            'tree1': self.load_texture('images\\decorations\\tree1_1.png', '2D', (300, 744)),
            'tree2': self.load_texture('images\\decorations\\tree2_1.png', '2D', (300, 698)),
            'heal_tower': self.load_texture('images\\towers\\tower_hp_1.png', '2D', (225, 661)),
            'energy_tower': self.load_texture('images\\towers\\tower_energy_1.png', '2D', (225, 661)),
            'turtle': self.load_texture('images\\boss', '3D', (280, 232))
        }

    @staticmethod
    def load_texture(path, dim, size):
        if dim.upper() == '2D':
            return tuple([pygame.transform.scale(pygame.image.load(path), size).convert_alpha()])
        elif dim.upper() == '3D':
            return tuple([pygame.transform.scale(pygame.image.load(f'{path}\\{i}.png').convert_alpha(), size)
                          for i in range(len(os.listdir(path))) if os.path.exists(f'{path}\\{i}.png')])
        raise ValueError("Wrong dimension type.\nIt's '2D' or '3D' only")


if __name__ == '__main__':
    ShooterWin().run()

#######################
# Добавить щит при рывке
# Добавить порталы рядом с башнями
# Добавить эффекты попадания (побеление)
# Сделать босса
# Сделать стартовое меню + база данных и рекорды
# Сделать конечное окно с перезапуском
# Сделать меню паузы
# Добавить звуки
# Сделать лончер (PyQT5)
