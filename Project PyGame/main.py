import random
import sys
import os
import pygame

FPS = 50

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
list_artifacts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4,
                  4, 4, 10, 10, 10, 10]
random.shuffle(list_artifacts)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                break
        pygame.display.flip()
        clock.tick(FPS)


def show_level():
    keeper = None
    player1 = None
    player2 = None
    player3 = None
    player4 = None
    d = {"top": (0, -1), "left": (-1, 0), "bottom": (0, 1), "right": (1, 0)}

    steps_keeper = ["right", "top", "top", "top", "left", "left", "left", "bottom", "bottom", "bottom", "bottom",
                    "bottom",
                    "right", "right", "right", "right", "right", "top", "top", "top", "top", "top", "top", "top",
                    "left",
                    "left", "left", "left", "left", "left", "left", "bottom", "bottom", "bottom", "bottom", "bottom",
                    "bottom",
                    "bottom", "bottom", "bottom"]

    steps_player = ["left", "bottom", "bottom", "bottom", "bottom",
                    "bottom",
                    "right", "right", "right", "right", "right", "top", "top", "top", "top", "top", "top", "top",
                    "left",
                    "left", "left", "left", "left", "left", "left", "bottom", "bottom", "bottom", "bottom", "bottom",
                    "bottom",
                    "bottom", "bottom", "bottom"]

    step_keeper = 0
    step_player1 = 0
    step_player2 = 0
    step_player3 = 0
    step_player4 = 0

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    keeper_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player3_group = pygame.sprite.Group()
    player4_group = pygame.sprite.Group()

    level = load_level('level1.txt')
    keeper, keeper_x, keeper_y, player1, player_x, player_y, player2, player3, player4 = generate_level(
        level, keeper_group, tiles_group, all_sprites, player_group, player3_group, player4_group)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and keeper is not None:
                    my_list = [1, 1, 2, 2, 3, 3, 4]
                    random.shuffle(my_list)
                    step_multiplier = my_list[0]
                    for _ in range(step_multiplier):
                        keeper.move(d[steps_keeper[step_keeper]], tiles_group)
                        step_keeper = (step_keeper + 1) % len(steps_keeper)
                elif event.key == pygame.K_1 and player1 is not None:
                    player1.move(d[steps_player[step_player1]], tiles_group)
                    step_player1 = (step_player1 + 1) % len(steps_player)
                elif event.key == pygame.K_2 and player2 is not None:
                    player2.move(d[steps_player[step_player2]], tiles_group)
                    step_player2 = (step_player2 + 1) % len(steps_player)
                elif event.key == pygame.K_3 and player3 is not None:
                    player3.move(d[steps_player[step_player3]], tiles_group)
                    step_player3 = (step_player3 + 1) % len(steps_player)
                elif event.key == pygame.K_4 and player4 is not None:
                    player4.move(d[steps_player[step_player4]], tiles_group)
                    step_player4 = (step_player4 + 1) % len(steps_player)

        all_sprites.draw(screen)
        keeper_group.draw(screen)
        player_group.draw(screen)
        player3_group.draw(screen)
        player4_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    tile_images = {
        'wall': load_image('2.jpg'),
        'bag': load_image('bag.jpg'),
        'exit': load_image('exit.jpg'),
        'empty': load_image('floor.jpg')
    }
    tile_width = tile_height = 50

    def __init__(self, tile_type, pos_x, pos_y, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = Tile.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            Tile.tile_width * pos_x, Tile.tile_height * pos_y)


class Keeper(pygame.sprite.Sprite):
    keeper_image = load_image('keeper.png')
    tile_width = tile_height = 50

    def __init__(self, pos_x, pos_y, keeper_group, all_sprites):
        super().__init__(keeper_group, all_sprites)
        self.image = Keeper.keeper_image
        self.rect = self.image.get_rect().move(
            Keeper.tile_width * pos_x, Keeper.tile_height * pos_y)
        self.direction = None
        self.x = pos_x
        self.y = pos_y

    def move(self, dest, tiles_group):
        dx, dy = dest
        self.rect.x += dx * Keeper.tile_width
        self.rect.y += dy * Keeper.tile_height
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * Keeper.tile_width
                self.rect.y -= dy * Keeper.tile_height


class Player(pygame.sprite.Sprite):
    player_image = load_image('blue.png')
    tile_width = tile_height = 50

    def __init__(self, pos_x, pos_y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.image = Player.player_image
        self.rect = self.image.get_rect().move(
            Player.tile_width * pos_x, Player.tile_height * pos_y)
        self.direction = None
        self.x = pos_x
        self.y = pos_y
        self.collected_artifacts1 = []

    def move(self, dest, tiles_group):
        dx, dy = dest
        self.rect.x += dx * Player.tile_width
        self.rect.y += dy * Player.tile_height
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * Player.tile_width
                self.rect.y -= dy * Player.tile_height
            elif tile_type == 'bag':
                artifact_value = random.choice(list_artifacts)
                self.collected_artifacts1.append(artifact_value)
                list_artifacts.remove(artifact_value)
                print(
                    f"Player 1 found artifact worth {artifact_value} money. Total money: {sum(self.collected_artifacts1)}")


class Player2(pygame.sprite.Sprite):
    player2_image = load_image('red.png')
    tile_width = tile_height = 50

    def __init__(self, pos_x, pos_y, player2_group, all_sprites):
        super().__init__(player2_group, all_sprites)
        self.image = Player2.player2_image
        self.rect = self.image.get_rect().move(
            Player2.tile_width * pos_x, Player2.tile_height * pos_y)
        self.direction = None
        self.x = pos_x
        self.y = pos_y
        self.collected_artifacts2 = []

    def move(self, dest, tiles_group):
        dx, dy = dest
        self.rect.x += dx * Player2.tile_width
        self.rect.y += dy * Player2.tile_height
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * Player2.tile_width
                self.rect.y -= dy * Player2.tile_height
            elif tile_type == 'bag':
                artifact_value = random.choice(list_artifacts)
                self.collected_artifacts2.append(artifact_value)
                list_artifacts.remove(artifact_value)
                print(
                    f"Player 2 found artifact worth {artifact_value} money. Total money: {sum(self.collected_artifacts2)}")


class Player3(pygame.sprite.Sprite):
    player3_image = load_image('yellow.png')
    tile_width = tile_height = 50

    def __init__(self, pos_x, pos_y, player3_group, all_sprites):
        super().__init__(player3_group, all_sprites)
        self.image = Player3.player3_image
        self.rect = self.image.get_rect().move(
            Player3.tile_width * pos_x, Player3.tile_height * pos_y)
        self.direction = None
        self.x = pos_x
        self.y = pos_y
        self.collected_artifacts3 = []

    def move(self, dest, tiles_group):
        dx, dy = dest
        self.rect.x += dx * Player3.tile_width
        self.rect.y += dy * Player3.tile_height
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * Player3.tile_width
                self.rect.y -= dy * Player3.tile_height
            elif tile_type == 'bag':
                artifact_value = random.choice(list_artifacts)
                self.collected_artifacts3.append(artifact_value)
                list_artifacts.remove(artifact_value)
                print(
                    f"Player 3 found artifact worth {artifact_value} money. Total money: {sum(self.collected_artifacts3)}")


class Player4(pygame.sprite.Sprite):
    player4_image = load_image('green.png')
    tile_width = tile_height = 50

    def __init__(self, pos_x, pos_y, player4_group, all_sprites):
        super().__init__(player4_group, all_sprites)
        self.image = Player4.player4_image
        self.rect = self.image.get_rect().move(
            Player4.tile_width * pos_x, Player4.tile_height * pos_y)
        self.direction = None
        self.x = pos_x
        self.y = pos_y
        self.collected_artifacts4 = []

    def move(self, dest, tiles_group):
        dx, dy = dest
        self.rect.x += dx * Player3.tile_width
        self.rect.y += dy * Player3.tile_height
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * Player3.tile_width
                self.rect.y -= dy * Player3.tile_height
            elif tile_type == 'bag':
                artifact_value = random.choice(list_artifacts)
                self.collected_artifacts4.append(artifact_value)
                list_artifacts.remove(artifact_value)
                print(
                    f"Player 3 found artifact worth {artifact_value} money. Total money: {sum(self.collected_artifacts4)}")


def generate_level(level, keeper_group, tiles_group, all_sprites, player_group, player3_group, player4_group):
    new_keeper, keeper_x, keeper_y, new_player1, player_x, player_y, new_player2, new_player3, new_player4 = None, None, None, None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                Tile('wall', x, y, tiles_group, all_sprites)
            elif level[y][x] == '@':
                Tile('bag', x, y, tiles_group, all_sprites)
            elif level[y][x] == 'z':
                Tile('exit', x, y, tiles_group, all_sprites)
            elif level[y][x] == '0':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_keeper = Keeper(x, y, keeper_group, all_sprites)
                keeper_x, keeper_y = x, y
            elif level[y][x] == '1':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player1 = Player(x, y, player_group, all_sprites)
                player_x, player_y = x, y
                new_player2 = Player2(x, y, player_group, all_sprites)
                new_player3 = Player3(x, y, player3_group, all_sprites)
                new_player4 = Player4(x, y, player4_group, all_sprites)

    return new_keeper, keeper_x, keeper_y, new_player1, player_x, player_y, new_player2, new_player3, new_player4


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


if __name__ == "__main__":
    start_screen()
    show_level()
