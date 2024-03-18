import pygame
pygame.init()

from random import choice
import math
from utils import clamp, drawText, isColliding
from settings import HEIGHT, WIDTH, speed, px, py, speedBoost

screen = pygame.display.set_mode([WIDTH, HEIGHT])

sprite_loc = lambda _ : "Catch_Rush/res/sprites/"+_
PLAYER_SPRITE = pygame.image.load(sprite_loc("bucket2.png")).convert_alpha()

def drawPlayer ():
    rect = PLAYER_SPRITE.get_rect(topleft=(px, py))
    screen.blit(PLAYER_SPRITE, rect)

fallables_sprites = list(map(lambda _ : pygame.image.load(_).convert_alpha(), (
    sprite_loc("tomato.png"),
)))

fallables = [] # [[x,y,sprite_index]]
def drawFallables ():
    for fallable in fallables:
        fx,fy,f_id = fallable
        rect = fallables_sprites[f_id].get_rect(topleft=(fx,fy))
        screen.blit(fallables_sprites[f_id], rect)

def addFallables(dt):
    fallables.append([choice(range(40,WIDTH-40)), -50,0])
    pass

fallableSpeed = 0.1
lastAdded = 0
def updateFallables(dt):
    global lastAdded
    lastAdded += dt

    # add new fallable after 3 secs
    if lastAdded > choice(range(1000, 3000)):
        lastAdded = 0
        addFallables(dt)

    # updating fallable Y locations
    for fallable in fallables:
        fallable[1] += fallableSpeed*dt
        pass

    # removing fallables which are out of screen
    a=0
    while a < len(fallables):
        fy = fallables[a][1]
        if fy > HEIGHT + 50:
            fallables.pop(a)
            onMiss()
            continue
        a+=1
    pass

    drawFallables()


lastFPS = 0
fps = 60
def showFPS(dt):
    global lastFPS
    global fps
    lastFPS += dt
    drawText(screen, "FPS:"+str(int(fps)), (WIDTH-60,10))
    if lastFPS < 1000:
        return
    fps = 1000/dt
    lastFPS = 0

def onMiss():
    global score
    score -= 10
    if score < 0: score=0

def checkCollision():
    if len(fallables) < 1 : 
        return
    indices = list()

    for (i,fallable) in enumerate(fallables):
        # print(fallable)
        fx,fy,f_id = fallable
        if isColliding(
            (px,py,63,33),
            (fx,fy,40,40)
        ):
            indices.append(i)

    for i in indices:
        onCollide(i)

score = 0
def onCollide(i):
    global score
    score += 1
    fallables.pop(i)

def updateScore():
    drawText(screen, "Score : "+str(score), )

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt=clock.tick(60)
    # print(dt)
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()

    newSpeed = speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        newSpeed += speedBoost

    if keys[pygame.K_LEFT]:
        px -= newSpeed*dt
    if keys[pygame.K_RIGHT]:
        px += newSpeed*dt
    
    px = clamp(20,WIDTH-80, px)
        
    updateFallables(dt)
    showFPS(dt)

    drawPlayer()
    updateScore()
    pygame.display.flip()
    checkCollision()


pygame.quit()