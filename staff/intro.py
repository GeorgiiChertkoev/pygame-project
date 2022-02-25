import pygame
import pygame_gui
import sys

size = w, h = 800, 600
FPS = 60
pygame.init()

screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)
bg = pygame.Surface(size)
bg.fill('red')


def start_window():
    level1_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 50), (100, 50)),
        text='1',
        manager=manager)

    level2_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 150), (100, 50)),
        text='2',
        manager=manager)

    level3_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 250), (100, 50)),
        text='3',
        manager=manager)

    level4_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 350), (100, 50)),
        text='4',
        manager=manager)

    level5_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 450), (100, 50)),
        text='5',
        manager=manager)


def intro():
    start_window()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                return event.ui_element.text
            manager.process_events(event)

        pygame.transform.scale(pygame.image.load('data/fon.jpg').convert(),
                               size, screen)
        manager.update(clock.tick(FPS) / 1000)
        manager.draw_ui(screen)
        pygame.display.update()


# clock = pygame.time.Clock()
# print(intro())
# run = True
# # run = 0
# while run:
#     fps = clock.tick(60) / 1000
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     screen.blit(bg, (0, 0))
#     pygame.display.update()
from collections import Counter

print(Counter({'1': 1, '2': 0, '3': 0, '4': 0, '5': 0}) + Counter({'2': 1, '1': 0, '3': 0, '4': 0, '5': 0}))