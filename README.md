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
There are also height values to the terrain. Currently this just determines where water is placed based on a sea level.

### Background
The background layer is for static entities that primarily Spread.
Currently there is just grass, and it's planted in one square and then spreads based on the dirt fertility.
Entities on this layer should just collide with other background entities on placement.

### Creatures
These are all the other entities.
They do whatever.
Entities on this layer should just collide with other creatures on placement.
Entities on this layer should be able to consider values from other layers for their behavior.

### Entity Ideas
In no particular order
  - Lilypads, a background entity that lives and spreads in water but dies if it's surrounded by entities
  - Weeds, a background entity that gains fertilization near water and overrides grass when more fertile
  - Munchers, a creature that eats grazers (grazers should run away to be given a fair chance to live)
  - Fish, a creature that only lives in water

### Park's biggest questions
- Should rocks be creatures or background entities? If they're creatures, can grass then grow under rocks?
  If they're background entities, can creatures move on rocks?
  - Maybe there will be a type of grass that can grow under rocks, or a type of creature that can move on rocks?
  - For now rocks/barriers will be both creatures and background entities
- Can creatures manipulate background entities? A creature might trample grass
- What other sorts of rocks should there be?
- What is the cost of having eyes?
- How should creatures be born?