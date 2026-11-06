import pygame
from pygame.locals import *
import pygame_textinput
import sys
from login_menu import login_menu
from db_functions import login, update_username, update_password, account_deleter
from useful_classes import rects_vertical, button, show_text
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ARCADE, ARCADE_I, ARCADE_N, WHITE, SQUARE_WIDTH, SQUARE_HEIGHT, BUTTON_BG, RED, DARKER_RED, BLUE

# Accounts main menu
def accounts_main(username):

    pygame.init()
    pygame.display.set_caption('Account Settings')
    clock = pygame.time.Clock()

    # screen setup
    window_size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)

    # button setup
    account_button = pygame.transform.scale(BUTTON_BG.convert_alpha(), (657,90))
    account_button_w, account_button_h = account_button.get_size()

    c_user_button = button(account_button, 'Change Username', ARCADE_N, 32, RED, DARKER_RED, screen, account_button_w, account_button_h, 2, 7, mult_y=2)
    c_pass_button = button(account_button, 'Change Password', ARCADE_N, 32, RED, DARKER_RED, screen, account_button_w, account_button_h, 2, 7, mult_y=3)
    d_accout_button = button(account_button, 'Delete Account', ARCADE_N, 32, RED, DARKER_RED, screen, account_button_w, account_button_h, 2, 7, mult_y=4)
    sign_out_button = button(account_button, 'Sign Out', ARCADE_N, 32, RED, DARKER_RED, screen, account_button_w, account_button_h, 2, 7, mult_y=5)
    back_button = button(account_button, 'Back', ARCADE_N, 32, RED, DARKER_RED, screen, account_button_w, account_button_h, 2, 7, mult_y=6)

    menus_back_bg = pygame.transform.scale(BUTTON_BG.convert_alpha(), (300,80))
    menus_back_w, menus_back_h = menus_back_bg.get_size()
    menus_back_button = button(menus_back_bg, 'Back', ARCADE_N, 48, RED, DARKER_RED, screen, menus_back_w, menus_back_h, 224, 104, 25, 5)

    txt = show_text
    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)
    is_deleted = False
    new_user = username

    while True:

        # Sets up text and buttons on screen
        screen.fill((0,0,0))
        screen.blit(surface, (0,0))
        txt.word(screen, ARCADE_I, 80, 'Account Settings', WHITE, 2, 7)
        txt.word(screen, ARCADE, 48, new_user, BLUE, x=984, y=0)

        x, y = pygame.mouse.get_pos()
        c_user_button.draw((x,y))
        c_pass_button.draw((x,y))
        d_accout_button.draw((x,y))
        sign_out_button.draw((x,y))
        back_button.draw((x,y))

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                # Enters Username change menu
                if x in range(c_user_button.rect.left, c_user_button.rect.right) and y in range(c_user_button.rect.top, c_user_button.rect.bottom):
                    changed_username = change_username(menus_back_button, username)
                    if changed_username is not None:
                        new_user = changed_username
                # Enters Password change menu
                if x in range(c_pass_button.rect.left, c_pass_button.rect.right) and y in range(c_pass_button.rect.top, c_pass_button.rect.bottom):
                    change_password(menus_back_button)
                # Enters Account delete menu
                if x in range(d_accout_button.rect.left, d_accout_button.rect.right) and y in range(d_accout_button.rect.top, d_accout_button.rect.bottom):
                    is_deleted = delete_account(username)
                    if is_deleted:
                        return False, None
                # Signs user out of account
                if x in range(sign_out_button.rect.left, sign_out_button.rect.right) and y in range(sign_out_button.rect.top, sign_out_button.rect.bottom):
                    return False, None
                # Returns to main menu
                if x in range(back_button.rect.left, back_button.rect.right) and y in range(back_button.rect.top, back_button.rect.bottom):
                    return True, new_user
                    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        pygame.display.flip()
        clock.tick(60)

# changes the username of the user, given that the correct username and password are entered and the new username is valid
# uses login() and update_username() functions from db_functions file
def change_username(back_button, username):

    pygame.init()
    pygame.key.set_repeat(400, 50)

    writing_font = pygame.font.Font(ARCADE, 64)

    pygame.display.set_caption('Account Settings')
    clock = pygame.time.Clock()

    window_size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)

    text_box_image = pygame.transform.scale(BUTTON_BG.convert_alpha(), (657,90))
    text_box_image_w, text_box_image_h = text_box_image.get_size()

    # setting up text boxes for user input using pygame_textinput library
    manager_new_user = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 15)
    new_user_text_in = pygame_textinput.TextInputVisualizer(manager=manager_new_user, font_object=writing_font, font_color=RED, cursor_color=DARKER_RED)
    n_u_cursor_y = (SCREEN_HEIGHT // 6) * 5 - (writing_font.get_height() // 2)
    user_selected = False

    manager_old_user = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 15)
    old_user_text_in = pygame_textinput.TextInputVisualizer(manager=manager_old_user, font_object=writing_font, font_color=RED, cursor_color=DARKER_RED)
    o_u_cursor_y = (SCREEN_HEIGHT // 2) - (writing_font.get_height() // 2)
    old_user_selected = False

    manager_pass = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 12)
    pass_text_in = pygame_textinput.TextInputVisualizer(manager=manager_pass, cursor_color=DARKER_RED, font_color=RED, font_object=writing_font)
    p_cursor_y = (SCREEN_HEIGHT // 3) * 2 - (writing_font.get_height() // 2)
    pass_selected = False


    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)
    new_user_button = button(text_box_image, 'New Username', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 6, 15, 5)
    old_user_button = button(text_box_image, 'Current Username', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 2, 15)
    pass_button = button(text_box_image, 'Enter Password', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 3, 15, 2)
    txt = show_text
    new_username = ''

    while True:
        screen.fill((0,0,0))
        screen.blit(surface, (0,0))
        events = pygame.event.get()
        x, y = pygame.mouse.get_pos()
        txt.word(screen, ARCADE_I, 80, 'Change Username', WHITE, 2, 6)
        txt.word(screen, ARCADE_I, 35, 'Current Username:', WHITE, 4, 2)
        txt.word(screen, ARCADE_I, 40, 'New Username:', WHITE, 4, 6, mult_y=5)
        txt.word(screen, ARCADE_I, 40, 'Enter Password:', WHITE, 4, 3, mult_y=2)
        back_button.draw((x,y))

        if new_username != '':
            txt.word(screen, ARCADE_N, 48, new_username, WHITE, 2, 3)

        if user_selected:
            new_user_text_in.update(events)
            screen.blit(text_box_image, new_user_button.rect.topleft)
            screen.blit(new_user_text_in.surface, (new_user_button.rect.left + 50, n_u_cursor_y))
        else:
            new_user_button.draw((x,y))

        if pass_selected:
            pass_text_in.update(events)
            screen.blit(text_box_image, pass_button.rect.topleft)
            screen.blit(pass_text_in.surface, (pass_button.rect.left + 50, p_cursor_y))
        else:
            pass_button.draw((x,y))

        if old_user_selected:
            old_user_text_in.update(events)
            screen.blit(text_box_image, old_user_button.rect.topleft)
            screen.blit(old_user_text_in.surface, (old_user_button.rect.left + 50, o_u_cursor_y))
        else:
            old_user_button.draw((x,y))

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if x in range(new_user_button.rect.left, new_user_button.rect.right) and y in range(new_user_button.rect.top, new_user_button.rect.bottom):
                    user_selected = True
                else:
                    if new_user_text_in.value.strip() != '':
                        new_user_button.text = new_user_text_in.value
                    else:
                        new_user_button.text = 'New Username'
                        new_user_text_in.value = ''
                    user_selected = False

                if x in range(pass_button.rect.left, pass_button.rect.right) and y in range(pass_button.rect.top, pass_button.rect.bottom):
                    pass_selected = True
                else:
                    if pass_text_in.value.strip() != '':
                        pass_button.text = pass_text_in.value
                    else:
                        pass_button.text = 'Enter Password'
                        pass_text_in.value = ''
                    pass_selected = False

                if x in range(old_user_button.rect.left, old_user_button.rect.right) and y in range(old_user_button.rect.top, old_user_button.rect.bottom):
                    old_user_selected = True
                else:
                    if old_user_text_in.value.strip() != '':
                        old_user_button.text = old_user_text_in.value
                    else:
                        old_user_button.text = 'Current Username'
                        old_user_text_in.value = ''
                    old_user_selected = False

                if x in range(back_button.rect.left, back_button.rect.right) and y in range(back_button.rect.top, back_button.rect.bottom):
                    return None

            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                if old_user_text_in.value.strip() != '' and new_user_text_in.value.strip() != '' and pass_text_in.value.strip() != '':
                    if username == old_user_text_in.value:
                        if login(old_user_text_in.value, pass_text_in.value) == True:
                            new_username = update_username(old_user_text_in.value, new_user_text_in.value, pass_text_in.value)
                            if new_username != True:
                                continue
                            else:
                                return new_user_text_in.value
                    else:
                        new_username = 'Username cannot be the same'
                else:
                    new_username = 'Please Fill all boxes'

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        pygame.display.flip()
        clock.tick(60)


# changes user's password given that the correct login details are added and the new password is valid
# uses the login() function again, and theupdate_password() function from db_functions
def change_password(back_button):

    pygame.init()
    pygame.key.set_repeat(400, 50)

    writing_font = pygame.font.Font(ARCADE, 64)

    pygame.display.set_caption('Account Settings')
    clock = pygame.time.Clock()

    window_size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)

    text_box_image = pygame.transform.scale(BUTTON_BG.convert_alpha(), (657,90))
    text_box_image_w, text_box_image_h = text_box_image.get_size()

    u_manager = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 15)
    user_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=u_manager)
    u_cursor_y = (SCREEN_HEIGHT // 7) * 3 - (writing_font.get_height() // 2)
    user_selected = False

    o_p_manager = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 15)
    old_pass_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=o_p_manager)
    o_p_cursor_y = (SCREEN_HEIGHT // 7) * 4 - (writing_font.get_height() // 2)
    old_pass_selected = False

    n_p_1_manager = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 15)
    n_p_1_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=n_p_1_manager)
    n_p_1_cursor_y = (SCREEN_HEIGHT // 7) * 5 - (writing_font.get_height() // 2)
    new_p_1_selected = False

    n_p_2_manager = pygame_textinput.TextInputManager(validator=lambda x: len(x) <= 15)
    n_p_2_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=n_p_2_manager)
    n_p_2_cursor_y = (SCREEN_HEIGHT // 7) * 6 - (writing_font.get_height() // 2) 
    new_p_2_selected = False

    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)
    txt = show_text
    user_button = button(text_box_image, 'Enter Username', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 7, 15, 3)
    old_pass_button = button(text_box_image, 'Enter Password', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 7, 15, 4)
    new_p_1_button = button(text_box_image, 'New Password', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 7, 15, 5)
    new_p_2_button = button(text_box_image, 'Confirm New Password', ARCADE, 64, RED, DARKER_RED, screen, text_box_image_w, text_box_image_h, 21, 7, 15, 6)
    new_password = ''

    while True:
        screen.fill((0,0,0))
        screen.blit(surface, (0,0))
        txt.word(screen, ARCADE_I, 80, 'Change Password', WHITE, 2, 7)
        txt.word(screen, ARCADE_I, 32, 'Enter Username:', WHITE, 4, 7, mult_y=3)
        txt.word(screen, ARCADE_I, 32, 'Enter Password:', WHITE, 4, 7, mult_y=4)
        txt.word(screen, ARCADE_I, 32, 'New Password:', WHITE, 4, 7, mult_y=5)
        txt.word(screen, ARCADE_I, 24, 'Confirm New Password:', WHITE, 4, 7, mult_y=6)

        events = pygame.event.get()
        x, y = pygame.mouse.get_pos()
        back_button.draw((x,y))


        if new_password != '':
            txt.word(screen, ARCADE_N, 48, new_password, WHITE, 2, 7, mult_y=2)

        if user_selected:
            user_text_in.update(events)
            screen.blit(text_box_image, user_button.rect.topleft)
            screen.blit(user_text_in.surface, (user_button.rect.left + 50, u_cursor_y))
        else:
            user_button.draw((x,y))

        if old_pass_selected:
            old_pass_text_in.update(events)
            screen.blit(text_box_image, old_pass_button.rect.topleft)
            screen.blit(old_pass_text_in.surface, (old_pass_button.rect.left + 50, o_p_cursor_y))
        else:
            old_pass_button.draw((x,y))

        if new_p_1_selected:
            n_p_1_text_in.update(events)
            screen.blit(text_box_image, new_p_1_button.rect.topleft)
            screen.blit(n_p_1_text_in.surface, (new_p_1_button.rect.left + 50, n_p_1_cursor_y))
        else:
            new_p_1_button.draw((x,y))

        if new_p_2_selected:
            n_p_2_text_in.update(events)
            screen.blit(text_box_image, new_p_2_button.rect.topleft)
            screen.blit(n_p_2_text_in.surface, (new_p_2_button.rect.left + 50, n_p_2_cursor_y))
        else:
            new_p_2_button.draw((x,y))

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if x in range(user_button.rect.left, user_button.rect.right) and y in range(user_button.rect.top, user_button.rect.bottom):
                    user_selected = True
                else:
                    if user_text_in.value.strip() != '':
                        user_button.text = user_text_in.value
                    else:
                        user_button.text = 'Enter Username'
                        user_text_in.value = ''
                    user_selected = False
                
                if x in range(old_pass_button.rect.left, old_pass_button.rect.right) and y in range(old_pass_button.rect.top, old_pass_button.rect.bottom):
                    old_pass_selected = True
                else:
                    if old_pass_text_in.value.strip() != '':
                        old_pass_button.text = old_pass_text_in.value
                    else:
                        old_pass_button.text = 'Enter Password'
                        old_pass_text_in.value = ''
                    old_pass_selected = False

                if x in range(new_p_1_button.rect.left, new_p_1_button.rect.right) and y in range(new_p_1_button.rect.top, new_p_1_button.rect.bottom):
                    new_p_1_selected = True
                else:
                    if n_p_1_text_in.value.strip() != '':
                        new_p_1_button.text = n_p_1_text_in.value
                    else:
                        new_p_1_button.text = 'New Password'
                        n_p_1_text_in.value = ''
                    new_p_1_selected = False
                
                if x in range(new_p_2_button.rect.left, new_p_2_button.rect.right) and y in range(new_p_2_button.rect.top, new_p_2_button.rect.bottom):
                    new_p_2_selected = True
                else:
                    if n_p_2_text_in.value.strip() != '':
                        new_p_2_button.text = n_p_2_text_in.value
                    else:
                        new_p_2_button.text = 'Confirm New Password'
                        n_p_2_text_in.value = ''
                    new_p_2_selected = False
                
                if x in range(back_button.rect.left, back_button.rect.right) and y in range(back_button.rect.top, back_button.rect.bottom):
                    return None
                
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                if user_text_in.value.strip() != '' and old_pass_text_in.value.strip() != '' and n_p_1_text_in.value.strip() != '' and n_p_2_text_in.value.strip() != '':
                    if login(user_text_in.value, old_pass_text_in.value) == True:
                        new_password = update_password(user_text_in.value, old_pass_text_in.value, n_p_1_text_in.value, n_p_2_text_in.value)
                        if new_password != True:
                            continue
                        else:
                            return True
                else:
                    new_password = 'Please fill all boxes'
                        

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
        
        pygame.display.flip()
        clock.tick(60)

# deletes user's account, piggybacking off of the login menu already made
# uses the account_deleter() function from db_functions to remove the account if a valid login was provided and the same account is deleted as the one logged in
def delete_account(u_logged):
    #u_logged = the username of the account currently logged in
    valid, username, password = login_menu(True, 'Delete Account', 'Back', u_logged)
    if valid is None:
        return False
    
    account_deleter(username, password)
    return True
