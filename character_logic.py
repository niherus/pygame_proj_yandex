import pygame, math
class Player:
    def __init__(self, screen, x, y, cur_map, scale=2, path='alien'):
        self.pos = x, y
        self.map = cur_map
        self.scale = scale
        self.frames = self.import_images(path, self.scale)
        self.angle = 0
        self.move = ''
        self.rotate = ''
        self.screen = screen
        self.move_frame = 200, 200
        self.speed_mv = 5
        self.speed_rt = 1
    def import_images(self, path, scale):
        images = []
        for i in range(42):
            img = pygame.image.load(f'{path}\\{i}.png')
            images.append(pygame.transform.scale_by(img, scale))
        return images

    def draw(self):
        for i, img in enumerate(self.frames):
            r_img = pygame.transform.rotate(img, self.angle)
            rect = r_img.get_rect()
            rect.center = (self.pos[0], self.pos[1] - i * self.scale)
            self.screen.blit(r_img, rect)
        #print(self.map.get_cell_pos(self.pos))
    def rotate_space(self):
        if self.rotate == 'left':
            self.angle -= self.speed_rt

        if self.rotate == 'right':
            self.angle += self.speed_rt
    def inside_map(self, x, y):

        x_calc1, y_calc1 = (self.map.borders[1][0] - x + self.map.st_pos[0], self.map.borders[1][1] - y + self.map.st_pos[1])
        x_calc2, y_calc2 = (self.map.borders[2][0] - x + self.map.st_pos[0], self.map.borders[2][1] - y + self.map.st_pos[1])
        a1, a2 = math.acos(-1 * y_calc1 / math.hypot(x_calc1, y_calc1)) * 180 / math.pi, math.acos(y_calc2 / math.hypot(x_calc2, y_calc2)) * 180 / math.pi
        return True


    def move_space(self):
        dx, dy = self.speed_mv * math.cos(self.angle * math.pi / 180), self.speed_mv * math.sin(self.angle * math.pi / 180)
        x, y = self.pos
        if self.move == 'forward':

            if self.map.inside_map((x - dx, y + dy)):
                if self.move_frame[0] < x - dx < self.screen.get_width() - self.move_frame[0] and self.move_frame[1] < y + dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x - dx, y + dy
                elif not self.move_frame[0] < x - dx < self.screen.get_width() - self.move_frame[0] and not self.move_frame[1] < y + dy < self.screen.get_height() - self.move_frame[1]:
                    self.map.move(dx, -dy)
                elif not self.move_frame[0] < x - dx < self.screen.get_width() - self.move_frame[0]:
                    self.pos = x, y + dy
                    self.map.move(dx, 0)
                elif not self.move_frame[1] < y + dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x - dx, y
                    self.map.move(0, -dy)

        if self.move == 'backward':
            if self.map.inside_map((x + dx, y - dy)):
                if self.move_frame[0] < x + dx < self.screen.get_width() - self.move_frame[0] and self.move_frame[1] < y - dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x + dx, y - dy
                elif not self.move_frame[0] < x + dx < self.screen.get_width() - self.move_frame[0] and not self.move_frame[1] < y - dy < self.screen.get_height() - self.move_frame[1]:
                    self.map.move(-dx, dy)
                elif not self.move_frame[0] < x + dx < self.screen.get_width() - self.move_frame[0]:
                    self.pos = x, y - dy
                    self.map.move(-dx, 0)
                elif not self.move_frame[1] < y - dy < self.screen.get_height() - self.move_frame[1]:
                    self.pos = x + dx, y
                    self.map.move(0, dy)
            #self.pos = x + dx, y - dy

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

    pl = Player(screen, 500, 500)

    keys = set()
    angle = 0
    while on_going:
        Clock.tick(60)
        screen.fill(colors['window'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                keys.add(event.key)
                if event.key == 100:
                    pl.rotate = 'left'
                if event.key == 97:
                    pl.rotate = 'right'
                if event.key == 119:
                    pl.move = 'forward'
                if event.key == 115:
                    pl.move = 'backward'
            if event.type == pygame.KEYUP:
                keys.discard(event.key)
                if not {100, 97} & keys:
                    pl.rotate = ''
                if not {115, 119} & keys:
                    pl.move = ''

        pl.draw()
        pl.rotate_space(10)
        pl.move_space(2)
        pygame.display.update()

    pygame.quit()