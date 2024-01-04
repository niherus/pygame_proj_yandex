from character_logic import *
from map_generating_logic import *
pygame.init()

WIDTH, HEIGHT = 1900, 1060
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

colors = {
    'window': (40, 40, 150)
}
Clock = pygame.time.Clock()
on_going = True
mp = Map_generator(screen, 10, 10)
pl = Player(screen, WIDTH // 2, HEIGHT // 2, mp)

keys = set()
angle = 0
while on_going:
    Clock.tick(60)
    screen.fill(colors['window'])
    mp.draw()
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
            if event.key == 1073742049:
                pl.speed_mv = 15
            if event.key == 1073742048:
                pl.angle += 180

        if event.type == pygame.KEYUP:
            keys.discard(event.key)
            if not {100, 97} & keys:
                pl.rotate = ''
            if not {115, 119} & keys:
                pl.move = ''
            if not {1073742049} & keys:
                pl.speed_mv = 5

    pl.draw()
    pl.rotate_space()
    pl.move_space()
    pygame.display.update()

pygame.quit()