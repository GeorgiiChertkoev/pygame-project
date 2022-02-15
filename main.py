import pygame


w, h = size = 600, 520
tw, th = 40, 40


pygame.init()
screen = pygame.display.set_mode(size)


class Tile(pygame.sprite.Sprite):
    floor = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    escape = pygame.sprite.Group()
    groups = floor, walls, escape

    def __init__(self, pos, level, value):
        super().__init__(self.groups[value])
        self.value = value
        self.image = pygame.image.load(
            f'data/level{str(level)}/{str(value)}.png')
        if value == 2:
            print(f'data/level{str(level)}/{str(value)}.png')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass


class Hero(pygame.sprite.Sprite):
    group = pygame.sprite.GroupSingle()
    image = pygame.image.load('data/hero.png')

    def __init__(self, pos):
        super().__init__(self.group)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        # if not pygame.sprite.spritecollideany(self, Platform.group):
        # self.rect.y += 1

        keys = pygame.key.get_pressed()

        delta = ((keys[pygame.K_d] - keys[pygame.K_a] +
                  keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3,
                 (keys[pygame.K_DOWN] - keys[pygame.K_UP] +
                  keys[pygame.K_s] - keys[pygame.K_w]) * 3)

        old_rect = self.rect
        self.rect = self.rect.move(delta)
        if (pygame.sprite.spritecollideany(self, Tile.walls)
            or not screen.get_rect().contains(self.rect)):
            self.rect = old_rect


class Enemy(pygame.sprite.Sprite):
    group = pygame.sprite.Group()
    image = pygame.image.load('data/enemy.png')

    def __init__(self, pos, move_style=(0, 0), speed=5):
        # move_style = direction
        super().__init__(self.group)
        self.tick = 0
        self.delta = pygame.math.Vector2(move_style) * 5
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        old_rect = self.rect
        self.rect = self.rect.move(self.delta)
        if (pygame.sprite.spritecollideany(self, Tile.walls)
            or not screen.get_rect().contains(self.rect)):
            self.delta *= -1
            self.rect = old_rect




clock = pygame.time.Clock()


# a = Hero(sc_center)
# print(a.rect)

# рисуем карту
# for row in range(0, h + 60, 60):
#     for col in range(0, w + 60, 60):
#         if (col / 60) % 2:
#             Tile((row, col))
#         else:
#             Tile((row, col), 1)


def load_map(filename):
    lines = open(filename).readlines()
    maxlen = max(map(len, lines)) - 1
    return [x.rstrip().ljust(maxlen, '.') for x in lines], maxlen, len(lines)


def draw_map(filename='1.map'):
    data, w, h = load_map(filename)
    surface = pygame.Surface((w * tw, h * th))
    dmap = {'.': 0, '#': 1, '1': 2, '@': 3, '-':}
    for y in range(len(data)):
        for x in range(len(data[0])):
            value = dmap[data[y][x]]
            if value == 3:
                # герой
                hero = Hero((x * tw, y * th))
                value = 0
            Tile((x * tw, y * th), 1, value)
    Tile.floor.draw(surface)
    Tile.walls.draw(surface)
    return surface, hero


bg, hero = draw_map()
scene = bg.copy()

area = screen.get_rect(center=hero.rect.center)
Hero.group.draw(scene)
screen.blit(scene, (0, 0), area)
pygame.display.update()


running = True
start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    Tile.walls.update()
    Tile.walls.draw(screen)
    Tile.floor.update()
    Tile.floor.draw(screen)
    Tile.escape.update()
    Tile.escape.draw(screen)


    Hero.group.draw(screen)
    Hero.group.update()

    pygame.display.update()
    clock.tick(60)
