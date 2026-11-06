import pygame
from pygame.locals import *
import sys
from checkers_game_screen import checkers_game
from rules import rules_screen
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_BG, RED, DARKER_RED, GREEN, DARKER_GREEN, BLUE, DARKER_BLUE, SQUARE_WIDTH, SQUARE_HEIGHT, BLACK, ARCADE_N
from useful_classes import button, rects_vertical

def play_menu(logged_in, username):

    pygame.init()

    pygame.display.set_caption('Play Menu')
    clock = pygame.time.Clock()

    button_font = ARCADE_N

    window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)

    play_bg = pygame.transform.scale(BUTTON_BG.convert_alpha(), (360,122))
    play_bg_w, play_bg_h = play_bg.get_size()

    play_back = pygame.transform.scale(BUTTON_BG.convert_alpha(), (400,122))
    play_back_w, play_back_h = play_back.get_size()

    play_rules = pygame.transform.scale(BUTTON_BG, (657,122))
    play_rules_w, play_rules_h = play_rules.get_size()

    human_button = button(play_bg, "Two Player", button_font, 32, RED, DARKER_RED, screen, play_bg_w, play_bg_h, 3, 2, 2)
    ai_button = button(play_bg, "One Player", button_font, 32, RED, DARKER_RED, screen, play_bg_w, play_bg_h, 3, 2)
    back_button_p = button(play_back, "Back to Main", button_font, 32, RED, DARKER_RED, screen, play_back_w, play_back_h, 2, 4, mult_y=3)
    rules_button = button(play_rules, "Rules", button_font, 32, RED, DARKER_RED, screen, play_rules_w, play_rules_h, 2, 4)

    ai_easy_button = button(play_rules, 'Easy', ARCADE_N, 32, GREEN, DARKER_GREEN, screen, play_rules_w, play_rules_h, 2, 5)
    ai_med_button = button(play_rules, 'Medium', ARCADE_N, 32, BLUE, DARKER_BLUE, screen, play_rules_w, play_rules_h, 2, 5, mult_y=2)
    ai_hard_button = button(play_rules, 'Hard', ARCADE_N, 32, RED, DARKER_RED, screen, play_rules_w, play_rules_h, 2, 5, mult_y=3)
    back_button_ai = button(play_rules, 'Back', ARCADE_N, 32, RED, DARKER_RED, screen, play_rules_w, play_rules_h, 2, 5, mult_y=4)

    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)
    ai_selected = False

    
    while True:

        x, y = pygame.mouse.get_pos()

        screen.fill(BLACK)
        screen.blit(surface, (0,0))
    
        if not ai_selected:
            human_button.draw((x,y))
            ai_button.draw((x,y))
            rules_button.draw((x,y))
            back_button_p.draw((x,y))
        else:
            ai_easy_button.draw((x,y))
            ai_med_button.draw((x,y))
            ai_hard_button.draw((x,y))
            back_button_ai.draw((x,y))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x in range(human_button.rect.left, human_button.rect.right) and y in range(human_button.rect.top, human_button.rect.bottom) and not ai_selected:
                    return checkers_game(False, logged_in, username), False
                if x in range(ai_button.rect.left, ai_button.rect.right) and y in range(ai_button.rect.top, ai_button.rect.bottom) and not ai_selected:
                    ai_selected = True
                    continue
                if x in range(back_button_p.rect.left, back_button_p.rect.right) and y in range(back_button_p.rect.top, back_button_p.rect.bottom) and not ai_selected:
                    return None, None
                if x in range(rules_button.rect.left, rules_button.rect.right) and y in range(rules_button.rect.top, rules_button.rect.bottom) and not ai_selected:
                    rules_screen()
                if x in range(ai_easy_button.rect.left, ai_easy_button.rect.right) and y in range(ai_easy_button.rect.top, ai_easy_button.rect.bottom) and ai_selected:
                    return checkers_game(True, logged_in, username, 2), True
                if x in range(ai_med_button.rect.left, ai_med_button.rect.right) and y in range(ai_med_button.rect.top, ai_med_button.rect.bottom) and ai_selected:
                    return checkers_game(True, logged_in, username, 3), True
                if x in range(ai_hard_button.rect.left, ai_hard_button.rect.right) and y in range(ai_hard_button.rect.top, ai_hard_button.rect.bottom) and ai_selected:
                    return checkers_game(True, logged_in, username, 5), True
                if x in range(back_button_ai.rect.left, back_button_ai.rect.right) and y in range(back_button_ai.rect.top, back_button_ai.rect.bottom) and ai_selected:
                    ai_selected = False
                    continue
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        pygame.display.flip()
        clock.tick(60)
