import random
import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Number Game")

card_deck = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]
random.shuffle(card_deck)
print("1:", card_deck)

button_width = 120
button_height = 200
distance_between_buttons = 40
button_x_start = (screen.get_width() - (3 * button_width + 2 * distance_between_buttons)) // 2
button_y = 150

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if len(card_deck) >= 3:
                last_three_numbers = card_deck[-3:]

                for i in range(3):
                    button_x = button_x_start + (button_width + distance_between_buttons) * i
                    pygame.draw.rect(screen, (0, 128, 255), (button_x, button_y, button_width, button_height))
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(last_three_numbers[i]), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                    screen.blit(text, text_rect)

                if event.key == pygame.K_1:
                    selected_number = card_deck[-3]
                    print(selected_number)
                    card_deck.pop(-3)
                    card_deck = card_deck[-2:] + card_deck[:-2]
                    print(card_deck)
                elif event.key == pygame.K_2:
                    selected_number = card_deck[-2]
                    print(selected_number)
                    card_deck.pop(-2)
                    card_deck = card_deck[-2:] + card_deck[:-2]
                    print(card_deck)
                elif event.key == pygame.K_3:
                    selected_number = card_deck[-1]
                    print(selected_number)
                    card_deck.pop(-1)
                    card_deck = card_deck[-2:] + card_deck[:-2]
                    print(card_deck)
            else:
                print("Карты закончились")
    pygame.display.flip()
