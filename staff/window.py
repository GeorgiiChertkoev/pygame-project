import pygame
import pygame_gui
import sys
import itertools

size = w, h = 600, 520
FPS = 60
pygame.init()

screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)
bg = pygame.Surface(size)
bg.fill(-1)
BUT_SOUNDC = pygame.mixer.Sound('data/sounds/click_button.wav')
WALLPAPERS = itertools.cycle((
    'art0.jpg', 'art1.jpg', 'art2.jpg',
    'art3.jpg', 'art4.jpg', 'art5.jpg',
    'art6.jpg', 'art7.jpg', 'art8.jpg',
    'art9.jpg', 'art10.jpg', 'art11.jpg',
    'art12.jpg', 'art13.jpg', 'art14.jpg',
    'art15.jpg',))


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

            manager.process_events(event)

        pygame.transform.scale(pygame.image.load(f'data/wallpapers/{wallpaper}').convert(),
                               size, screen)
        manager.update(clock.tick(FPS) / 1000)
        manager.draw_ui(screen)
        pygame.display.update()


# clock = pygame.time.Clock()
# run = True
# while run:
#     fps = clock.tick(60) / 1000
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#     intro()

#     screen.blit(bg, (0, 0))
    # pygame.display.update()
d = {'qwe': 1123}
d1 = {
    'asd': 1
}

print(d | d1)