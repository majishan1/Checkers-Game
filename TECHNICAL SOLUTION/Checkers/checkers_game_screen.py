# imports
import pygame, sys
from pygame.locals import *
from game import Game
from minimax import Minimax
from useful_classes import button, show_text, rects_vertical
from db_functions import find_wins
from constants import BOARD_WIDTH, BOARD_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, START_X, START_Y, AI_R, USER_R, USER_B, RED, DARKER_RED, BLACK, WHITE, GREEN, DARKER_GREEN, BLUE, DARKER_BLUE, BUTTON_BG, ARCADE_N


def checkers_game(ai_player, logged_in, username, ai_diff=None):

  button_font = ARCADE_N
  user_r_x, user_r_y = (SCREEN_WIDTH // 2) - (USER_R.get_width() // 2), (SCREEN_HEIGHT // 52) * 5 - (USER_R.get_height() // 2)
  user_b_x, user_b_y = (SCREEN_WIDTH // 2) - (USER_B.get_width() // 2), (SCREEN_HEIGHT // 52) * 48 - (USER_B.get_width() // 2)

  # Pygame window initialisation
  pygame.display.set_caption('Game')
  clock = pygame.time.Clock()

  window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)


  screen = pygame.display.set_mode(window_size)
  surface = pygame.Surface(window_size, pygame.SRCALPHA)
  surface_bg = pygame.Surface(window_size, pygame.SRCALPHA)

  # draw button calculations
  game_draw = pygame.transform.scale(BUTTON_BG, (360, 90))
  game_draw_w, game_draw_h = game_draw.get_size()
  draw_drawn = False

  # back button calculations
  rules_back = pygame.transform.scale(BUTTON_BG, (300, 80))
  rules_back_w, rules_back_h = rules_back.get_size()

  # wins table calculations
  wins_bg = pygame.transform.scale(BUTTON_BG, (386, 400))
  wins_w, wins_h = wins_bg.get_size()
  wins_x, wins_y = (SCREEN_WIDTH // 84) * 71 - (wins_w // 2), (SCREEN_HEIGHT // 26) * 13 - (wins_h // 2)

  # Uses library from Game.py to create game environment
  game = Game(screen, surface)
  draw_button = button(game_draw, "Declare Draw", button_font, 24, RED, DARKER_RED, screen, game_draw_w, game_draw_h, 84, 2, 13, 1)
  back_button = button(rules_back, 'Back to main', button_font, 24, RED, DARKER_RED, screen, rules_back_w, rules_back_h, 224, 104, 25, 5)

  rects_vertical(surface_bg, SQUARE_WIDTH, SQUARE_HEIGHT, 0, 0)
  text = show_text

  if logged_in:
    wins, draws, losses = find_wins(username)

  def get_mouse_pos(x, y):
    row = int((y - START_Y) // SQUARE_WIDTH)
    col = int((x - START_X) // SQUARE_HEIGHT)
    return row, col
  
  def find_selected_piece(colour, new_board, old_board):
    diff = []
    for row in range(8):
      for col in range(8):
         if (new_board[row][col] == 0 and old_board[row][col] != 0):
           diff.append((row, col))
    if colour == BLUE: return diff[-1]
    else: 
      return diff[0]


  # Condition Loop for game
  while True:

    x, y = pygame.mouse.get_pos()

    # Putting images on screen
    screen.fill(BLACK)
    screen.blit(surface_bg, (0,0))
    game.board.draw(screen)
    screen.blit(wins_bg, (wins_x, wins_y))
    back_button.draw((x,y))
    surface.fill((0,0,0,0))

    if ai_player:
      screen.blit(AI_R, (user_r_x, user_r_y))
    else:
      screen.blit(USER_R, (user_r_x, user_r_y))
    screen.blit(USER_B, (user_b_x, user_b_y))
    

    # Showing draw button in 2-player game
    if (game.blue_moves + game.red_moves) >= 80 and not ai_player:
      draw_drawn = True
      draw_button.draw((x,y))

    # Showing win record if user is signed in
    if logged_in:
      text.word(screen, ARCADE_N, 25, username, WHITE, 84, 26, 71, 9)
      text.word(screen, ARCADE_N, 35, f'Wins: {wins}', DARKER_BLUE, 84, 26, 71, 11)
      text.word(screen, ARCADE_N, 35, f'Draws: {draws}', GREEN, 84, 26, 71, 13)
      text.word(screen, ARCADE_N, 35, f'Losses: {losses}', DARKER_RED, 84, 26, 71, 15)
    else:
      text.word(screen, ARCADE_N, 24, 'Login to see results', DARKER_GREEN, 84, 26, 71, 13, rotation=45)

    # Handling AI moves
    if game.turn == RED and ai_player:
      new_board, new_jump = Minimax(ai_diff, True, game.board, game.turn, True)[1:]
      selected = find_selected_piece(RED, new_board.board, game.board.board)
      game.ai_move(new_board, new_jump, selected)
      
    # Event loop
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        break
      if event.type == pygame.MOUSEBUTTONDOWN:
        # Finding if piece is selected
        if x in range(START_X, START_X + BOARD_WIDTH) and y in range(START_Y, START_Y + BOARD_HEIGHT):
          row, col = get_mouse_pos(x, y)
          game.select(row, col)
        # Determining draw if draw button clicked and the draw button is on the screen
        if x in range(draw_button.rect.left, draw_button.rect.right) and y in range(draw_button.rect.top, draw_button.rect.bottom) and draw_drawn:
          return GREEN
        # Returning to main menu if back button clicked
        if x in range(back_button.rect.left, back_button.rect.right) and y in range(back_button.rect.top, back_button.rect.bottom):
          return None
        
    # Draw conditions
    if game.board.kings_draw() != None:
      return GREEN
    
    if game.board.sixteen_moves_draw(game.red_moves) != None:
      return GREEN
    
    if game.board.repeated_moves_draw(game.last_25_moves) != None:
      return GREEN

    # Win condition
    # If one team has no pieces, they have no valid moves, so this still works
    if game.board.valid_winner(game.turn) != None:
      return game.board.valid_winner(game.turn)

    game.update_screen()
    clock.tick(60)
