import pygame


def cut_sprite_list(path, row, col, output_name=''):
    sheet = pygame.image.load(path)
    rect = pygame.Rect(0, 0, sheet.get_width() // col,
                       sheet.get_height() // row)

    frames = []
    for j in range(row):
        for i in range(col):
            frame_location = (rect.w * i, rect.h * j)
            sub_surf = sheet.subsurface(pygame.Rect(
                frame_location, rect.size))
            frames.append(sub_surf)
            pygame.image.save(sub_surf, f'data/{output_name}_{col * j + i}.png')
    return frames


if __name__ == "__main__":
    cut_sprite_list(input('path: '),
                    int(input('row: ')),
                    int(input('col: ')),
                    output_name=input('output_name: '))
