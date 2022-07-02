import sys
import time
from itertools import chain
import pygame
from numpy.polynomial.polynomial import polyfit

import park.park_util as pu
from park.constructs.rock import create_rock
from park.creatures.bug import Bug
from park.creatures.grass import Grass
from park.creatures.grazer import Grazer
from park.creatures.swirly_bug import SwirlyBug
from park.layered_dirty_cutoff import LayeredDirtyCutoff
from park.park_state import State

import matplotlib.pyplot as plt

GRASS_CUTOFF = 300
PIXEL_SIZE = 10
FPS = 60


def run_park():
    # create game state
    state = pu.time_and_log(lambda: State(grid_depth=7, pixel_size=PIXEL_SIZE), "Time to generate state:")
    state.init_screen()

    active_grasses = LayeredDirtyCutoff(GRASS_CUTOFF)
    creatures = pygame.sprite.LayeredDirty()

    # TODO - find smarter / more interesting strategy for placing initial park elements

    # create grass
    active_grasses.add(
        Grass(state, starting_position=(240, 240), scaler=.5, fertility=.1, active_grass_group=active_grasses),
        Grass(state, starting_position=(800, 800), scaler=.5, fertility=.4, active_grass_group=active_grasses),
        Grass(state, starting_position=(240, 800), scaler=.5, fertility=.5, active_grass_group=active_grasses),
        Grass(state, starting_position=(800, 240), scaler=.5, fertility=.6, active_grass_group=active_grasses)
    )

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
        SwirlyBug(state, starting_position=(800, 800), scaler=3, fertility=1, speed=5),
        SwirlyBug(state, starting_position=(700, 150), scaler=2, fertility=1, speed=15)
    ]]

    for i in range(8):
        creatures.add(
            Grazer(state, starting_position=(100 * i, 150 * i), scaler=1.25, fertility=1, speed=10, viewing_distance=40))

    # going = True
    grass_times = []
    creature_times = []
    draw_times = []
    ticking_times = []
    # rect_counts = []

    print("Incubating Park...")
    # run park for a bit without showing anything
    while len(ticking_times) < 0:
        g, c, d, t = park_tick(state, creatures, rocks, active_grasses, tick_speed=300, display=False)
        grass_times.append(g)
        creature_times.append(c)
        draw_times.append(d)
        ticking_times.append(t)

    print("Displaying Park.")
    # while len(ticking_times) < 2000:
    while True:
        try:
            g, c, d, t = park_tick(state, creatures, rocks, active_grasses, tick_speed=FPS)
            grass_times.append(g)
            creature_times.append(c)
            draw_times.append(d)
            ticking_times.append(t)
        except TypeError as e:
            print("Park is closing.")

            if len(ticking_times) <= 0:
                raise e
            break

        # rect_counts.append(r)

    x = range(len(ticking_times))
    b, m = polyfit(x, ticking_times, 1)

    # fig = plt.figure(figsize=[10, 10])
    # graph = fig.add_subplot(111)
    fig, axs = plt.subplots(4, sharex='all', sharey='all', figsize=[10, 10])
    axs[0].plot(x, ticking_times, 'or', linewidth=0.5, label="ticking time")
    axs[0].plot(x, b + m * x, '.-.c', label="tick time slope")
    axs[1].plot(x, grass_times, 'og', linewidth=0.5, label="grass time")
    axs[2].plot(x, creature_times, 'oy', linewidth=0.5, label="creature time")
    axs[3].plot(x, draw_times, 'ok', linewidth=0.5, label="draw time")
    # plt.xlabel("tick count")
    # plt.ylabel("time per tick")
    # plt.legend(loc="lower right")

    for ax in axs:
        ax.grid(linestyle='-', linewidth='0.5', color='blue')
        ax.set(xlabel="tick count", ylabel="time per tick")
        ax.legend(loc="lower right")
        ax.label_outer()

    # graph2 = graph.twinx()  # put another graph in the same plot on the right side
    # graph2.set_ylabel("count rects to draw")
    # graph2.plot(x, rect_counts, '.-m', linewidth=0.5, label="rect count")

    # plt.grid(linestyle='-', linewidth='0.5', color='blue')
    # plt.ylim(0, 50)
    fig.tight_layout(pad=1)

    print("number of sprites: ", state.global_sprite_counter)

    plt.show()


def run_test_park():
    # create game state
    test_fps = 30
    state = pu.time_and_log(lambda: State(grid_depth=6,
                                          pixel_size=10,
                                          tick_speed=test_fps,
                                          sea_level=10), "Time to generate state:")
    state.init_screen()

    creatures, rocks, active_grasses = generate_test_entities(state)

    going = True
    # ticking_times = []
    while going:
        park_tick(state, creatures, rocks, active_grasses, tick_speed=test_fps)


def generate_test_entities(state):
    active_grasses = pygame.sprite.RenderUpdates()
    grasses = pygame.sprite.RenderUpdates()
    creatures = pygame.sprite.RenderUpdates()

    # create grass
    first_grass = Grass(state, starting_position=(120, 200), scaler=.5, fertility=1, active_grass_group=active_grasses)
    first_grass.add(active_grasses)
    first_grass.add(grasses)

    # create rocks
    rocks = [
        create_rock(state, starting_position=(150, 230), size=2)
    ]
    # swirly_one = \
    #     SwirlyBug(state, starting_position=(100, 200), scaler=1, fertility=1, speed=5)
    # swirly_one.add(creatures)

    creatures.add([
        Grazer(state, starting_position=(170, 280), scaler=1, fertility=1, speed=10, viewing_distance=120)
    ])

    return creatures, rocks, active_grasses


def park_tick(state, creatures, rocks, active_grasses, tick_speed=10, display=True):
    start = time.time()
    state.clock.tick(tick_speed)
    # print("all grass", len(grasses))
    # print("active", len(active_grasses))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            return

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

    dirty_grass_rects = active_grasses.draw(state.screen)

    dirty_rock_rects = [rect for rect_list in [rock.group.draw(state.screen) for rock in rocks]
                        for rect in rect_list]

    # fill in creatures with background and redraw them, for movement
    if display:
        for rect in old_creature_rects:
            state.screen.blit(source=state.terrain_screen, dest=rect, area=rect)

        # take the background entities intersected by any creature and draw those
        intersected_grasses = [state.global_entities[sprite_id] for sprite_id in
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
        # seeing_rects = [rect
        #                 for creature in creatures if isinstance(creature, Grazer)
        #                 for rect in [
        #                     pygame.draw.polygon(state.screen, (255, 0, 0), creature.seesBehavior.points, 1),
        #                     pygame.draw.rect(state.screen, (0, 255, 0), creature.seesBehavior.bounding_box, 1)]
        #                 ]
        # print(seeing_rects)
        # state.update_screen(
        #     dirty_rock_rects + dirty_grass_rects + dirty_creature_recs + intersected_grass_rects + seeing_rects)
        # rects_to_update = dirty_rock_rects + dirty_grass_rects + dirty_creature_recs + intersected_grass_rects
        # print(f"r {len(rects_to_update)}")

        state.update_screen([])

    drawing_time = time.time() - start - grass_time - creature_time

    if not len(active_grasses):
        pass
        # going = False
        # print("out of active grasses")
    # print(len(active_sprites))
    return grass_time * 1000, creature_time * 1000, drawing_time * 1000, (time.time() - start) * 1000


if __name__ == "__main__":
    # larger context
    import os

    # position pygame window on screen
    position = 300, 50
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
    pygame.init()

    # run_test_park()
    run_park()
