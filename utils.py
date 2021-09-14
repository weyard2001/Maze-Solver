import pygame
import sys
import time
import config as cf

def checkPygameEvents():
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            sys.exit()

def draw(x, y, color, sleepTime = 0.005, update = True):
    checkPygameEvents()

    pygame.draw.rect(cf.scr, color, (x * cf.cellSize, y * cf.cellSize, cf.cellSize, cf.cellSize))
    if update:
        pygame.display.update()

    time.sleep(sleepTime)