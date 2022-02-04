import pygame
import random
import math

from pygame import mixer
# from pygame.constants import K_RETURN

# Initialize game
pygame.init()

# Create game window
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Customizing the Window
pygame.display.set_caption("Game that is bad")

background = pygame.image.load('stars.png')
splash = pygame.image.load('splash.png')

icon = pygame.image.load('Minimal_Profile.png')
pygame.display.set_icon(icon)

# Start Font
start_font = pygame.font.Font('freesansbold.ttf', 48)


# Splash Screen
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                    pygame.quit()
                    quit()
        screen.fill((0, 0, 0))
        screen.blit(splash, (390, 110))
        game_start = start_font.render("PRESS ENTER TO BEGIN", True, (255, 255, 255))
        screen.blit(game_start, (350, 650))
        pygame.display.update()
        clock.tick(5)


# Background Music
mixer.music.load('music.wav')
mixer.music.set_volume(0.25)
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 600
playerY = 600
playerX_change = 0
playerSpeed = 10

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
enemySpeed = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 1216))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemySpeed)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 600
bulletSpeed = 20
bulletY_change = 20
bullet_state = "ready"

# Score
score_value = 0

font = pygame.font.Font('freesansbold.ttf', 36)

textX = 10
textY = 10

# Game End
end_font = pygame.font.Font('freesansbold.ttf', 72)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 24, y + 16))


def isColliding(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 25:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_end = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_end, (400, 300))


# Keep window open
def game_loop():
    # Variables
    running = True
    global playerX
    global playerX_change
    global playerY
    global bulletX
    global bulletY
    global bulletY_change
    global enemyX
    global enemyY
    global enemyX_change
    global enemyY_change
    global bullet_state

    while running:
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                running = False
            # Input from player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1 * playerSpeed
                if event.key == pygame.K_RIGHT:
                    playerX_change = playerSpeed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_sound = mixer.Sound('shoot.wav')
                        bullet_sound.play()
                        fire_bullet(bulletX, playerY)
                    
            # Revert Player Movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and playerX_change < 0:
                    playerX_change = 0
                if event.key == pygame.K_RIGHT and playerX_change > 0:
                    playerX_change = 0

        # Screen Updates
        screen.fill((0, 255, 255))
        screen.blit(background, (0, 0))
        
        # Player Movement
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 1216:
            playerX = 1216
        player(playerX, playerY)

        # Enemy Movement
        for i in range(num_of_enemies):
            # Game End
            if enemyY[i] > 550:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = enemySpeed
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 1216:
                enemyX_change[i] = -1 * enemySpeed
                enemyY[i] += enemyY_change[i]
            enemy(enemyX[i], enemyY[i], i)

            # Collision Detection
            colliding = isColliding(enemyX[i], enemyY[i], bulletX, bulletY)
            if colliding:
                hit_sound = mixer.Sound('hit.wav')
                hit_sound.play()
                bullet_state = "ready"
                bulletY = 600
                global score_value
                score_value += 1
                enemyX[i] = (random.randint(0, 1216))
                enemyY[i] = (random.randint(50, 150))

        # Bullet Movement
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = 600
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Player Score
        show_score(textX, textY)

        pygame.display.update()


game_intro()
game_loop()
pygame.quit()
quit()
