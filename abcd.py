import pygame
from pygame.locals import *




class Screen(object):
    def __init__(self, width, height, pixel_size, caption=""):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.DSURF = pygame.display.set_mode((width * pixel_size, height * pixel_size))
        self.board = [[(0, 0, 0)] * width for x in range(0, height)]
        pygame.display.set_caption(caption)
    def draw_pixel(self, x, y, rgb_color):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        self.board[x][y] = rgb_color
        pygame.draw.rect(self.DSURF, rgb_color, (x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size))
        return True
    def draw_n_pixels(self, pixels, rgb_colors):
        length = len(pixels)
        drawn_pixels = 0 #number of pixels drawn successfully
        for i in range(0, length):
            if self.draw_pixel(pixels[i][0], pixels[i][1], rgbs_colors[i]):
                draw_pixels += 1
        return drawn_pixels


class Game(object):
    def __init__(self, width, height, pixel_size=20):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size


if __name__ == "__main__":
    pygame.init()
    a = Screen(20, 20, 20)
    a.draw_pixel(10, 10, (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
