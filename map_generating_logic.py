import pygame, math


class Map_generator:
    def __init__(self, screen, width=100, height=100):

        self.screen = screen
        self.size = width, height
        self.plat = pygame.transform.scale_by(pygame.image.load('tile_test.png'), 0.5)
        self.rect = self.plat.get_rect()
        self.w, self.h = self.rect.size
        self.st_pos = -width * self.w / 2 + self.screen.get_width() / 2, -height * self.h / 4 + self.screen.get_height() / 2
        self.main_surf = pygame.Surface((width * self.w, height * self.h // 2 + self.h))
        self.main_surf.set_colorkey((0, 0, 0, 0))
        self.generate_all()
    def generate_all(self):
        pygame.draw.circle(self.main_surf, (255, 0, 0), (0, 0), 20)

        mw, mh = self.main_surf.get_size()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.rect.center = (mw // 2 + (i * self.w + j * self.w * -1) / 2,
                                    self.h // 2 + (i * 0.5 * self.h + j * 0.5 * self.h) / 2)
                self.main_surf.blit(self.plat, self.rect)

        self.borders = (
            (round(mw // 2 + (0 * self.w + 0 * self.w * -1) / 2),
             round(self.h // 2  + (0 * 0.5 * self.h + 0 * 0.5 * self.h) / 2)),
            (round(mw // 2 + (0 * self.w + (self.size[1] - 1) * self.w * -1) / 2),
             round(self.h // 2  + (0 * 0.5 * self.h + (self.size[1] - 1) * 0.5 * self.h) / 2)),
            (round(mw // 2 + ((self.size[0] - 1) * self.w + 0 * self.w * -1) / 2),
             round(self.h // 2  + ((self.size[0] - 1) * 0.5 * self.h + 0 * 0.5 * self.h) / 2)),
            (round(mw // 2 + ((self.size[0] - 1) * self.w + (self.size[1] - 1) * self.w * -1) / 2),
             round(self.h // 2  + ((self.size[0] - 1) * 0.5 * self.h + (self.size[1] - 1) * 0.5 * self.h) / 2))
        )
    def move(self, dx, dy):
        self.st_pos = self.st_pos[0] + dx, self.st_pos[1] + dy

    def draw(self):
        self.screen.blit(self.main_surf, self.st_pos)




if __name__ == '__main__':
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    colors = {
        'window': (40, 40, 150)
    }
    Clock = pygame.time.Clock()
    on_going = True
    mp = Map_generator(screen, 100, 100)

    while on_going:
        Clock.tick(60)
        screen.fill(colors['window'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        mp.draw()
        pygame.display.update()

    pygame.quit()