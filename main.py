import pygame
import math
import random

pygame.init()

w = 768     # window width
h = 768     # window height

bg = pygame.image.load('space.png')
playerShip = pygame.image.load('spaceship.png')   # player
ast32 = pygame.image.load('asteroid32.png')
ast64 = pygame.image.load('asteroid64.png')
ast96 = pygame.image.load('asteroid96.png')

pygame.display.set_caption('Asteroids')
window = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()


class Player(object):
    def __init__(self):
        self.img = playerShip
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = w//2
        self.y = h//2 
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.rotateSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotateSurf.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
        self.accel = 0


    def draw(self, window):
        window.blit(self.rotateSurf, self.rotateRect)

    def leftArrow(self):
        self.angle += 5
        self.rotateSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotateSurf.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2) 

    def rightArrow(self):
        self.angle -= 5
        self.rotateSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotateSurf.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)


    def upArrow(self):
        # self.x += self.cosine * 6
        # self.y -= self.sine * 6
        self.x += self.dx
        self.y -= self.dy
        self.rotateSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotateSurf.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.dx += self.cosine * 0.1 
        self.dy += self.sine * 0.1
        if math.hypot(self.x, self.y) > 1:
            self.dx -= self.cosine * 0.07
            self.dy -= self.sine * 0.07
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)


    def checkPos(self):
        if self.x > w + 50:
            self.x = 0
        elif self.x < 0- self.w:
            self.x = w
        elif self.y < -50:
            self.y = h
        elif self.y > h + 50:
            self.y = 0
    
    def reset(self):
        self.x = w//2
        self.y = h//2 
        self.dx = 0
        self.dy = 0
        self.angle = 0


class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.xVel = player.cosine * 10
        self.yVel = player.sine * 10

    def move(self):
        self.x += self.xVel
        self.y -= self.yVel

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def offScreen(self):
        if self.x > w or self.x < -50 or self.y > h or self.y < -50:
            return True


class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = ast32
        elif self.rank == 2:
            self.image = ast64
        else:
            self.image = ast96
        self.w = 32 * rank
        self.h = 32 * rank

        self.ranPoint = random.choice([(random.randrange(0, w - self.w),
        random.choice([-1 * self.h - 5, h + 5])), 
        (random.choice([-1 * self.w - 5, w + 5]), 
        random.randrange(0, h - self.h))])

        self.x, self.y = self.ranPoint
        if self.x < w//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < h//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xVel = self.xdir * random.randrange(1,3)
        self.yVel = self.ydir * random.randrange(1,3)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        

def redrawGameWindow():
    window.blit(bg, (0,0))
    font = pygame.font.Font("ARCADE_N.TTF", 20)
    bigFont = pygame.font.Font("ARCADE_N.TTF", 50)

    livesDisplay = font.render('Lives:' + str(lives), 1, (255,255,255))
    scoreDisplay = font.render('Score:' + str(score), 1, (255,255,255))

    overTxt = bigFont.render('GAME OVER', 1, (255,255,255))

    player.draw(window)
    for b in ammo:
        b.draw(window)
    for a in asteroids:
        a.draw(window)

    window.blit(livesDisplay, (575,25))
    window.blit(scoreDisplay, (575, 25 - livesDisplay.get_height()))

    if endGame:
        window.blit(overTxt, (w//2-overTxt.get_width()//2, h//2-overTxt.get_height()//2))
        

    pygame.display.update()

endGame = False
lives = 3
score = 0
rapidFire = False

player = Player()
ammo = []
asteroids = []
i = 0

run = True
while run:
    clock.tick(60)  # framerate
    i += 1
    if not endGame:
        if i % 50 == 0:
            rand = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(rand))
        player.checkPos()
        for b in ammo:
            b.move()
            if b.offScreen():
                ammo.pop(ammo.index(b))
        for a in asteroids:
            a.x += a.xVel
            a.y += a.yVel

            # Collision with asteroids
            if (player.x >= a.x and player.x <= a.x + a.w) or (player.x + player.w >= a.x and player.x + player.w <= a.x + a.w):
                if(player.y >= a.y and player.y <= a.y + a.h) or (player.y + player.h >= a.y and player.y + player.h <= a.y + a.h):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break

            # If bullet hits asteroid
            for b in ammo:
                # Check if bullet x and y coords is inside the asteroid
                if (b.x >= a.x and b.x <= a.x + a.w) or (b.x + b.w >= a.x and b.x + b.w <= a.x + a.w):
                    if (b.y >= a.y and b.y <= a.y + a.h) or (b.y + b.h >= a.y and b.y + b.h <= a.y + a.h):
                        if a.rank == 3:
                            score += 1
                            subAst = Asteroid(2)
                            subAst2 = Asteroid(2)
                            subAst3 = Asteroid(2)
                            subAst.x = a.x
                            subAst2.x = a.x
                            subAst3.x = a.x
                            subAst.y = a.y
                            subAst2.y = a.y
                            subAst3.y = a.y
                            asteroids.append(subAst)
                            asteroids.append(subAst2)
                            asteroids.append(subAst3)
                        elif a.rank == 2:
                            score += 5
                            subAst = Asteroid(1)
                            subAst2 = Asteroid(1)
                            subAst.x = a.x
                            subAst2.x = a.x
                            subAst.y = a.y
                            subAst2.y = a.y
                            asteroids.append(subAst)
                            asteroids.append(subAst2)
                            asteroids.append(subAst)
                            asteroids.append(subAst2)
                        else:
                            score += 10
                        asteroids.pop(asteroids.index(a))   # pop initial asteroid
                        ammo.pop(ammo.index(b))             # pop bullet

    if lives == 0:
        player.reset()
        endGame = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.leftArrow()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.rightArrow()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.upArrow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not endGame:
                    ammo.append(Bullet())
                else:
                    endGame = False
                    player.x = w//2
                    player.y = h//2
                    lives = 3
                    asteroids.clear()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not endGame:
                    ammo.append(Bullet())
                else:
                    endGame = False
                    lives = 3
                    score = 0
                    asteroids.clear()


    redrawGameWindow()

pygame.quit()

