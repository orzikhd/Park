import sys

import pygame

import park.park_util as pu
from park.constructs.rock import create_rock
from park.creatures.bug import Bug
from park.creatures.grass import Grass
from park.park_state import State


def run_park():
    # larger context
    pygame.init()

    # create game state
    state = pu.time_and_log(lambda: State(), "Time to generate state:")

    active_grasses = pygame.sprite.RenderUpdates()
    grasses = pygame.sprite.RenderUpdates()
    creatures = pygame.sprite.RenderUpdates()

    # create grass
    first_grass = Grass(state.screen, state, (240, 240), .5, 1)
    first_grass.add(active_grasses)
    first_grass.add(grasses)

    # create rocks
    rocks = [
        create_rock(state.screen, state, starting_position=(60, 60), size=2),
        create_rock(state.screen, state, starting_position=(0, 420), size=4),
        create_rock(state.screen, state, starting_position=(500, 420), size=1),
        create_rock(state.screen, state, starting_position=(360, 260), size=3)
    ]

    # add a bug
    bug_one = Bug(state.screen, state, starting_position=(0, 0), scaler=1, fertility=1, speed=5)
    bug_two = Bug(state.screen, state, starting_position=(200, 200), scaler=1, fertility=1, speed=10)
    bug_three = Bug(state.screen, state, starting_position=(300, 300), scaler=1, fertility=1, speed=15)
    bug_one.add(creatures)
    bug_two.add(creatures)
    bug_three.add(creatures)
    going = True
    while going:
        state.clock.tick(20)
        # print("all", len(state.global_sprites))
        # print("active", len(active_sprites))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        active_grasses.update()
        # print("global counter", state.global_sprite_counter)
        for rock in rocks:
            rock.group.update()

        # fill in creatures with background and redraw them, for movement
        old_spots = [creature.rect for creature in creatures.sprites()]
        creatures.update()
        for rect in old_spots:
            state.screen.blit(state.terrain_screen, rect, rect)

        dirty_recs = []
        # TODO Get just the active grasses + grasses walked on
        # TODO Otherwise it slows down a lot with a lot of grass
        dirty_recs += grasses.draw(state.screen)

        for rock in rocks:
            dirty_recs += rock.group.draw(state.screen)

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
