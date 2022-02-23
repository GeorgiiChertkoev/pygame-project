import pygame
import pygame_gui


w, h = size = 600, 520
tw, th = 40, 40
FPS = 60


pygame.init()
pygame.event.set_blocked((pygame.MOUSEMOTION))
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)

heart = pygame.image.load("data/heart.png").convert_alpha()
empty_heart = pygame.image.load("data/empty_heart1.png").convert_alpha()
menu_pic = 'data/fon.jpg'


class Hero(pygame.sprite.Sprite):
    group = pygame.sprite.GroupSingle()
    image = pygame.image.load('data/hero.png')
    im3 = pygame.image.load('data/hero3.png')
    im2 = pygame.image.load('data/hero2.png')
    im1 = pygame.image.load('data/hero1.png')
    im0 = pygame.image.load('data/hero0.png')
    im_nums = (im3, im2, im1, im0)

    def __init__(self, pos, level, hp=3):
        super().__init__(self.group)
        self.hp = hp
        self.damaged = 0
        self.complete = 0
        self.level = level
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if self.complete > 10:
            n = self.complete // FPS
            if n == 3:
                draw_map(intro())
            self.image = self.im_nums[n]
        elif self.complete == 0:
            self.image = Hero.image

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
        if pygame.sprite.spritecollideany(
                self, Enemy.group) and not self.damaged:
            self.hp -= 1
            self.damaged = 30
        self.damaged = max(0, self.damaged - 1)
        if self.hp == 0:
            end_screen(1)
        try:
            collided = pygame.sprite.spritecollide(self, group_all, False)
            # print(collided)
            if len(collided) == 1 and collided[0].value == 2:
                self.complete += 1
            else:
                self.complete = 0
                # print(collided[0].value)
        except Exception:
            self.complete = 0


class Tile(pygame.sprite.Sprite):
    floor = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    escape = pygame.sprite.Group()
    groups = floor, walls, escape

    def __init__(self, pos, level, value):
        super().__init__(self.groups[value])
        group_all.add(self)
        self.value = value
        if value != 2:
            self.image = pygame.image.load(
                f'data/level{str(level)}/{str(value)}.png')
        else:
            self.image = pygame.image.load('data/escape.png')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    group = pygame.sprite.Group()
    image = pygame.image.load('data/enemy1.png')

    def __init__(self, pos, move_style=(0, 0), speed=0):
        # move_style = direction
        super().__init__(self.group)
        group_all.add(self)
        self.tick = 0
        self.value = 10
        self.delta = pygame.math.Vector2(move_style) * speed
        self.image = Enemy.image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        old_rect = self.rect
        self.rect = self.rect.move(self.delta)
        if (pygame.sprite.spritecollideany(self, Tile.walls) or
            pygame.sprite.spritecollideany(self, Tile.escape)
                or not screen.get_rect().contains(self.rect)):
            self.delta *= -1
            self.rect = old_rect


class Hearts(pygame.sprite.Sprite):
    group = pygame.sprite.GroupSingle()

    def __init__(self, hero):
        super().__init__(self.group)
        self.hero = hero
        self.old_hp = 4
        self.update()
        self.rect = self.image.get_rect()

    def update(self):
        if self.old_hp == self.hero.hp:
            return
        surf = pygame.Surface((120, 40))
        surf.fill((4, 0, 0))
        surf.set_colorkey((4, 0, 0, 255))
        for i in range(0, 3):
            if self.hero.hp >= i + 1:
                surf.blit(heart, (i * 40, 0))
            else:
                surf.blit(empty_heart, (i * 40, 0))

        # surf.set_alpha(255)
        self.image = surf
        self.old_hp == self.hero.hp


def start_window():
    level1_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 50), (100, 50)),
        text='1',
        manager=manager)

    level2_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 150), (100, 50)),
        text='2',
        manager=manager)

    level3_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 250), (100, 50)),
        text='3',
        manager=manager)

    level4_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 350), (100, 50)),
        text='4',
        manager=manager)

    level5_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 450), (100, 50)),
        text='5',
        manager=manager)


def intro():
    start_window()
    pygame.transform.scale(pygame.image.load(menu_pic).convert(),
                           size, screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                return event.ui_element.text
            manager.process_events(event)

        manager.draw_ui(screen)
        manager.update(clock.tick(FPS))
        pygame.display.update()


def blackout(alpha=50, n=10):
    transparent = pygame.Surface(size)
    transparent.set_alpha(alpha)
    # Плавный переход
    for i in range(n):
        screen.blit(transparent, (0, 0))
        pygame.display.flip()
        pygame.time.wait(30)


def pause(level):
    blackout(alpha=10, n=10)
    font = pygame.font.Font('data/fonts/casual.ttf', 30)
    text = font.render('Игра приостановлена', 0, 'white', 0)
    t_rect = text.get_rect()
    screen.blit(text, (w // 2 - t_rect.w // 2, 50))

    font = pygame.font.Font('data/fonts/casual.ttf', 20)
    text = font.render(f'уровень {level}', 0, 'white', 0)
    t_rect = text.get_rect()
    screen.blit(text, (w // 2 - t_rect.w // 2, 80))

    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            break
            # print(1)
        # print(event)


def end_screen(level):
    font = pygame.font.Font('data/fonts/casual.ttf', 20)
    text = font.render('Вы проиграли', 0, 'red', 0)
    t_rect = text.get_rect()
    blackout()
    screen.blit(text, (w // 2 - t_rect.w // 2, 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type in (pygame.KEYDOWN,
                              pygame.MOUSEBUTTONDOWN):
                draw_map(intro())


def load_map(filename):
    lines = open(filename).readlines()
    maxlen = max(map(len, lines)) - 1
    return [x.rstrip().ljust(maxlen, '.') for x in lines], maxlen, len(lines)


def draw_map(level):
    data, w, h = load_map(f'data/level{level}/map.txt')
    dmap = {'.': 0, '#': 1, '1': 2,
            '@': 3, '-': (1, 0),
            '|': (0, 1)}
    cleaner()
    for y in range(len(data)):
        for x in range(len(data[0])):
            value = dmap[data[y][x]]
            pos = (x * tw, y * th)
            if value == 3:
                # герой
                hero = Hero(pos, level)
                value = 0
            if isinstance(value, tuple):
                Enemy(pos, move_style=value, speed=4)
                value = 0
            Tile(pos, level, value)
    Tile.floor.draw(screen)
    Tile.walls.draw(screen)
    Enemy.group.draw(screen)

    updater(hero, level)


def updater(hero, level):
    Hearts(hero)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(level)
        # screen.fill(0)

        Tile.walls.update()
        Tile.walls.draw(screen)
        Tile.floor.update()
        Tile.floor.draw(screen)
        Tile.escape.update()
        Tile.escape.draw(screen)

        Hero.group.draw(screen)
        Hero.group.update()

        Enemy.group.draw(screen)
        Enemy.group.update()

        Hearts.group.update()
        Hearts.group.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


def cleaner():
    Tile.walls.empty()
    Tile.floor.empty()
    Tile.escape.empty()
    Hero.group.empty()
    Enemy.group.empty()
    Hearts.group.empty()
    group_all.empty()


pygame.display.update()
clock = pygame.time.Clock()
group_all = pygame.sprite.Group()

# running = 0

draw_map(intro())
