import pygame.locals
from character_logic import *
from enemy_logic import Enemy
from map_generating_logic import *
from enemy_logic import *
from random import randint as rnd

class ShooterWin:
    def __init__(self):
        width, height = 1900, 1060
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode((width, height), pygame.locals.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.level = LevelGenerator(self.screen, 20, 20)
        self.player = Player(self.screen, self.level, 'alien2', (width // 2, height // 2), (63, 60))
        self.crokos = [Enemy(self.screen, self.level, 'croko', (rnd(0, width), rnd(0, height)),
                             (90, 28), self.player, z_scale=1, attack_type='close') for i in range(5)]
        self.dinos = [Enemy(self.screen, self.level, 'dino', (rnd(0, width), rnd(0, height)),
                            (50, 42), self.player, z_scale=1, attack_type='range') for i in range(5)]
        self.player.add_enemies(self.crokos)
        self.player.add_enemies(self.dinos)
        for croko in self.crokos:
            croko.add_enemies([self.player])
        for dino in self.dinos:
            dino.add_enemies([self.player])

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
            self.level.draw()
            self.draw_priority()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                self.player.control(ev)
            self.player.rotate_space()
            self.player.move_space()
            for dino in self.dinos:
                dino.follow_char()
            for croko in self.crokos:
                croko.follow_char()
            self.dinos = [dino for dino in self.dinos if dino.hp > 0]
            self.crokos = [croko for croko in self.crokos if croko.hp > 0]
            pygame.display.set_caption(f'{self.clock.get_fps()}')
            text_surface = self.my_font.render(f'{self.player.hp}', False, (255, 0, 0))
            self.screen.blit(text_surface, (100, 100))
            pygame.display.update()


if __name__ == '__main__':
    ShooterWin().run()


#######################
# базовый класс для ГУИ и наследовать все от него
# Зарядная и лечащая башни



