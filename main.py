import pygame


w, h = size = 600, 500

pygame.init()
screen = pygame.display.set_mode(size)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(self.group)
        self.rect = self.image.get_rect(center=pos)


class Tile(Sprite):
    group = pygame.sprite.Group()
    bg = pygame.image.load('data/bg_tile2.png')
    wall = pygame.Surface((62, 62))
    wall.fill(0)

    """
    есть показатель верхняя ли это стенка
    """


    def update(self):
        pass


class Floor(Tile):
    value = 0
    image = Tile.bg
    # group = pygame.sprite.Group()

class Wall(Tile):
    value = 1
    image = Tile.wall

class Hero(Sprite):
    image = pygame.image.load('data/hero_1.png')
    group = pygame.sprite.GroupSingle()

    def update(self):
        # if not pygame.sprite.spritecollideany(self, Platform.group):
        # self.rect.y += 1
        keys = pygame.key.get_pressed()

        self.rect.x += (keys[pygame.K_d] - keys[pygame.K_a] +
                        keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP] +
                        keys[pygame.K_s] - keys[pygame.K_w]) * 3


sc_center = pygame.math.Vector2(screen.get_rect().center)
clock = pygame.time.Clock()


Hero(sc_center)

# рисуем карту
for row in range(0, h + 60, 60):
    for col in range(0, w + 60, 60):
        if (col / 60) % 2:
            Floor((row, col))
        else:
            Wall((row, col))

# def load_map(filename=''):




running = True
start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    Floor.group.draw(screen)
    Floor.group.update()

    Hero.group.draw(screen)
    Hero.group.update()

    pygame.display.update()
    clock.tick(30)
