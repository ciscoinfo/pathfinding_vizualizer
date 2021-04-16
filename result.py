import pygame

from constants import *

class Result():
    def __init__(self, color, x, y, width, height, text='', text_color=(0, 0, 0)):
        self.color = color
        self.initial_color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            # font = pygame.font.SysFont('comicsans', 60)
            # font = pygame.font.Font(FONT_NAME, 20)
            font = pygame.font.SysFont('arial', 24)
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def set_text_result(self, text):
        self.text = f"lenght : {text}"

    def set_text_start(self):
        self.text = "Start..."

    def clear(self):
        self.text = ""
