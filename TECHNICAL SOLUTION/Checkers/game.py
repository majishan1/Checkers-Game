import pygame
from pygame.locals import *
from board import Board
from constants import SQUARE_WIDTH, SQUARE_HEIGHT, START_X, START_Y, RED, BLUE, GREEN_TRANS, DARKER_GREEN_TRANS, ARCADE_N
from useful_classes import queue, show_text


class Game:
    
    def __init__(self, screen, surface):
       self.text = show_text
       self._standard()
       self.screen = screen
       self.surface = surface
       
    def _standard(self):
       self.board = Board(START_X, START_Y, SQUARE_WIDTH, SQUARE_HEIGHT)
       self.selected = None
       self.turn = BLUE
       self.valid_move = {}
       self.red_moves = 38
       self.blue_moves = 38
       self.last_25_moves = queue(25)

       
    # updates game screen with the board and valid moves
    def update_screen(self):
       self.board.draw(self.screen)
       self.draw_valid_moves()
       self.screen.blit(self.surface, (0, 0))
       self.text.word(self.screen, ARCADE_N, 25, f'Blue Moves: {self.blue_moves}', BLUE, 21, 26, 18)
       self.text.word(self.screen, ARCADE_N, 25, f'Red Moves: {self.red_moves}', RED, 21, 26, 18, 3)
       pygame.display.flip()
       
       
    # selects piece on board from given row and column and determines the valid moves if a piece isnt already selected
    def select(self, row, col):
        if self.selected:
          res = self._move(row, col)
          if not res:
            self.selected = None
            self.select(row, col)
        
        piece = self.board.find_piece(row, col)
        if piece != 0 and piece.colour == self.turn:
          self.selected = piece
          blanks = self.board.find_blank_spaces()
          if not piece.is_King():
            self.valid_move = self.board.find_valid_moves(piece, piece.row, piece.col, piece.dir, blanks, king_check=False)[0]
          else:
            self.valid_move = self.board.king_movement(piece, piece.row, piece.col, blanks)
          return True
        else:
          self.valid_move = {}
          self.update_screen()
          return False

    # moves a piece from an initial position to a final position
    def _move(self, row, col):
        piece = self.board.find_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_move.keys():
          
          jump = self.valid_move[(row, col)]
          if jump:
            self.board.remove(jump)
           
          self.board.move(self.selected, row, col)
          self.turn_change(jump)
          return True
        else:
          return False

    # changes the player's turn at the end of each move
    # and updates the queue containing the last 25 moves with whether a king moved and whether there was a jump
    def turn_change(self, jump):
        self.valid_move = {}
        if self.turn == RED:
          self.turn = BLUE
          self.red_moves += 1
        else:
          self.turn = RED
          self.blue_moves += 1

        if self.last_25_moves.isMax():
            self.last_25_moves.remove()
          
        is_jump = False
        for value in jump:
          if value: is_jump = True
        self.last_25_moves.add([self.selected.is_King(), is_jump])


    # draws valid moves onto the board
    def draw_valid_moves(self):
        for move in self.valid_move:
            row, col = move
            x_cal = START_X + (SQUARE_WIDTH * col) + SQUARE_WIDTH // 2
            y_cal = START_Y + (SQUARE_HEIGHT * row) + SQUARE_HEIGHT // 2
            radius = (SQUARE_WIDTH // 2) - 5           
            pygame.draw.circle(self.surface, GREEN_TRANS, (x_cal,y_cal), radius)
            pygame.draw.circle(self.surface, DARKER_GREEN_TRANS, (x_cal,y_cal), radius * 0.8)
            pygame.draw.circle(self.surface, GREEN_TRANS, (x_cal,y_cal), radius * 0.6)

    # handles AI movement and changes the turn afterwards  
    def ai_move(self, board, jump, selected):
       self.selected = self.board.board[selected[0]][selected[1]]
       self.board = board
       self.turn_change(jump)
