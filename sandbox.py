import os
import pygame

'''
class Rain:
    def __init__(self, screen, speed):
        self.screen = screen
        self.speed = speed
        self.effect = pygame.Surface(self.screen.get_size())
        self.color = (0, 0, 50)
        self.effect.fill(self.color)
        self.effect.set_alpha(50)
        self.rain1 = self.make_rain(pygame.Surface(self.screen.get_size()))
        self.rain1.set_colorkey((0, 0, 0))
        self.rain2 = self.make_rain(pygame.Surface(self.screen.get_size()))
        self.rain1.set_colorkey((0, 0, 0))
        self.y1 = -self.screen.get_size()[1]
        self.y2 = 0
        self.time = random.randint(500, 1000)
        self.k = 6

    def make_rain(self, image):
        for i in range(1000):
            x, y = random.randint(0, self.screen.get_size()[0]), random.randint(0, self.screen.get_size()[1])
            pygame.draw.line(image, (0, 0, 50), (x, y), (x, y + 4), 2)
        return image

    def update(self):
        self.time -= 1
        if not self.time and self.color == (0, 0, 50) and self.k == 4:
            self.color = (255, 255, 255)
            self.effect.fill(self.color)
            self.time = 10
            self.k -= 1
        elif not self.time and self.color == (255, 255, 255) and self.k > 0:
            self.color = (0, 0, 50)
            self.effect.fill(self.color)
            self.time = 5
            self.k -= 1
        elif not self.time and self.color == (0, 0, 50) and self.k > 0:
            self.color = (255, 255, 255)
            self.effect.fill(self.color)
            self.time = 10
            self.k -= 1
        elif self.k == 0:
            self.color = (0, 0, 50)
            self.effect.fill(self.color)
            self.time = random.randint(500, 1000)
            self.k = 4

        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= self.screen.get_size()[1]:
            self.y1 -= 2 * self.screen.get_size()[1]
        if self.y2 >= self.screen.get_size()[1]:
            self.y2 -= 2 * self.screen.get_size()[1]
    def draw(self):
        self.screen.blit(self.effect, (0, 0))
        self.screen.blit(self.rain1, (0, self.y1))
        self.screen.blit(self.rain1, (0, self.y2))
colors = {
    'window': (40, 40, 150)
}
'''


class Object(pygame.sprite.Sprite):
    def __init__(self, image, pos, size, angle):
        super().__init__()
        self.pos = pos
        self.base_image = image
        self.size = size
        self.angle = angle
        self.vec = -1, 0
        self.rot = 0
        self.image = pygame.transform.rotate(pygame.transform.scale(self.base_image, self.size), self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, *args, **kwargs):
        self.angle += 1
        self.pos = self.pos[0] + self.vec[0], self.pos[1] + self.vec[1]
        self.image = pygame.transform.rotate(pygame.transform.scale(self.base_image, self.size), self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        print(1)



