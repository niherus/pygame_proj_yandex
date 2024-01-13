from character_logic import *
from map_generating_logic import *


class ShooterWin:
    def __init__(self):
        width, height = 1900, 1060
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.level = Map_generator(self.screen, 25, 25)
        self.player = Player(self.screen, self.level, 'alien2', (width // 2, height // 2), (42, 40))

    def draw_priority(self):
        to_draw = [
            self.player,
            *self.player.bullets_in_shoot,
            *self.level.deco_list
        ]
        if self.player.bullets_in_shoot:
            print(self.player.bullets_in_shoot[0].pos)
        to_draw.sort(key=lambda obj: (obj.status, obj.pos[1], obj.pos[0]))
        for img in to_draw:
            if -self.player.move_frame[0] < img.pos[0] + self.level.st_pos[0] < self.screen.get_width() + self.player.move_frame[0] and \
                    -self.player.move_frame[1] < img.pos[1] + self.level.st_pos[1] < self.screen.get_height() + self.player.move_frame[1]:
                img.draw()

    def run(self):
        keys = set()
        while True:
            self.clock.tick(60)
            self.screen.fill("red")
            self.level.draw()
            self.draw_priority()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                self.player.control(ev)
            self.player.rotate_space()
            self.player.move_space()
            pygame.display.set_caption(f'{self.clock.get_fps()}')
            pygame.display.update()


ShooterWin().run()


#######################
# Нужно создать базовый класс для всех объектов на экране, базовый класс для ГУИ и наследовать все от него
# Нужно создавать все объекты внутри основного класса, где управлять порядком отрисовки и взаимодействием между объектами
# Перевести данные в формат векторов pygame

