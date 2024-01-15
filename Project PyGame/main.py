import random
import sys
import os
import pygame
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

FPS = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = '710, 120'

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Хранитель. Сокровища Богов Египта")

list_artifacts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3,
                  4, 4, 4, 4, 4, 10, 10, 10, 10]

random.shuffle(list_artifacts)
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
    intro_text = ["", "        Хранитель. Сокровища Богов Египта.",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "                              Тясачи лет он охранял",
                  "                              несметные богатства древней",
                  "                              пирамиды, но люди дерзнули",
                  "                              нарушить его покой..."]

    fon = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    button_color = (0, 0, 0)
    hover_color = (50, 50, 50)

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    button_rect = pygame.Rect(150, 200, 200, 60)
    button_text = font.render("Начать играть", True, 'white')
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    qt_window.show()
                    qt_window2.show()
                    break

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))
        pygame.display.flip()


def show_level():
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
    player2_group = pygame.sprite.Group()
    player3_group = pygame.sprite.Group()
    player4_group = pygame.sprite.Group()

    level = load_level('level1.txt')
    keeper, keeper_x, keeper_y, player1, player_x, player_y, player2, player3, player4 = generate_level(
        level, keeper_group, tiles_group, all_sprites, player_group, player2_group, player3_group, player4_group)

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
        player4_group.draw(screen)
        player3_group.draw(screen)
        player2_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    tile_images = {
        'wall': load_image('wall.jpg'),
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
                    f'1 Игрок: "{artifact_value}" list: {self.collected_artifacts1}')


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
                    f'2 Игрок: "{artifact_value}" list: {self.collected_artifacts2}')


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
                    f'3 Игрок: "{artifact_value}" list: {self.collected_artifacts3}')


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
                    f'4 Игрок: "{artifact_value}" list: {self.collected_artifacts4}')


def generate_level(level, keeper_group, tiles_group, all_sprites, player_group, player2_group, player3_group,
                   player4_group):
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
                new_player2 = Player2(x, y, player2_group, all_sprites)
                new_player3 = Player3(x, y, player3_group, all_sprites)
                new_player4 = Player4(x, y, player4_group, all_sprites)

    return new_keeper, keeper_x, keeper_y, new_player1, player_x, player_y, new_player2, new_player3, new_player4


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class QtWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.card_deck1 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]
        self.card_deck2 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]
        self.card_deck3 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]
        self.card_deck4 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]

        self.card_deck5_1 = [1, 2, 3, 4]
        self.card_deck5_2 = [1, 2, 3, 4]
        self.card_deck5_3 = [1, 2, 3, 4]
        self.card_deck5_4 = [1, 2, 3, 4]
        self.color_card = ["blue", "red", "yellow", "green"] * 4
        random.shuffle(self.card_deck1)
        random.shuffle(self.card_deck2)
        random.shuffle(self.card_deck3)
        random.shuffle(self.card_deck4)
        random.shuffle(self.card_deck5_1)
        random.shuffle(self.card_deck5_2)
        random.shuffle(self.card_deck5_3)
        random.shuffle(self.card_deck5_4)

        random.shuffle(self.color_card)

        self.selected_number = None
        self.border_image_botton = None
        self.carrent_player = [1, 2, 3, 4, 5]
        self.step = 0

        self.selected_number1 = None
        self.selected_number2 = None
        self.selected_number3 = None
        self.selected_number4 = None
        self.selected_number5 = None
        self.keeper_color_card = None

        self.initUI()

    def initUI(self):
        self.setGeometry(710, 690, 500, 300)
        self.setFixedSize(500, 300)
        self.setWindowTitle("Хранитель. Сокровища Богов Египта")
        self.setWindowIcon(QIcon('data/icon.png'))
        self.setStyleSheet("background-color: rgb(150,75,0);")
        self.button1_text = None
        self.button2_text = None
        self.button3_text = None

        self.button1_text = str(self.card_deck1[-3])
        self.button2_text = str(self.card_deck1[-2])
        self.button3_text = str(self.card_deck1[-1])
        self.border_image_botton = 'data/1.jpg'

        font_size = 4

        self.button1 = QPushButton(self.button1_text, self)
        self.button1.setObjectName('button1')
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setFixedHeight(230)
        self.button1.setFont(QFont('Arial', font_size * self.button1.font().pointSize()))

        self.button2 = QPushButton(self.button2_text, self)
        self.button2.setObjectName('button2')
        self.button2.clicked.connect(self.button2_clicked)
        self.button2.setFixedHeight(230)
        self.button2.setFont(QFont('Arial', font_size * self.button2.font().pointSize()))

        self.button3 = QPushButton(self.button3_text, self)
        self.button3.setObjectName('button3')
        self.button3.clicked.connect(self.button3_clicked)
        self.button3.setFixedHeight(230)
        self.button3.setFont(QFont('Arial', font_size * self.button3.font().pointSize()))

        self.button1.setStyleSheet(
            f"QPushButton{{border-image: url({self.border_image_botton}); color: black;}}")
        self.button2.setStyleSheet(
            f"QPushButton{{border-image: url({self.border_image_botton}); color: black;}}")
        self.button3.setStyleSheet(
            f"QPushButton{{border-image: url({self.border_image_botton}); color: black;}}")

        spacing = 8

        vbox = QHBoxLayout()
        vbox.addWidget(self.button1)
        vbox.addSpacing(spacing)
        vbox.addWidget(self.button2)
        vbox.addSpacing(spacing)
        vbox.addWidget(self.button3)

        self.setLayout(vbox)

    def get_current_player_card_deck(self):
        player_number = self.carrent_player[self.step % len(self.carrent_player)]
        if player_number == 1:
            return self.card_deck1, 1
        elif player_number == 2:
            return self.card_deck2, 2
        elif player_number == 3:
            return self.card_deck3, 3
        elif player_number == 4:
            return self.card_deck4, 4
        elif player_number == 5:
            color_card_deck_map = {"blue": self.card_deck5_1, "red": self.card_deck5_2,
                                   "yellow": self.card_deck5_3, "green": self.card_deck5_4}
            return color_card_deck_map[self.keeper_color_card], 5

    def button1_clicked(self):
        self.card_deck = self.get_current_player_card_deck()
        self.handle_selection(self.card_deck[0][-3], 3)

    def button2_clicked(self):
        self.card_deck = self.get_current_player_card_deck()
        if not (self.card_deck[1] == 5):
            self.handle_selection(self.card_deck[0][-2], 2)
        else:
            self.handle_selection(self.card_deck[0][-1], 2)

    def button3_clicked(self):
        self.card_deck = self.get_current_player_card_deck()
        self.handle_selection(self.card_deck[0][-1], 1)

    def handle_selection(self, selectednumber, num):
        self.selected_number = selectednumber

        self.num = -num

        if self.carrent_player[self.step % len(self.carrent_player)] == 1:
            self.card_deck1.pop(self.num)
            self.card_deck1 = self.card_deck1[-2:] + self.card_deck1[:-2]
            self.selected_number1 = self.selected_number
        elif self.carrent_player[self.step % len(self.carrent_player)] == 2:
            self.card_deck2.pop(self.num)
            self.card_deck2 = self.card_deck2[-2:] + self.card_deck2[:-2]
            self.selected_number2 = self.selected_number
        elif self.carrent_player[self.step % len(self.carrent_player)] == 3:
            self.card_deck3.pop(self.num)
            self.card_deck3 = self.card_deck3[-2:] + self.card_deck3[:-2]
            self.selected_number3 = self.selected_number
        elif self.carrent_player[self.step % len(self.carrent_player)] == 4:
            self.card_deck4.pop(self.num)
            self.card_deck4 = self.card_deck4[-2:] + self.card_deck4[:-2]
            self.selected_number4 = self.selected_number
        elif self.carrent_player[self.step % len(self.carrent_player)] == 5:
            self.selected_number5 = self.selected_number
            if self.keeper_color_card == "blue":
                self.card_deck5_1.pop(-1)
            elif self.keeper_color_card == "red":
                self.card_deck5_2.pop(-1)
            elif self.keeper_color_card == "yellow":
                self.card_deck5_3.pop(-1)
            elif self.keeper_color_card == "green":
                self.card_deck5_4.pop(-1)

        if self.carrent_player[self.step % len(self.carrent_player)] == 5:
            if self.keeper_color_card == "blue":
                if self.selected_number1 < self.selected_number5:
                    self.selected_number5 = self.selected_number5 + self.selected_number1
                elif self.selected_number1 == self.selected_number5:
                    self.selected_number5 = 0
                    self.selected_number1 = 0
                elif self.selected_number1 > self.selected_number5:
                    self.selected_number1 = self.selected_number1 - self.selected_number5
                    self.selected_number5 = 0

            elif self.keeper_color_card == "red":
                if self.selected_number2 < self.selected_number5:
                    self.selected_number5 = self.selected_number5 + self.selected_number2
                elif self.selected_number2 == self.selected_number5:
                    self.selected_number5 = 0
                    self.selected_number2 = 0
                elif self.selected_number2 > self.selected_number5:
                    self.selected_number2 = self.selected_number2 - self.selected_number2
                    self.selected_number5 = 0

            elif self.keeper_color_card == "yellow":
                if self.selected_number3 < self.selected_number5:
                    self.selected_number5 = self.selected_number5 + self.selected_number3
                elif self.selected_number3 == self.selected_number5:
                    self.selected_number5 = 0
                    self.selected_number3 = 0
                elif self.selected_number3 > self.selected_number5:
                    self.selected_number3 = self.selected_number3 - self.selected_number5
                    self.selected_number5 = 0

            elif self.keeper_color_card == "green":
                if self.selected_number4 < self.selected_number5:
                    self.selected_number5 = self.selected_number5 + self.selected_number4
                elif self.selected_number4 == self.selected_number5:
                    self.selected_number5 = 0
                    self.selected_number4 = 0
                elif self.selected_number4 > self.selected_number5:
                    self.selected_number4 = self.selected_number4 - self.selected_number5
                    self.selected_number5 = 0

        self.step += 1

        if self.carrent_player[self.step % len(self.carrent_player)] == 1:
            self.findChild(QPushButton, 'button1').show()
            self.findChild(QPushButton, 'button3').show()
            self.findChild(QPushButton, 'button1').setText(str(self.card_deck1[-3]))
            self.findChild(QPushButton, 'button2').setText(str(self.card_deck1[-2]))
            self.findChild(QPushButton, 'button3').setText(str(self.card_deck1[-1]))
            self.border_image_botton = 'data/1.jpg'

        elif self.carrent_player[self.step % len(self.carrent_player)] == 2:
            self.findChild(QPushButton, 'button1').setText(str(self.card_deck2[-3]))
            self.findChild(QPushButton, 'button2').setText(str(self.card_deck2[-2]))
            self.findChild(QPushButton, 'button3').setText(str(self.card_deck2[-1]))
            self.border_image_botton = 'data/2.jpg'

        elif self.carrent_player[self.step % len(self.carrent_player)] == 3:
            self.findChild(QPushButton, 'button1').setText(str(self.card_deck3[-3]))
            self.findChild(QPushButton, 'button2').setText(str(self.card_deck3[-2]))
            self.findChild(QPushButton, 'button3').setText(str(self.card_deck3[-1]))
            self.border_image_botton = 'data/3.jpg'

        elif self.carrent_player[self.step % len(self.carrent_player)] == 4:
            self.findChild(QPushButton, 'button1').setText(str(self.card_deck4[-3]))
            self.findChild(QPushButton, 'button2').setText(str(self.card_deck4[-2]))
            self.findChild(QPushButton, 'button3').setText(str(self.card_deck4[-1]))
            self.border_image_botton = 'data/4.jpg'

        elif self.carrent_player[self.step % len(self.carrent_player)] == 5:
            self.keeper_color_card = self.color_card[-1]
            self.color_card.pop(-1)

            fixed_width = 150
            if self.keeper_color_card == "blue":
                self.findChild(QPushButton, 'button2').setFixedWidth(fixed_width)
                self.findChild(QPushButton, 'button2').setText(str(self.card_deck5_1[-1]))
                self.findChild(QPushButton, 'button1').hide()
                self.findChild(QPushButton, 'button3').hide()
                self.border_image_botton = 'data/5_1.jpg'

            elif self.keeper_color_card == "red":
                self.findChild(QPushButton, 'button2').setFixedWidth(fixed_width)
                self.findChild(QPushButton, 'button2').setText(str(self.card_deck5_2[-1]))
                self.findChild(QPushButton, 'button1').hide()
                self.findChild(QPushButton, 'button3').hide()
                self.border_image_botton = 'data/5_2.jpg'

            elif self.keeper_color_card == "yellow":
                self.findChild(QPushButton, 'button2').setFixedWidth(fixed_width)
                self.findChild(QPushButton, 'button2').setText(str(self.card_deck5_3[-1]))
                self.findChild(QPushButton, 'button1').hide()
                self.findChild(QPushButton, 'button3').hide()
                self.border_image_botton = 'data/5_3.jpg'

            elif self.keeper_color_card == "green":
                self.findChild(QPushButton, 'button2').setFixedWidth(fixed_width)
                self.findChild(QPushButton, 'button2').setText(str(self.card_deck5_4[-1]))
                self.findChild(QPushButton, 'button1').hide()
                self.findChild(QPushButton, 'button3').hide()
                self.border_image_botton = 'data/5_4.jpg'

        self.button1.setStyleSheet(
            f"QPushButton{{border-image: url({self.border_image_botton}); color: black;}}")
        self.button2.setStyleSheet(
            f"QPushButton{{border-image: url({self.border_image_botton}); color: black;}}")
        self.button3.setStyleSheet(
            f"QPushButton{{border-image: url({self.border_image_botton}); color: black;}}")

    def closeEvent(self, event):
        event.ignore()


class QtWindow2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1250, 120, 500, 500)
        self.setWindowTitle("Хранитель. Сокровища Богов Египта")
        self.setStyleSheet("background-color: rgb(150,75,0);")

        self.button1 = QPushButton(self)
        self.button1.setGeometry(20, 75, 100, 150)

        self.button2 = QPushButton(self)
        self.button2.setGeometry(135, 75, 100, 150)

        self.button3 = QPushButton(self)
        self.button3.setGeometry(250, 75, 100, 150)

        self.button4 = QPushButton(self)
        self.button4.setGeometry(365, 75, 100, 150)

        self.button5_1 = QPushButton(self)
        self.button5_1.setGeometry(20, 275, 100, 150)
        self.button5_2 = QPushButton(self)
        self.button5_2.setGeometry(135, 275, 100, 150)
        self.button5_3 = QPushButton(self)
        self.button5_3.setGeometry(250, 275, 100, 150)
        self.button5_4 = QPushButton(self)
        self.button5_4.setGeometry(365, 275, 100, 150)

        self.button1.setStyleSheet(
            f"QPushButton{{border-image: url({'data/1.jpg'}); color: black;}}")
        self.button2.setStyleSheet(
            f"QPushButton{{border-image: url({'data/2.jpg'}); color: black;}}")
        self.button3.setStyleSheet(
            f"QPushButton{{border-image: url({'data/3.jpg'}); color: black;}}")
        self.button4.setStyleSheet(
            f"QPushButton{{border-image: url({'data/4.jpg'}); color: black;}}")
        self.button5_1.setStyleSheet(
            f"QPushButton{{border-image: url({'data/5_1.jpg'}); color: black;}}")
        self.button5_2.setStyleSheet(
            f"QPushButton{{border-image: url({'data/5_2.jpg'}); color: black;}}")
        self.button5_3.setStyleSheet(
            f"QPushButton{{border-image: url({'data/5_3.jpg'}); color: black;}}")
        self.button5_4.setStyleSheet(
            f"QPushButton{{border-image: url({'data/5_4.jpg'}); color: black;}}")

    # self.button5_1.hide()
    # self.button5_2.hide()
    # self.button5_3.hide()
    # self.button5_4.hide()

    def closeEvent(self, event):
        event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app2 = QApplication(sys.argv)
    qt_window = QtWindow()
    qt_window2 = QtWindow2()
    start_screen()
    show_level()
    sys.exit(app.exec_())
