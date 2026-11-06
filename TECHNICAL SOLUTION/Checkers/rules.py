import pygame
from pygame.locals import *
import sys
from useful_classes import button, show_text, rects_vertical
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT, JUMP, DOUBLE, KING_DOUBLE, KING_MOVES, KING_IMAGE, WIN, END_PIECE, BUTTON_BG, RED, DARKER_RED, WHITE, ARCADE_N, ARCADE_I


def rules_screen():
    button_font = ARCADE_N
    text_font = ARCADE_I
    
    pygame.init()
    pygame.display.set_caption("Rules")
    clock = pygame.time.Clock()

    window_size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(window_size)
    surface = pygame.Surface(window_size, pygame.SRCALPHA)
    rects_vertical(surface, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)

    rules_but = pygame.transform.scale(BUTTON_BG, (200,90))
    rules_but_w, rules_but_h = rules_but.get_size()

    rules_back = pygame.transform.scale(BUTTON_BG, (300, 80))
    rules_back_w, rules_back_h = rules_back.get_size()

    prev_button = button(rules_but, "Prev", button_font, 32, RED, DARKER_RED, screen, rules_but_w, rules_but_h, 21, 2)
    next_button = button(rules_but, "Next", button_font, 32, RED, DARKER_RED, screen, rules_but_w, rules_but_h, 21, 2, 20)
    back_button = button(rules_back, 'Back', button_font, 48, RED, DARKER_RED, screen, rules_back_w, rules_back_h, 224, 104, 25, 5)
    txt = show_text
    

    cur_screen = 0

    while True:
        x, y = pygame.mouse.get_pos()
        
        screen.fill((0,0,0))
        screen.blit(surface, (0,0)) 
        back_button.draw((x,y))


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x in range(prev_button.rect.left, prev_button.rect.right) and y in range(prev_button.rect.top, prev_button.rect.bottom):
                    if cur_screen != 0:
                        cur_screen -= 1

                if x in range(next_button.rect.left, next_button.rect.right) and y in range(next_button.rect.top, next_button.rect.bottom):
                    if cur_screen != 5:
                        cur_screen += 1
                
                if x in range(back_button.rect.left, back_button.rect.right) and y in range(back_button.rect.top, back_button.rect.bottom):
                    return None


            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        if cur_screen != 0:
            prev_button.draw((x,y))
        if cur_screen != 5:
            next_button.draw((x,y))

        if cur_screen == 0:
            single_jump(screen, txt, text_font, button_font)
        elif cur_screen == 1:
            double_jump(screen, txt, text_font, button_font)
        elif cur_screen == 2:
            make_king(screen, txt, text_font, button_font)
        elif cur_screen == 3:
            kings(screen, txt, text_font, button_font)
        elif cur_screen == 4:
            win(screen, txt, text_font, button_font)
        else:
            drawing(screen, txt, text_font, button_font)

        pygame.display.flip()
        clock.tick(60)


def single_jump(screen, txt, text_font, button_font):
    txt.word(screen, text_font, 92, 'Single Jumps', WHITE, 2, 13, mult_y=2)
    screen.blit(JUMP, ((SCREEN_WIDTH // 24) * 7 - (JUMP.get_width() // 2), (SCREEN_HEIGHT // 2) - (JUMP.get_height() // 2)))
    text_file = open('Text_files/single explanation.txt')
    div_y = 100
    mult_y = 35
    for line in text_file.readlines():
        txt.word(screen, button_font, 10, line.strip('\n'), WHITE, 3, div_y, 2, mult_y)
        mult_y += 5



def double_jump(screen, txt, text_font, button_font):
    txt.word(screen, text_font, 92, 'Double Jumps', WHITE, 2, 13, mult_y=2)
    screen.blit(DOUBLE, ((SCREEN_WIDTH // 24) * 7 - (DOUBLE.get_width() // 2), (SCREEN_HEIGHT // 2) - (DOUBLE.get_height() // 2)))
    text_file = open('Text_files/double explanation.txt')
    div_y = 100
    mult_y = 45
    for line in text_file.readlines():
        txt.word(screen, button_font, 10, line.strip('\n'), WHITE, 3, div_y, 2, mult_y)
        mult_y += 5


def make_king(screen, txt, text_font, button_font):
    txt.word(screen, text_font, 92, 'Making kings', WHITE, 2, 13, mult_y=2)
    screen.blit(END_PIECE, ((SCREEN_WIDTH // 24) * 7 - (END_PIECE.get_width() // 2), (SCREEN_HEIGHT // 3) - (END_PIECE.get_height() // 2)))
    screen.blit(KING_IMAGE, ((SCREEN_WIDTH // 24) * 7 - (KING_IMAGE.get_width() // 2), (SCREEN_HEIGHT // 3)  * 2 - (KING_IMAGE.get_height() // 2)))
    text_file = open('Text_files/make king explanation.txt')
    div_y = 100
    mult_y = 45
    for line in text_file.readlines():
        txt.word(screen, button_font, 10, line.strip('\n'), WHITE, 3, div_y, 2, mult_y)
        mult_y += 5

def kings(screen, txt, text_font, button_font):
    txt.word(screen, text_font, 92, 'King movements', WHITE, 2, 13, mult_y=2)
    screen.blit(KING_MOVES, ((SCREEN_WIDTH // 7) * 2 - (KING_MOVES.get_width() // 2), (SCREEN_HEIGHT // 13) * 5 - (KING_MOVES.get_height() // 2)))
    screen.blit(KING_DOUBLE, ((SCREEN_WIDTH // 7) * 2 - (KING_DOUBLE.get_width() // 2), (SCREEN_HEIGHT // 13) * 9 - (KING_DOUBLE.get_height() // 2)))
    text_file = open('Text_files/king moves explanation.txt')
    div_y = 100
    mult_y = 45
    for line in text_file.readlines():
        txt.word(screen, button_font, 10, line.strip('\n'), WHITE, 21, div_y, 13, mult_y)
        mult_y += 5

def win(screen, txt, text_font, button_font):
    txt.word(screen, text_font, 80, 'Win conditions', WHITE, 2, 13, mult_y=2)
    screen.blit(WIN, ((SCREEN_WIDTH // 24) * 7 - (WIN.get_width() // 2), (SCREEN_HEIGHT // 2) - (WIN.get_height() // 2)))
    text_file = open('Text_files/win explanation.txt')
    div_y = 100
    mult_y = 45
    for line in text_file.readlines():
        txt.word(screen, button_font, 10, line.strip('\n'), WHITE, 3, div_y, 2, mult_y)
        mult_y += 5


def drawing(screen, txt, text_font, button_font):
    txt.word(screen, text_font, 80, 'Draw conditions', WHITE, 2, 13, mult_y=2)
    text_file = open('Text_files/draw explanation.txt')
    div_y = 100
    mult_y = 45
    for line in text_file.readlines():
        txt.word(screen, button_font, 10, line.strip('\n'), WHITE, x=224, div_y=div_y, mult_y=mult_y)
        mult_y += 5
