import pygame
from pygame.locals import *

#Screen constants
SCREEN_WIDTH = 1344
SCREEN_HEIGHT = 832


# Board constants
BOARD_WIDTH = BOARD_HEIGHT = 512
SQUARE_WIDTH = SQUARE_HEIGHT = BOARD_WIDTH // 8


# Location constants
START_X = (SCREEN_WIDTH // 2) - (BOARD_WIDTH // 2)
START_Y = (SCREEN_HEIGHT // 2) - (BOARD_WIDTH // 2)

# Piece colour constants
RED = 255,49,49
RED_TRANS = 255,49,49,192
#ff3131

DARKER_RED = 179,0,0
DARKER_RED_TRANS = 179,0,0,192
#b30000

BLUE = 31,81,255
BLUE_TRANS = 31,81,255,192
#1f50ff

DARKER_BLUE = 0,39,179
DARKER_BLUE_TRANS = 0,39,179,192
#0027b3

GREEN = 0,163,108
GREEN_TRANS = 0,163,108,128


DARKER_GREEN = 0,112,74
DARKER_GREEN_TRANS = 0,112,74,128



# Board colour constants
BLACK = 0,0,0
BLACK_TRANS = 0,0,0,32

WHITE = 255,255,255
WHITE_TRANS = 255,255,255,32

# King image
CROWN = pygame.transform.scale(pygame.image.load('Assets/Crown.png'), (40,26))

# User images
AI_R = pygame.transform.scale(pygame.image.load('Assets/AiImageRed.png'), (106, 64))
USER_R = pygame.transform.scale(pygame.image.load('Assets/UserImageRed.png'), (106, 64))
USER_B = pygame.transform.scale(pygame.image.load('Assets/UserImageBlue.png'), (106, 64))

# Button images
BUTTON_BG = pygame.image.load('Assets/button_bg.png')

#Rules example images
JUMP = pygame.image.load('Assets/single_jump.png')
DOUBLE = pygame.image.load('Assets/double_jump.png')
KING_DOUBLE = pygame.transform.scale_by(pygame.image.load("Assets/king_double_jump.png"), (2/3))
KING_MOVES = pygame.image.load("Assets/king_moves.png")
END_PIECE = pygame.image.load("Assets/piece_at_end.png")
KING_IMAGE = pygame.transform.scale(pygame.image.load("Assets/king_piece.png"), (128,128))
WIN = pygame.transform.scale_by(pygame.image.load("Assets/win_sample.png"), (2/3))

#Fonts
ARCADE = 'Fonts/ARCADE.TTF'
ARCADE_N = 'Fonts/ARCADE_N.TTF'
ARCADE_I = 'FOnts/ARCADE_I.TTF'
