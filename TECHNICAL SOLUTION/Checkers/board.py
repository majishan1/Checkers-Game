# CREATE CHECKERBOARD
# total width & height = 512px
# square width & height = 64px
# board start = (401,144)
# background size = 1344x832

# imports
import pygame
from pygame.locals import *
from piece import Piece
from constants import BLACK, WHITE, RED, BLUE, DARKER_BLUE, DARKER_RED, GREEN
import uuid


class Board:

  # initialises object variables
  def __init__(self, x, y, sqW, sqH):
    self.board = []
    self.startX = x
    self.startY = y
    self.x = x
    self.y = y
    self.sqWidth = sqW
    self.sqHeight = sqH
    self.blue_remaining = self.red_remaining  = 12
    self.blue_kings = self.red_kings = 0
    self.create_pieces()



  # increases x value by width of one square
  def xincrease(self):
    self.x += self.sqWidth

  # increases y value by height of one square
  def yincrease(self):
    self.y += self.sqHeight

  # resets x value every time a line is created
  def xreset(self):
    self.x = self.startX

  # resets y value every time the board is created
  def yreset(self):
    self.y = self.startY

  # Create horizontal line of squares for board
  def create_rect_horizontal(self, colour1, colour2, surface):    
    for i in range(0,8):
      rects = Rect(self.x, self.y, self.sqWidth, self.sqHeight)

      if i % 2 == 0:
        pygame.draw.rect(surface, colour1, rects)
      else:
        pygame.draw.rect(surface, colour2, rects)
      self.xincrease()

  def create_pieces(self):
    # Create 2D list that shows the location of all pieces on the board
    # e.g. [0] - for square (0,0) because no pieces in square
    for row in range(8):
      self.board.append([])
      for col in range(8):
        if (row + 1) % 2 != col % 2:
          self.board[row].append(0)
        else:
          if row < 3:
            self.board[row].append(Piece(row, col, RED, DARKER_RED, uuid.uuid4()))
          elif row > 4:
            self.board[row].append(Piece(row, col, BLUE, DARKER_BLUE, uuid.uuid4()))
          else:
            self.board[row].append(0)
   
  def draw(self, screen):
    # Draw checkerboard
    for i in range(8):
      if i % 2 == 0:
        self.create_rect_horizontal(WHITE, BLACK, screen)
      else:
        self.create_rect_horizontal(BLACK, WHITE, screen)
      self.yincrease()
      self.xreset()
    self.yreset()

    # Draw pieces
    for row in range(8):
      for col in range(8):
        piece = self.board[row][col]
        if piece != 0:
          piece.display(screen)

  # move piece from current row to new row
  def move(self, piece, row, col):
    self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
    piece.move(row, col)

    if (row == 7 or row == 0) and not piece.is_King():
      piece.make_King()
      if piece.colour == BLUE: self.blue_kings += 1
      elif piece.colour == RED: self.red_kings += 1

  # finds piece on board
  def find_piece(self, row, col):
    return self.board[row][col]
  
  # Finds coordinates of squares adjacent to selected piece
  def find_coords_around(self, piece):
    self.up_l = piece.row - 1, piece.col + piece.dir
    self.down_l = piece.row - 1, piece.col - piece.dir
    self.up_r = piece.row + 1, piece.col + piece.dir
    self.down_r = piece.row + 1, piece.col - piece.dir
  
  # evaluates bord for minimax algorithm
  def check_board(self):
    pieces_score = self.red_remaining - self.blue_remaining
    king_score = (self.red_kings - self.blue_kings) * 0.5
    other_scores = self.get_other_scores()
    return pieces_score * 1000 + king_score * 100 + other_scores * 50
  
  # checks to see how good each position is for game strategy and prioritises further obtaining king pieces
  def get_other_scores(self):
    pieces = []
    pos_score = 0
    prom_score = 0
    surr_score = 0
    weighting = [ [0, 5, 0, 6, 0, 6, 0, 5],
                  [4, 0, 4, 0, 5, 0, 4, 0],
                  [0, 3, 0, 4, 0, 4, 0, 3],
                  [3, 0, 4, 0, 5, 0, 4, 0],
                  [0, 4, 0, 5, 0, 4, 0, 3],
                  [3, 0, 4, 0, 4, 0, 3, 0],
                  [0, 4, 0, 4, 0, 4, 0, 4],
                  [6, 0, 7, 0, 7, 0, 6, 0]  ]

    # Find all pieces on the board
    for colour in [RED, BLUE]:
      pieces.extend(self.find_all_pieces(colour))
      
    for piece in pieces:
      self.find_coords_around(piece)
      if piece.colour == RED:

        # Alters position score based on location on the board
        pos_score += weighting[piece.row][piece.col]

        # Increases position score if piece is closer to being promoted
        if not piece.is_King:
          prom_score += (5 - piece.row)
        
        # Looks for pieces in surrounding locations to selected piece 
        # and increases score if other pieces are red, but decreases if other pieces are blue
        for row, col in [self.up_l, self.up_r, self.down_l, self.down_r]:
          if not (0 < row < 8 and 0 < col < 8):
            continue
          surrounding_loc = self.find_piece(row, col)
          if surrounding_loc != 0 and surrounding_loc.colour == BLUE:
            surr_score -= 10
          elif surrounding_loc != 0 and surrounding_loc.colour == RED:
            surr_score += 10
      # Opposite of other part of if statement
      else:

        pos_score -= weighting[piece.row][piece.col]
        if not piece.is_King:
          prom_score -= piece.row
        
        for row, col in [self.up_l, self.up_r, self.down_l, self.down_r]:
          if not (0 < row < 8 and 0 < col < 8):
            continue
          surrounding_loc = self.find_piece(row, col)
          if surrounding_loc != 0 and surrounding_loc.colour == RED:
            surr_score += 10
          elif surrounding_loc != 0 and surrounding_loc.colour == BLUE:
            surr_score -= 10
    return (5 * surr_score) + pos_score + prom_score

  # finds all pieces of a given colour on the board
  def find_all_pieces(self, colour):
    pieces = []
    for row in range(8):
      for col in range(8):
        current_piece = self.find_piece(row, col)
        if current_piece != 0 and current_piece.colour == colour:
          pieces.append(current_piece)
    return pieces

  # Finds all blank spaces on the board
  def find_blank_spaces(self):
    blanks = []
    for r_check in range(8):
      for c_check in range(8):
        if r_check % 2 == 0 and c_check % 2 == 1:
          if self.board[r_check][c_check] == 0: 
            blanks.append((r_check, c_check))
        elif r_check % 2 == 1 and c_check % 2 == 0:
          if self.board[r_check][c_check] == 0:
            blanks.append((r_check, c_check))

    return blanks

  # find valid move method
  # determines whether 0 or more pieces can be taken then puts then in a dictionary
  # {ending position: jumps in path to ending position}
  # checks whether an ending position is in a jumps path or if there is a path that takes more pieces and ends in the same position
  def find_valid_moves(self, piece, row, col, direction, blank_spaces, king_check, step = 1, visited = None):
    if visited == None:
      visited = set()
    moves = {}
    new_row = row + direction
    new_col_l, new_col_r = col - 1, col + 1
    
    
    for new_col in [new_col_l, new_col_r]:
      # Make sure that the move is valid with basic checks
      if self._can_jump(new_col, new_row, row, piece):

        if (new_row, new_col) in visited:
          continue

        visited.add((new_row, new_col))
        
        new_loc = self.find_piece(new_row, new_col)
        
        if (new_row, new_col) in blank_spaces and step == 1:
          moves.update({(new_row, new_col): []})
        # Checks if the move is a jump
        if new_loc != 0 and new_loc.colour != piece.colour:

          mid_row, mid_col = new_row, new_col
          jump_row, jump_col = new_row + direction, new_col + (new_col - col)

          if (jump_row, jump_col) in blank_spaces:
            if king_check:
              king_double_jump, visited_double_k = self.find_valid_moves(piece, jump_row, jump_col, -direction, blank_spaces, step=2, king_check=True, visited=visited)
              visited.update(visited_double_k)
              
              double_jump, visited_double = self.find_valid_moves(piece, jump_row, jump_col, direction, blank_spaces, step=2, king_check=True, visited=visited)

              if king_double_jump:
                for key, king_jumps in king_double_jump.items():
                  if key not in moves.keys() or len(king_jumps) > len(moves[key]):
                    temp = [(mid_row, mid_col)] + king_jumps
                    moves.update({key: temp})
            else:
              double_jump, visited_double = self.find_valid_moves(piece, jump_row, jump_col, direction, blank_spaces, step=2, king_check=False, visited = visited)
            
            visited.update(visited_double)


            if not double_jump:
              jump_in_path = False
              for jump in moves.values():
                if (mid_row, mid_col) in jump:
                  jump_in_path = True
              if not jump_in_path:
                moves.update({(jump_row, jump_col): [(mid_row, mid_col)]})
            else:
              for key, jumps in double_jump.items():
                  temp = [(mid_row, mid_col)] + jumps
                  moves.update({key: temp})
    return moves, visited


  
  # adds more valid moves in each direction because kings can move in any direction
  # provides double jumps combining jumps in different directions
  def king_movement(self, piece, row, col, blanks, visited = None):
    if visited == None:
      visited = set()
    moves = {}

    for direction in [-1, 1]:
      valid_moves, visited_king = self.find_valid_moves(piece, row, col, direction, blanks, king_check=True, visited=visited)
      moves.update(valid_moves)

      visited.update(visited_king)
    
    return moves

    
  # General checks to initially see if a jump is valid
  def _can_jump(self, new_col, new_row, row, piece):
    # Piece not on board 
    if not(0 <= new_col <= 7 and 0 <= new_row <= 7):
      return False
    # New row in wrong direction
    if not(new_row == row + piece.dir or piece.is_King()):
      return False
    return True

  
  def remove(self, jump):
    # Removes all the pieces in the path taken by the piece on the board
    for piece in jump:
      remove_check = self.board[piece[0]][piece[1]]
      if remove_check != 0:
        if remove_check.colour == RED: self.red_remaining -= 1
        elif remove_check.colour == BLUE: self.blue_remaining -= 1
      self.board[piece[0]][piece[1]] = 0

  # checks to see if any team has no valid moves in a turn, leading to the other team winning
  def valid_winner(self, turn):
    blanks  = self.find_blank_spaces()
    total_valids = {}
    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        piece = self.find_piece(row, col)
        if piece != 0:
          if piece.colour == turn:
            if not piece.is_King():
              total_valids.update(self.find_valid_moves(piece, piece.row, piece.col, piece.dir, blanks, king_check=False)[0])
            else:
              total_valids.update(self.king_movement(piece, piece.row, piece.col, blanks))
    if not total_valids and turn == BLUE: return RED
    elif not total_valids and turn == RED: return BLUE
    else: return None

  # if there is only 1 king on each team, a draw is declared
  def kings_draw(self):
    if self.blue_kings == self.red_kings == 1 and self.blue_remaining == self.red_remaining == 1:
      return GREEN
    return None
  
  # declares draw if certain conditions are met after each player has player 16 moves
  def sixteen_moves_draw(self, red_turns):
    if red_turns >= 16:
      # blue with more pieces
      if self.red_kings == 1 and ((self.blue_kings == 2 and self.blue_remaining == 3) or (self.blue_kings == self.blue_remaining == 3) or (self.blue_kings == 1 and self.blue_remaining == 3)):  
        return GREEN
      # red with more pieces
      elif self.blue_kings == 1 and ((self.red_kings == 2 and self.red_remaining == 3) or (self.red_kings == self.red_remaining == 3) or (self.red_kings == 1 and self.red_remaining == 3)):
        return GREEN
      return None
    
  # declares draw if only kings move and there are no pieces taken in the last 25 moves
  def repeated_moves_draw(self, last_25_moves):
    if last_25_moves.isMax():
      for is_king, is_jump in last_25_moves.showQueue():
        if not is_king or is_jump:
          return None
      return GREEN
    return None
