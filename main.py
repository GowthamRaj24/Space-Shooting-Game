import math
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
game_on = True
pygame.display.set_caption("Grand Shooting")
game_icon = pygame.image.load('data/logo.png')
pygame.display.set_icon(game_icon)
bg = pygame.image.load('data/spacebg.png')
count = 0

# sounds
pygame.mixer.music.load('data/background.wav')
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound('data/laser_sound.wav')
collision_sound = pygame.mixer.Sound('data/collision.wav')
game_over_sound = pygame.mixer.Sound('data/game_over.wav')
start_game_sound = pygame.mixer.Sound('data/start_game.wav')
# Add font
score_Font = pygame.font.Font('data/Aldrich-Regular.ttf', 30)
game_over_font = pygame.font.Font('data/Aldrich-Regular.ttf', 54)
restart_font = pygame.font.Font('data/Aldrich-Regular.ttf', 24)


def show_game_over():
    score_img = score_Font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(score_img, (300, 250))


def show_restart():
    restart_img = restart_font.render('Press R to Restart', True, (255, 255, 0))
    screen.blit(restart_img, (300, 350))


def show_score(c, x, y):
    score_img = score_Font.render("SCORE : " + str(c), True, (255, 255, 255))
    screen.blit(score_img, (x, y))


# player
player_icon = pygame.image.load('data/player.png')
playerX = 400 - 35
playerY = 500
playerX_change = 0
playerY_change = 0

# Enemy
enemy_icon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
n = 5
for i in range(n):
    enemy_icon.append(pygame.image.load('data/enemy.png'))
    enemyX.append(random.randint(25, 710))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.randint(10, 20))
    enemyY_change.append(50)

# Bullet
bullet_icon = pygame.image.load('data/bullet.png')
bulletX = 400 - 35 + 20
bulletY = 500 + 10
bulletY_change = -25
bullet_state = 'ready'
game_state = 'running'

explosion_icon = pygame.image.load('data/explosion.png')


def collision(x1, y1, x2, y2):
    distance1 = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance1 < 25:
        return True
    else:
        return False


def hit(x1, y1, x2, y2):
    distance1 = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance1 < 50:

        return True
    else:
        return False


def move_enemy(x, y, a):
    screen.blit(enemy_icon[a], (x, y))


def move_player(x, y):
    screen.blit(player_icon, (x, y))


def move_bullet(x, y):
    screen.blit(bullet_icon, (x + 20, y))


while game_on:
    screen.fill((100, 150, 250))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -12
            if event.key == pygame.K_RIGHT:
                playerX_change = +12
            if event.key == pygame.K_UP:
                playerY_change = -12
            if event.key == pygame.K_DOWN:
                playerY_change = 12
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_state = 'fire'
                    bulletX = playerX
                    bulletY = playerY
                    move_bullet(bulletX, bulletY)
                    bullet_sound.play()
            if event.key == pygame.K_r:
                start_game_sound.play()
                if game_state == 'end':
                    for i in range(n):
                        enemyX[i] = random.randint(25, 710)
                        enemyY[i] = random.randint(50, 150)
                        game_state = 'running'

                    pygame.mixer.music.play(-1)
                    playerX = 400 - 35
                    playerY = 500

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    for i in range(n):
        if enemyY[i] > 500 - 70 or hit(enemyX[i], enemyY[i], playerX, playerY):
            for j in range(n):
                enemyY[j] = 1200
            pygame.mixer.music.stop()
            game_over_sound.play()
            show_game_over()
            show_restart()
            show_score(show, 300, 150)
            bullet_state = "ready"
            game_state = 'end'
            count = 0
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 710:
            enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] < 25:
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        move_enemy(enemyX[i], enemyY[i], i)
        if collision(bulletX, bulletY, enemyX[i], enemyY[i]):
            screen.blit(explosion_icon, (enemyX[i], enemyY[i]))
            collision_sound.play()
            enemyX[i] = random.randint(25, 710)
            enemyY[i] = random.randint(50, 150)
            bullet_state = 'ready'
            bulletY = 500
            count += 1
            show = count
        show_score(count, 10, 10)

    playerX += playerX_change
    playerY += playerY_change
    if playerX < 50:
        playerX = 50
    elif playerX > 750 - 70:
        playerX = 750 - 70
    if playerY > 500:
        playerY = 500
    elif playerY < 300:
        playerY = 300
    if bullet_state == 'fire':
        bulletY += bulletY_change
        move_bullet(bulletX, bulletY)
        if bulletY < 20:
            bulletY = playerY
            bullet_state = 'ready'

    move_player(playerX, playerY)

    pygame.display.update()
