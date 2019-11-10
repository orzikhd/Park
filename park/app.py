import sys
import time
from itertools import chain

import matplotlib.pyplot as plt
import pygame
from numpy.polynomial.polynomial import polyfit

import park.park_util as pu
from park.constructs.rock import create_rock
from park.creatures.bug import Bug
from park.creatures.grass import Grass
from park.creatures.grazer import Grazer
from park.creatures.swirly_bug import SwirlyBug
from park.park_state import State


def run_park():
    # create game state
    state = pu.time_and_log(lambda: State(grid_depth=8, pixel_size=5), "Time to generate state:")

    active_grasses = pygame.sprite.LayeredDirty()
    creatures = pygame.sprite.LayeredDirty()

    # create grass
    active_grasses.add(
        Grass(state, starting_position=(240, 240), scaler=.25, fertility=1, active_grass_group=active_grasses))

    # create rocks
    rocks = [
        create_rock(state, starting_position=(60, 60), size=2),
        create_rock(state, starting_position=(0, 420), size=4),
        create_rock(state, starting_position=(500, 420), size=1),
        create_rock(state, starting_position=(360, 260), size=3)
    ]

    # add bugs
    [creatures.add(bug) for bug in [
        Bug(state, starting_position=(500, 500), scaler=3, fertility=1, speed=5),
        Bug(state, starting_position=(1000, 1000), scaler=1, fertility=1, speed=10),
        Bug(state, starting_position=(300, 300), scaler=1, fertility=1, speed=15),
    ]]

    [creatures.add(swirly) for swirly in [
        SwirlyBug(state, starting_position=(800, 800), scaler=2, fertility=1, speed=5),
        SwirlyBug(state, starting_position=(700, 150), scaler=1, fertility=1, speed=15)
    ]]

    for i in range(10):
        creatures.add(
            Grazer(state, starting_position=(100 * i, 150 * i), scaler=1, fertility=1, speed=10, viewing_distance=12))

    # going = True
    grass_times = []
    creature_times = []
    draw_times = []
    ticking_times = []
    while len(ticking_times) < 1000:
        g, c, d, t = park_tick(state, creatures, rocks, active_grasses, tick_speed=60)
        grass_times.append(g)
        creature_times.append(c)
        draw_times.append(d)
        ticking_times.append(t)

    print("number of sprites: ", state.global_sprite_counter)

    fig = plt.figure()
    graph = fig.add_subplot(111)
    x = range(len(ticking_times))
    graph.plot(x, ticking_times, 'o-r', linewidth=0.5)
    b, m = polyfit(x, ticking_times, 1)
    graph.plot(x, grass_times, 'o-g', linewidth=0.5)
    graph.plot(x, creature_times, 'o-y', linewidth=0.5)
    graph.plot(x, draw_times, 'o-k', linewidth=0.5)
    graph.plot(x, b + m * x, '.-.c')
    plt.xlabel("tick count")
    plt.ylabel("time per tick")
    plt.grid(linestyle='-', linewidth='0.5', color='blue')
    plt.show()


def run_test_park():
    # create game state
    state = pu.time_and_log(lambda: State(grid_depth=4, pixel_size=20), "Time to generate state:")

    active_grasses = pygame.sprite.RenderUpdates()
    grasses = pygame.sprite.RenderUpdates()
    creatures = pygame.sprite.RenderUpdates()

    # create grass
    first_grass = Grass(state, starting_position=(120, 200), scaler=1, fertility=0, active_grass_group=active_grasses)
    first_grass.add(active_grasses)
    first_grass.add(grasses)

    # create rocks
    rocks = [
        create_rock(state, starting_position=(0, 0), size=2)
    ]
    # swirly_one = \
    #     SwirlyBug(state, starting_position=(100, 200), scaler=1, fertility=1, speed=5)
    # swirly_one.add(creatures)

    grazer_one = Grazer(state, starting_position=(150, 230), scaler=1, fertility=1, speed=10, viewing_distance=120)
    grazer_one.add(creatures)

    going = True
    # ticking_times = []
    while going:
        park_tick(state, creatures, rocks, active_grasses, tick_speed=1)


def park_tick(state, creatures, rocks, active_grasses, tick_speed=10):
    start = time.time()
    state.clock.tick(tick_speed)
    # print("all grass", len(grasses))
    # print("active", len(active_grasses))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    active_grasses.update()
    grass_time = time.time() - start
    # print("global counter", state.global_sprite_counter)
    for rock in rocks:
        rock.group.update()

    # get old and new positions of all creatures
    old_creature_rects = [creature.rect for creature in creatures.sprites()]
    creatures.update()
    new_creature_rects = [creature.rect for creature in creatures.sprites()]

    creature_time = time.time() - start - grass_time

    # fill in creatures with background and redraw them, for movement
    for rect in old_creature_rects:
        state.screen.blit(state.terrain_screen, rect, rect)

    dirty_grass_rects = active_grasses.draw(state.screen)

    dirty_rock_rects = [rect for rect_list in [rock.group.draw(state.screen) for rock in rocks]
                        for rect in rect_list]

    # take the background entities intersected by any creature and draw those
    intersected_grasses = [state.global_sprites[sprite_id] for sprite_id in
                           chain.from_iterable([state.background_tree.tree.intersection(
                               (rect.left,
                                rect.top,
                                rect.right,
                                rect.bottom))
                               for rect in old_creature_rects + new_creature_rects])]

    ig_group = pygame.sprite.RenderUpdates()
    for grass in intersected_grasses:
        grass.add(ig_group)
    intersected_grass_rects = ig_group.draw(state.screen)
    ig_group.empty()

    # finally draw the creatures new positions
    dirty_creature_recs = creatures.draw(state.screen)

    # TODO remove after debugging completes
    # seeing_rects = [pygame.draw.polygon(state.park_screen, (255, 0, 0), grazer_one.seesBehavior.points, 1),
    #                 pygame.draw.rect(state.park_screen, (0, 255, 0), grazer_one.seesBehavior.bounding_box, 1)]
    # pygame.display.update(
    #     dirty_rock_rects + dirty_grass_rects + dirty_creature_recs + intersected_grass_rects + seeing_rects)
    pygame.display.update(dirty_rock_rects + dirty_grass_rects + dirty_creature_recs + intersected_grass_rects)

    drawing_time = time.time() - start - grass_time - creature_time

    if not len(active_grasses):
        # going = False
        print("out of active grasses")
    # print(len(active_sprites))
    return grass_time * 1000, creature_time * 1000, drawing_time * 1000, (time.time() - start) * 1000


if __name__ == "__main__":
    # larger context
    pygame.init()

    # run_test_park()
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
