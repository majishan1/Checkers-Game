import pygame
from pygame.locals import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE_TRANS, BLACK_TRANS


#button class
class button:
    def __init__(self, bg, txt_in, font, size, txt_colour, alt_txt_colour, screen, width, height, div_x, div_y, mult_x = 1, mult_y = 1):
        self.screen = screen
        self.image = bg
        self.text = txt_in
        self.txt_colour = txt_colour
        self.alt_txt_colour = alt_txt_colour
        self.show_text = show_text
        self.font = font
        self.size = size
        self.rect = self.image.get_rect()
        self.div_x, self.mult_x = div_x, mult_x
        self.div_y, self.mult_y = div_y, mult_y
        self.x, self.y = (SCREEN_WIDTH // div_x) * mult_x - (width // 2), (SCREEN_HEIGHT // div_y) * mult_y - (height // 2)
        self.rect.topleft = (self.x,self.y)

    def draw(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.screen.blit(self.image, self.rect.topleft)
            self.show_text.word(self.screen, self.font, self.size, self.text, self.alt_txt_colour, self.div_x, self.div_y, self.mult_x, self.mult_y)
        else:
            self.screen.blit(self.image, self.rect.topleft)
            self.show_text.word(self.screen, self.font, self.size, self.text, self.txt_colour, self.div_x, self.div_y, self.mult_x, self.mult_y)



#text class
class show_text:

    def word(screen, font_type, size, string, colour, div_x = 1, div_y = 1, mult_x = 1, mult_y = 1, x = None, y = None, rotation=0):
        font = pygame.font.Font(font_type, size)
        text = pygame.transform.rotate(font.render(string, True, colour), rotation)
        text_w, text_h = text.get_size()
        title_x, title_y = (SCREEN_WIDTH // div_x) * mult_x - (text_w // 2), (SCREEN_HEIGHT // div_y) * mult_y - (text_h // 2)
        if x is not None:
            title_x = x
        if y is not None:
            title_y = y
        screen.blit(text, (title_x, title_y))

# Creates checkerboard pattern for background
def rect_horizontal(colour1, colour2, surface, width, height, x, y):
    number_of_rects = 21
    for i in range(number_of_rects):
        rect = Rect(x, y, width, height)
        if i % 2 == 0:
            pygame.draw.rect(surface, colour1, rect)
        else:
            pygame.draw.rect(surface, colour2, rect)
        x += width

def rects_vertical(surface, width, height, x_initial, y_initial):
    number_of_rows = 13
    x, y = x_initial, y_initial
    for i in range(number_of_rows):
        if i % 2 == 0:
            rect_horizontal(WHITE_TRANS, BLACK_TRANS, surface, width, height, x, y)
        else:
            rect_horizontal(BLACK_TRANS, WHITE_TRANS, surface, width, height, x, y)
        y += height
        x = x_initial
    y = y_initial

# Circular queue data structure
# Uses (rear + 1) % (maxSize) to keep pointers within bounds of list
class queue:
    def __init__(self, maxSize):
        self._contents = [None] * maxSize
        self._maxSize = maxSize
        self._front = 0
        self._rear = -1
        self._size = 0

    def isMax(self):
        if self._size == self._maxSize:
            return True
        return False
    
    def isEmpty(self):
        if self._size == 0:
            return True
        return False
    
    def add(self, item):
        if not self.isMax():
            self._rear = (self._rear + 1) % (self._maxSize)
            self._contents[self._rear] = item
            self._size += 1
            return True
        return False
        
    def remove(self):
        if not self.isEmpty():
            lead = self._contents[self._front]
            self._front = (self._front + 1) % (self._maxSize)
            self._size -= 1
            return lead
        return None

    def showQueue(self):
        return self._contents
