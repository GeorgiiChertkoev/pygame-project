import pygame
import pytmx

size = w, h = 672, 608
FPS = 15
MAPS_DIR = 'maps'
MUSICS_DIR = 'music'
TILE_SIZE = 32


# def cut_sprite_list(path, row, col):
#     sheet = pygame.image.load(path)
#     rect = pygame.Rect(0, 0, sheet.get_width() // col,
#                        sheet.get_height() // row)
#
#     frames = []
#     for x in range(row):
#         for y in range(col):
#             frame_location = (rect.w * y, rect.h * x)
#             frames.append(sheet.subsurface(pygame.Rect(
#                 frame_location, rect.size)))
#     return frames
#
#
# class Sprite(pygame.sprite.Sprite):
#     def __init__(self, pos):
#         super().__init__(self.group)
#         self.rect = self.image.get_rect(center=pos)

def start_menu():
    pass


class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.w, self.h = self.map.width, self.map.height
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tiles = finish_tile

    def render(self, screen):
        for x in range(self.w):
            for y in range(self.h):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]

    def is_free_tile(self, pos):
        return self.get_tile_id(pos) in self.free_tiles


class Hero:
    def __init__(self, pos):
        self.x, self.y = pos

    def get_position(self):
        return self.x, self.y

    def set_position(self, pos):
        self.x, self.y = pos

    def render(self, screen):
        center = (self.x * TILE_SIZE + TILE_SIZE // 2,
                  self.y * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(screen, -1, center, TILE_SIZE // 2)


class Game:
    def __init__(self, labyrinth, hero):
        self.labyrinth = labyrinth
        self.hero = hero

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero.render(screen)

    def update_hero(self):
        # if not pygame.sprite.spritecollideany(self, Platform.group):
        # self.rect.y += 1
        next_x, next_y = self.hero.get_position()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            next_x += 1
        if keys[pygame.K_LEFT]:
            next_x -= 1
        if keys[pygame.K_UP]:
            next_y -= 1
        if keys[pygame.K_DOWN]:
            next_y += 1

        if self.labyrinth.is_free_tile((next_x, next_y)):
            self.hero.set_position((next_x, next_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    pygame.mixer.music.load(f'{MUSICS_DIR}/caravan.ogg.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)

    labyrinth = Labyrinth('1mission_map.tmx', [30], 46)
    hero = Hero((0, 1))
    game = Game(labyrinth, hero)

    clock = pygame.time.Clock()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        game.update_hero()
        screen.fill(-1)
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
