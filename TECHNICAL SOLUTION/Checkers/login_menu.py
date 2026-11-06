import pygame_textinput
import pygame
from pygame.locals import *
import sys
from db_functions import login, signup
from useful_classes import rects_vertical, button, show_text
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT, WHITE, BLACK, RED, DARKER_RED, BUTTON_BG, ARCADE, ARCADE_N, ARCADE_I


def login_menu(login_t_f, title_name, back_name='Back to Main', account_user=None):

    pygame.init()

    pygame.display.set_caption('Accounts')
    clock = pygame.time.Clock()

    writing_font = pygame.font.Font(ARCADE, 64)
    screen_font = ARCADE_I
    button_font = ARCADE
    button_font_back = ARCADE_N

    # Allows repeated key inputs if a key is held down
    pygame.key.set_repeat(400, 50)

    window_size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)
    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)

    text_box_image = pygame.transform.scale(BUTTON_BG.convert_alpha(), (672, 90))
    text_box_w, text_box_h = text_box_image.get_size()
    
    # If True, enters login menu, otherwise enters sign up menu
    if login_t_f:

        # Username text box information
        u_manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 15)
        username_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=u_manager)

        # Password text box information
        p_manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 12)
        password_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=p_manager)
    
        u_cursor_y = (SCREEN_HEIGHT // 2) - (writing_font.get_height() // 2)

        p_cursor_y = (SCREEN_HEIGHT // 3) * 2 - (writing_font.get_height() // 2)
    
        user_button = button(text_box_image, 'Enter Username', button_font, 64, RED, DARKER_RED, screen, text_box_w, text_box_h, 21, 2, 15)
        pass_button = button(text_box_image, 'Enter Password', button_font, 64, RED, DARKER_RED, screen, text_box_w, text_box_h, 21, 3, 15, 2)

        clicked_user, clicked_pass = False, False
    
    else:

        # Username text box information
        user_manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 15)
        user_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=user_manager)

        u_cursor_y = (SCREEN_HEIGHT // 2) - (writing_font.get_height() // 2)

        # 1st password text box information
        pass_1_manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 12)
        pass_1_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=pass_1_manager)

        p_1_cursor_y = (SCREEN_HEIGHT // 3) * 2 - (writing_font.get_height() // 2)

        # 2nd password text box information
        pass_2_manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 12)
        pass_2_text_in = pygame_textinput.TextInputVisualizer(font_color=RED, cursor_color=DARKER_RED, font_object=writing_font, manager=pass_2_manager)

        p_2_cursor_y = (SCREEN_HEIGHT // 6) * 5 - (writing_font.get_height() // 2)

        user_button = button(text_box_image, 'Enter Username', button_font, 64, RED, DARKER_RED, screen, text_box_w, text_box_h, 21, 2, 15)
        pass_1_button = button(text_box_image, 'Enter Password', button_font, 64, RED, DARKER_RED, screen, text_box_w, text_box_h, 21, 3, 15, 2)
        pass_2_button = button(text_box_image, 'Confirm Password', button_font, 64, RED, DARKER_RED, screen, text_box_w, text_box_h, 21, 6, 15, 5)
        
        clicked_user, clicked_pass_1, clicked_pass_2 = False, False, False


    login_back = pygame.transform.scale(BUTTON_BG.convert_alpha(), (300, 80))
    login_back_w, login_back_h = login_back.get_size()

    logged_in = ''

    back_button = button(login_back, back_name, button_font_back, 24, RED, DARKER_RED, screen, login_back_w, login_back_h, 224, 104, 25, 5)
    txt = show_text


    while True:

        x,y = pygame.mouse.get_pos()

        screen.fill(BLACK)
        screen.blit(surface, (0,0))
        back_button.draw((x,y))
        events = pygame.event.get()

        # If True, enters login menu
        if login_t_f:
            txt.word(screen, screen_font, 92, title_name, WHITE, 2, 5)
            txt.word(screen, screen_font, 48, 'Username:', WHITE, 4, 2)
            txt.word(screen, screen_font, 48, 'Password:', WHITE, 4, 3, mult_y=2)

            # Showing invalid credential problems
            if logged_in != '':
                txt.word(screen, button_font_back, 32, logged_in, WHITE, 2, 3)
            
            # Checking if textbox has been selected
            if clicked_user:
                username_text_in.update(events)
                screen.blit(text_box_image,  user_button.rect.topleft)
                screen.blit(username_text_in.surface, (user_button.rect.left + 50, u_cursor_y))
            else:
                user_button.draw((x,y))
            
            if clicked_pass:
                password_text_in.update(events)
                screen.blit(text_box_image, pass_button.rect.topleft)
                screen.blit(password_text_in.surface, (pass_button.rect.left + 50, p_cursor_y))
            else:
                pass_button.draw((x,y))

            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    # Checks if user wants to select textbox
                    if x in range(user_button.rect.left, user_button.rect.right) and y in range(user_button.rect.top, user_button.rect.bottom) and not clicked_user:
                        clicked_user = True
                    # If box is deselected, replaces button name with inputted test, or returns to original text if empty string is inputted
                    else:
                        if username_text_in.value.strip() != '':
                            user_button.text = username_text_in.value
                        else:
                            user_button.text = 'Enter Username'
                            username_text_in.value = ''
                        clicked_user = False
                    if x in range(pass_button.rect.left, pass_button.rect.right) and y in range(pass_button.rect.top, pass_button.rect.right) and not clicked_pass:
                        clicked_pass = True
                    else:
                        if password_text_in.value.strip() != '':
                            pass_button.text = password_text_in.value
                        else:
                            pass_button.text = 'Enter Password'
                            password_text_in.value = ''
                        clicked_pass = False


                if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                    # Checks to make sure no empty strings are entered, then attempts to log user in
                    # Will exit menu if user successfully logged in
                    if username_text_in.value.strip() != '' and password_text_in.value.strip() != '':
                        if account_user is None or account_user == username_text_in.value:
                            logged_in = login(username_text_in.value, password_text_in.value)
                            if logged_in == True:
                                return True, username_text_in.value, password_text_in.value
                            else:
                                continue
                        else:
                            logged_in = 'Incorrect Username or Password'
                    else:
                        logged_in = 'Please fill all boxes'

        # Enters sign up menu
        else:
            txt.word(screen, screen_font, 92, title_name, WHITE, 2, 5)
            txt.word(screen, screen_font, 48, 'Username:', WHITE, 4, 2)
            txt.word(screen, screen_font, 48, 'Password:', WHITE, 4, 3, mult_y=2)
            txt.word(screen, screen_font, 32, 'Confirm Password:', WHITE, 4, 6, mult_y=5)

            if logged_in != '':
                txt.word(screen, button_font_back, 32, logged_in, WHITE, 2, 3)

            if clicked_user:
                user_text_in.update(events)
                screen.blit(text_box_image, (user_button.rect.topleft))
                screen.blit(user_text_in.surface, (user_button.rect.left + 50, u_cursor_y))
            else:
                user_button.draw((x,y))

            if clicked_pass_1:
                pass_1_text_in.update(events)
                screen.blit(text_box_image, (pass_1_button.rect.topleft))
                screen.blit(pass_1_text_in.surface, (pass_1_button.rect.left + 50, p_1_cursor_y))
            else:
                pass_1_button.draw((x,y))

            if clicked_pass_2:
                pass_2_text_in.update(events)
                screen.blit(text_box_image, (pass_2_button.rect.topleft))
                screen.blit(pass_2_text_in.surface, (pass_2_button.rect.left + 50, p_2_cursor_y))
            else:
                pass_2_button.draw((x,y))

            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if x in range(user_button.rect.left, user_button.rect.right) and y in range(user_button.rect.top, user_button.rect.bottom):
                        clicked_user = True
                    else:
                        if user_text_in.value.strip() != '':
                            user_button.text = user_text_in.value
                        else:
                            user_button.text = 'Enter Username'
                            user_text_in.value = ''
                        clicked_user = False

                    if x in range(pass_1_button.rect.left, pass_1_button.rect.right) and y in range(pass_1_button.rect.top, pass_1_button.rect.bottom):
                        clicked_pass_1 = True
                    else:
                        if pass_1_text_in.value.strip() != '':
                            pass_1_button.text = pass_1_text_in.value
                        else:
                            pass_1_button.text = 'Enter Password'
                            pass_1_text_in.value = ''
                        clicked_pass_1 = False

                    if x in range(pass_2_button.rect.left, pass_2_button.rect.right) and y in range(pass_2_button.rect.top, pass_2_button.rect.bottom):
                        clicked_pass_2 = True
                    else:
                        if pass_2_text_in.value.strip() != '':
                            pass_2_button.text = pass_2_text_in.value
                        else:
                            pass_2_button.text = 'Confirm Password'
                            pass_2_text_in.value = ''
                        clicked_pass_2 = False

                if event.type == KEYDOWN and event.key == K_RETURN:
                    # Attempts to sign user up if fields aren't empty
                    if user_text_in.value.strip() != '' and pass_1_text_in.value.strip() != '' and pass_2_text_in.value.strip() != '':
                        logged_in = signup(user_text_in.value, pass_1_text_in.value, pass_2_text_in.value)
                        if logged_in == True:
                            return True, user_text_in.value, pass_1_text_in.value
                        else:
                            continue
                    else:
                            logged_in = 'Please fill all boxes'

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if x in range(back_button.rect.left, back_button.rect.right) and y in range(back_button.rect.top, back_button.rect.bottom):
                    return None, None, None

            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break
        
        pygame.display.flip()
        clock.tick(60)
