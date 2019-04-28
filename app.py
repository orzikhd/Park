import sys

import pygame

from park_grass import Grass
from park_util import global_tree, global_sprite_counter, global_sprites

# larger context
pygame.init()
size = width, height = 1000, 1000
black = 0, 0, 0
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

active_sprites = pygame.sprite.RenderUpdates()
first_grass = Grass(screen, (5, 5), 0.3)
first_grass.add(active_sprites)
global_sprite_counter += 1
global_sprites[global_sprite_counter] = first_grass
global_tree.insert(global_sprite_counter,
                   (first_grass.rect.left,
                    first_grass.rect.top,
                    first_grass.rect.right,
                    first_grass.rect.bottom))
print((first_grass.rect.left,
                    first_grass.rect.top,
                    first_grass.rect.right,
                    first_grass.rect.bottom))
print(first_grass.groups())
print(global_sprite_counter)

print(list(global_tree.intersection(
                    (521,
                     521,
                     540,
                     540))))

going = True
while going:
    clock.tick(10)
    print("all", len(global_sprites))
    print("active", len(active_sprites))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    active_sprites.update()
    dirty_recs = active_sprites.draw(screen)
    pygame.display.update(dirty_recs)

'''
size = width, height = 1080, 920
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("C:\\Users\\Dennis\\AppData\\Local\\Temp\\intro_ball.gif")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]

    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    pygame.time.delay(10)
'''

'''
class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > 600:
            self.pos.left = 0


size = width, height = 1080, 920
screen = pygame.display.set_mode(size)
ball = pygame.image.load("C:\\Users\\Dennis\\AppData\\Local\\Temp\\intro_ball.gif").convert_alpha()
ball.convert()

black = 0, 0, 0

objects = []
for x in range(10):
    o = GameObject(ball, x*40, x)
    objects.append(o)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    for o in objects:
        o.move()
        screen.blit(o.image, o.pos)

    pygame.display.update()
    pygame.time.delay(10)
'''
