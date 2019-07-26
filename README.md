# Park

This is park.

## Philosophy

Park should be simple by definition.
It should be visually clear.
Its architecture should only be complex enough to handle Park as it exists in the moment.
Park is not about the optimal, it is about the moment.
Park is not about interaction, it is about observation.

## View Design

Park should be visually simple.

## Architecture

Park should somewhat consist of three layers.

### Terrain
The terrain layer is currently procedurally generated dirt.
It's got a level of fertility to it that should somehow effect things on other layers.
Maybe someday there could be water in the terrain.

### Background
The background layer is for static entities that primarily Spread.
Currently there is just grass, and it's planted in one square and then spreads based on the dirt fertility.
Entities on this layer should collide with everything.

### Creatures
These are all the other entities.
They do whatever.
Entities on this layer should just collide with other creatures.
Entities on this layer should be able to consider values from other layers for their behavior.