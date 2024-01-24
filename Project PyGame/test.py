import os
import pygame
import sys


def start_window_keeper_won():
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Keeper Won")
    background_image = pygame.image.load("data/fon3.png")

    pygame.mixer.init()
    pygame.mixer.music.load("data/music_keeper.mp3")
    pygame.mixer.music.play(-1)

    font = pygame.font.Font(None, 68)
    text = font.render("Хранитель победил!", True, (200, 150, 100))
    text_rect = text.get_rect(center=(width // 2, height // 13))

    images = [pygame.image.load(os.path.join("data/dancing mummy", f"{i}.png")) for i in
              range(1, 13)]
    current_frame = 0
    last_frame_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time > 85:
            current_frame = (current_frame + 1) % len(images)
            last_frame_time = current_time

        scaled_image = pygame.transform.scale(images[current_frame], (int(500 / 1.4), int(450 / 1.4)))
        image_rect = scaled_image.get_rect(center=(width // 2, height - scaled_image.get_height() // 2))

        screen.blit(background_image, (0, 0))
        screen.blit(scaled_image, image_rect.topleft)
        screen.blit(text, text_rect)
        pygame.display.flip()


if __name__ == "__main__":
    start_window_keeper_won()
