import pygame


w, h = size = 600, 500
tw, th = 60, 60


pygame.init()
screen = pygame.display.set_mode(size)


def cut_sprite_list(path, row, col):
    sheet = pygame.image.load(path)
    rect = pygame.Rect(0, 0, sheet.get_width() // col,
                       sheet.get_height() // row)

    frames = []
    for j in range(row):
        for i in range(col):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


class Sprite(pygame.sprite.Sprite):
    tick = 0
    def __init__(self, pos):
        super().__init__(self.group)
        self.rect = self.image.get_rect(center=pos)


class Tile(pygame.sprite.Sprite):
    floor = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    groups = floor, walls
    bg = pygame.image.load('data/bg_tile2.png')
    wall = pygame.Surface((60, 60))
    wall.fill(0)
    images = (bg, wall)

    def __init__(self, pos, value):
        super().__init__(self.groups[value])
        self.value = value
        self.image = Tile.images[value]
        self.rect = self.image.get_rect(center=pos)

    """
    есть показатель верхняя ли это стенка
    """

    def update(self):
        pass


class Hero(Sprite):
    # image = pygame.image.load('data/hero_1.png')
    group = pygame.sprite.GroupSingle()
    stay_sprites = cut_sprite_list('data/hero_moves/idle.png', 1, 3)
    image = stay_sprites[0]
    cur_frame = 0

    def update(self):
        # if not pygame.sprite.spritecollideany(self, Platform.group):
        # self.rect.y += 1

        keys = pygame.key.get_pressed()

        delta = ((keys[pygame.K_d] - keys[pygame.K_a] +
                  keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3,
                 (keys[pygame.K_DOWN] - keys[pygame.K_UP] +
                  keys[pygame.K_s] - keys[pygame.K_w]) * 3)

        if delta != (0, 0):
            old_rect = self.rect
            self.rect = self.rect.move(delta)
            if pygame.sprite.spritecollideany(self, Tile.walls):
                if any(pygame.sprite.collide_mask(self, sp) for sp in Tile.walls):
                    self.rect = old_rect
            self.cur_frame = 0

        else:
            if not self.tick % 6:
                self.image = self.stay_sprites[self.cur_frame]
                self.cur_frame = (self.cur_frame + 1) % 3
        self.tick = (self.tick + 1) % 60


sc_center = pygame.math.Vector2(screen.get_rect().center)
clock = pygame.time.Clock()


a = Hero(sc_center)
print(a.rect)

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
    dmap = {'.': 0, '#': 1, '@': 2}
    for y in range(len(data)):
        for x in range(len(data[0])):
            value = dmap[data[y][x]]
            if value == 2:
                hero = Hero((x * tw, y * th))
                value = 0
            Tile((x * tw, y * th), value)
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

    Hero.group.draw(screen)
    Hero.group.update()

    pygame.display.update()
    clock.tick(60)
