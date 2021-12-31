import pygame


size = 600, 500

pygame.init()
screen = pygame.display.set_mode(size)

pygame.display.update()
clock = pygame.time.Clock()

running = True
start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

    clock.tick(30)
