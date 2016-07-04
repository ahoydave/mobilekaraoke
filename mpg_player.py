import pygame
import sys

delay = 200

def main(filepath):
    pygame.init()
    pygame.mixer.quit()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    play_movie(screen, filepath)

def play_movie(screen, filepath, escape_callback):
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie(filepath)
    # screen = pygame.display.set_mode((0,0), 0, 32)
    movie.set_display(screen, screen.get_rect())
    movie.set_volume(1.0)

    pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
    pygame.time.set_timer(pygame.USEREVENT, 100)
    movie.play()
    while movie.get_busy():
        evt = pygame.event.wait()
        if evt.type == pygame.QUIT:
            break
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            break
        if escape_callback():
            break

    if movie.get_busy():
        movie.stop()
    pygame.time.set_timer(pygame.USEREVENT, 0)

if __name__ == '__main__':
    main(sys.argv[1])
