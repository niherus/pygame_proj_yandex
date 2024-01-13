import os
import pygame


class Object:

    def __init__(self, screen, level, dim, path, pos, size, angle=0, status=0, hit_rect=None, z_scale=1):
        self.screen = screen
        self.level = level
        self.dim = dim
        self.pos = pos[0], pos[1]
        self.size = size
        self.image_pack = self.load(path, dim, size)
        self.status = status
        self.hit_rect = hit_rect
        self.z_scale = z_scale
        self.angle = angle

    def draw(self):
        for i, img in enumerate(self.image_pack):
            r_image = pygame.transform.rotate(img, self.angle)
            rect = r_image.get_rect()
            rect.center = (self.pos[0] + self.level.st_pos[0],
                           self.pos[1] - i * self.z_scale + self.level.st_pos[1])
            self.screen.blit(r_image, rect)

    @staticmethod
    def load(path, dim, size):
        if dim.upper() == '2D':
            return [pygame.transform.scale(pygame.image.load(path), size)]
        elif dim.upper() == '3D':
            return [pygame.transform.scale(pygame.image.load(f'{path}\\{i}.png'), size)
                    for i in range(len(os.listdir(path))) if os.path.exists(f'{path}\\{i}.png')]
        raise ValueError("Wrong dimension type.\nIt's '2D' or '3D' only")
