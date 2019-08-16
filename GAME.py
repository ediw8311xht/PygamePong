import random
from threading import Timer
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

    def draw_text_center(self, text, color, background_color, font_size=32, font_family="freesansbold.ttf"):
        font_obj = pygame.font.Font(font_family, 32)
        text_surface_obj = font_obj.render(text, True, color, background_color)
        text_surf_rect = text_surface_obj.get_rect()
        text_surf_rect.center = (int(self.width / 2) * self.pixel_size, int(self.height / 2) * self.pixel_size)
        self.DSURF.blit(text_surface_obj, text_surf_rect)

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
    directions = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    ball_color = (0, 0, 255)

    def __init__(self, width, height, pixel_size=10):
        #DEFAULT SETTERS
        self.width = width
        self.height = height
        self.screen_object = Screen(width, height, pixel_size)
        self.pixel_size = pixel_size

        #PADDLE SETTING MAGIC
        self.paddle_size = max(1, int(height * 0.2))
        temp_var1 = int((height - self.paddle_size) / 2)
        self.paddle_positions = [[0, temp_var1], [width - 1, temp_var1]]

        #BALL/WALL SETTINGS
        self.ball_pos = [int(self.width / 2), int(self.height / 2)]
        self.ball_dir = random.choice(self.directions)
        self.wall_left = False
        self.wall_right = True

    def start(self, event_num, ball_speed=40):
        WAIT = 5
        self.play_countdown(WAIT)
        t = Timer(WAIT + 1, self.start_ball_move, [event_num, ball_speed])
        t.start()

    def play_countdown(self, n_counts, font_size=32, font_family="freesansbold.ttf"):
        if n_counts > 0:
            self.screen_object.draw_text_center(str(n_counts), (255, 255, 255), (0, 0, 0))
            t = Timer(1, self.play_countdown, [n_counts - 1])
            t.start()
        else:
            self.screen_object.draw_text_center("a", (0, 0, 0), (0, 0, 0))
            return True

    def move_paddle_key(self, paddle_n, up_down):
        self.draw_paddle(paddle_n, "erase")
        if up_down == "UP":
            self.paddle_positions[paddle_n][1] = max(0, self.paddle_positions[paddle_n][1] - 1)
        else:
            self.paddle_positions[paddle_n][1] = min(self.height - self.paddle_size, self.paddle_positions[paddle_n][1] + 1)
        self.draw_paddle(paddle_n)

    def move_paddle(self, paddle_n, mouse_pos):
        self.draw_paddle(paddle_n, "erase")
        self.paddle_positions[paddle_n][1] = int(mouse_pos[1] / self.pixel_size) - int(self.paddle_size / 2)
        self.draw_paddle(paddle_n)

    def draw_paddle(self, paddle_n, rgb_color="default"):
        if rgb_color == "default":
            rgb_color = self.paddle_colors[paddle_n]
        elif rgb_color == "erase":
            rgb_color = self.board_color
        p_n = self.paddle_positions[paddle_n]
        t_pixels = [(p_n[0], p_n[1] + x) for x in range(0, self.paddle_size)]
        t_colors = [rgb_color] * self.paddle_size
        self.screen_object.draw_n_pixels(t_pixels, t_colors)

    def draw_ball(self, rgb_color="default"):
        if rgb_color == "default":
            rgb_color = self.ball_color
        elif rgb_color == "erase":
            rgb_color = self.board_color
        self.screen_object.draw_pixel(self.ball_pos[0], self.ball_pos[1], rgb_color)

    #Speed: slower is faster.
    def start_ball_move(self, event_num, speed):
        pygame.time.set_timer(event_num, speed)


    def update_ball_pos(self):
        self.draw_ball("erase")
        self.ball_pos = [self.ball_pos[0] + self.ball_dir[0], self.ball_pos[1] + self.ball_dir[1]]
        if self.ball_pos[1] == 0 or self.ball_pos[1] == (self.height - 1):
            self.ball_dir[1] *= -1
        if (self.ball_pos[0] == 0 and self.ball_dir[0] == -1) or (self.ball_pos[0] == (self.width - 1) and self.ball_dir[0] == 1):
            if (self.ball_pos[0] == 0 and self.wall_left) or (self.ball_pos[0] == (self.width - 1) and self.wall_right):
                self.ball_dir[0] *= -1
            else:
                pp = self.paddle_positions[0] if self.ball_pos[0] == 0 else self.paddle_positions[1]
                if self.ball_pos[1] > pp[1] and self.ball_pos[1] <= (pp[1] + self.paddle_size):
                    self.ball_dir[0] *= -1
        self.draw_ball()

if __name__ == "__main__":

    event_num = pygame.USEREVENT + 1

    pygame.init()
    GAME = Game(70, 70)

    GAME.start(event_num)

    mouse_pos = pygame.mouse.get_pos()
    while True:
        for event in pygame.event.get():
            if event.type == event_num:
                GAME.update_ball_pos()
            if mouse_pos != pygame.mouse.get_pos():
                GAME.move_paddle(0, mouse_pos)
                mouse_pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_k:
            #         GAME.move_paddle_key(0, "UP")
            #     elif event.key == pygame.K_j:
            #         GAME.move_paddle_key(0, "DOWN")
        pygame.display.update()
