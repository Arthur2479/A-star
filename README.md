## Project

A basic visual implementation of the `A* algorithm`, using `Python` and the `Processing` language.

![During the solving](/src/2_during.png)

To run the program, you need to [install Processing](https://processing.org/) (I'm using version 4.2) and run it from
its IDE.  
I sadly couldn't get Processing to export an executable file, maybe it will be fixed in the future.

## How to play

### Start the program

After opening the folder in Processing's IDE, click on play.  
A 800x800 window should appear, and the algorithm will immediately start searching for the end point.

### Interact with the game

There are a few ways you can interact with the simulation:

- Mouse buttons: _(Tip: you can keep them pressed and move your mouse)_

    - `Left`: add blocks
    - `Center`: move the end point
    - `Right`: remove blocks

- Keyboard keys:

    - `P`: pause the current simulation
    - `R`: restart the current simulation
    - `N`: Go to next simulation

### Game steps

| Start                                                             | During                                                                                                                                                | End                                                                                                        |
|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| ![Beginning](/src/1_start.png)                                    | ![During the solving](/src/2_during.png)                                                                                                              | ![Found the path](/src/3_end.png)                                                                          |
| A random map is generated. The pathfinder starts at the top right | The pathfinder uses A* to find the best path. In blue is its current path, in red explored tiles and in green are the potential tiles to explore next | The pathfinder found the optimal path ! Its displayed in blue. The programs wait for a bit and starts over |
