import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
import pygame.time

pygame.init()

# Game clock
clock = pygame.time.Clock()
current_time = 0

# Create the Screen
screen_height = 800
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Background image
background = pygame.image.load("background.png")

# Background sound
# mixer.music.load("")
# mixer.music.play(loop)

# Title and Icon
pygame.display.set_caption("Fun Blasters")
icon = pygame.image.load("icon_32_1.png")
pygame.display.set_icon(icon)

# Menu
menu = True
menu_top = (screen_height / 2) - (screen_height / 4)
# Cursor options: "start"  "options
cursor_y = "start"

# Player
playerImg = pygame.image.load("player_asset_64_1.png")
playerX = (screen_width / 2) - 32
playerY = screen_height - 120
playerX_change = 0

# Records if Left or Right buttons are held
playerX_left_button_held = False
playerX_right_button_held = False

# Weapons
weapon_starting_y = playerY

# Enemy
enemy_x_speed = 5
enemy_y_speed = 40
enemy_image = []
enemy_exp = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 8
new_enemy_timer = 0
enemy_wall_edge_left = 0
enemy_wall_edge_right = screen_width - 65
enemy_spawn_edge_left = 20
enemy_spawn_edge_right = screen_width - 85
enemy_spawn_edge_top = 20
enemy_spawn_edge_bottom = 150
enemy_death_speed_increaseX = 0.2
enemy_death_speed_increaseY = 5
enemy_starting_exp = 0

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load("enemy_asset_64_1.png"))
    enemy_x.append(random.randint(enemy_spawn_edge_left, enemy_spawn_edge_right))
    enemy_y.append(random.randint(enemy_spawn_edge_top, enemy_spawn_edge_bottom))
    enemy_x_change.append(enemy_x_speed)
    enemy_y_change.append(enemy_y_speed)
    enemy_exp.append(enemy_starting_exp)


# Weapons - Laser and Big Blast
# ready - you can't see the big blast on the screen
# fire - the laser is currently on screen moving
class Weapon:
    def __init__(self):
        self.x = 0
        self.y = screen_height - 120
        self.x_change = 0
        self.state = "ready"


class Laser(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser_asset_1.png")
        self.sound = mixer.Sound("laser_noise.wav")
        self.y_change = 6

    def fire_laser(self, x, y):
        self.state = "fire"
        screen.blit(self.image, (x + 16, y + 10))


class Big_Blast(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("big_blast_asset_1.png")
        self.sound = mixer.Sound("laser_noise.wav")
        self.y_change = 4

    def fire_big_blast(self, x, y):
        self.state = "fire"
        screen.blit(self.image, (x + 16, y + 10))


class Big_Blast_Explode(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("big_blast_explosion.png")
        self.state = "ready"
        self.time = 0

    def big_blast_explode(self, x, y):
        self.state = "fire"
        screen.blit(self.image, (x, y))


# Weapons

laser1 = Laser()
laser2 = Laser()
big_blast = Big_Blast()
big_blast_explode = Big_Blast_Explode()

# Scoring System
score_value = 0
font = pygame.font.Font('press_start_2p.ttf', 32)
textX = 10
textY = 10

# Text and Fonts

# Game Over Text
over_font = pygame.font.Font("press_start_2p.ttf", 40)

# Intro Menu Font
menu_title_font = pygame.font.Font('press_start_2p.ttf', 40)

# Game Over
game_over = False


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 123))
    screen.blit(over_text, (screen_width - 580, screen_height / 2))


def draw_cursor(y):
    cursor = menu_title_font.render("*", True, (0, 255, 123))
    if y == "start":
        screen.blit(cursor, ((screen_width / 2) - 150, menu_top + 120))

    elif y == "options":
        screen.blit(cursor, ((screen_width / 2) - 150, menu_top + 180))


def cursor_move(cursor_location):
    if cursor_location == "options":
        return "start"
    elif cursor_location == "start":
        return "options"


def menu_select():
    global cursor_y
    global menu
    if cursor_y == "start":
        menu = False

    elif cursor_y == "options":
        print("options menu")


def game_intro():
    global menu
    global cursor_y

    while menu:
        # RGB
        screen.fill((3, 10, 30))
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if menu_event.type == pygame.KEYDOWN:
                if menu_event.key == pygame.K_UP or menu_event.key == pygame.K_DOWN:
                    cursor_y = cursor_move(cursor_y)
                elif menu_event.key == pygame.K_SPACE or pygame.K_RETURN:
                    menu_select()

        menu_title_text = menu_title_font.render("Fun Blasters!", True, (0, 255, 123))
        screen.blit(menu_title_text, (135, menu_top))

        menu_title_text = menu_title_font.render("Start", True, (0, 255, 123))
        screen.blit(menu_title_text, ((screen_width / 2) - 100, menu_top + 120))

        menu_title_text = menu_title_font.render("Options", True, (0, 255, 123))
        screen.blit(menu_title_text, ((screen_width / 2) - 100, menu_top + 180))

        draw_cursor(cursor_y)

        pygame.display.update()
        clock.tick(15)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (135, 0, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def enemy_death(i):
    global score_value
    score_value += 1
    enemy_exp[i] += 1
    enemy_y_change[i] += enemy_death_speed_increaseY
    if enemy_x_change[i] > 0:
        enemy_x_change[i] += enemy_death_speed_increaseX
    if enemy_x_change[i] < 0:
        enemy_x_change[i] -= enemy_death_speed_increaseX
    enemy_x[i] = random.randint(enemy_spawn_edge_left, enemy_spawn_edge_right)
    enemy_y[i] = random.randint(enemy_spawn_edge_top, enemy_spawn_edge_bottom)


def new_enemy():
    # Produce Additional Enemies while playing
    global num_of_enemies
    num_of_enemies += 1
    enemy_image.append(pygame.image.load("enemy_asset_64_1.png"))
    enemy_x.append(random.randint(enemy_spawn_edge_left, enemy_spawn_edge_right))
    enemy_y.append(random.randint(enemy_spawn_edge_top, enemy_spawn_edge_bottom))
    enemy_x_change.append(enemy_x_speed)
    enemy_y_change.append(enemy_y_speed)
    enemy_exp.append(enemy_starting_exp)


def collision_calc(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def is_collision(enemy_x_fun, enemy_y_fun, weapon_x, weapon_y):
    distance = collision_calc(enemy_x_fun, enemy_y_fun, weapon_x, weapon_y)
    if distance < 30:
        return True
    else:
        return False


def is_explode_collision(enemy_x_fun, enemy_y_fun, weapon_x, weapon_y):
    distance = collision_calc(enemy_x_fun, enemy_y_fun, weapon_x, weapon_y)
    if distance < 60:
        return True
    else:
        return False


def game_over_collision(enemy_x_fun, enemy_y_fun, player_x, player_y):
    distance = collision_calc(enemy_x_fun, enemy_y_fun, player_x, player_y)
    if distance < 50:
        return True
    else:
        return False


game_intro()

# Game Loop
running = True

while running:

    # RGB
    screen.fill((3, 10, 30))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_left_button_held = True

            if event.key == pygame.K_RIGHT:
                playerX_right_button_held = True

            # Gets the current x coordinate of the player
            # for the weapon firing
            if event.key == pygame.K_SPACE:
                if laser1.state == "ready":
                    laser1.sound.play()
                    laser1.x = playerX
                    laser1.fire_laser(laser1.x, laser1.y)

                elif laser2.state == "ready":
                    laser2.sound.play()
                    laser2.x = playerX
                    laser2.fire_laser(laser2.x, laser2.y)

                elif big_blast.state == "ready":
                    big_blast.sound.play()
                    big_blast.x = playerX
                    big_blast.fire_big_blast(big_blast.x, big_blast.y)

        # If keystroke is removed check if it is right or left
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                playerX_left_button_held = False

            if event.key == pygame.K_RIGHT:
                playerX_right_button_held = False

        # If Left only is held go left, if right only is held go right, if both or neither are held dont move
        if playerX_left_button_held and playerX_right_button_held:
            playerX_change = 0
            playerImg = pygame.image.load("player_asset_64_1.png")

        if playerX_left_button_held and not playerX_right_button_held:
            playerX_change = -7
            playerImg = pygame.image.load("player_asset_left_64_1.png")

        if playerX_right_button_held and not playerX_left_button_held:
            playerX_change = 7
            playerImg = pygame.image.load("player_asset_right_64_1.png")

        if not playerX_right_button_held and not playerX_left_button_held:
            playerX_change = 0
            playerImg = pygame.image.load("player_asset_64_1.png")

    # Player movement
    playerX += playerX_change

    # Wall boundary for Player
    if playerX <= 5:
        playerX = 5
    elif playerX >= 730:
        playerX = 730

    # Enemy movement

    for i in range(num_of_enemies):

        # Game Over Enemy too Low
        if enemy_y[i] > 660:
            game_over = True

        # Game Over Enemy Collision
        kill_collision = game_over_collision(enemy_x[i], enemy_y[i], playerX, playerY)
        if kill_collision:
            game_over = True

        if game_over:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        # Level Up Enemy
        if enemy_exp[i] > 5:
            enemy_image[i] = pygame.image.load("enemy_level2_asset_64_1.png")
            if enemy_exp[i] > 10:
                enemy_image[i] = pygame.image.load("enemy_level3_asset_64_1.png")

        # Wall boundary for Enemy
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= enemy_wall_edge_left:
            enemy_x_change[i] = (-enemy_x_change[i])
            enemy_y[i] += enemy_y_change[i]

        elif enemy_x[i] >= enemy_wall_edge_right:
            enemy_x_change[i] = (-enemy_x_change[i])
            enemy_y[i] += enemy_y_change[i]

        # Collision Laser
        collision = is_collision(enemy_x[i], enemy_y[i], laser1.x, laser1.y)
        if collision:
            laser1.y = weapon_starting_y
            laser1.state = "ready"
            enemy_death(i)

        # Collision Laser2
        collision = is_collision(enemy_x[i], enemy_y[i], laser2.x, laser2.y)
        if collision:
            laser2.y = weapon_starting_y
            laser2.state = "ready"
            enemy_death(i)

        # Collision Big Blast
        collision = is_collision(enemy_x[i], enemy_y[i], big_blast.x, big_blast.y)
        if collision:
            big_blast_explode.x = big_blast.x - 32
            big_blast_explode.y = big_blast.y - 32
            big_blast_explode.time = pygame.time.get_ticks()
            big_blast_explode.big_blast_explode(big_blast_explode.x, big_blast_explode.y)
            big_blast.y = weapon_starting_y
            big_blast.state = "ready"
            enemy_death(i)

        # Collision Fuck Blast Explode
        explode_collision = is_explode_collision(enemy_x[i], enemy_y[i], big_blast_explode.x, big_blast_explode.y)
        if explode_collision:
            enemy_death(i)

        enemy(enemy_x[i], enemy_y[i], i)

    # Laser movement
    if laser1.y <= 0:
        laser1.y = weapon_starting_y
        laser1.state = "ready"

    if laser1.state == "fire":
        laser1.fire_laser(laser1.x, laser1.y)
        laser1.y -= laser1.y_change

    # Laser movement

    if laser2.y <= 0:
        laser2.y = weapon_starting_y
        laser2.state = "ready"

    if laser2.state == "fire":
        laser2.fire_laser(laser2.x, laser2.y)
        laser2.y -= laser2.y_change

    # Big Blast movement

    if big_blast.y <= 0:
        big_blast.y = weapon_starting_y
        big_blast.state = "ready"

    if big_blast.state == "fire":
        big_blast.fire_big_blast(big_blast.x, big_blast.y)
        big_blast.y -= big_blast.y_change

    # Big Blast Explode
    current_time = pygame.time.get_ticks()

    if big_blast_explode.state == "fire":
        big_blast_explode.big_blast_explode(big_blast_explode.x, big_blast_explode.y)

        if current_time - big_blast_explode.time > 1000:
            big_blast_explode.state = "ready"
            big_blast_explode.x = 0
            big_blast_explode.y = 1000

    if not game_over:
        if current_time - new_enemy_timer > 4000:
            new_enemy_timer = pygame.time.get_ticks()
            new_enemy()
            score_value += 5

    show_score(textX, textY)

    clock.tick(60)

    player(playerX, playerY)

    pygame.display.update()
