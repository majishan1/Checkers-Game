# background size = 1344x832
import pygame
from pygame.locals import *
import sys
from constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_BG, RED, DARKER_RED, BLUE, SQUARE_WIDTH, SQUARE_HEIGHT, ARCADE_N, ARCADE_I, ARCADE
from play_menu import play_menu
from end_menu import end_menu
from login_menu import login_menu
from accounts import accounts_main
from useful_classes import button, show_text, rects_vertical


pygame.init()
pygame.display.set_caption('Main Menu')
clock = pygame.time.Clock()

# fonts
button_font = ARCADE_N
text_font = ARCADE_I

# screen setups
window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(window_size)
surface = pygame.Surface(window_size, pygame.SRCALPHA)

# images
main_play = pygame.transform.scale(BUTTON_BG.convert_alpha(), (689,210))
main_play_w, main_play_h = main_play.get_size()
main_play_x, main_play_y = (SCREEN_WIDTH // 2) - (main_play_w // 2), (SCREEN_HEIGHT // 13) * 8.5 - (main_play_h // 2)

main_quit = pygame.transform.scale(BUTTON_BG.convert_alpha(), (689, 90))
main_quit_w, main_quit_h = main_quit.get_size()
main_quit_x, main_quit_y = (SCREEN_WIDTH // 2) - (main_quit_w // 2), (SCREEN_HEIGHT // 13) * 12 - (main_quit_h // 2)

acc_x, acc_y = (SCREEN_WIDTH // 2) - (main_quit_w // 2), (SCREEN_HEIGHT // 13) * 5 - (main_quit_h // 2)

main_login = pygame.transform.scale(BUTTON_BG.convert_alpha(), (360, 90))
main_login_w, main_login_h = main_login.get_size()
login_x, login_y = (SCREEN_WIDTH // 3) - (main_login_w // 2), (SCREEN_HEIGHT // 13) * 5 - (main_login_h // 2)
signup_x, signup_y = (SCREEN_WIDTH // 3) * 2 - (main_login_w // 2), (SCREEN_HEIGHT // 13) * 5 - (main_login_h // 2)


#creating instances of buttons and text
play_button = button(main_play, "Play Game", button_font, 64, RED, DARKER_RED, screen, main_play_w, main_play_h, 2, 13, mult_y=8.5)
quit_button = button(main_quit, "Quit", button_font, 64, RED, DARKER_RED, screen, main_quit_w, main_quit_h, 2, 13, mult_y=12)
login_button = button(main_login, 'Login', button_font, 48, RED, DARKER_RED, screen, main_login_w, main_login_h, 3, 13, mult_y=5)
signup_button = button(main_login, 'Sign Up', button_font, 48, RED, DARKER_RED, screen, main_login_w, main_login_h, 3, 13, 2, 5)
account_button = button(main_quit, 'Account Settings', button_font, 38, RED, DARKER_RED, screen, main_quit_w, main_quit_h, 2, 13, mult_y=5)
start = show_text

logged_in = False

rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)

def checkers(username):
    winner, is_ai = play_menu(logged_in, username)
    if winner != None:
        restart = end_menu(winner, username, is_ai)
    else:
        restart = None

    return restart

while True:
    x,y = pygame.mouse.get_pos()
    screen.fill((0,0,0))
    screen.blit(surface, (0,0))
    start.word(screen, text_font, 92, "Checkers", WHITE, 2, 5)
    play_button.draw((x,y))
    quit_button.draw((x,y))


    # shows different buttons for whether the user is logged in or not
    if not logged_in:
        login_button.draw((x,y))
        signup_button.draw((x,y))
        username = None
    else:
        start.word(screen, ARCADE, 48, username, BLUE, x=984, y=0)
        account_button.draw((x,y))

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:

            # if play button selected
            if x in range(play_button.rect.left, play_button.rect.right) and y in range(play_button.rect.top, play_button.rect.bottom):
                if checkers(username):
                    checkers(username)
                else:
                    continue

            # if quit is selected
            if x in range(quit_button.rect.left, quit_button.rect.right) and y in range(quit_button.rect.top, quit_button.rect.bottom):
                pygame.quit()
                sys.exit()
                break

            # if login or sign up is selected and there is no account logged in
            if x in range(login_button.rect.left, login_button.rect.right) and y in range(login_button.rect.top, login_button.rect.bottom) and not logged_in:
                logged_in, username = login_menu(True, 'Login')[:2]
                continue
            
            if x in range(signup_button.rect.left, signup_button.rect.right) and y in range(signup_button.rect.top, signup_button.rect.bottom) and not logged_in:
                logged_in, username = login_menu(False, 'Sign Up')[:2]
                continue

            # if account settings is selected and there is an account logged in
            if x in range(account_button.rect.left, account_button.rect.right) and y in range(account_button.rect.top, account_button.rect.bottom) and logged_in:
                logged_in, new_username = accounts_main(username)
                if new_username is not None:
                    username = new_username
                continue

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break

    pygame.display.flip()
    clock.tick(60)

