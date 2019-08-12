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
            if self.draw_pixel(pixels[i][0], pixels[i][1], rgb_colors[i]):
                drawn_pixels += 1
        return drawn_pixels

class Game(object):

    paddle_colors = [(255, 0, 0), (0, 255, 0)]
    board_color = (0, 0, 0)

    def __init__(self, width, height, pixel_size=20):
        #DEFAULT SETTERS
        self.width = width
        self.height = height
        self.screen_object = Screen(width, height, pixel_size)
        self.pixel_size = pixel_size

        #PADDLE SETTING MAGIC
        self.paddle_size = max(1, int(height * 0.2))
        temp_var1 = int((height - self.paddle_size) / 2)
        self.paddle_positions = [(0, temp_var1), (width - 1, temp_var1)]

    def move_paddle(self, paddle_n, up_down):
        if up_down == "UP":
            self.paddle_positions[paddle_n][1] = min(0, paddle_positions[paddle_n][1] - 1)
        else:
            self.paddle_positoins[paddle_n][1] = max(self.height - 1, paddle_positions[paddle_n][1] + 1)
    def draw_paddle(self, paddle_n, rgb_color="default"):
        if rgb_color == "default":
            rgb_color = self.paddle_colors[paddle_n]
        elif rgb_color == "erase":
            rgb_color = self.board_color
        p_n = self.paddle_positions[paddle_n]
        t_pixels = [(p_n[0], p_n[1] + x) for x in range(0, self.paddle_size)]
        t_colors = [rgb_color] * self.paddle_size
        self.screen_object.draw_n_pixels(t_pixels, t_colors)


if __name__ == "__main__":
    pygame.init()
    GAME = Game(20, 20)
    GAME.draw_paddle(0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
