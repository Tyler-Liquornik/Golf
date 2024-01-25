import pygame
import math
import random
import sys
import os

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 220, 0)
GRAY = (220, 220, 220)

windowXDim = 900
windowYDim = 500
window = pygame.display.set_mode((windowXDim, windowYDim))
window.fill(GREEN)
pygame.display.set_caption("Golf")
clock = pygame.time.Clock()
clicking = False
clicked_on_ball = False

borderPercent = 0.10
xBorder = round(windowXDim * borderPercent)
yBorder = round(windowYDim * borderPercent)

ballXCoord = windowXDim // 2
ballYCoord = windowYDim // 2
ballCenter = [ballXCoord, ballYCoord]
ballRadius = 7
ballXDim = ballYDim = ballRadius * 2
ballLocation = pygame.Rect(ballCenter[0] - ballRadius, ballCenter[1] - ballRadius, ballXDim, ballYDim)

power = 1

flagPresent = False
flagScale = 0.25
flagXDim = round(279 * flagScale)
flagYDim = round(349 * flagScale)
flag = pygame.transform.scale((pygame.image.load(os.path.join("Assets", "Flag.png"))), (flagXDim, flagYDim))
flagLocation = ""


pygame.draw.circle(window, WHITE, ballCenter, ballRadius)
pygame.display.flip()


def mouse_pos():
    return [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]


def mouse_distance_to_ball():
    sqx = (mouse_pos()[0] - ballCenter[0]) ** 2
    sqy = (mouse_pos()[1] - ballCenter[1]) ** 2
    distance = math.sqrt(sqx + sqy)
    return distance


def is_clicking_on_ball():
    if clicking:
        if mouse_distance_to_ball() < ballRadius:
            return True


while True:
    clock.tick(500)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False

    if is_clicking_on_ball():
        pygame.draw.circle(window, GRAY, ballCenter, ballRadius)
        pygame.display.flip()
        clicked_on_ball = True

    if not flagPresent:

        flagXCoord = random.choice(range(xBorder, windowXDim - xBorder - flagXDim))
        flagYCoord = random.choice(range(yBorder, windowYDim - yBorder - flagYDim))
        flagLocation = pygame.Rect(flagXCoord, flagYCoord, flagXDim, flagYDim)
        if not flagLocation.colliderect(ballLocation):
            window.blit(flag, (flagXCoord, flagYCoord))
            pygame.display.flip()
            flagPresent = True

    if clicked_on_ball:

        if not clicking:

            instantMouseX = mouse_pos()[0]
            instantMouseY = mouse_pos()[1]
            instantBallX = ballCenter[0]
            instantBallY = ballCenter[1]

            deltaX = round((instantMouseX - instantBallX) * power)
            deltaY = round((instantMouseY - instantBallY) * power)
            error = 0

            if deltaX != 0:
                absSlope = abs(deltaY / deltaX)
            else:
                absSlope = math.inf

            if absSlope <= 1:

                y = ballCenter[1]

                if deltaX < 0:
                    loopRange = range(round(instantBallX), round(-deltaX + instantBallX))
                else:
                    loopRange = range(round(instantBallX), round(-deltaX + instantBallX), -1)

                for x in loopRange:

                    pygame.draw.circle(window, GREEN, ballCenter, ballRadius)
                    ballCenter = [x, y]
                    error = error + absSlope
                    ballLocation = pygame.Rect(ballCenter[0] - ballRadius, ballCenter[1] - ballRadius,
                                               ballXDim, ballYDim)
                    if ballLocation.colliderect(flagLocation):
                        window.fill(GREEN)
                        flagPresent = False

                    pygame.draw.circle(window, WHITE, ballCenter, ballRadius)
                    pygame.display.flip()
                    if error >= 0.5:
                        y = y - math.copysign(1, deltaY)
                        error -= 1

            else:

                x = ballCenter[0]

                absSlope = abs(deltaX / deltaY)

                if deltaY < 0:
                    loopRange = range(round(instantBallY), round(-deltaY + instantBallY))
                else:
                    loopRange = range(round(instantBallY), round(-deltaY + instantBallY), -1)

                for y in loopRange:
                    pygame.draw.circle(window, GREEN, ballCenter, ballRadius)
                    ballCenter = [x, y]
                    error = error + absSlope
                    ballLocation = pygame.Rect(ballCenter[0] - ballRadius, ballCenter[1] - ballRadius,
                                               ballXDim, ballYDim)
                    if ballLocation.colliderect(flagLocation):
                        window.fill(GREEN)
                        flagPresent = False

                    pygame.draw.circle(window, WHITE, ballCenter, ballRadius)
                    pygame.display.flip()
                    if error >= 0.5:
                        x = x - math.copysign(1, deltaX)
                        error -= 1

            clicked_on_ball = False
