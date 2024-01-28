import math
import pygame
from abstract import SHIFT, ANGLE


class HUD:
    def __init__(self, screen, char, clock):
        pygame.font.init()
        self.max_blink_time = 10
        self.blink_time = self.max_blink_time
        self.health_color = (255, 0, 0)
        self.energy_color = (0, 255, 0)
        self.score_font = pygame.font.SysFont('Comic Sans MS', 16)
        self.score_font_label = pygame.font.SysFont('Comic Sans MS', 20)
        self.boss_hp_label = pygame.font.SysFont('Wide Latin', 30)
        self.screen = screen
        main_size = self.screen.get_width() // 3, self.screen.get_height() // 3
        self.char = char
        self.clock = clock
        self.back_layer = pygame.image.load("images\\gui\\back_gui.png")
        self.front_layer = pygame.image.load("images\\gui\\front_gui.png")
        self.boss_hp_front_layer = pygame.image.load("images\\gui\\boss_hp_front_gui.png")
        self.boss_hp_back_layer = pygame.image.load("images\\gui\\boss_hp_back_gui.png")
        gui_size = self.back_layer.get_size()
        self.back_layer = pygame.transform.scale(self.back_layer, main_size)
        self.front_layer = pygame.transform.scale(self.front_layer, main_size)
        self.boss_hp_front_layer = pygame.transform.scale(self.boss_hp_front_layer, (self.screen.get_width() * 0.9,
                                                                                     self.screen.get_height() * 0.2))
        self.boss_hp_back_layer = pygame.transform.scale(self.boss_hp_back_layer, (self.screen.get_width() * 0.9,
                                                                                     self.screen.get_height() * 0.2))
        self.coeff = main_size[0] / gui_size[0]
        self.rect = self.front_layer.get_rect()
        self.rect.bottomright = screen.get_size()
        self.hud_settings = {
            'heath_bar_shift_x': 424,
            'heath_bar_shift_y': 82,
            'heath_bar_shift_width': 260,
            'heath_bar_shift_height': 22,
            'energy_bar_shift_x': 408,
            'energy_bar_shift_y': 40,
            'energy_bar_shift_width': 264,
            'energy_bar_shift_height': 22,
            'score_text_x': 70,
            'score_text_y': 85,
            'score_x': 70,
            'score_y': 50,
            'red_x': 170,
            'red_y': 212,
            'green_x': 53,
            'green_y': 210,
            'level_x': 190,
            'level_y': 212,
            'level_width': 155,
            'level_height': 155,
        }
        self.level_map_scale = self.hud_settings['level_width'] * self.coeff / (self.char.level.size[0] * 200)

    def draw(self):
        self.screen.blit(self.back_layer, self.rect)
        x_hp, y_hp = (self.screen.get_width() - self.hud_settings['heath_bar_shift_x'] * self.coeff,
                      self.screen.get_height() - self.hud_settings['heath_bar_shift_y'] * self.coeff)
        w_hp, h_hp = (self.hud_settings['heath_bar_shift_width'] * self.coeff,
                      self.hud_settings['heath_bar_shift_height'] * self.coeff)
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x_hp, y_hp, w_hp * self.char.hp // 100, h_hp))

        x_en, y_en = (self.screen.get_width() - self.hud_settings['energy_bar_shift_x'] * self.coeff,
                      self.screen.get_height() - self.hud_settings['energy_bar_shift_y'] * self.coeff)
        w_en, h_en = (self.hud_settings['energy_bar_shift_width'] * self.coeff,
                      self.hud_settings['energy_bar_shift_height'] * self.coeff)
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(x_en, y_en, w_en * self.char.energy // 100, h_en))

        pos_score = (self.screen.get_width() - self.hud_settings['score_x'] * self.coeff,
                     self.screen.get_height() - self.hud_settings['score_y'] * self.coeff)
        text_surface = self.score_font.render(f'{self.char.score}', False, (0, 255, 0))
        self.screen.blit(text_surface, pos_score)
        health_tower_attacked = False
        for enemy in self.char.enemies:
            if enemy.obj_to_kill is not None and enemy.obj_to_kill.name == "heal_tower":
                health_tower_attacked = True
                break
        towers = [deco.name for deco in self.char.level.deco_list if 'tower' in deco.name]
        pos_red = (self.screen.get_width() - self.hud_settings['red_x'] * self.coeff,
                   self.screen.get_height() - self.hud_settings['red_y'] * self.coeff)
        pygame.draw.circle(self.screen, self.health_color, pos_red, 16)
        energy_tower_attacked = False
        for enemy in self.char.enemies:
            if enemy.obj_to_kill is not None and enemy.obj_to_kill.name == "energy_tower":
                energy_tower_attacked = True
                break
        if health_tower_attacked or energy_tower_attacked:
            self.blink_time -= 1
        else:
            self.blink_time = self.max_blink_time
        if self.blink_time == 0:
            self.blink_time = self.max_blink_time

            if 'heal_tower' in towers and health_tower_attacked:
                if self.health_color == (255, 0, 0):
                    self.health_color = (255, 255, 255)
                else:
                    self.health_color = (255, 0, 0)
            elif 'heal_tower' not in towers:
                self.health_color = (0, 0, 0)
            elif not health_tower_attacked:
                self.health_color = (255, 0, 0)

            if 'energy_tower' in towers and energy_tower_attacked:
                if self.energy_color == (0, 255, 0):
                    self.energy_color = (255, 255, 255)
                else:
                    self.energy_color = (0, 255, 0)
            elif 'energy_tower' not in towers:
                self.energy_color = (0, 0, 0)
            elif not energy_tower_attacked:
                self.energy_color = (0, 255, 0)

        pos_green = (self.screen.get_width() - self.hud_settings['green_x'] * self.coeff,
                     self.screen.get_height() - self.hud_settings['green_y'] * self.coeff)
        pygame.draw.circle(self.screen, self.energy_color, pos_green, 16)
        show_boss_hp = False
        for enemy in self.char.enemies:
            x_enemy_on_level, y_enemy_on_level = self.get_pos_on_map(enemy.pos)
            if enemy.name == 'croko':
                pygame.draw.rect(self.screen, (0, 0, 255),
                                 pygame.Rect(x_enemy_on_level - 5, y_enemy_on_level - 5, 10, 10))
            elif enemy.name == 'dino':
                pygame.draw.rect(self.screen, (0, 255, 0),
                                 pygame.Rect(x_enemy_on_level - 5, y_enemy_on_level - 5, 10, 10))
            elif enemy.name == 'boss_turtle':
                show_boss_hp = True
                pygame.draw.rect(self.screen, (128, 64, 48),
                                 pygame.Rect(x_enemy_on_level - 7, y_enemy_on_level - 7, 14, 14))
        x_char_on_level, y_char_on_level = self.get_pos_on_map(self.char.pos)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x_char_on_level - 7, y_char_on_level - 7, 14, 14))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x_char_on_level - 5, y_char_on_level - 5, 10, 10))

        self.screen.blit(self.front_layer, self.rect)

        pos_score_text = (self.screen.get_width() - self.hud_settings['score_text_x'] * self.coeff,
                          self.screen.get_height() - self.hud_settings['score_text_y'] * self.coeff)
        text_surface = self.score_font_label.render('Счет: ', False, (0, 0, 0))
        self.screen.blit(text_surface, pos_score_text)

        text_surface = self.score_font_label.render(f'FPS: {self.clock.get_fps():.2f} ', False, (0, 0, 0))
        self.screen.blit(text_surface, (0, 0))

        if show_boss_hp:
            boss = [enemy for enemy in self.char.enemies if enemy.name == 'boss_turtle'][0]
            self.screen.blit(self.boss_hp_back_layer,
                             (self.screen.get_width() * 0.05, 0))
            pygame.draw.rect(self.screen, (178, 34, 34), pygame.Rect(
                self.screen.get_width() * 0.08, self.screen.get_height() * 0.04 + 50,
                self.screen.get_width() * 0.85 * boss.hp / 5000, 65
            ))
            self.screen.blit(self.boss_hp_front_layer, (self.screen.get_width() * 0.05, 0))

    def get_pos_on_map(self, pos):
        st_x, st_y = (self.screen.get_width() - self.hud_settings['level_x'] * self.coeff,
                      self.screen.get_height() - self.hud_settings['level_y'] * self.coeff)
        rel_x, rel_y = (self.hud_settings['level_width'] * self.coeff * pos[0] /
                        (self.char.level.size[0] * self.char.level.plat.get_rect().size[0] - 2 * SHIFT),
                        self.hud_settings['level_height'] * self.coeff * pos[1] /
                        (ANGLE * self.char.level.size[1] * self.char.level.plat.get_rect().size[0] - 2 * SHIFT))

        return st_x + rel_x, st_y + rel_y


class Button:

    def __init__(self, screen, pos, text, size, image, pressed_image, font=('Comic Sans MS', 40, True)):
        self.font = pygame.font.SysFont(*font)
        self.screen = screen
        self.text = self.font.render(text, False, (238, 249, 93))
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image), self.size)
        self.pressed_image = pygame.transform.scale(pygame.image.load(pressed_image), self.size)
        self.click_rect = self.image.get_rect()
        self.click_rect.center = pos
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.pressed = False

    def draw(self):
        if not self.pressed:
            self.screen.blit(self.image, self.click_rect)
        else:
            self.screen.blit(self.pressed_image, self.click_rect)
        self.screen.blit(self.text, self.text_rect)

    def is_clicked(self, pos):
        return self.click_rect.collidepoint(pos)