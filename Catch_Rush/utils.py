import pygame
from random import choice
from settings import HEIGHT, WIDTH
def clamp(min, max, val):
    if val <= min:
        return min
    if val >= max:
        return max
    return val

def getRandXY():
    return (choice(range(0,WIDTH)), choice(range(0, HEIGHT)))

font = pygame.font.SysFont('monospace', 15)
def drawText(screen, txt, pos=(10,10)):
    tx,ty=pos
    text_surface = font.render(txt, True, (0,0,0))
    text_rect = text_surface.get_rect()
    # text_rect.center = (tx,ty)
    text_rect.x = tx
    text_rect.y = ty
    screen.blit(text_surface, text_rect)

def isColliding(p1,p2):
    x1,y1,w1,h1 = p1
    x2,y2,w2,h2 = p2
    a=False
    if x1 < x2+w2 and x1+w1>x2 and y1<y2+h2 and y1+h1>y2:
        a=True
    return a