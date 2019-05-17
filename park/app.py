import sys
import time
import pygame

from park.creatures.park_grass import Grass
from park.creatures.park_bug import Bug
from park.constructs.multisprite import Multisprite
from park.park_state import State


def run_park():
    # larger context
    pygame.init()

    # create dirt
    start = time.time()
    state = State()
    print("time to generate state", (time.time() - start) * 1000, "ms")

    active_grasses = pygame.sprite.RenderUpdates()
    grasses = pygame.sprite.Group()
    creatures = pygame.sprite.RenderUpdates()

    # create grass
    first_grass = Grass(state.screen, state, (240, 240), .5, 10)
    first_grass.add(active_grasses)
    first_grass.add(grasses)
    #
    # # create boulders
    # boulder1 = Multisprite(state.screen, state, (60, 60))
    # boulder2 = Multisprite(state.screen, state, (300, 360))

    # add a bug
    bug_one = Bug(state.screen, state, (0, 0), .5, 1, 10)
    bug_one.add(creatures)
    print(state.width)
    print(state.height)
    going = True
    while going:
        state.clock.tick(40)
        # print("all", len(state.global_sprites))
        # print("active", len(active_sprites))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        active_grasses.update()
        # print("global counter", state.global_sprite_counter)
        # boulder1.group.update()
        # boulder2.group.update()
        old_spots = [creature.rect for creature in creatures.sprites()]
        creatures.update()
        for rec in old_spots:
            state.screen.blit(state.background_screen, rec, rec)
        dirty_recs = old_spots
        dirty_recs += active_grasses.draw(state.screen)
        # dirty_recs += boulder1.group.draw(state.screen)
        # dirty_recs += boulder2.group.draw(state.screen)
        dirty_recs += creatures.draw(state.screen)

        pygame.display.update(dirty_recs)

        if not len(active_grasses):
            # going = False
            print("out of active grasses")
        # print(len(active_sprites))


if __name__ == "__main__":
    run_park()

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
