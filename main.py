# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
pygame.init()

# Parameters for game window
WIN_W = 500
WIN_H = 520
LINES_DIST = 25
FPS = 60

# Parameters for player
SNAKE_SIZE = 23
ani = 4
GAME_STARTED = False
GAME_OVER = False
MOVMENT_BUSY = False

# Colors in game
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (81, 81, 81)
SCORE_COLOR = (255, 0, 127)

# Set up the drawing window
screen = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption('Snake Game by DavArmenia')

GAME_CLOCK = pygame.time.Clock()

class InfoText():
    def draw_score(self):
        font = pygame.font.Font('Lightdot-13x9.ttf', 14)
        text_for_show = "Score: %d" % (player.score)
        text = font.render(text_for_show, True, SCORE_COLOR)
        textRect = text.get_rect()
        textRect.left = (10)
        textRect.top = (WIN_H - 15)
        screen.blit(text, textRect)

    def draw_game_over(self):
        font = pygame.font.Font('Lightdot-13x9.ttf', 32)
        text_for_show = "!!! GAME OVER !!!"
        text = font.render(text_for_show, True, SCORE_COLOR)
        textRect = text.get_rect()
        textRect.center = (WIN_W // 2, WIN_H // 2)
        screen.blit(text, textRect)

class Fruit():
    def __init__(self):
        self.coordinates = [0,0]

    def update(self):
        new_coor_x = random.randint(0,19)
        new_coor_y = random.randint(0,19)
        if player.check_pos_emp([new_coor_x, new_coor_y]):
            self.coordinates[0] = new_coor_x
            self.coordinates[1] = new_coor_y
        else:
            fruit.update()

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.coordinates[0] * (SNAKE_SIZE + 2) + (SNAKE_SIZE + 2)/2 + 1, self.coordinates[1] * (SNAKE_SIZE + 2) + (SNAKE_SIZE + 2)/2 + 1), 7)    

class Player():
    def __init__(self):
        self.default_pos = [[2,0], [1,0], [0,0]]
        self.points_coordinates = [[2,0], [1,0], [0,0]]
        self.move_dir_x = 0
        self.move_dir_y = 0
        self.frame = 0
        self.speed = 1
        self.score = 0


    def update(self, x, y):
        if (x and (x + self.move_dir_x == 0)) or (y and (y + self.move_dir_y == 0)):
            return
        if x + self.move_dir_x != 0:
            self.move_dir_x = x
        if y + self.move_dir_y != 0:
            self.move_dir_y = y

    def check_pos_emp(self, coor_to_check):
        if coor_to_check in self.points_coordinates:
            return 0
        else:
            return 1

    def draw(self):
        if GAME_STARTED:
            self.check_collision(fruit.coordinates)
        for coordinates in self.points_coordinates:
            pygame.draw.rect(screen, BLUE, (coordinates[0] * (SNAKE_SIZE + 2) + 1, coordinates[1] * (SNAKE_SIZE + 2) + 1, SNAKE_SIZE, SNAKE_SIZE))
        if GAME_OVER:
            return
        self.frame += self.speed
        if self.frame > 3*ani:
            self.frame = 0
            if GAME_STARTED:
                head_coordinate = [self.points_coordinates[0][0],self.points_coordinates[0][1]]
                head_coordinate[0] += self.move_dir_x
                head_coordinate[1] += self.move_dir_y
                if self.self_collision(head_coordinate) == -1:
                    return
                self.points_coordinates.insert(0, head_coordinate)
                self.points_coordinates.pop()
                global MOVMENT_BUSY
                MOVMENT_BUSY = False

    def check_collision(self, coor_to_check):
        if coor_to_check in self.points_coordinates:
            self.speed += 0.05
            self.score += 1
            self.points_coordinates.insert(-1, self.points_coordinates[-1])
            fruit.update()

    def self_collision(self, new_position):
        if new_position in self.points_coordinates:
            global GAME_STARTED, GAME_OVER
            GAME_STARTED = False
            GAME_OVER = True
            return -1
        if new_position[0] < 0 or new_position[0] > 19 or new_position[1] < 0 or new_position[1] > 19:
            GAME_STARTED = False
            GAME_OVER = True
            return -1

    def reset(self):
        self.move_dir_x = 0
        self.move_dir_y = 0
        self.frame = 0
        self.speed = 1
        self.score = 0
        self.points_coordinates = self.default_pos.copy()
        global GAME_OVER, GAME_STARTED, MOVMENT_BUSY
        GAME_OVER = False
        GAME_STARTED = False
        MOVMENT_BUSY = False

player = Player()  # spawn player
fruit = Fruit()
info_text = InfoText()

# Run until the user asks to quit
running = True
fruit.update()
while running:
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if GAME_OVER:
                    player.reset()
                continue
            if not MOVMENT_BUSY:
                if event.key == pygame.K_RIGHT:
                    player.update(1,0)
                if event.key == pygame.K_LEFT:
                    if GAME_STARTED:
                        player.update(-1,0)
                if event.key == pygame.K_UP:
                    if GAME_STARTED:
                        player.update(0, -1)
                if event.key == pygame.K_DOWN:
                    player.update(0, 1)
                
                GAME_STARTED = True
                MOVMENT_BUSY = True

    # Fill the background with white
    screen.fill(BLACK)

    # Draw a solid blue circle in the center
    for pos_row in range(20) :
        pygame.draw.line(screen, GRAY, (0, (pos_row + 1) * LINES_DIST), (WIN_W, (pos_row + 1) * LINES_DIST), 1)
    for pos_colum in range(19) :
        pygame.draw.line(screen, GRAY, ((pos_colum + 1) * LINES_DIST, 0), ((pos_colum + 1) * LINES_DIST, WIN_H - 20), 1)
        
    pygame.time.get_ticks()

    # Flip the display
    if GAME_OVER:
            info_text.draw_game_over()
    player.draw()
    fruit.draw()
    fruit.draw()
    info_text.draw_score()
    GAME_CLOCK.tick(FPS)
    pygame.display.update()

# Done! Time to quit.
pygame.quit()