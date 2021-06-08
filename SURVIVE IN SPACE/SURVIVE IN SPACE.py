import pygame
import random
import sys
from pygame.locals import *

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 50)
FPS = 60
ASTEROID_MIN_SIZE = 10
ASTEROID_MAX_SIZE = 40
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 8
ADD_NEW_ASTEROID_RATE = 6
PLAYER_MOVE_RATE = 5

def end():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    end()
                return

def playerHasHitAsteroid(playerRect, asteroids):
    for b in asteroids:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('SURVIVE IN SPACE')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
playerImage = pygame.image.load('rocket.png')
playerRect = playerImage.get_rect()
asteroidImage = pygame.image.load('asteroid.png')

# show the "Start" screen
drawText('SURVIVE IN SPACE', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOW_WIDTH / 3) - 30, (WINDOW_HEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    asteroids = []
    score = 0
    playerRect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    asteroidAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                end()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        end()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new asteroids at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            asteroidAddCounter += 1
        if asteroidAddCounter == ADD_NEW_ASTEROID_RATE:
            asteroidAddCounter = 0
            asteroidSize = random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
            newAsteroid = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-asteroidSize), 0 - asteroidSize, asteroidSize, asteroidSize),
                        'speed': random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED),
                        'surface':pygame.transform.scale(asteroidImage, (asteroidSize, asteroidSize)),
                        }

            asteroids.append(newAsteroid)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if moveRight and playerRect.right < WINDOW_WIDTH:
            playerRect.move_ip(PLAYER_MOVE_RATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if moveDown and playerRect.bottom < WINDOW_HEIGHT:
            playerRect.move_ip(0, PLAYER_MOVE_RATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the asteroids down.
        for b in asteroids:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete asteroids that have fallen past the bottom.
        for b in asteroids[:]:
            if b['rect'].top > WINDOW_HEIGHT:
                asteroids.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUND_COLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each asteroid
        for b in asteroids:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the asteroids have hit the player.
        if playerHasHitAsteroid(playerRect, asteroids):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOW_WIDTH / 3) - 80, (WINDOW_HEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
