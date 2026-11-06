# imports
import pygame
from pygame.locals import *
from constants import RED, CROWN, SQUARE_WIDTH, SQUARE_HEIGHT, START_X, START_Y

# Checker piece class
class Piece:

  # initialises object variabes
  def __init__(self, row, col, colour, dark_colour, id):
    self.sq_Width = SQUARE_WIDTH
    self.sq_Height = SQUARE_HEIGHT
    self.row = row
    self.col = col
    self.colour = colour
    self.dark_colour = dark_colour
    self.king = False
    self.ID = id

    if self.colour == RED: self.dir = 1
    else: 
      self.dir = -1

    self.x = 0
    self.y = 0
    self.calc_pos()

  # Determines position of the piece
  def calc_pos(self):
    # e.g. Column[3] - 401 + (64 * 3) + 64 // 2
    # 401 + 192 + 32
    # 625
    self.x = START_X + (self.sq_Width * self.col) + self.sq_Width // 2
    self.y = START_Y + (self.sq_Height * self.row) + self.sq_Height // 2

  # draws a circle for each piece
  def display(self, screen):
    #radius = 27
    rad = (self.sq_Width // 2) - 5
    pygame. draw.circle(screen, self.colour, (self.x, self.y), rad)
    pygame.draw.circle(screen, self.dark_colour, (self.x,self.y), rad * 0.8)
    pygame.draw.circle(screen, self.colour, (self.x,self.y), rad * 0.6)
    if self.king:
      screen.blit(CROWN, ((self.x - CROWN.get_width() // 2), (self.y - CROWN.get_height() // 2)))

  # Turns piece from man to king
  def make_King(self):
    self.king = True

  # Returns whether the piece is a king or not
  def is_King(self):
    return self.king

  # Updates the coordinates of the piece and draws it in its new position
  def move(self, row, col):
    self.row = row
    self.col = col
    self.calc_pos()
