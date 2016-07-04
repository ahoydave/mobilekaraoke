import pygame
import os
import sys
import subprocess
import mpg_player
import RPi.GPIO as GPIO

selected_item = 0
padding = 30
delay = 100
max_scroll_delay = 20
up_pin = 7 
down_pin = 8
select_pin = 10 
escape_pin = 11 

FONT_SIZE = 60

def quit_song(p):
    p.stdin.write('q')
    p.terminate()
    p.wait()

if __name__ == "__main__":

    files = os.listdir(sys.argv[1])
    files.sort()
    menu_items = [f.replace('.mpg', '') for f in files]

    pygame.init()
    pygame.mixer.quit()
    pygame.display.init()

    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((0,0), 0, 32)
    pygame.display.set_caption('Karaoke Menu')

    pygame.key.set_repeat(500, 10)

    screen_height = screen.get_rect().height
    center_x = screen.get_rect().width/2
    center_y = screen_height/2

    clock = pygame.time.Clock()

    rs = []
    for i, t in enumerate(menu_items):
        rs.append(pygame.font.Font(None, FONT_SIZE).render(t, 1, (255,255,255)))

    text_height = rs[0].get_rect().height

    running = True
   
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(up_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(down_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(select_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(escape_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    scroll_delay = max_scroll_delay

    song_process = None

    while running:
        if song_process:
            for event in pygame.event.get():
                if event.key == pygame.K_ESCAPE:
                    quit_song(song_process)
                    song_process = None
            if(GPIO.input(escape_pin)):
                quit_song(song_process)
                song_process = None
                
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(rs)
                    if event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(rs)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        filepath = os.path.join(sys.argv[1], files[selected_item])
                        #mpg_player.play_movie(screen, filepath, escape_callback)
                        song_process = subprocess.Popen(['omxplayer',filepath],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)

            if (GPIO.input(up_pin)):
                if (scroll_delay == max_scroll_delay):
                    selected_item = (selected_item - 1) % len(rs)
                    scroll_delay = scroll_delay - 1
                elif (scroll_delay == 0):
                    selected_item = (selected_item - 1) % len(rs)
                else:
                    scroll_delay = scroll_delay - 1
            elif (GPIO.input(down_pin)):
                if (scroll_delay == max_scroll_delay):
                    selected_item = (selected_item + 1) % len(rs)
                    scroll_delay = scroll_delay - 1
                if (scroll_delay == 0):
                    selected_item = (selected_item + 1) % len(rs)
                else:
                    scroll_delay = scroll_delay - 1
            else:
                scroll_delay = max_scroll_delay

            if (GPIO.input(select_pin)):
                filepath = os.path.join(sys.argv[1], files[selected_item])
                mpg_player.play_movie(screen, filepath, escape_callback)

        screen.fill((0,0,0))
        if (not song_process):
            pygame.draw.rect(screen, (100,100,100), pygame.Rect(0, center_y - text_height/2 - padding, screen.get_rect().width, text_height + 2*padding))
            num_items_visible = screen_height / text_height
            for i in range(selected_item - num_items_visible/2, selected_item + num_items_visible + 1):
                r = rs[i % len(rs)]
                screen.blit(r, (center_x - r.get_rect().width/2, center_y - r.get_rect().height/2 + (i - selected_item) * (r.get_rect().height +  padding)))

        pygame.display.update()
        clock.tick(delay)

