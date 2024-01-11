import pygame, math


class Map_generator:
    def __init__(self, screen, width=100, height=100):

        self.screen = screen
        self.size = width, height
        self.plat = pygame.transform.scale_by(pygame.image.load('ntile.png'), 0.5)
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
                                    self.h // 2 + (i * 0.5773502691896257 * self.h + j * 0.5773502691896257 * self.h) / 2)
                self.main_surf.blit(self.plat, self.rect)
        self.borders = (
            (round(mw // 2 + (0 * self.w + 0 * self.w * -1) / 2),
             round(self.h // 2  + (0 * 0.5773502691896257 * self.h + 0 * 0.5773502691896257 * self.h) / 2) - 50),
            (round(mw // 2 + (0 * self.w + (self.size[1]) * self.w * -1) / 2),
             round(self.h // 2  + (0 * 0.5773502691896257 * self.h + (self.size[1] ) * 0.5773502691896257 * self.h) / 2) - 50),
            (round(mw // 2 + ((self.size[0]) * self.w + 0 * self.w * -1) / 2),
             round(self.h // 2  + ((self.size[0]) * 0.5773502691896257 * self.h + 0 * 0.5773502691896257 * self.h) / 2 ) - 50),
            (round(mw // 2 + ((self.size[0] - 1) * self.w + (self.size[1] - 1) * self.w * -1) / 2),
             round(self.h // 2  + ((self.size[0]) * 0.5773502691896257 * self.h + (self.size[1]) * 0.5773502691896257 * self.h) / 2) - 50)
        )
        print(*self.borders, sep='\n')
        pygame.draw.circle(self.main_surf, (255, 0, 0), self.borders[0], 20)
        pygame.draw.circle(self.main_surf, (0, 255, 0), self.borders[1], 20)
        pygame.draw.circle(self.main_surf, (0, 0, 255), self.borders[2], 20)
        pygame.draw.circle(self.main_surf, (255, 255, 0), self.borders[3], 20)
    def move(self, dx, dy):
        self.st_pos = self.st_pos[0] + dx, self.st_pos[1] + dy

    def draw(self):
        self.screen.blit(self.main_surf, self.st_pos)

    def distance(self, p1, p2, p0):
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        return abs(dy * p0[0] - dx * p0[1] + p2[0] * p1[1] - p2[1] * p1[0]) / math.hypot(dx, dy)

    def get_cell_pos(self, pos):
        x, y = pos[0] - self.st_pos[0], pos[1] - self.st_pos[1]
        dx = (self.distance(self.borders[0], self.borders[1], (x, y)) / 0.577) / 173.2
        dy = (self.distance(self.borders[0], self.borders[2], (x, y)) / 0.577) / 173.2
        return int(dx), int(dy)

    def inside_map(self, pos):
        x, y = pos[0] - self.st_pos[0], pos[1] - self.st_pos[1]
        x1, x2, x3 = self.borders[1][0],  self.borders[0][0], self.borders[2][0]
        y1, y2, y3 = self.borders[1][1], self.borders[0][1], self.borders[2][1]
        shift = 50

        if x1 < x < x2 and abs(y - y1) < x / (3 ** 0.5) - shift:
            return True
        elif x2 <= x < x3 and abs(y - y1) < (x3 - x) / (3 ** 0.5) - shift:
            return True

        return False


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