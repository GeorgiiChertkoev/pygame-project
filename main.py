import sys
import datetime
import itertools
import json
import pygame
import pygame_gui


w, h = size = 600, 520
tw, th = 40, 40
FPS = 60
levels_passed = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0
}
data = {
    'injured': 0,
    'deaths': 0
}

pygame.init()
pygame.event.set_blocked((pygame.MOUSEMOTION))
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)

BUT_SOUNDC = pygame.mixer.Sound('data/sounds/click_button.wav')
WALLPAPERS = itertools.cycle((
    'art0.jpg', 'art1.jpg', 'art2.jpg',
    'art3.jpg', 'art4.jpg', 'art5.jpg',
    'art6.jpg', 'art7.jpg', 'art8.jpg',
    'art9.jpg', 'art10.jpg', 'art11.jpg',
    'art12.jpg', 'art13.jpg', 'art14.jpg',
    'art15.jpg',))
heart = pygame.image.load("data/heart.png").convert_alpha()
empty_heart = pygame.image.load("data/empty_heart1.png").convert_alpha()


def exit():
    write_statistics()
    sys.exit()


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
                levels_passed[self.level] += 1
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
            data['injured'] += 1
        self.damaged = max(0, self.damaged - 1)
        if self.hp == 0:
            data['deaths'] += 1
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
        self.image = pygame.image.load(
            f'data/level{str(level)}/{str(value)}.png')
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


def write_statistics():
    seconds = pygame.time.get_ticks() // 1000
    data['time'] = seconds
    try:
        with open('data/stats.json') as f:
            old_d = json.load(f)
        has_old_data = True
    except Exception:
        has_old_data = False

    if has_old_data:
        new_stats = {
            'injured': old_d['injured'] + data['injured'],
            'deaths': old_d['deaths'] + data['deaths'],
            'time': old_d['time'] + data['time']
        }
        new_stats['levels'] = {}
        for k, v in levels_passed.items():
            new_stats['levels'][k] = v + old_d['levels'][k]
    else:
        new_stats = data
        new_stats['levels'] = levels_passed
    with open('data/stats.json', 'w') as f:
        f.write(json.dumps(new_stats))


def exit_diolog():
    exit_diolog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((150, 200), (300, 200)),
        manager=manager,
        window_title='Подтверждение',
        action_long_desc='Вы уверены что хотите выйти?',
        action_short_name='ОК',
        blocking=True
    )


def main_window():
    play_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 320), (400, 50)),
        text='Играть',
        manager=manager)

    statistics_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 380), (400, 50)),
        text='Статистика',
        manager=manager)

    exit_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 440), (400, 50)),
        text='Выход',
        manager=manager)

    wallpaper_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((540, 460), (60, 60)),
        text='Обои',
        manager=manager)


def levels_window():
    level1_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 50), (200, 50)),
        text='Уровень 1',
        manager=manager)

    level2_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 130), (200, 50)),
        text='Уровень 2',
        manager=manager)

    level3_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 210), (200, 50)),
        text='Уровень 3',

        manager=manager)

    level4_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 290), (200, 50)),
        text='Уровень 4',

        manager=manager)

    level5_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 370), (200, 50)),
        text='Уровень 5',

        manager=manager)

    exit_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 450), (200, 50)),
        text='Назад',
        manager=manager)


def intro():
    # start_window()
    manager.clear_and_reset()
    main_window_is_open = True
    levels_window_is_open = False
    wallpaper = next(WALLPAPERS)
    pygame.mixer.music.load('data/music/menu_music.mp3')
    pygame.mixer.music.play(-1)
    while True:
        if main_window_is_open:
            main_window()
        if levels_window_is_open:
            levels_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_diolog()
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                exit()
            # if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            #     return event.text.split()[1]
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                BUT_SOUNDC.set_volume(0.5)
                BUT_SOUNDC.play()
                if event.ui_element.text == 'Выход':
                    exit_diolog()

                elif event.ui_element.text == 'Играть':
                    main_window_is_open = False
                    levels_window_is_open = True
                    manager.clear_and_reset()

                elif event.ui_element.text == 'Обои':
                    wallpaper = next(WALLPAPERS)

                elif 'Уровень' in event.ui_element.text:
                    return event.ui_element.text.split()[1]

                elif event.ui_element.text == 'Назад':
                    main_window_is_open = True
                    levels_window_is_open = False
                    manager.clear_and_reset()
                elif event.ui_element.text == 'Статистика':
                    show_stats()

            manager.process_events(event)

        pygame.transform.scale(pygame.image.load(f'data/wallpapers/{wallpaper}').convert(),
                               size, screen)
        manager.update(clock.tick(FPS) / 10)
        manager.draw_ui(screen)
        pygame.display.update()


def time_in_game(form='str'):
    # form == 'str' or 'surf'
    milliseconds = pygame.time.get_ticks()
    hours, remainder = divmod(milliseconds // 1000, 3600)
    minutes, seconds = divmod(remainder, 60)
    human_format = 'время в игре {:02} ч {:02} мин {:02} сек'.format(
        int(hours), int(minutes), int(seconds))
    if form == 'str':
        return human_format
    elif form == 'surf':
        font = pygame.font.Font(None, 25)
        text = font.render(human_format, 0, 'white', 0)
        return text


def blackout(alpha=50, n=10, tick=30):
    transparent = pygame.Surface(size)
    transparent.set_alpha(alpha)
    # Плавный переход
    for i in range(n):
        screen.blit(transparent, (0, 0))
        pygame.display.flip()
        pygame.time.wait(tick)


def pause(level):
    blackout(alpha=10, n=10, tick=10)
    font = pygame.font.Font('data/fonts/casual.ttf', 30)
    text = font.render('Игра приостановлена', 0, 'white')
    t_rect = text.get_rect()
    screen.blit(text, (w // 2 - t_rect.w // 2, 50))

    font = pygame.font.Font('data/fonts/casual.ttf', 20)
    text = font.render(f'уровень {level}', 0, 'white')
    t_rect = text.get_rect()
    screen.blit(text, (w // 2 - t_rect.w // 2, 80))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
        surf = time_in_game(form='surf')
        screen.blit(surf, (surf.get_rect(
            bottomleft=screen.get_rect().bottomleft)))
        pygame.display.update()

        clock.tick(10)


def end_screen(level):
    font = pygame.font.Font('data/fonts/casual.ttf', 20)
    text = font.render('Вы проиграли', 0, 'red', 0)
    t_rect = text.get_rect()
    blackout()
    screen.blit(text, (w // 2 - t_rect.w // 2, 50))
    pygame.display.update()
    wait = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type in (pygame.KEYDOWN,
                              pygame.MOUSEBUTTONDOWN) and wait > FPS * 1.5:
                draw_map(intro())
        wait += 1
        clock.tick(FPS)


def show_stats():
    write_statistics()
    header = pygame.font.Font('data/fonts/casual.ttf', 30)
    text = header.render('Статистика', 0, 'white', 0)

    t_rect = text.get_rect()
    screen.fill(0)
    screen.blit(text, (w // 2 - t_rect.w // 2, 30))

    with open('data/stats.json') as f:
        statistic = json.load(f)
    inj = f"Ранен: {statistic['injured']}"
    deaths = f"Убит: {statistic['deaths']}"
    t_in_g = f"Время в игре: {str(datetime.timedelta(seconds=statistic['time']))}"
    
    font = pygame.font.Font(None, 30)
    for i, text in enumerate((inj, deaths, t_in_g)):
        text = font.render(text, 0, 'white', 0)
        screen.blit(text, (40, i * 30 + 80))

    header = pygame.font.Font('data/fonts/casual.ttf', 20)
    text = header.render('Пройденные уровни', 0, 'white', 0)
    t_rect = text.get_rect()
    screen.blit(text, (w // 2 - t_rect.w // 2, 200))

    for k, v in statistic['levels'].items():
        text = font.render(f'уровень {k}:   {v}', 0, 'white', 0)
        screen.blit(text, (40, int(k) * 30 + 210))


    # screen.fill(0)
    manager.clear_and_reset()
    back = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 450), (200, 50)),
        text='Назад',
        manager=manager)

    while True:
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                draw_map(intro())
            else:
        manager.update(clock.tick(FPS) / 10)
        manager.draw_ui(screen)
        pygame.display.update()
        clock.tick(FPS)

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
    level_time.tick()

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
level_time = pygame.time.Clock()
group_all = pygame.sprite.Group()

draw_map(intro())
