import pygame


w, h = size = 600, 500

pygame.init()
screen = pygame.display.set_mode(size)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(self.group)
        self.rect = self.image.get_rect(center=pos)


class Tile(Sprite):
    """
    есть показатель верхняя ли это стенка
    """
    pass


class Hero(Sprite):
    image = pygame.image.load('data/Player_Idle_Run_Stop.png').convert()
    group = pygame.sprite.GroupSingle()

    def update(self):
        # if not pygame.sprite.spritecollideany(self, Platform.group):
            # self.rect.y += 1
        keys = pygame.key.get_pressed()
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3


sc_center = screen.get_rect().center
clock = pygame.time.Clock()


Hero(sc_center)

running = True
start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)
    Hero.group.draw(screen)
    Hero.group.update()

    pygame.display.update()
    clock.tick(30)
