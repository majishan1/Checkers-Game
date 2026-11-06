import pygame, sys
from pygame.locals import *
import random
from useful_classes import button, show_text, rects_vertical
from db_functions import GameParticipants_entry, Games_entry
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, RED, DARKER_RED, BLUE, DARKER_BLUE, BUTTON_BG, BLACK, SQUARE_WIDTH, SQUARE_HEIGHT, GREEN, ARCADE_N, ARCADE_I


def end_menu(winner_rgb, username, is_ai):

    button_font = ARCADE_N
    text_font = ARCADE_I

    # Adding to Games and GameParticipands entities in database
    if username != None:
        g_id = Games_entry(is_ai)
        if winner_rgb == BLUE: IsWinner = 1
        elif winner_rgb == GREEN: IsWinner = 2
        else: IsWinner = 0
        GameParticipants_entry(username, g_id, IsWinner)

    pygame.init()

    pygame.display.set_caption("End Menu")
    clock = pygame.time.Clock()

    window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)

    #quit button
    end_quit = pygame.transform.scale(BUTTON_BG.convert_alpha(), (689,122))
    end_quit_w, end_quit_h = end_quit.get_size()

    #restart button
    end_res = pygame.transform.scale(BUTTON_BG.convert_alpha(), (689,122))
    end_res_w, end_res_h = end_res.get_size()

    # Determining colour of buttons on end menu
    if winner_rgb == RED: colour, dark_colour = BLUE, DARKER_BLUE
    elif winner_rgb == BLUE: colour, dark_colour = RED, DARKER_RED
    else: colour, dark_colour = random.choice([BLUE, RED]), random.choice([DARKER_BLUE, DARKER_RED])

    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)

    #Instantiaton
    quit_button = button(end_quit, "Quit", button_font, 64, colour, dark_colour, screen, end_quit_w, end_quit_h, 2, 5, 1, 4)
    restart_button = button(end_quit, "Restart", button_font, 64, colour, dark_colour, screen, end_res_w, end_res_h, 2, 5, 1, 2)
    main_button = button(end_quit, "Main Menu", button_font, 64, colour, dark_colour, screen, end_quit_w, end_quit_h, 2, 5, 1, 3)
    winner_text = show_text

    #winner text object
    if winner_rgb == RED: winner = 'RED wins'
    elif winner_rgb == BLUE: winner = 'BLUE wins'
    elif winner_rgb == GREEN: winner = "It's a draw"


    while True:

        x, y = pygame.mouse.get_pos()

        screen.fill(BLACK)
        screen.blit(surface, (0,0))
        winner_text.word(screen, text_font, 64, winner, winner_rgb, 2, 5)
        quit_button.draw((x,y))
        restart_button.draw((x,y))
        main_button.draw((x,y))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x in range(quit_button.rect.left, quit_button.rect.right) and y in range(quit_button.rect.top, quit_button.rect.bottom):
                    pygame.quit()
                    sys.exit()
                    break
                elif x in range(restart_button.rect.left, restart_button.rect.right) and y in range(restart_button.rect.top, restart_button.rect.bottom):
                    return True
                elif x in range(main_button.rect.left, main_button.rect.right) and y in range(main_button.rect.top, main_button.rect.bottom):
                    return False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        pygame.display.update()
        clock.tick(60)
